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

# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

cmd_install() {
    echo "Installing ${SERVICE_NAME} systemd user service..."

    # Create directory if needed
    mkdir -p "${SYSTEMD_USER_DIR}"

    # Write service file
    echo "Writing service file: ${SERVICE_FILE}"
    generate_service_file >"${SERVICE_FILE}"
    chmod 644 "${SERVICE_FILE}"
    echo "Service file written."

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

    # Reload daemon
    echo "Reloading systemd user daemon..."
    systemctl --user daemon-reload

    # Enable and start
    echo "Enabling and starting ${SERVICE_NAME}.service..."
    systemctl --user enable "${SERVICE_NAME}.service"
    systemctl --user restart "${SERVICE_NAME}.service"

    echo "Installation complete."
    echo ""
    echo "  Service: ${SERVICE_FILE}"
    echo "  Env:     ${ENV_FILE}"
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

    echo "Uninstalled successfully. Configuration in ${ENV_FILE} is preserved."
}

cmd_start() { systemctl --user start "${SERVICE_NAME}.service"; }
cmd_stop() { systemctl --user stop "${SERVICE_NAME}.service"; }
cmd_restart() { systemctl --user restart "${SERVICE_NAME}.service"; }
cmd_status() { systemctl --user status "${SERVICE_NAME}.service"; }
cmd_enable() { systemctl --user enable "${SERVICE_NAME}.service"; }
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
        # shellcheck disable=SC2016
        systemd-run "${opts[@]}" /bin/sh -c 'exec llama-server \
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
