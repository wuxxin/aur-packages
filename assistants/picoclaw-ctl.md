# PicoClaw Agent Management Guide

`picoclaw-ctl` is a control script for the PicoClaw agent and its launcher, designed similarly to the `openfang-ctl` and `moltis-ctl` architecture.

## Installation

```bash
./scripts/picoclaw-ctl install
```

## Commands

`picoclaw-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Implementation Considerations

### Configuration & Ports
- **Default Ports**:
  - **Gateway (HTTP/Webhook channels)**: `18790`
  - **Launcher Web UI**: `18800`
- **Secrets & Configuration**: Loaded from `~/.config/systemd/user/picoclaw.env` and defined via config settings in `~/.local/share/picoclaw/config.json`.

### Strict Sandboxing
Unlike OpenFang, which relaxes some system restrictions to allow nested `bwrap` sandboxing, PicoClaw uses a stricter confinement profile as recommended by the upstream maintainers:
- **Process Info**: `ProtectProc=invisible` and `ProcSubset=pid` are enabled to hide other system processes from the daemon.
- **Namespaces**: `RestrictNamespaces=yes` is enforced, preventing the creation of new namespaces.
- **Memory Protection**: `MemoryDenyWriteExecute=yes` is enabled to prevent the creation of memory mappings that are writable and executable at the same time.

### Storage and Isolation
- **Persistent Data**: All state is stored in `~/.local/share/picoclaw` (which is mapped to `PICOCLAW_HOME`).
- **Integration**: Explicitly binds `~/agent-shared` to allow cross-agent data sharing and integration.
- **Hardening**: Standard systemd sandbox features such as `NoNewPrivileges=yes`, `ProtectSystem=strict`, and `PrivateTmp=yes` are strictly applied.

### Launcher vs CLI
- **Service Execution**: The systemd background service uses `picoclaw-launcher -no-browser` as its `ExecStart` target, running the built-in web console service.
- **CLI Execution**: The `picoclaw-ctl exec` command specifically targets the `/usr/bin/picoclaw` executable rather than the launcher, providing direct access to the core agent CLI binary.

### Environment Context
Environment variables are securely loaded from `~/.config/systemd/user/picoclaw.env`. The systemd service implicitly passes essential context to the underlying agent using specific environment variables:
- `PICOCLAW_HOME=%h/.local/share/picoclaw`
- `PICOCLAW_CONFIG=%h/.local/share/picoclaw/config.json`
- `PICOCLAW_BINARY=/usr/bin/picoclaw`
