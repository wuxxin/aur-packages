# NanoClaw Agent Management Guide

`nanoclaw-ctl` manages the NanoClaw runtime, ensuring secure operations for the webhook server and container executions.

## Installation

```bash
./scripts/nanoclaw-ctl install
```

## Commands

`nanoclaw-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Implementation Considerations

### Configuration & Ports
- **Default Port**: `3000` (NanoClaw Webhook server, overridable via `WEBHOOK_PORT`).
- **Environment**: Loaded from `~/.config/systemd/user/nanoclaw.env`.

### Sandboxing Profile
NanoClaw runs the **Relaxed Namespaces Profile** alongside disabled `PrivateDevices=yes` (`PrivateDevices=no`). This relaxed setup is required because NanoClaw spins up local Docker/Podman containers (`nanoclaw-agent:latest`) for isolated tool execution.
- `ProtectProc=invisible`, `ProcSubset=pid`, and `RestrictNamespaces=yes` are disabled to allow nested container isolation.
- `PrivateDevices=no` is set to ensure the agent has visibility to resources (like `/dev`) required to interact with local container runtimes.
