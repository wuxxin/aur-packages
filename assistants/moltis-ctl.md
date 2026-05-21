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

`moltis-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Configuration & Ports

- **Default Port**: `13131` (Moltis Agent Server Web UI/API)
- **Secrets & Configuration**: Loaded from `~/.config/systemd/user/moltis.env`. Key variables include `MOLTIS_PASSWORD`, `MOLTIS_PROVIDER`, and `MOLTIS_API_KEY`.

## Signal Channel Configuration

Moltis has native support for receiving and sending Signal messages through an external `signal-cli` daemon.

### Configuration

Add a `[channels.signal.<account-id>]` section to `~/.local/share/moltis/moltis.toml`:

```toml
[channels.signal.personal]
account = "+1234567890"               # Your registered Signal phone number
http_url = "http://127.0.0.1:50888"   # Local signal-cli HTTP daemon port
dm_policy = "allowlist"               # "open", "allowlist", or "disabled"
allowlist = ["+1987654321"]           # Allowed sender phone numbers or UUIDs
group_policy = "disabled"             # "open", "allowlist", or "disabled"
mention_mode = "mention"              # "mention", "always", or "none"
otp_self_approval = true              # Let unknown DM senders self-approve with a PIN challenge
otp_cooldown_secs = 300               # Cooldown after 3 failed OTP attempts
text_chunk_limit = 4000               # Maximum UTF-8 bytes per outbound text chunk
```

Make sure `"signal"` is included in `channels.offered` in `moltis.toml` (it is included by default).

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
