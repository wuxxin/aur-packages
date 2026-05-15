# Hermes Agent Management Guide

`hermes-ctl` is a management wrapper for the `hermes-agent` messaging gateway. It provides a standardized interface for installation, configuration, and service lifecycle management using `systemd` user units.

## Installation

```bash
./scripts/hermes-ctl install
```

This command will:
1. Create the `~/.hermes` home directory.
2. Generate a default environment file at `~/.config/systemd/user/hermes-gateway.env`.
3. Create and enable the `hermes-gateway.service` systemd user unit.

## Commands

| Command | Description |
|---|---|
| `install` | Full setup of home directory, environment, and systemd service. |
| `uninstall` | Stops and removes the service (preserves data and config). |
| `start` / `stop` / `restart` | Standard service controls. |
| `status` | View service health and uptime. |
| `logs` | Tail service output via `journalctl`. |
| `edit` | Open the environment file in `$EDITOR` and restart the service on exit. |
| `exec` | Run a one-shot `hermes` command inside the hardened service environment. |
| `shell` | Spawn an interactive shell with the same environment and sandboxing. |

## Implementation Considerations

### Graceful Shutdown and Restarts
Hermes uses a graceful drain mechanism. The service is configured with:
- `KillMode=mixed`: Ensures that if the gateway is interrupted, child processes (like tool-call subshells) are correctly handled.
- `KillSignal=SIGTERM`: Standard termination signal.
- `ExecReload=/bin/kill -USR1 $MAINPID`: Triggers the gateway's internal graceful restart logic.
- `TimeoutStopSec=210`: Provides a budget for the 180s default drain timeout plus cleanup headroom.
- `RestartForceExitStatus=75`: Hermes exits with status 75 when a planned restart is requested; systemd is configured to always restart on this status.

### Security and Sandboxing
The service runs with `ProtectSystem=strict` and `TemporaryFileSystem=%h`. Only the following paths are writable:
- `~/.hermes`: The persistent home for config, logs, and state.
- `~/agent-shared`: Shared directory for agent-to-agent or agent-to-human integration.

### Environment and Isolation
- **Isolated HOME**: The `HOME` environment variable is redirected to `~/.hermes` within the service to ensure that any tools called by the agent (pip, git, etc.) do not leak state into the user's real home.
- **Secrets Management**: API keys and secrets are stored in `~/.config/systemd/user/hermes-gateway.env` and loaded via `EnvironmentFile`.

### Container Backend Support
If you plan to use `docker` or `podman` as a terminal backend from within the gateway:
- The default `NoNewPrivileges=yes` and `PrivateDevices=yes` may need to be relaxed.
- Rootless podman specifically requires access to `/dev/fuse` and certain namespaces that are restricted by default systemd hardening. See the comments in `hermes-ctl` for suggested overrides.
