# Nanobot Setup and Usage Guide

`nanobot-ctl` is a lightweight, virtual environment based installation and management script designed to deploy the `nanobot` python service. It utilizes `uv` to manage an isolated virtual environment and integrates seamlessly with `systemd` user services.

## Installation

Ensure you have `uv` installed, then simply run the script's `install` command:

```bash
./scripts/nanobot-ctl install
```

During installation, `nanobot-ctl` will:
1. Create a dedicated isolated virtual environment at `~/.local/share/nanobot/venv`.
2. Install the `nanobot` package into that environment using `uv pip`.
3. Generate a secured `systemd` user service unit (`nanobot.service`).
4. Automatically enable and start the newly created service.

## Usage

The `nanobot-ctl` wrapper acts as your primary entry point for managing the service. 

Available commands:

| Command | Description |
|---|---|
| `install` | Creates the virtual environment, installs nanobot, and sets up systemd. |
| `uninstall` | Tears down the setup: stops/disables the service, removes the `.service` file, and deletes the `venv`. |
| `update` | Upgrades the nanobot python package using `uv pip` and restarts the service. |
| `start` / `stop` / `restart` / `status` | Hooks directly to corresponding `systemctl --user` commands for managing the daemon. |
| `enable` / `disable` | Toggles whether the nanobot service auto-starts on host boot. |
| `logs` | Quickly tail and follow the service metrics using `journalctl --user -f`. |
| `config` | Opens `~/.nanobot/config.json` inside your `$EDITOR` (or `nano` by default). |
| `shell` | Spawns a subshell with the nanobot virtual environment instantly activated for debugging. |
| `exec` | Spawns a transient, one-shot `systemd-run` user unit executing the nanobot binary with identical sandboxing as the background daemon, allowing you to run standalone tasks (e.g. `./scripts/nanobot-ctl exec onboard`). |

## Security Architecture

The `nanobot` service runs as a restrictive `systemd` user service. By design, the overarching system prevents `nanobot` from compromising user data.

### Isolated Home Directory
Similar to `picoclaw`, explicit paths are obfuscated to prevent rogue agent behavior:
- `ProtectSystem=strict` and `TemporaryFileSystem=%h` prevent the background process from interacting with your real home partitions.
- Specific necessary paths are re-bound using `BindPaths` (e.g., `%h/.nanobot-service:%h/.nanobot` and `%h/agent-shared:%h/agent-shared`), allowing the agent *only* to access data within explicit operational directories.

### Allowed Nested Sandboxing (Bubblewrap Support)
While many systemd hardening guidelines dictate strict sandbox rules, the `nanobot.service` unit specifically relaxes constraints that interfere with `bwrap`. `nanobot` is designed to run its *own* agent code wrapped in **bubblewrap (`bwrap`) nested isolation**.

To make `bwrap` function optimally, the `systemd` service:
- Excludes the `RestrictNamespaces=yes` directive, as `bwrap` leverages unprivileged user namespaces (`CLONE_NEWUSER` + `CLONE_NEWNS`) to build its sandbox dynamically.
- Drops explicit `ProtectProc` limitations allowing `bwrap` to securely bind a localized `/proc` interface without crashing on unshare.
- Employs `NoNewPrivileges=yes`, preventing escalation while naturally supporting `bwrap`'s internal capability drop patterns.
