# NanoClaw Agent Management Guide

`nanoclaw-ctl` manages the NanoClaw runtime, ensuring secure operations for the webhook server and container executions.

## Installation

```bash
./scripts/nanoclaw-ctl install
```

## Commands

| Command | Description |
|---|---|
| `install` | Initializes `~/.local/share/nanoclaw` and the systemd service. |
| `uninstall` | Tears down the service (preserves data and environment). |
| `edit` | Edit `nanoclaw.env` to apply custom environment variables. |
| `logs` | View webhook server and background execution output. |
| `exec` | Run `nanoclaw` CLI commands in the sandboxed environment. |
| `shell` | Spawn an interactive shell in the nanoclaw systemd environment. |

## Implementation Considerations

### Configuration & Ports
- **Default Port**: `3000` (NanoClaw Webhook server, overridable via `WEBHOOK_PORT`).
- **Environment**: Loaded from `~/.config/systemd/user/nanoclaw.env`.

### Sandboxing Profile
NanoClaw runs the **Relaxed Namespaces Profile** alongside disabled `PrivateDevices=yes` (`PrivateDevices=no`). This relaxed setup is required because NanoClaw spins up local Docker/Podman containers (`nanoclaw-agent:latest`) for isolated tool execution.
- `ProtectProc=invisible`, `ProcSubset=pid`, and `RestrictNamespaces=yes` are disabled to allow nested container isolation.
- `PrivateDevices=no` is set to ensure the agent has visibility to resources (like `/dev`) required to interact with local container runtimes.
