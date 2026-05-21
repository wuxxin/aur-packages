# ZeroClaw Agent Management Guide

`zeroclaw-ctl` manages the ZeroClaw Gateway and agent runtime, providing a hardened execution environment that supports Bubblewrap/Landlock isolation.

## Installation

```bash
./scripts/zeroclaw-ctl install
```

## Commands

| Command | Description |
|---|---|
| `install` | Initializes `~/.local/share/zeroclaw` and the systemd service. |
| `uninstall` | Tears down the service (preserves data and environment). |
| `edit` | Edit `zeroclaw.env` to apply custom environment variables. |
| `logs` | View server and gateway output. |
| `exec` | Run `zeroclaw` CLI commands in the sandboxed environment. |
| `shell` | Spawn an interactive shell in the zeroclaw systemd environment. |

## Implementation Considerations

### Configuration & Ports
- **Default Port**: `42617` (ZeroClaw Gateway)
- **Environment**: Loaded from `~/.config/systemd/user/zeroclaw.env` and passed to the `zeroclaw gateway --port $ZEROCLAW_PORT` command.

### Sandboxing Profile
ZeroClaw utilizes the **Relaxed Namespaces Profile** in its systemd unit. This is necessary because ZeroClaw supports nested sandboxing mechanisms (Bubblewrap) for its tool executions.
- `ProtectProc=invisible`, `ProcSubset=pid`, and `RestrictNamespaces=yes` are omitted.
- Provides standard system filesystem isolation while preserving the ability for the agent to spawn secure sub-sandboxes via `bwrap`.
