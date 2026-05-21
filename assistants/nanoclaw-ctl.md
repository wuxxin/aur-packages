# NanoClaw Agent Management Guide

`nanoclaw-ctl` manages the NanoClaw runtime, ensuring secure operations for the webhook server and container executions.

## Installation

```bash
./assistants/nanoclaw-ctl install
```

## Commands

`nanoclaw-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Onboarding

1. **Install Service**: Run `./assistants/nanoclaw-ctl install` to set up `~/.local/share/nanoclaw` and register the systemd user service.
2. **Bootstrap Agent**: Run the initial setup command `./assistants/nanoclaw-ctl exec tsx scripts/init-first-agent.ts` (or trigger it interactively using the `/init-first-agent` operational skill via Claude Code) to initialize the central database, pair your messaging channel (Telegram, Discord, WhatsApp), and wire a messaging group.
3. **Authorize OneCLI Vault Secrets**: Access the OneCLI interface (default `http://127.0.0.1:10254`). Since new agents start in `selective` credential mode, authorize keys by running:
   ```bash
   onecli agents set-secret-mode --id <agent-group-id> --mode all
   ```
4. **Start Webhook Service**: Run `./assistants/nanoclaw-ctl start` to start the webhook server on the configured port (default `3000`). Inspect routing and execution via `./assistants/nanoclaw-ctl logs` or the `ncl` admin CLI.
5. **Switch to Local Inference & Qwen**: Edit `~/.config/systemd/user/nanoclaw.env` (via `./assistants/nanoclaw-ctl edit`) and set `LLM_PROVIDER=openai`, `LLM_BASE_URL=http://localhost:50080/v1`, `LLM_API_KEY=unused`, and `LLM_MODEL=qwen`.

### OpenClaw Migration

OpenClaw migration is not natively supported by NanoClaw. You will need to define your agents, platform channels, and credentials manually or write custom scripts to import data into NanoClaw's datastore.

## Implementation Considerations

### Configuration & Ports
- **Default Port**: `3000` (NanoClaw Webhook server, overridable via `WEBHOOK_PORT`).
- **Environment**: Loaded from `~/.config/systemd/user/nanoclaw.env`.

### Sandboxing Profile
NanoClaw runs the **Relaxed Namespaces Profile** alongside disabled `PrivateDevices=yes` (`PrivateDevices=no`). This relaxed setup is required because NanoClaw spins up local Docker/Podman containers (`nanoclaw-agent:latest`) for isolated tool execution.
- `ProtectProc=invisible`, `ProcSubset=pid`, and `RestrictNamespaces=yes` are disabled to allow nested container isolation.
- `PrivateDevices=no` is set to ensure the agent has visibility to resources (like `/dev`) required to interact with local container runtimes.
