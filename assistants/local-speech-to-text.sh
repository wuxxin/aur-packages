#!/usr/bin/env bash
# local-speech-to-text.sh - Manage local whisper-server systemd user service
#
# Usage: local-speech-to-text.sh <command> [args...]
#
# Manages a systemd user service (local-speech-to-text.service) that runs whisper-server
# for speech-to-text (STT) transcription.
#
# Hardware target: AMD Radeon Pro W6800.
#
# ---------------------------------------------------------------------------

set -euo pipefail

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_NAME="local-speech-to-text"
SERVICE_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.service"
ENV_FILE="${SYSTEMD_USER_DIR}/${SERVICE_NAME}.env"

# ---------------------------------------------------------------------------
# Load environment
# ---------------------------------------------------------------------------
load_env() {
	# Default parameters
	LSTT_PORT=50090
	LSTT_HOST=127.0.0.1
	LSTT_MODEL=/data/public/machine-learning/models/speech-to-text/ggml-large-v3-turbo-q5_0.bin
	LSTT_THREADS=4
	LSTT_DEVICE=0
	LSTT_INFERENCE_PATH=/v1/audio/transcriptions
	LSTT_EXTRA_ARGS=""

	# Source the env file to get model paths and settings if it exists
	if [[ -f "$ENV_FILE" ]]; then
		set +u
		# shellcheck disable=SC1090
		source "$ENV_FILE"
		set -u
	fi
}

# ---------------------------------------------------------------------------
# Embedded service file (heredoc written by install/start/restart)
# ---------------------------------------------------------------------------
generate_service_file() {
	load_env

	cat <<EOF
[Unit]
Description=Local Speech-to-Text Transcription Server (whisper-server)
Documentation=https://github.com/ggerganov/whisper.cpp
After=network.target

[Service]
Type=simple

# Load model/runtime configuration from env file
EnvironmentFile=${ENV_FILE}

# Working directory
WorkingDirectory=%h

# ExecStart running whisper-server with ROCm GPU acceleration and OpenAI compat path
ExecStart=whisper-server \\
    --model ${LSTT_MODEL} \\
    --host ${LSTT_HOST} \\
    --port ${LSTT_PORT} \\
    --threads ${LSTT_THREADS} \\
    --device ${LSTT_DEVICE} \\
    --inference-path "${LSTT_INFERENCE_PATH}" \\
    --convert \\
    -fa \\
    ${LSTT_EXTRA_ARGS}

Restart=on-failure
RestartSec=10s

StandardOutput=journal
StandardError=journal
SyslogIdentifier=local-speech-to-text

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
# Allow read-write access to home-based paths (for temp ffmpeg files)
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
# local-speech-to-text.env
# ---------------------------------------------------------------------------
# Configuration for the local-speech-to-text.service whisper-server instance.
#
# Edit this file to switch models or tune runtime parameters.
# Reload with:  local-speech-to-text.sh restart
# ---------------------------------------------------------------------------

# Port to bind the server to (default: 50090)
LSTT_PORT=50090

# Host to bind the server to (127.0.0.1 for local access only)
LSTT_HOST=127.0.0.1

# Path to the GGML Whisper model file
# Source: https://huggingface.co/ggerganov/whisper.cpp/blob/main/ggml-large-v3-turbo-q5_0.bin
LSTT_MODEL=/data/public/machine-learning/models/speech-to-text/ggml-large-v3-turbo-q5_0.bin

# Number of threads to use for CPU-bound computations/preprocessing
LSTT_THREADS=4

# GPU Device ID to use (default: 0)
LSTT_DEVICE=0

# Inference API endpoint path (default: /v1/audio/transcriptions for OpenAI-compatibility)
LSTT_INFERENCE_PATH=/v1/audio/transcriptions

# Extra arguments to pass to whisper-server (e.g. VAD options, diarization, etc.)
LSTT_EXTRA_ARGS=""
EOF
}

# ---------------------------------------------------------------------------
# Write service file
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

	# Write service file
	echo "Writing service file: ${SERVICE_FILE}"
	write_service_file
	echo "Service file written."

	# Enable and start
	echo "Enabling and starting ${SERVICE_NAME}.service..."
	systemctl --user enable "${SERVICE_NAME}.service"
	systemctl --user restart "${SERVICE_NAME}.service"

	echo "Installation complete."
	echo ""
	echo "  Service: ${SERVICE_FILE}"
	echo "  Env:     ${ENV_FILE}"
	echo ""
	echo "  Edit the env file to select models, then:"
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
cmd_enable() {
	write_service_file
	systemctl --user enable "${SERVICE_NAME}.service"
}
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
	echo "Starting whisper-server as a transient systemd service with args: $*"

	load_env

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
		# shellcheck disable=SC2086
		systemd-run "${opts[@]}" whisper-server "$@"
	else
		# shellcheck disable=SC2086
		systemd-run "${opts[@]}" whisper-server \
			--model "${LSTT_MODEL}" \
			--host "${LSTT_HOST}" \
			--port "${LSTT_PORT}" \
			--threads "${LSTT_THREADS}" \
			--device "${LSTT_DEVICE}" \
			--inference-path "${LSTT_INFERENCE_PATH}" \
			--convert \
			-fa \
			${LSTT_EXTRA_ARGS}
	fi
}

cmd_shell() {
	echo "Starting interactive shell in the whisper-server systemd environment..."

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
	echo "  exec      - Run whisper-server as a transient systemd user service"
	echo "  shell     - Spawn an interactive shell in the whisper-server environment"
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
