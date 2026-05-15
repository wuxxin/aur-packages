# Antigravity Sandbox Launcher

`antigravity-launcher.sh` is a wrapper for running the Antigravity IDE (and other Electron apps) inside a **Bubblewrap (`bwrap`)** sandbox with a persistent, isolated home directory.

## Features

- **Persistent Home**: Redirects `$HOME` to `~/.antigravity` within the sandbox.
- **Filesystem Isolation**: Mounts the host root as read-only and uses a `tmpfs` for `/tmp`.
- **Workspace Integration**: Explicitly binds `~/AntigravityWorkspace` and `~/agent-shared` into the sandbox.
- **X11/Wayland Support**: Securely shares display sockets and environment variables.
- **Configurable Flags**: Supports custom Electron and Antigravity flags via configuration files.

## Configuration

The launcher reads flags from the following files inside `~/.antigravity`:
- `.config/electron-flags.conf`: Arguments passed to the Electron runtime (e.g. `--disable-gpu`).
- `.config/antigravity-flags.conf`: Arguments passed directly to the Antigravity application.

## Usage

```bash
./scripts/antigravity-launcher.sh
```

### Advanced Usage: Transient Sandboxing
You can use the launcher to run *any* binary inside the same hardened Antigravity environment using the `--exec` flag:

```bash
./scripts/antigravity-launcher.sh --exec /usr/bin/bash
```

## Implementation Considerations

### Security Model
- **`--unshare-all`**: All namespaces are unshared by default. Only network access (`--share-net`) is retained.
- **Privilege Control**: Adds `CAP_SYS_PTRACE` to allow Antigravity to debug child processes (e.g. compilers or test runners) while maintaining isolation.
- **Sandboxing Relaxations**: Electron requires `--no-sandbox` and `--disable-chromium-sandbox` when running inside a pre-existing `bwrap` container to avoid namespace conflicts.

### Directory Mapping
- **Downloads**: Symlinks `~/download` inside the sandbox to `/data/download` on the host (if available).
- **Home**: The host's `~/.antigravity` is presented as `$HOME` inside the sandbox, ensuring that configuration files (like `.gitconfig` or `.ssh`) created within the app are persistent but isolated from the real host home.
