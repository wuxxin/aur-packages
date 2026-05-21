#!/usr/bin/env bash
# local-inference.sh - Manage local llama-server systemd user service
#
# Usage: local-inference.sh <command> [args...]
#
# Manages a systemd user service (local-inference.service) that runs llama-server
# in router mode (--models-preset), serving an LLM, an embedding model, and
# optionally a reranker model — all from a single process on one port.
#
# Hardware target: AMD Radeon Pro W6800 (30 GiB VRAM = 30,704 MiB usable).
#
# All three models are kept warm simultaneously (--models-max 2 or 3).
# Context budget is calculated for the LLM only; the 0.6B embedding and
# reranker models have negligible KV-cache overhead.
#
# ---------------------------------------------------------------------------
# VRAM budgets  (q4_0 KV ≈ 35.1 bytes/token, parallel=2, per-slot cap=120000)
# ---------------------------------------------------------------------------
#
# Model weights on GPU:
#   MoE   LLM   (Qwen3.6-35B-A3B Compact)     : ~17,408 MiB  (17 GiB file)
#   MoE   mmproj                              :    ~861 MiB
#   Dense LLM   (Qwen3.6-27B Q5_K_L)          : ~19,013 MiB  (20 GiB file)
#   Embedding   (Qwen3-Embedding-0.6B Q8_0)   :    ~700 MiB  (610 MiB file)
#   Reranker    (Qwen3-Reranker-0.6B Q4_K_M)  :    ~450 MiB  (379 MiB file)
#   Compute overhead (per LLM)                :    ~990 MiB
#   Dense recurrent state (Qwen 27B only)     :    ~299 MiB
#
# Config A — MoE + Embedding + Reranker:
#   30704 - 17408 - 861 - 990 - 700 - 450 = 10,295 MiB free for KV
#   KV @ 240,000 tokens = ~8,031 MiB  →  free headroom: ~2,264 MiB
#   n_ctx = 240,000  (per slot: 120,000)
#
# Config B — Dense + Embedding + Reranker:
#   30704 - 19013 - 990 - 299 - 700 - 450 = 9,252 MiB free for KV
#   KV @ 240,000 tokens = ~8,031 MiB  →  free headroom: ~1,221 MiB
#   n_ctx = 240,000  (per slot: 120,000)
#
# Endpoints (all on LI_PORT, default 50080):
#   /v1/chat/completions  →  LLM         (model: LI_ALIAS)
#   /v1/embeddings        →  Embedding   (model: LI_EMBEDDING_ALIAS)
#   /v1/rerank            →  Reranker    (model: LI_RERANKER_ALIAS)  [if enabled]
# ---------------------------------------------------------------------------

set -euo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_NAME="local-inference"
SERVICE_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.service"
ENV_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.env"
INI_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.ini"

# ---------------------------------------------------------------------------
# Load environment and compute models-max
# ---------------------------------------------------------------------------
load_env() {
    # Source the env file to get model paths and settings
    if [[ -f "$ENV_FILE" ]]; then
        set +u
        # shellcheck disable=SC1090
        source "$ENV_FILE"
        set -u
    fi
}

