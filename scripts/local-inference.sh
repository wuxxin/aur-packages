#!/usr/bin/env bash
# local-inference.sh - Manage local llama-server systemd user service
#
# Usage: local-inference.sh [--install | --remove | --enable | --disable | --edit | --help]
#
# Manages a systemd user service (local-inference.service) that runs llama-server
# with optimized settings for AMD Radeon Pro W6800 (30 GiB VRAM).
#
# Context size is maximized per the formula:
#   available_vram = total_vram - model_vram - compute_vram - recurrent_vram
#   kv_total_tokens = available_vram / kv_bytes_per_token (q4_0 = ~35.1 bytes/token)
#   n_ctx = kv_total_tokens  (split equally across --parallel 2)
#
# MoE  (Qwen3.6-35B-A3B Compact, ~17 GiB file): model ~17,408 MiB + compute ~990 MiB
#   => ~12,306 MiB free => ~358,900 tokens, capped at n_ctx_train = 262144
#   => n_ctx = 262144 (per slot: 131072 tokens)
#
# Dense (Qwen3.6-27B Q5_K_L): model ~19,013 MiB + compute ~990 MiB + recurrent ~299 MiB
#   => ~10,402 MiB free => ~294,000 tokens, capped at n_ctx_train = 262144
#   => n_ctx = 262144 (per slot: 131072 tokens)

set -euo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_NAME="local-inference"
SERVICE_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.service"
ENV_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.env"

