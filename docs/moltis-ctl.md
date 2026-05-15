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
Then visit `http://localhost:13131`.

## Commands

| Command | Description |
|---|---|
| `install` | Initializes `~/.moltis` and the systemd service. |
| `edit` | Edit `moltis.env` (passwords, providers, etc.). |
| `logs` | View server output and setup codes. |
| `exec` / `shell` | Sandboxed execution environment for CLI tasks. |

## Implementation Considerations

### Network Access
- `CapabilityBoundingSet=CAP_NET_BIND_SERVICE`: Allows the service to bind to privileged ports or all interfaces if configured.
- Default bind address is `0.0.0.0` (accessible from the network).

### Storage
- Uses `~/.moltis` for all persistent data, including sessions and local databases.
- `HERMES_HOME` pattern: Integrated with `~/agent-shared` for cross-agent collaboration.

### Device Access
- `PrivateDevices=no`: Set to allow potential hardware acceleration or specific device-bound operations.

### Environment
Configured via `~/.config/systemd/user/moltis.env`. Key variables include `MOLTIS_PASSWORD`, `MOLTIS_PROVIDER`, and `MOLTIS_API_KEY`.