# ---------------------------------------------------------------------------
# Generate models-preset INI file from environment variables
# ---------------------------------------------------------------------------
generate_ini_file() {
    load_env

    local models_max=2
    local ini_content=""

    # Global defaults
    ini_content+="version = 1"$'\n'
    ini_content+=""$'\n'
    ini_content+="[*]"$'\n'
    ini_content+="flash-attn = on"$'\n'
    ini_content+="n-gpu-layers = 99"$'\n'

    # --- LLM section ---
    ini_content+=""$'\n'
    ini_content+="[${LI_ALIAS:-qwen3}]"$'\n'
    ini_content+="model = ${LI_MODEL}"$'\n'
    if [[ -n "${LI_MMPROJ_ARGS:-}" ]]; then
        # Extract mmproj path from "--mmproj /path/to/file"
        local mmproj_path
        mmproj_path="${LI_MMPROJ_ARGS#--mmproj }"
        ini_content+="mmproj = ${mmproj_path}"$'\n'
    fi
    if [[ -n "${LI_CHAT_TEMPLATE_ARGS:-}" ]]; then
        # Extract template path from "--chat-template-file /path/to/file"
        local template_path
        template_path="${LI_CHAT_TEMPLATE_ARGS#--chat-template-file }"
        ini_content+="chat-template-file = ${template_path}"$'\n'
    fi
    ini_content+="ctx-size = ${LI_N_CTX:-240000}"$'\n'
    ini_content+="parallel = 2"$'\n'
    ini_content+="cache-type-k = q4_0"$'\n'
    ini_content+="cache-type-v = q4_0"$'\n'
    ini_content+="batch-size = 2048"$'\n'
    ini_content+="ubatch-size = 1024"$'\n'

    # --- Embedding section (always enabled) ---
    ini_content+=""$'\n'
    ini_content+="[${LI_EMBEDDING_ALIAS:-qwen3-embedding}]"$'\n'
    ini_content+="model = ${LI_EMBEDDING_MODEL}"$'\n'
    ini_content+="embedding = true"$'\n'
    ini_content+="pooling = mean"$'\n'
    ini_content+="ctx-size = 8192"$'\n'

    # --- Reranker section (optional, toggled by LI_RERANKER_ENABLED) ---
    if [[ "${LI_RERANKER_ENABLED:-false}" == "true" ]]; then
        models_max=3
        ini_content+=""$'\n'
        ini_content+="[${LI_RERANKER_ALIAS:-qwen3-reranker}]"$'\n'
        ini_content+="model = ${LI_RERANKER_MODEL}"$'\n'
        ini_content+="embedding = true"$'\n'
        ini_content+="pooling = rank"$'\n'
        ini_content+="ctx-size = 8192"$'\n'
    fi

    printf '%s' "$ini_content" >"$INI_FILE"
    chmod 600 "$INI_FILE"

    # Export for use by callers
    MODELS_MAX="$models_max"
}

# ---------------------------------------------------------------------------
# Embedded service file (heredoc written by install/start/restart)
# ---------------------------------------------------------------------------
generate_service_file() {
    load_env
    generate_ini_file

    cat <<EOF
[Unit]
Description=Local LLM Inference Server (llama-server, router mode)
Documentation=https://github.com/ggml-org/llama.cpp
After=network.target

[Service]
Type=simple

# Load model/runtime configuration from env file
EnvironmentFile=${ENV_FILE}

# Working directory
WorkingDirectory=%h

# Router mode: serve LLM + embedding (+ optional reranker) from one process.
# The models-preset INI file is generated dynamically from the env file.
ExecStart=llama-server \\
    --models-preset ${INI_FILE} \\
    --models-max ${MODELS_MAX} \\
    --host ${LI_HOST:-127.0.0.1} \\
    --port ${LI_PORT:-50080}

Restart=on-failure
RestartSec=10s

StandardOutput=journal
StandardError=journal
SyslogIdentifier=local-inference

# --- Basic hardening (kept minimal for GPU access) ---
NoNewPrivileges=yes
CapabilityBoundingSet=
AmbientCapabilities=

# GPU/DRI access requires PrivateDevices=no (ROCm needs /dev/dri, /dev/kfd)
PrivateDevices=no
PrivateTmp=yes
PrivateMounts=yes
PrivateIPC=yes

ProtectSystem=strict
# Allow read-write access to model storage and home-based paths
BindPaths=%h
ReadOnlyPaths=/etc/ssl /etc/ca-certificates /etc/resolv.conf /etc/hosts /etc/nsswitch.conf
ReadWritePaths=/data/public/machine-learning

ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes

LockPersonality=yes
RestrictSUIDSGID=yes
RestrictRealtime=yes
KeyringMode=private
UMask=0077

[Install]
WantedBy=default.target
EOF
}