# ---------------------------------------------------------------------------
# Embedded service file (heredoc written by --install)
# ---------------------------------------------------------------------------
generate_service_file() {
    cat <<'EOF'
[Unit]
Description=Local LLM Inference Server (llama-server)
Documentation=https://github.com/ggml-org/llama.cpp
After=network.target

[Service]
Type=simple

# Load model/runtime configuration from env file
EnvironmentFile=%h/.config/systemd/user/local-inference.env

# Working directory (used for relative log paths if needed)
WorkingDirectory=%h

# Build the ExecStart command using env vars from the EnvironmentFile.
# MMPROJ_ARGS and CHAT_TEMPLATE_ARGS may be empty strings for dense models.
ExecStart=/bin/sh -c 'exec llama-server \
    -m "${LI_MODEL}" \
    ${LI_MMPROJ_ARGS} \
    ${LI_CHAT_TEMPLATE_ARGS} \
    -c ${LI_N_CTX} \
    --parallel 2 \
    --cache-type-k q4_0 \
    --cache-type-v q4_0 \
    -fa on \
    -b 2048 \
    -ub 1024 \
    -ngl 99 \
    --host ${LI_HOST} \
    --port ${LI_PORT}'

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
# Edit this file to switch models or tune runtime parameters.
# Reload with:  systemctl --user daemon-reload && systemctl --user restart local-inference
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# MODEL SELECTION - uncomment exactly ONE block below
# Default: MoE (Qwen3.6-35B-A3B) with vision support
# ---------------------------------------------------------------------------

# --- MoE: Qwen3.6-35B-A3B Compact (~17 GiB file, ~17,408 MiB on GPU, vision-enabled) ---
# Context budget: ~30704 - 17408 - 990 = ~12306 MiB free for KV
#   q4_0 KV: ~35.1 bytes/token => ~358900 tokens, capped at n_ctx_train=262144
#   Per slot (parallel=2): 131072 tokens
LI_MODEL=/data/public/machine-learning/models/vision-text/Qwen3.6-35B-A3B-APEX-I-Compact.gguf
LI_MMPROJ_ARGS=--mmproj /data/public/machine-learning/models/vision-text/Qwen3.6-35B-A3B-APEX-I-Compact-mmproj.gguf
LI_CHAT_TEMPLATE_ARGS=--chat-template-file /data/public/machine-learning/models/vision-text/Qwen3.6-chat_template.jinja
LI_N_CTX=262144

# --- Dense: Qwen3.6-27B Q5_K_L (~19 GiB on GPU, no vision) ---
# Context budget: ~30704 - 19013 - 990 - 299 = ~10402 MiB free for KV
#   q4_0 KV: ~35.1 bytes/token => ~294000 tokens, capped at n_ctx_train=262144
#   Per slot (parallel=2): 131072 tokens
#LI_MODEL=/data/public/machine-learning/models/vision-text/Qwen_Qwen3.6-27B-Q5_K_L.gguf
#LI_MMPROJ_ARGS=
#LI_CHAT_TEMPLATE_ARGS=--chat-template-file /data/public/machine-learning/models/vision-text/Qwen3.6-chat_template.jinja
#LI_N_CTX=262144

# ---------------------------------------------------------------------------
# SERVER NETWORK SETTINGS
# ---------------------------------------------------------------------------
LI_HOST=127.0.0.1
LI_PORT=50080

# ---------------------------------------------------------------------------
# Notes on parameters (fixed in service file, not overridable via env):
#   --parallel 2        : 2 concurrent sessions
#   --cache-type-k q4_0 : 4-bit KV cache (K)
#   --cache-type-v q4_0 : 4-bit KV cache (V)
#   -fa on              : Flash Attention enabled
#   -b 2048             : logical batch size (faster prefill)
#   -ub 1024            : physical micro-batch (sweet-spot: 16% faster vs 512,
#                         stays under 1.5s cache-hit threshold)
#   -ngl 99             : offload all layers to GPU
# ---------------------------------------------------------------------------
EOF
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
info()    { echo "[INFO]  $*"; }
success() { echo "[OK]    $*"; }
warn()    { echo "[WARN]  $*" >&2; }
die()     { echo "[ERROR] $*" >&2; exit 1; }

check_systemctl() {
    if ! command -v systemctl &>/dev/null; then
        die "systemctl not found. Is systemd available?"
    fi
}

# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

do_install() {
    check_systemctl
    info "Installing ${SERVICE_NAME} systemd user service..."

    # Create directory if needed
    mkdir -p "${SYSTEMD_USER_DIR}"

    # Write service file
    info "Writing service file: ${SERVICE_FILE}"
    generate_service_file > "${SERVICE_FILE}"
    chmod 644 "${SERVICE_FILE}"
    success "Service file written."

    # Write env file only if it doesn't exist (preserve user edits)
    if [[ -f "${ENV_FILE}" ]]; then
        warn "Env file already exists, skipping: ${ENV_FILE}"
        warn "Remove it manually if you want to regenerate the defaults."
    else
        info "Writing default env file: ${ENV_FILE}"
        generate_env_file > "${ENV_FILE}"
        chmod 600 "${ENV_FILE}"
        success "Env file written."
    fi

    # Reload daemon
    info "Reloading systemd user daemon..."
    systemctl --user daemon-reload

    # Enable and start
    info "Enabling and starting ${SERVICE_NAME}.service..."
    systemctl --user enable "${SERVICE_NAME}.service"
    systemctl --user restart "${SERVICE_NAME}.service"

    success "Installation complete."
    echo ""
    echo "  Service: ${SERVICE_FILE}"
    echo "  Env:     ${ENV_FILE}"
    echo ""
    echo "  Edit the env file to select model/mmproj/template, then:"
    echo "    systemctl --user daemon-reload"
    echo "    systemctl --user restart ${SERVICE_NAME}"
    echo ""
    echo "  Status:  systemctl --user status ${SERVICE_NAME}"
    echo "  Logs:    journalctl --user -u ${SERVICE_NAME} -f"
}

do_remove() {
    check_systemctl

    info "Stopping ${SERVICE_NAME}.service..."
    systemctl --user stop "${SERVICE_NAME}.service" 2>/dev/null || true

    info "Disabling ${SERVICE_NAME}.service..."
    systemctl --user disable "${SERVICE_NAME}.service" 2>/dev/null || true

    if [[ -f "${SERVICE_FILE}" ]]; then
        info "Removing service file: ${SERVICE_FILE}"
        rm -f "${SERVICE_FILE}"
        success "Service file removed."
    else
        warn "Service file not found: ${SERVICE_FILE}"
    fi

    info "Reloading systemd user daemon..."
    systemctl --user daemon-reload

    success "Service removed."
    echo ""
    echo "  Note: The env file was NOT removed: ${ENV_FILE}"
    echo "  Remove it manually if you no longer need it:"
    echo "    rm '${ENV_FILE}'"
}

do_enable() {
    check_systemctl

    if [[ ! -f "${SERVICE_FILE}" ]]; then
        die "Service file not found: ${SERVICE_FILE}. Run --install first."
    fi

    info "Enabling and restarting ${SERVICE_NAME}.service..."
    systemctl --user enable "${SERVICE_NAME}.service"
    systemctl --user restart "${SERVICE_NAME}.service"
    success "Service enabled and restarted."
    echo ""
    echo "  Status:  systemctl --user status ${SERVICE_NAME}"
    echo "  Logs:    journalctl --user -u ${SERVICE_NAME} -f"
}

do_disable() {
    check_systemctl

    info "Stopping ${SERVICE_NAME}.service..."
    systemctl --user stop "${SERVICE_NAME}.service" 2>/dev/null || true

    info "Disabling ${SERVICE_NAME}.service..."
    systemctl --user disable "${SERVICE_NAME}.service"
    success "Service stopped and disabled."
}

do_edit() {
    check_systemctl

    if [[ ! -f "${ENV_FILE}" ]]; then
        die "Env file not found: ${ENV_FILE}. Run --install first."
    fi

    local editor
    editor="${VISUAL:-${EDITOR:-}}"
    if [[ -z "${editor}" ]]; then
        # fallback: try common editors in order
        for e in sensible-editor nano vim vi; do
            if command -v "${e}" &>/dev/null; then
                editor="${e}"
                break
            fi
        done
    fi
    if [[ -z "${editor}" ]]; then
        die "No editor found. Set \$VISUAL or \$EDITOR."
    fi

    info "Opening env file with ${editor}: ${ENV_FILE}"
    "${editor}" "${ENV_FILE}"

    info "Reloading systemd user daemon and restarting ${SERVICE_NAME}..."
    systemctl --user daemon-reload
    systemctl --user restart "${SERVICE_NAME}.service"
    success "Service restarted with updated configuration."
    echo ""
    echo "  Status:  systemctl --user status ${SERVICE_NAME}"
    echo "  Logs:    journalctl --user -u ${SERVICE_NAME} -f"
}

do_help() {
    cat <<EOF
Usage: $(basename "$0") <command>

Manage the local-inference systemd user service (llama-server).

Commands:
  --install   Install the service file, create default env file (if not present),
              reload the systemd daemon, then enable and start the service.

  --remove    Stop and disable the service, remove the service file, and reload
              the daemon. The env file is preserved.

  --enable    Enable and restart the service (requires prior --install).

  --disable   Stop and disable the service (does not remove files).

  --edit      Open the env file in \$VISUAL/\$EDITOR, then daemon-reload and
              restart the service automatically on editor exit.

  --help      Show this help message.

Files managed:
  Service:  ${SERVICE_FILE}
  Env:      ${ENV_FILE}

Environment variables (set in the env file):
  LI_MODEL                Path to the GGUF model file
  LI_MMPROJ_ARGS          --mmproj <path>  (empty string for dense/no-vision models)
  LI_CHAT_TEMPLATE_ARGS   --chat-template-file <path>  (empty string to use built-in)
  LI_N_CTX                Total context size in tokens (split across 2 parallel slots)
  LI_HOST                 Bind address (default: 127.0.5.1)
  LI_PORT                 Bind port    (default: 8088)

Fixed server parameters (hardcoded in the service ExecStart):
  --parallel 2            Two concurrent inference slots
  --cache-type-k q4_0    4-bit quantized KV cache (K matrices)
  --cache-type-v q4_0    4-bit quantized KV cache (V matrices)
  -fa on                  Flash Attention enabled
  -b 2048                 Logical batch size (fast prefill)
  -ub 1024                Physical micro-batch size (cache-hit sweet spot)
  -ngl 99                 All layers offloaded to GPU (ROCm)

Context size rationale for AMD Radeon Pro W6800 (30,704 MiB VRAM):
  MoE  (default): 30704 - 17408(model) - 990(compute)               = ~12306 MiB free
                  q4_0 KV ~35.1 bytes/token => capped at n_ctx_train 262144 (131072/slot)
  Dense:          30704 - 19013(model) - 990(compute) - 299(recurrent) = ~10402 MiB
                  q4_0 KV ~35.1 bytes/token => capped at n_ctx_train 262144 (131072/slot)

Workflow:
  $(basename "$0") --install    # First-time setup
  $(basename "$0") --edit       # Edit env file and auto-restart
  journalctl --user -u ${SERVICE_NAME} -f
EOF
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if [[ $# -ne 1 ]]; then
    do_help
    exit 1
fi

case "$1" in
    --install)  do_install ;;
    --remove)   do_remove  ;;
    --enable)   do_enable  ;;
    --disable)  do_disable ;;
    --edit)     do_edit    ;;
    --help|-h)  do_help    ;;
    *)
        echo "[ERROR] Unknown command: $1" >&2
        echo "" >&2
        do_help >&2
        exit 1
        ;;
esac
