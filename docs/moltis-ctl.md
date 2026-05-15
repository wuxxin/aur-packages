# Moltis Agent Management Guide

`moltis-ctl` is a control script for the Moltis Agent server, based on the `openfang-ctl` architecture.

## Installation

```bash
./scripts/moltis-ctl install
```

### Setup Code
On the first run, Moltis generates a unique setup code. You must retrieve this from the logs to complete the web-based configuration:
```bash
./scripts/moltis-ctl logs
```
Then visit `http://localhost:13131` to enter the code and create your admin account.

## Commands

| Command | Description |
|---|---|
| `install` | Initializes `~/.local/share/moltis` and the systemd service. |
| `uninstall` | Tears down the service (preserves data and env). |
| `edit` | Edit `moltis.env` (passwords, providers, etc.). |
| `logs` | View server output and setup codes. |
| `exec` | Run `moltis` CLI commands in the sandboxed environment. |
| `shell` | Spawn an interactive shell in the moltis systemd environment. |

## Implementation Considerations

### Network Access
- **Privileged Binding**: `CapabilityBoundingSet=CAP_NET_BIND_SERVICE` and `AmbientCapabilities=CAP_NET_BIND_SERVICE` are set to allow Moltis to bind to privileged ports if necessary.
- **Bind Address**: The default `ExecStart` uses `--bind 0.0.0.0`, making the server accessible across the local network.

### Storage and Isolation
- **Persistent Data**: All state is stored in `~/.local/share/moltis`.
- **HOME Redirection**: The service redirects `HOME` to `%h/.local/share/moltis` to ensure all application state stays within the designated data directory.
- **Integration**: Explicitly binds `~/agent-shared` to allow cross-agent data sharing.

### Security
- **Hardening**: Uses `NoNewPrivileges=yes`, `ProtectSystem=strict`, and `PrivateTmp=yes`.
- **Devices**: `PrivateDevices=no` is set to allow potential hardware-backed operations if required by specific plugins.

### Environment
Configured via `~/.config/systemd/user/moltis.env`. Key variables include `MOLTIS_PASSWORD`, `MOLTIS_PROVIDER`, and `MOLTIS_API_KEY`.
