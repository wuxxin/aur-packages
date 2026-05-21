# ZeroClaw Agent Management Guide

`zeroclaw-ctl` manages the ZeroClaw Gateway and agent runtime, providing a hardened execution environment that supports Bubblewrap/Landlock isolation.

## Installation

```bash
./scripts/zeroclaw-ctl install
```

## Commands

`zeroclaw-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Configuration & Ports

- **Default Port**: `42617` (ZeroClaw Gateway)
- **Environment**: Loaded from `~/.config/systemd/user/zeroclaw.env` and passed to the `zeroclaw gateway --port $ZEROCLAW_PORT` command.

## Signal Channel Configuration

ZeroClaw supports native Signal integration. It communicates with the daemon via the REST API wrapper.

### Configuration

Add the following to your `config.toml` configuration file (located in the sandboxed home directory at `~/.local/share/zeroclaw/.zeroclaw/config.toml`):

```toml
[channels.signal]
enabled = true
phone_number = "+1234567890"                  # Your registered Signal phone number
signal_cli_rest_url = "http://localhost:50889" # Endpoint of the signal-cli-rest-api service
```

Make sure both the `signal-cli` daemon and the REST API wrapper (listening on port `50889`) are active. ZeroClaw will retrieve message payloads and send messages through this endpoint.

## Implementation Considerations

### Sandboxing Profile
ZeroClaw utilizes the **Relaxed Namespaces Profile** in its systemd unit. This is necessary because ZeroClaw supports nested sandboxing mechanisms (Bubblewrap) for its tool executions.
- `ProtectProc=invisible`, `ProcSubset=pid`, and `RestrictNamespaces=yes` are omitted.
- Provides standard system filesystem isolation while preserving the ability for the agent to spawn secure sub-sandboxes via `bwrap`.
