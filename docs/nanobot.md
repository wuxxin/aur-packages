# Nanobot Setup and Usage Guide

`nanobot-ctl` is a lightweight, virtual environment based installation and management script designed to deploy the `nanobot` python service. It utilizes `uv` to manage an isolated virtual environment and integrates seamlessly with `systemd` user services.

## Installation

Ensure you have `uv` installed, then simply run the script's `install` command:

```bash
./scripts/nanobot-ctl install
```

During installation, `nanobot-ctl` will:
1. Create a dedicated isolated virtual environment at `~/.local/share/nanobot/venv`.
2. Install the `nanobot-ai` package into that environment using `uv pip`.
3. Create the `~/.local/share/nanobot` configuration directory.
4. Generate a secured `systemd` user service unit (`nanobot.service`).
5. Automatically enable and start the service (if initialized).

## Commands

The `nanobot-ctl` wrapper acts as your primary entry point for managing the service. 

| Command | Description |
|---|---|
| `install` | Creates the virtual environment, installs nanobot, and sets up systemd. |
| `uninstall` | Tears down the setup: stops/disables the service, removes the `.service` file, and deletes the `venv`. |
| `update` | Upgrades the nanobot python package using `uv pip` and restarts the service. |
| `start` / `stop` / `restart` | standard `systemctl --user` commands for managing the daemon. |
| `status` | View service health and journal status. |
| `logs` | Tail service logs using `journalctl --user -f`. |
| `config` | Opens `~/.local/share/nanobot/config.json` inside your `$EDITOR`. |
| `shell` | Spawns an interactive shell with the nanobot virtual environment and sandbox environment. |
| `exec` | Run `nanobot` CLI commands in the transient sandboxed service. |

## Implementation Considerations

### Initialization
If the configuration is empty, the installer will prompt you to run the onboarding wizard:
```bash
./scripts/nanobot-ctl exec onboard --wizard
```

### Security and Isolation
- **Isolated HOME**: `HOME` is redirected to `~/.local/share/nanobot` within the service.
- **Sandboxing**: Uses `ProtectSystem=strict` and `TemporaryFileSystem=%h` to prevent unauthorized home directory access.
- **Persistent Bindings**:
    - `~/.local/share/nanobot`: Primary configuration and state.
    - `~/.local/share/nanobot`: Virtual environment and transient data.
    - `~/agent-shared`: Shared integration directory.

### Nested Sandboxing (Bubblewrap Support)
Nanobot is designed to run its own agent code wrapped in **bubblewrap (`bwrap`)** nested isolation. To support this:
- `RestrictNamespaces=yes` is **omitted**.
- `ProtectProc=invisible` and `ProcSubset=pid` are **omitted**.
- `NoNewPrivileges=yes` is retained as it naturally supports `bwrap`'s internal capability drop patterns.
