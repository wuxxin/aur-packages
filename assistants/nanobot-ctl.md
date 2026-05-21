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

## Onboarding

1. **Install Service**: Run `./scripts/nanobot-ctl install` to initialize `~/.local/share/nanobot`, set up the python virtualenv, install the `nanobot-ai` package, and create the systemd unit.
2. **Configuration Wizard**: Run the interactive onboarding wizard via `./scripts/nanobot-ctl exec onboard --wizard` to generate the default configuration.
3. **Configure API & Model**: Edit `~/.local/share/nanobot/config.json` (via `./scripts/nanobot-ctl config`) to configure your API keys (e.g. OpenRouter/Anthropic under `providers`) and default models (under `agents.defaults`).
4. **Enable WebUI**: In the config, ensure the WebSocket channel is enabled:
   ```json
   { "channels": { "websocket": { "enabled": true } } }
   ```
5. **Start & Verify**: Run `./scripts/nanobot-ctl start`. Verify status with `./scripts/nanobot-ctl status` and access the WebUI console at `http://localhost:8790`.
6. **Switch to Local Inference & Qwen**: Edit `~/.local/share/nanobot/config.json` to configure the local OpenAI-compatible endpoint:
   ```json
   {
     "providers": {
       "openai_compatible": {
         "local": {
           "api_key": "unused",
           "base_url": "http://localhost:50080/v1"
         }
       }
     },
     "agents": {
       "defaults": {
         "provider": "openai_compatible/local",
         "model": "qwen"
       }
     }
   }
   ```

### OpenClaw Migration

OpenClaw migration is not natively supported by NanoBot. Configuration must be set up manually using the configuration wizard (`onboard --wizard`) or by editing the JSON configuration.

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
