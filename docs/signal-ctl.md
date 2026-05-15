# Signal CLI Management Guide

`signal-ctl` manages `signal-cli` as a background daemon and provides an optional REST API wrapper for integration with other agents.

## Installation

```bash
./scripts/signal-ctl install
```

This command:
1. Initializes `~/.local/share/signal-cli`.
2. Generates environment files for both the CLI daemon and the REST API.
3. Configures a JSON-RPC bridge.
4. Enables and starts both services: `signal-cli.service` and `signal-rest-api.service`.

## Account Setup

Before starting the service for the first time, you must link or register an account. Use the `shell` command to perform this in the restricted environment:

```bash
./scripts/signal-ctl stop
./scripts/signal-ctl shell

# Link an existing account (shows a QR code)
signal-cli --config "$SC_CONFIG_DIR" link --name "$(hostname)" | \
    tee >(head -1 | qrencode -t ANSIUTF8 >&2)

# Verify if prompted
signal-cli --config "$SC_CONFIG_DIR" verify <code>

# Exit shell and start services
exit
./scripts/signal-ctl start
```

## Commands

| Command | Description |
|---|---|
| `install` | Full dual-service setup. |
| `uninstall` | Stops and removes services (preserves account data). |
| `edit` | Opens both `.env` files and restarts services on exit. |
| `logs` | Combined logs for the daemon and the REST API. |
| `exec` | Run `signal-cli` commands (e.g. `listGroups`) in the sandbox. |
| `shell` | Interactive shell for manual account management. |

## Implementation Considerations

### Architecture
- **Dual Services**: Runs the Java-based `signal-cli` as a JSON-RPC daemon (TCP port 50888) and a Go-based `signal-cli-rest-api` as a frontend (HTTP port 51888).
- **Communication**: The REST API connects to the daemon via the JSON-RPC interface.

### Security
- **Hardening**: `signal-cli` runs with `ProtectSystem=strict` and `TemporaryFileSystem=%h`.
- **JVM Requirements**: `MemoryDenyWriteExecute` is **disabled** because the JVM requires writable and executable memory for JIT compilation.
- **Isolation**: The data directory `~/.local/share/signal-cli` is bind-mounted, but the rest of the home directory is hidden.

### Configuration
- `signal-cli.env`: Controls the phone number (`SC_ACCOUNT`), RPC ports, and extra flags (e.g. `--ignore-stories`).
- `signal-api.env`: Controls the REST API bind address and `MODE=json-rpc`.
