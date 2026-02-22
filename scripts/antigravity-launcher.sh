#!/usr/bin/env bash
# Antigravity Bubblewrapped Launcher
set -euo pipefail

# Configuration
app_bin="/usr/lib/electron/electron"
app_dir="/usr/lib/antigravity/"
persistent_home="$HOME/.antigravity"
work_dir="$HOME/AntigravityWorkspace"
antigravity_flags_file="${persistent_home}/.config/antigravity-flags.conf"
electron_flags_file="${persistent_home}/.config/electron-flags.conf"
antigravity_flags=()
electron_flags=(
	--disable-dev-shm-usage
	--disable-chromium-sandbox
	--no-sandbox
)

DESKTOP_FILE_MAIN="[Desktop Entry]
Type=Application
Name=Antigravity(Sb)
GenericName=Code Editor
Comment=Agentic development platform (Sandboxed)
# TryExec: Desktop environment checks if command exists before showing in menu.
# This avoids showing broken icons if the script isn't installed.
TryExec=%h/.local/bin/antigravity-launcher.sh
Exec=%h/.local/bin/antigravity-launcher.sh --launch %F
Icon=antigravity
Terminal=false
Categories=Development;IDE;TextEditor;
Keywords=vscode;ide;editor;
StartupNotify=true
StartupWMClass=Antigravity
MimeType=application/x-antigravity-workspace;
Actions=new-empty-window;

[Desktop Action new-empty-window]
Name=New Empty Window
Exec=%h/.local/bin/antigravity-launcher.sh --launch --new-window %F
Icon=antigravity
"

DESKTOP_FILE_URL="[Desktop Entry]
Type=Application
Name=Antigravity(SB) - URL Handler
Comment=Handle antigravity:// URLs
Exec=%h/.local/bin/antigravity-launcher.sh --launch --open-url %U
Icon=antigravity
Terminal=false
NoDisplay=true
Categories=Development;
MimeType=x-scheme-handler/antigravity;
StartupNotify=true
"

do_install() {
	local bin_dir="$HOME/.local/bin"
	local desktop_dir="$HOME/.local/share/applications"

	mkdir -p "$bin_dir" "$desktop_dir"

	cp "$0" "$bin_dir/antigravity-launcher.sh"
	chmod +x "$bin_dir/antigravity-launcher.sh"

	echo "$DESKTOP_FILE_MAIN" >"$desktop_dir/antigravity.desktop"
	echo "$DESKTOP_FILE_URL" >"$desktop_dir/antigravity-url-handler.desktop"
	chmod +x "$desktop_dir/antigravity.desktop" "$desktop_dir/antigravity-url-handler.desktop"
	update-desktop-database "$desktop_dir" 2>/dev/null || true

	echo "Installed launcher to $bin_dir/antigravity-launcher.sh"
	echo "Desktop files installed to $desktop_dir"
	exit 0
}

do_remove() {
	local bin_dir="$HOME/.local/bin"
	local desktop_dir="$HOME/.local/share/applications"

	rm -f "$bin_dir/antigravity-launcher.sh"
	rm -f "$desktop_dir/antigravity.desktop"
	rm -f "$desktop_dir/antigravity-url-handler.desktop"
	update-desktop-database "$desktop_dir" 2>/dev/null || true

	echo "Removed launcher and desktop files"
	exit 0
}

show_help() {
	cat <<EOF
Antigravity Launcher

Usage: antigravity-launcher.sh
  --install                 Copy launcher and desktop files to ~/.local
  --remove                  Remove installed launcher and desktop files
  --exec <bin> [args...]    Run arbitrary binary with bubblewrap isolation
  --launch [args...]        Launch Antigravity
  --help                    Show this help

Environment variables:
  ANTIGRAVITY_BWRAP_EXTRA_ARGS  Additional bubblewrap arguments (space-separated)

EOF
	exit 0
}

case "${1:-}" in
--install)
	do_install
	;;
--remove)
	do_remove
	;;
--help | -h | "")
	show_help
	;;
--launch)
	shift
	;;
esac

# update electron flags from config file
lines=()
if [[ -f "${electron_flags_file}" ]]; then
	mapfile -t lines <"${electron_flags_file}"
fi
for line in "${lines[@]}"; do
	if [[ ! "${line}" =~ ^[[:space:]]*#.* ]] && [[ -n "${line}" ]]; then
		electron_flags+=("${line}")
	fi
done

# update antigravity flags from config file
if [[ -f "${antigravity_flags_file}" ]]; then
	mapfile -t CODEMAPFILE <"${antigravity_flags_file}"
fi
for line in "${CODEMAPFILE[@]}"; do
	if [[ ! "${line}" =~ ^[[:space:]]*#.* ]] && [[ -n "${line}" ]]; then
		antigravity_flags+=("${line}")
	fi
done

# basic bubblewrap argument list
bwrap_args=(
	# Unshare namespaces for isolation
	--unshare-all
	--share-net
	--die-with-parent
	--new-session
	# let antigravity debug processes
	--cap-add CAP_SYS_PTRACE
	# Mount host root read-only
	--ro-bind / /
	# Overlay a writable tmpfs on /tmp
	--tmpfs /tmp
	# Mount devices and process info
	--dev-bind /dev /dev
	--ro-bind /sys /sys
	--proc /proc
	# bind the .antigravity folder to $HOME
	--bind "$persistent_home" "$HOME"
	# --- OVERRIDES ---
	# Map: $HOME/AntigravityWorkspace -> $persistent_home/AntigravityWorkspace
	--bind "$work_dir" "$work_dir"
	# Bind X11 / Wayland Sockets (Display)
	--ro-bind /tmp/.X11-unix /tmp/.X11-unix
	--setenv DISPLAY "$DISPLAY"
	--setenv XAUTHORITY "$XAUTHORITY"
	# Change Dir to AntigravityWorkspace
	--chdir "$work_dir"
)

# Wayland Support
if [[ -n "$XDG_RUNTIME_DIR" ]]; then
	bwrap_args+=(
		--bind "$XDG_RUNTIME_DIR" "$XDG_RUNTIME_DIR"
		--setenv XDG_RUNTIME_DIR "$XDG_RUNTIME_DIR"
	)
fi

# Optional: Add extra arguments via environment variable
if [[ -n "${ANTIGRAVITY_BWRAP_EXTRA_ARGS:-}" ]]; then
	read -ra EXTRA_ARGS <<<"$ANTIGRAVITY_BWRAP_EXTRA_ARGS"
	bwrap_args+=("${EXTRA_ARGS[@]}")
fi

mkdir -p "$persistent_home" "$work_dir"
mkdir -p "$persistent_home/$(realpath --relative-to="$HOME" "$work_dir")"

# Check if the first argument is --exec and a second argument exists
if [[ "${1:-}" == "--exec" ]] && [[ -n "${2:-}" ]]; then
	app_bin="$2"
	shift 2 # Remove --exec and the path from the argument list
	exec bwrap "${bwrap_args[@]}" "$app_bin" "$@"
fi

cat <<EOF
Starting Antigravity with Persistent Home
  Container Home:     $persistent_home
  Workspace:          $work_dir
  BubbleWrap Args:    ${bwrap_args[@]}
  Electron Bin:       $app_bin
  Electron App Dir:   $app_dir
  Electron Flags:     ${electron_flags[@]}
  Antigravity Flags:  ${antigravity_flags[@]}
EOF

exec bwrap "${bwrap_args[@]}" \
	"$app_bin" "$app_dir" "${electron_flags[@]}" "${antigravity_flags[@]}" "$@"
