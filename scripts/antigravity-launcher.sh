#!/usr/bin/env bash
# Antigravity Sandbox - Persistent Home Edition

# Configuration
app_bin="/opt/Antigravity/antigravity"
app_dir="/opt/Antigravity"
persistent_home="$HOME/.local/share/antigravity"
work_dir="$HOME/AntigravityWorkspace"
agent_shared_dir="$HOME/agent-shared"
download_dir="/data/download"
antigravity_flags_file="${persistent_home}/.config/antigravity-flags.conf"
electron_flags_file="${persistent_home}/.config/electron-flags.conf"
antigravity_flags=()
electron_flags=(
    --disable-dev-shm-usage
    --disable-chromium-sandbox
    --no-sandbox
)

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
lines=()
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
    # bind the .local/share/antigravity folder to $HOME
    --bind "$persistent_home" "$HOME"
    # --- OVERRIDES ---
    # Map: $HOME/AntigravityWorkspace -> $persistent_home/AntigravityWorkspace
    --bind "$work_dir" "$work_dir"
    # Map: $HOME/agent-shared -> $persistent_home/agent-shared
    --bind "$agent_shared_dir" "$agent_shared_dir"
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

mkdir -p "$persistent_home" "$work_dir"
mkdir -p "$persistent_home/$(realpath --relative-to="$HOME" "$work_dir")"
mkdir -p "$persistent_home/$(realpath --relative-to="$HOME" "$agent_shared_dir")"
# create symlink for ~/download to $download_dir
download_symlink="$persistent_home/download"
if test ! -L "$download_symlink"; then
    if test -e "$download_symlink"; then rm "$download_symlink"; fi
    ln -s "$download_dir" "$download_symlink"
fi

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
  Agent Shared:       $agent_shared_dir
  Download Dir:       $download_dir
  BubbleWrap Args:    ${bwrap_args[@]}
  Electron Bin:       $app_bin
  Electron App Dir:   $app_dir
  Electron Flags:     ${electron_flags[@]}
  Antigravity Flags:  ${antigravity_flags[@]}
EOF

exec bwrap "${bwrap_args[@]}" \
    "$app_bin" "$app_dir" "${electron_flags[@]}" "${antigravity_flags[@]}" "$@"