# ---------------------------------------------------------------------------
# Embedded default env file (heredoc written by --install)
# ---------------------------------------------------------------------------
generate_env_file() {
    cat <<'EOF'
# local-inference.env
# ---------------------------------------------------------------------------
# Configuration for the local-inference.service llama-server instance.
# Uses router mode (--models-preset) to serve LLM + embedding + reranker
# from a single process on one port.
#
# Edit this file to switch models or tune runtime parameters.
# Reload with:  systemctl --user daemon-reload && systemctl --user restart local-inference
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# LLM MODEL SELECTION - uncomment exactly ONE block below
# Default: MoE (Qwen3.6-35B-A3B) with vision support
# ---------------------------------------------------------------------------

# Alias for the LLM model used by agents (the "model" field in API requests)
LI_ALIAS=qwen3

# --- MoE: Qwen3.6-35B-A3B Compact (~17 GiB file, vision-enabled) ---
# VRAM budget (with embedding + reranker):
#   LLM model:     ~17,408 MiB
#   mmproj:           ~861 MiB
#   compute:          ~990 MiB
#   embedding:        ~700 MiB
#   reranker:         ~450 MiB
#   ─────────────────────────────
#   Total models:  ~20,409 MiB  (of 30,704 MiB)
#   Free for KV:   ~10,295 MiB
#   KV @ 240,000 tokens (q4_0 ~35.1 B/tok) = ~8,031 MiB
#   Free headroom: ~2,264 MiB
#   n_ctx: 240,000  (per slot: 120,000)
LI_MODEL=/data/public/machine-learning/models/vision-text/Qwen3.6-35B-A3B-APEX-I-Compact.gguf
LI_MMPROJ_ARGS=--mmproj /data/public/machine-learning/models/vision-text/Qwen3.6-35B-A3B-APEX-I-Compact-mmproj.gguf
LI_CHAT_TEMPLATE_ARGS=--chat-template-file /data/public/machine-learning/models/vision-text/Qwen3.6-chat_template.jinja
LI_N_CTX=240000

# --- Dense: Qwen3.6-27B Q5_K_L (~20 GiB file, no vision) ---
# VRAM budget (with embedding + reranker):
#   LLM model:     ~19,013 MiB
#   compute:          ~990 MiB
#   recurrent:        ~299 MiB
#   embedding:        ~700 MiB
#   reranker:         ~450 MiB
#   ─────────────────────────────
#   Total models:  ~21,452 MiB  (of 30,704 MiB)
#   Free for KV:    ~9,252 MiB
#   KV @ 240,000 tokens (q4_0 ~35.1 B/tok) = ~8,031 MiB
#   Free headroom:  ~1,221 MiB
#   n_ctx: 240,000  (per slot: 120,000)
#LI_MODEL=/data/public/machine-learning/models/vision-text/Qwen_Qwen3.6-27B-Q5_K_L.gguf
#LI_MMPROJ_ARGS=
#LI_CHAT_TEMPLATE_ARGS=--chat-template-file /data/public/machine-learning/models/vision-text/Qwen3.6-chat_template.jinja
#LI_N_CTX=240000

# ---------------------------------------------------------------------------
# EMBEDDING MODEL (always enabled)
# Qwen3-Embedding-0.6B Q8_0 (610 MiB file, ~700 MiB on GPU)
# Endpoint: /v1/embeddings (model: LI_EMBEDDING_ALIAS)
# ---------------------------------------------------------------------------
LI_EMBEDDING_MODEL=/data/public/machine-learning/models/embedding/Qwen3-Embedding-0.6B-Q8_0.gguf
LI_EMBEDDING_ALIAS=qwen3-embedding

# ---------------------------------------------------------------------------
# RERANKER MODEL (optional, toggle on/off)
# Qwen3-Reranker-0.6B Q4_K_M (379 MiB file, ~450 MiB on GPU)
# Endpoint: /v1/rerank (model: LI_RERANKER_ALIAS)
# Set to "true" to enable, "false" to disable.
# ---------------------------------------------------------------------------
LI_RERANKER_ENABLED=true
LI_RERANKER_MODEL=/data/public/machine-learning/models/reranker/Qwen3-Reranker-0.6B.Q4_K_M.gguf
LI_RERANKER_ALIAS=qwen3-reranker

# ---------------------------------------------------------------------------
# SERVER NETWORK SETTINGS
# ---------------------------------------------------------------------------
LI_HOST=127.0.0.1
LI_PORT=50080

# ---------------------------------------------------------------------------
# Notes on LLM parameters (set in the generated models.ini, not here):
#   parallel 2          : 2 concurrent sessions
#   cache-type-k q4_0   : 4-bit KV cache (K)
#   cache-type-v q4_0   : 4-bit KV cache (V)
#   flash-attn on       : Flash Attention enabled
#   batch-size 2048     : logical batch size (faster prefill)
#   ubatch-size 1024    : physical micro-batch (sweet-spot: 16% faster vs 512,
#                         stays under 1.5s cache-hit threshold)
#   n-gpu-layers 99     : offload all layers to GPU
# ---------------------------------------------------------------------------
EOF
}

