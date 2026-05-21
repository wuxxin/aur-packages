# Nanobot Setup and Usage Guide

`nanobot-ctl` is a lightweight, virtual environment based installation and management script designed to deploy the `nanobot` python service. It utilizes `uv` to manage an isolated virtual environment and integrates seamlessly with `systemd` user services.

## Installation

Ensure you have `uv` installed, then simply run the script's `install` command:

```bash
./scripts/nanobot-ctl install
```

During installation, `nanobot-ctl` will set up the isolated environment and generate standard service files.

## Commands

`nanobot-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Implementation Considerations

### Initialization
If the configuration is empty, the installer will prompt you to run the onboarding wizard:
```bash
./scripts/nanobot-ctl exec onboard --wizard
```

### Configuration & Ports
- **Configuration File**: Stored at `~/.local/share/nanobot/config.json`.
- **Default Port**: The gateway service runs on port `8790` (set via `--port 8790` in the systemd service unit) to prevent conflicts with other services.

## Signal Channel Configuration

NanoBot supports native Signal integration. It communicates with a local `signal-cli` daemon in HTTP mode.

### Configuration

Add the following to your `~/.local/share/nanobot/config.json` configuration file under the `"channels"` block (via `nanobot-ctl config`):

```json
{
  "channels": {
    "signal": {
      "enabled": true,
      "phoneNumber": "+1234567890",
      "daemonHost": "localhost",
      "daemonPort": 50888,
      "dm": {
        "enabled": true,
        "policy": "open"
      },
      "group": {
        "enabled": true,
        "policy": "open",
        "requireMention": true
      }
    }
  }
}
```

Ensure the local `signal-cli` daemon is running. NanoBot will connect, handle inbound messages via Server-Sent Events, convert markdown formatting to native Signal styles, and handle reconnects automatically.

### Security and Isolation
- **Isolated HOME**: `HOME` is redirected to `~/.local/share/nanobot` within the service.
- **Sandboxing**: Uses `ProtectSystem=strict` and `TemporaryFileSystem=%h` to prevent unauthorized home directory access.
- **Persistent Bindings**:
    - `~/.local/share/nanobot`: Primary configuration and state.
    - `~/agent-shared`: Shared integration directory.

### Nested Sandboxing (Bubblewrap Support)
Nanobot is designed to run its own agent code wrapped in **bubblewrap (`bwrap`)** nested isolation. To support this:
- `RestrictNamespaces=yes` is **omitted**.
- `ProtectProc=invisible` and `ProcSubset=pid` are **omitted**.
- `NoNewPrivileges=yes` is retained as it naturally supports `bwrap`'s internal capability drop patterns.
