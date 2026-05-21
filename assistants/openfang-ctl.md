# OpenFang Agent OS Management Guide

`openfang-ctl` manages the OpenFang Agent OS daemon, providing a hardened execution environment for agentic workloads.

## Installation

```bash
./scripts/openfang-ctl install
```

## Commands

`openfang-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Configuration & Ports

- **Default Port**: `4200` (OpenFang daemon API)
- **Secrets & Configuration**: Loaded from `~/.config/systemd/user/openfang.env` and defined via config settings in the configuration file (`~/.openfang/config.toml`).

## Signal Channel Configuration

OpenFang supports native Signal integration. In this environment, it interfaces with the Go-based REST API wrapper.

### Configuration

Add the following to your `~/.openfang/config.toml` config file (located in the sandboxed home directory at `~/.local/share/openfang/.openfang/config.toml`):

```toml
[channels.signal]
api_url = "http://localhost:50889"  # Endpoint of the signal-cli REST API
phone_number = "+1234567890"        # Your registered Signal phone number
allowed_users = ["+1987654321"]     # Optional: List of allowed phone numbers/UUIDs (empty = allow all)
default_agent = "my-agent"          # Optional: Default agent name to route messages to
```

Ensure both the `signal-cli` daemon and the REST API wrapper (listening on port `50889`) are active. OpenFang will connect to the REST wrapper to retrieve message updates and send replies.

## Onboarding

1. **Install Service**: Run `./scripts/openfang-ctl install` to set up the OpenFang home directory (`~/.local/share/openfang`) and register the systemd user service.
2. **Initialize Workspace**: Run `./scripts/openfang-ctl exec init` to initialize the configuration workspace and prompt you interactively for LLM API keys to build `openfang.toml`.
3. **Start Service**: Start the daemon with `./scripts/openfang-ctl start`. Verify it is running by checking the dashboard at `http://localhost:4200`.
4. **Activate Hands**: Run `./scripts/openfang-ctl exec hand activate researcher` (or your hand of choice) to start autonomous background execution. Or run `./scripts/openfang-ctl exec chat <hand_name>` to converse directly.
5. **Switch to Local Inference & Qwen**: Add a local OpenAI provider to `~/.openfang/config.toml` (which is located under the isolated home at `~/.local/share/openfang/.openfang/config.toml`):
   ```toml
   [providers.models.openai.local]
   model = "qwen"
   uri = "http://localhost:50080/v1"
   api_key = "unused"
   ```
   Update your default agent profile's routing to target `openai.local`.

### OpenClaw Migration

OpenFang supports automatic migration from an existing OpenClaw installation. When you run:
```bash
./scripts/openfang-ctl exec init
```
OpenFang will scan your system for legacy OpenClaw directories (such as `~/.openclaw`), read your configuration, and import existing data, agent specifications, and credentials into `openfang.toml`.

## Implementation Considerations

### Nested Sandboxing (Bubblewrap Support)
OpenFang often orchestrates sub-agents that require their own isolation. To support **bubblewrap (`bwrap`)** nested sandboxing:
- **Namespaces**: `RestrictNamespaces=yes` is **omitted**. `bwrap` relies on unprivileged user namespaces (`CLONE_NEWUSER` and `CLONE_NEWNS`) to build its sandbox.
- **Process Info**: `ProtectProc=invisible` and `ProcSubset=pid` are **omitted**. This allows `bwrap` to securely bind its own `/proc` filesystem without crashing due to lack of visibility.
- **Elevation**: `NoNewPrivileges=yes` is maintained as it is compatible with modern `bwrap` and enhances overall security.

### Filesystem Hardening
- **Strict Protection**: Uses `ProtectSystem=strict` and `TemporaryFileSystem=%h` to ensure the daemon cannot see or modify the user's real home directory by default.
- **Explicit Mounts**:
    - `~/.local/share/openfang`: Persistent data and state store.
    - `~/agent-shared`: Shared integration directory.
- **Read-Only System Paths**: SSL certificates and network configuration are mounted as read-only.

### Environment
- **HOME Redirection**: `HOME` is set to `%h/.local/share/openfang` within the service to isolate user-level configuration (like `.ssh` or `.gitconfig`).
- **Secrets**: Environment variables are loaded from `~/.config/systemd/user/openfang.env`.