# ---------------------------------------------------------------------------
# Write service file and regenerate INI
# ---------------------------------------------------------------------------
write_service_file() {
    generate_service_file >"${SERVICE_FILE}"
    chmod 644 "${SERVICE_FILE}"
    systemctl --user daemon-reload
}

# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

cmd_install() {
    echo "Installing ${SERVICE_NAME} systemd user service..."

    # Create directory if needed
    mkdir -p "${SYSTEMD_USER_DIR}"

    # Write env file only if it doesn't exist (preserve user edits)
    if [[ -f "${ENV_FILE}" ]]; then
        echo "Warning: Env file already exists, skipping: ${ENV_FILE}"
        echo "Remove it manually if you want to regenerate the defaults."
    else
        echo "Writing default env file: ${ENV_FILE}"
        generate_env_file >"${ENV_FILE}"
        chmod 600 "${ENV_FILE}"
        echo "Env file written."
    fi

    # Write service file (also generates INI)
    echo "Writing service file: ${SERVICE_FILE}"
    write_service_file
    echo "Service file written."
    echo "Generated INI file: ${INI_FILE}"

    # Enable and start
    echo "Enabling and starting ${SERVICE_NAME}.service..."
    systemctl --user enable "${SERVICE_NAME}.service"
    systemctl --user restart "${SERVICE_NAME}.service"

    echo "Installation complete."
    echo ""
    echo "  Service: ${SERVICE_FILE}"
    echo "  Env:     ${ENV_FILE}"
    echo "  INI:     ${INI_FILE}"
    echo ""
    echo "  Edit the env file to select model/mmproj/template, then:"
    echo "    $0 restart"
    echo ""
    echo "  Status:  $0 status"
    echo "  Logs:    $0 logs"
}

cmd_uninstall() {
    echo "Uninstalling ${SERVICE_NAME} systemd user service..."
    systemctl --user stop "${SERVICE_NAME}.service" || true
    systemctl --user disable "${SERVICE_NAME}.service" || true

    if [[ -f "${SERVICE_FILE}" ]]; then
        rm -f "${SERVICE_FILE}"
        systemctl --user daemon-reload
        echo "Removed service file."
    fi

    if [[ -f "${INI_FILE}" ]]; then
        rm -f "${INI_FILE}"
        echo "Removed INI file."
    fi

    echo "Uninstalled successfully. Configuration in ${ENV_FILE} is preserved."
}

cmd_start() {
    write_service_file
    systemctl --user start "${SERVICE_NAME}.service"
}

cmd_stop() { systemctl --user stop "${SERVICE_NAME}.service"; }

cmd_restart() {
    write_service_file
    systemctl --user restart "${SERVICE_NAME}.service"
}

cmd_status() { systemctl --user status "${SERVICE_NAME}.service"; }
cmd_enable() { write_service_file; systemctl --user enable "${SERVICE_NAME}.service"; }
cmd_disable() { systemctl --user disable "${SERVICE_NAME}.service"; }
cmd_logs() { journalctl --user -u "${SERVICE_NAME}.service" -f; }

cmd_edit() {
    mkdir -p "$(dirname "${ENV_FILE}")"
    touch "${ENV_FILE}"
    ${EDITOR:-nano} "${ENV_FILE}"
    echo "Restarting service to apply updated environment..."
    cmd_restart
}

cmd_exec() {
    echo "Starting llama-server as a transient systemd service with args: $*"

    load_env
    generate_ini_file

    local opts=(
        --user
        --pty
        --wait
        --collect
        --quiet
        -p "Type=exec"
        -p "EnvironmentFile=-${ENV_FILE}"
        -p "WorkingDirectory=$HOME"
        -p "NoNewPrivileges=yes"
        -p "CapabilityBoundingSet="
        -p "AmbientCapabilities="
        -p "PrivateDevices=no"
        -p "PrivateTmp=yes"
        -p "PrivateMounts=yes"
        -p "PrivateIPC=yes"
        -p "ProtectSystem=strict"
        -p "BindPaths=$HOME"
        -p "ReadOnlyPaths=/etc/ssl /etc/ca-certificates /etc/resolv.conf /etc/hosts /etc/nsswitch.conf"
        -p "ReadWritePaths=/data/public/machine-learning"
        -p "ProtectKernelTunables=yes"
        -p "ProtectKernelModules=yes"
        -p "ProtectKernelLogs=yes"
        -p "ProtectControlGroups=yes"
        -p "ProtectClock=yes"
        -p "ProtectHostname=yes"
        -p "LockPersonality=yes"
        -p "RestrictSUIDSGID=yes"
        -p "RestrictRealtime=yes"
        -p "KeyringMode=private"
        -p "UMask=0077"
    )

    if [ $# -gt 0 ]; then
        systemd-run "${opts[@]}" llama-server "$@"
    else
        systemd-run "${opts[@]}" llama-server \
            --models-preset "${INI_FILE}" \
            --models-max "${MODELS_MAX}" \
            --host "${LI_HOST:-127.0.0.1}" \
            --port "${LI_PORT:-50080}"
    fi
}

cmd_shell() {
    echo "Starting interactive shell in the llama-server systemd environment..."

    local opts=(
        --user
        --pty
        --wait
        --collect
        --quiet
        -p "Type=exec"
        -p "EnvironmentFile=-${ENV_FILE}"
        -p "WorkingDirectory=$HOME"
        -p "NoNewPrivileges=yes"
        -p "CapabilityBoundingSet="
        -p "AmbientCapabilities="
        -p "PrivateDevices=no"
        -p "PrivateTmp=yes"
        -p "PrivateMounts=yes"
        -p "PrivateIPC=yes"
        -p "ProtectSystem=strict"
        -p "BindPaths=$HOME"
        -p "ReadOnlyPaths=/etc/ssl /etc/ca-certificates /etc/resolv.conf /etc/hosts /etc/nsswitch.conf"
        -p "ReadWritePaths=/data/public/machine-learning"
        -p "ProtectKernelTunables=yes"
        -p "ProtectKernelModules=yes"
        -p "ProtectKernelLogs=yes"
        -p "ProtectControlGroups=yes"
        -p "ProtectClock=yes"
        -p "ProtectHostname=yes"
        -p "LockPersonality=yes"
        -p "RestrictSUIDSGID=yes"
        -p "RestrictRealtime=yes"
        -p "KeyringMode=private"
        -p "UMask=0077"
    )

    systemd-run "${opts[@]}" "${SHELL:-/bin/bash}" "$@"
}

usage() {
    echo "Usage: $0 <command>"
    echo "Commands:"
    echo "  install   - Setup service and default environment"
    echo "  uninstall - Stop and remove systemd service"
    echo "  start     - Start the systemd service"
    echo "  stop      - Stop the systemd service"
    echo "  restart   - Restart the systemd service"
    echo "  status    - View systemd service status"
    echo "  enable    - Enable systemd service on boot"
    echo "  disable   - Disable systemd service on boot"
    echo "  logs      - Tail the systemd service logs"
    echo "  edit      - Edit the .env file and restart the service upon exit"
    echo "  exec      - Run llama-server as a transient systemd user service"
    echo "  shell     - Spawn an interactive shell in the llama-server environment"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if [ $# -lt 1 ]; then
    usage
    exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
install) cmd_install ;;
uninstall) cmd_uninstall ;;
start) cmd_start ;;
stop) cmd_stop ;;
restart) cmd_restart ;;
status) cmd_status ;;
enable) cmd_enable ;;
disable) cmd_disable ;;
logs) cmd_logs ;;
edit) cmd_edit ;;
exec) cmd_exec "$@" ;;
shell) cmd_shell "$@" ;;
*)
    echo "Unknown command: $COMMAND"
    usage
    exit 1
    ;;
esac
