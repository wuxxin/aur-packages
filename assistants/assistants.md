# Assistants and Integrations

This document describes information about several AI assistants, their sandboxing requirements, default port allocations, and external integrations (Local Inference and Signal) managed within this repository.

## Integrations

### Local Inference
- **Description**: Manages a persistent `llama-server` instance optimized for local LLM serving, specifically tuned for AMD ROCm hardware (tested on Radeon Pro W6800). Designed for high context lengths (Qwen 35B/27B) with optimized memory access and KV cache.
- **Sandboxing**: Requires `PrivateDevices=no` to access `/dev/dri` and `/dev/kfd`. Enforces `ProtectSystem=strict` while bind-mounting the user's home configuration and granting read-write access to `/data/public/machine-learning`.
- **Features**: Flash Attention, layer GPU offloading, hardware-specific concurrency parameters.

### Signal Integration
- **Description**: Connects agents to Signal. Runs a `signal-cli` daemon exposing both TCP and HTTP JSON-RPC interfaces. It also provides an optional Go-based REST API wrapper for robust, HTTP-based polling/webhook integrations (like linking OpenFang).
- **Sandboxing**: Standard filesystem hardening, but disables `MemoryDenyWriteExecute` because the underlying JVM (Java) requires it for JIT compilation. 
- **Features**: Account linking via QR code, dual daemon interfaces, and isolated home directory execution to prevent contamination.

The following assistants have native Signal channel integration available in their source code:
- [Hermes](hermes-ctl.md)
- [Moltis](moltis-ctl.md)
- [NanoBot](nanobot-ctl.md)
- [OpenFang](openfang-ctl.md)
- [ZeroClaw](zeroclaw-ctl.md)

To configure them, refer to their specific configuration sections in their respective control guides.


## Default Ports

The following default ports are used by various agent systems and services to avoid conflicts. When integrating new agents, ensure their configured `PORT` or `WEBHOOK_PORT` does not overlap with existing infrastructure.

| Agent/Service | Default Port(s) | Description / Protocol |
|---------------|-----------------|------------------------|
| **OpenFang** | `4200` | OpenFang daemon API (HTTP) |
| **Moltis** | `13131` | Moltis agent server Web UI/API (HTTP) |
| **PicoClaw** | `18790`, `18800` | Gateway (HTTP/Webhook) & Launcher Web UI |
| **NanoBot** | `8790` | NanoBot Gateway API |
| **Hermes** | `8000`, `8642`, `9119` | Hermes Messaging Gateway (API: 8642, UI: 9119) |
| **ZeroClaw** | `42617` | ZeroClaw Gateway |
| **NanoClaw** | `3000` | Webhook Server |
| **Signal-CLI** | `50887`, `50888`, `50889` | TCP JSON-RPC, HTTP JSON-RPC, REST API |
| **Local-Inference** | `50080` | Llama-server local instance |

## Sandboxing Architecture

Agent runtimes in this repository operate under strict, layered sandboxing configurations via systemd user services to protect the host system while allowing agents to execute their tools securely. 

Two primary isolation profiles are used across all assistants:

### 1. Strict Confinement Profile
Used by agents that execute tools directly or do not require creating new user namespaces for their internal sandboxing.
- `ProtectProc=invisible` and `ProcSubset=pid`: Hides other system processes.
- `RestrictNamespaces=yes`: Prevents the creation of new namespaces.
- `MemoryDenyWriteExecute=yes`: Prevents W^X memory mappings (unless specifically required by an interpreter).
- `PrivateTmp=yes`, `ProtectSystem=strict`, `PrivateDevices=yes`: Standard filesystem hardening.

### 2. Relaxed Namespaces Profile
Used by agents that orchestrate sub-agents or use tools like Bubblewrap (`bwrap`), Rootless Podman, or Docker for internal sandboxing.
- `RestrictNamespaces=yes` is **omitted** to allow `bwrap` or Podman to create `CLONE_NEWUSER` and `CLONE_NEWNS` unprivileged namespaces.
- `ProtectProc=invisible` and `ProcSubset=pid` are **omitted** so `bwrap` can securely bind its own `/proc` filesystem.
- `NoNewPrivileges=yes` is maintained for modern `bwrap` compatibility.
- `PrivateDevices` may be disabled (`no`) if access to the container daemon or GPU devices is required.

---

## Assistants

### Hermes
- **Major Features**: Messaging Gateway designed for agent-to-agent and agent-to-human integration. Features an OpenAI-compatible API and a Dashboard Web UI. Supports graceful shutdowns and nested container execution.
- **Language/Runtime**: Compiled binary.
- **Requirements**: `~/.local/share/hermes` for persistent state, `~/agent-shared` for integration. Can integrate with podman/docker backend.
- **Sandboxing**: Utilizes the **Relaxed Namespaces Profile** to support nested `bwrap` orchestration. Isolated `HOME` directory redirection.
- **Onboarding**:
  1. **Install Service**: Run `hermes-ctl install` to set up the home directory (`~/.local/share/hermes`) and generate/enable the systemd user service.
  2. **Set Environment**: Run `hermes-ctl edit` (or edit `~/.config/systemd/user/hermes-gateway.env`) to configure necessary provider environment variables (e.g. `OPENROUTER_API_KEY`).
  3. **Setup Wizard**: Run `hermes-ctl exec setup` to launch the interactive configuration setup (or `hermes-ctl exec claw migrate` to import configuration from an existing OpenClaw setup).
  4. **Start & Verify**: Start the service with `hermes-ctl start`. Monitor its logs via `hermes-ctl logs` and access the Web UI at `http://localhost:9119`.
  5. **Switch to Local Inference & Qwen**: Run `hermes-ctl edit` to set `OPENAI_API_BASE=http://localhost:50080/v1` and `OPENAI_API_KEY=unused`. Run `hermes-ctl exec setup` and configure the default model to `qwen` (or whatever model name is served by your local instance).

### Moltis
- **Major Features**: Agent server based on the openfang-ctl architecture. Web-based configuration and administration, persistent plugin/provider support, capable of privileged port binding.
- **Language/Runtime**: Compiled binary.
- **Requirements**: Needs a setup code on initial run to unlock the web UI. Uses `~/.local/share/moltis` for data.
- **Sandboxing**: Uses a mostly strict configuration but relies on specific network capability bounding (`CAP_NET_BIND_SERVICE`) and `PrivateDevices=no` if hardware-backed plugins are used. Isolated `HOME`.
- **Onboarding**:
  1. **Install Service**: Run `moltis-ctl install` to initialize `~/.local/share/moltis`, compile assets, and generate the systemd user service.
  2. **Launch Daemon**: Start the service via `moltis-ctl start`. On first run, a unique setup token is printed to the service output logs.
  3. **Extract Setup Token**: Run `moltis-ctl logs | grep "setup code"` to retrieve the unique authentication code.
  4. **Initialize Web UI**: Navigate to `http://localhost:13131` in your browser, enter the setup code, and configure your administrator password or WebAuthn passkey.
  > [!TIP]
  > For unattended deployments, edit `~/.config/systemd/user/moltis.env` via `moltis-ctl edit` and define `MOLTIS_PASSWORD`, `MOLTIS_PROVIDER`, and `MOLTIS_API_KEY` before starting the daemon to bypass the setup wizard.
  5. **Switch to Local Inference & Qwen**: Edit `~/.local/share/moltis/moltis.toml` (or via the Web UI) to configure a local OpenAI-compatible provider:
     ```toml
     [providers.models.openai.local]
     model = "qwen"
     uri = "http://localhost:50080/v1"
     api_key = "unused"
     ```
     Then point your target agent to use `model_provider = "openai.local"`.

### NanoBot
- **Major Features**: Lightweight python service built with `uv`. Features an onboarding wizard for simple configuration.
- **Language/Runtime**: Python. Uses isolated virtual environments managed by `uv`.
- **Requirements**: `uv` package manager installed.
- **Sandboxing**: Relies on the **Relaxed Namespaces Profile** because it natively spawns agent code wrapped in nested `bwrap` isolation. Isolated `HOME`.
- **Onboarding**:
  1. **Install Service**: Run `nanobot-ctl install` to initialize `~/.local/share/nanobot`, set up the python virtualenv, install the `nanobot-ai` package, and create the systemd unit.
  2. **Configuration Wizard**: Run the interactive onboarding wizard via `nanobot-ctl exec onboard --wizard` to generate the default configuration.
  3. **Configure API & Model**: Edit `~/.local/share/nanobot/config.json` to configure your API keys (e.g. OpenRouter/Anthropic under `providers`) and default models (under `agents.defaults`).
  4. **Enable WebUI**: In the config, ensure the WebSocket channel is enabled:
     ```json
     { "channels": { "websocket": { "enabled": true } } }
     ```
  5. **Start & Verify**: Run `nanobot-ctl start`. Verify status with `nanobot-ctl status` and access the WebUI console at `http://localhost:8790`.
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

### NanoClaw
- **Major Features**: Webhook server capable of securely executing containers for runtime tools.
- **Language/Runtime**: Container-based (`nanoclaw-agent:latest`).
- **Requirements**: Requires Docker/Podman running locally to spawn tool environments.
- **Sandboxing**: **Relaxed Namespaces Profile** with `PrivateDevices=no`. Strict profiles are dropped to allow the agent to launch local Docker/Podman containers successfully.
- **Onboarding**:
  1. **Install Service**: Run `nanoclaw-ctl install` to set up `~/.local/share/nanoclaw` and register the systemd user service.
  2. **Bootstrap Agent**: Run the initial setup command `nanoclaw-ctl exec tsx scripts/init-first-agent.ts` (or trigger it interactively using the `/init-first-agent` operational skill via Claude Code) to initialize the central database, pair your messaging channel (Telegram, Discord, WhatsApp), and wire a messaging group.
  3. **Authorize OneCLI Vault Secrets**: Access the OneCLI interface (default `http://127.0.0.1:10254`). Since new agents start in `selective` credential mode, authorize keys by running:
     ```bash
     onecli agents set-secret-mode --id <agent-group-id> --mode all
     ```
  4. **Start Webhook Service**: Run `nanoclaw-ctl start` to start the webhook server on the configured port (default `3000`). Inspect routing and execution via `nanoclaw-ctl logs` or the `ncl` admin CLI.
  5. **Switch to Local Inference & Qwen**: Edit `~/.config/systemd/user/nanoclaw.env` (via `nanoclaw-ctl edit`) and set `LLM_PROVIDER=openai`, `LLM_BASE_URL=http://localhost:50080/v1`, `LLM_API_KEY=unused`, and `LLM_MODEL=qwen`.

### OpenFang
- **Major Features**: Agent OS daemon that provides a hardened execution environment and orchestrates complex agentic workloads.
- **Language/Runtime**: Compiled binary.
- **Requirements**: `~/.local/share/openfang` and `~/agent-shared`.
- **Sandboxing**: **Relaxed Namespaces Profile** to support bubblewrap (`bwrap`) nested sandboxing for sub-agents. Read-only system paths and strict filesystem protection for the host.
- **Onboarding**:
  1. **Install Service**: Run `openfang-ctl install` to set up the OpenFang home directory (`~/.local/share/openfang`) and register the systemd user service.
  2. **Initialize Workspace**: Run `openfang-ctl exec init` to initialize the configuration workspace and prompt you interactively for LLM API keys to build `openfang.toml`.
  3. **Start Service**: Start the daemon with `openfang-ctl start`. Verify it is running by checking the dashboard at `http://localhost:4200`.
  4. **Activate Hands**: Run `openfang-ctl exec hand activate researcher` (or your hand of choice) to start autonomous background execution. Or run `openfang-ctl exec chat <hand_name>` to converse directly.
  5. **Switch to Local Inference & Qwen**: Add a local OpenAI provider to `~/.openfang/config.toml` (which is located under the isolated home at `~/.local/share/openfang/.openfang/config.toml`):
     ```toml
     [providers.models.openai.local]
     model = "qwen"
     uri = "http://localhost:50080/v1"
     api_key = "unused"
     ```
     Update your default agent profile's routing to target `openai.local`.

### PicoClaw
- **Major Features**: HTTP/Webhook gateway and a dedicated Web UI launcher. Built-in web console and CLI integration.
- **Language/Runtime**: Compiled binary (`picoclaw`).
- **Requirements**: `~/.local/share/picoclaw` for persistent configuration.
- **Sandboxing**: **Strict Confinement Profile**. It hides other processes, prevents new namespaces, and denies writable/executable memory mappings. 
- **Onboarding**:
  - **Using the WebUI Launcher (Recommended)**:
    1. **Install Service**: Run `picoclaw-ctl install` to create the home directory (`~/.local/share/picoclaw`) and start `picoclaw-launcher -no-browser`.
    2. **Web Onboarding**: Open `http://localhost:18800` in your browser. Configure your LLM API Key under **Settings -> Providers** (credentials are saved securely in `.security.yml`) and set up a platform channel under **Settings -> Channels**.
    3. **Launch Gateway**: Click "Start Gateway" in the launcher web interface (runs on port `18790` by default) and begin chatting.
  - **Headless CLI Alternative**:
    1. **Onboard Configuration**: Run `picoclaw-ctl exec onboard` to generate `config.json` and initialize the workspace directory.
    2. **Define Config**: Configure model providers and channel rules in `~/.local/share/picoclaw/config.json`.
    3. **Test & Run**: Run `picoclaw-ctl exec agent -m "Hello"` to test connection. Launch background messaging gateway with `picoclaw-ctl exec gateway`.
  - **Switch to Local Inference & Qwen**: In the WebUI, add a Custom OpenAI provider with endpoint `http://localhost:50080/v1`, model `qwen`, and key `unused`. Alternatively, configure `~/.local/share/picoclaw/config.json` manually:
    ```json
    {
      "providers": {
        "openai": {
          "local": {
            "api_key": "unused",
            "base_url": "http://localhost:50080/v1"
          }
        }
      },
      "agents": {
        "default": {
          "model_provider": "openai.local",
          "model": "qwen"
        }
      }
    }
    ```

### ZeroClaw
- **Major Features**: Gateway and agent runtime supporting multiple sandbox backends (auto-prefers Landlock or Bubblewrap).
- **Language/Runtime**: Compiled binary.
- **Requirements**: Support for Linux namespace isolation or Landlock.
- **Sandboxing**: **Relaxed Namespaces Profile** is enforced via the systemd unit so that ZeroClaw can spawn secure nested sub-sandboxes via `bwrap` internally.
- **Onboarding**:
  1. **Install Service**: Run `zeroclaw-ctl install` to initialize `~/.local/share/zeroclaw` and register the systemd user service.
  2. **Interactive Onboarding**: Run the onboarding setup wizard with `zeroclaw-ctl exec onboard`. This will guide you through providers, models, channels, and agent configuration, outputting a minimal four-section configuration to `~/.local/share/zeroclaw/.zeroclaw/config.toml`.
  3. **Verify Connection**: Run `zeroclaw-ctl exec auth status` to check credentials and model fallback status. Test chat via `zeroclaw-ctl exec agent -a <agent_alias>`.
  4. **Start Gateway**: Start the service via `zeroclaw-ctl start` to launch the background daemon (listening on port `42617`). Watch logs with `zeroclaw-ctl logs`.
  5. **Switch to Local Inference & Qwen**: Edit `~/.local/share/zeroclaw/.zeroclaw/config.toml` and configure the local provider:
     ```toml
     [providers.models.openai.local]
     model = "qwen"
     uri = "http://localhost:50080/v1"
     api_key = "unused"
     ```
     Point the target agent at this provider using `model_provider = "openai.local"` under `[agents.<alias>]`.

---

## Standard Control Wrappers (assistant-ctl)

Each assistant in this repository is managed by a dedicated shell wrapper script (`scripts/<assistant>-ctl`) adhering to standard design and lifecycle management guidelines.

### Common Commands

| Command | Action | Description |
|---|---|---|
| `install` | Install | Set up local directory structures under `~/.local/share/<assistant>`, generate environment file `.env` if missing, and create/register the systemd user unit. |
| `uninstall` | Uninstall | Stop and disable the systemd service, and clean up the systemd service files. (Data is preserved). |
| `start` / `stop` / `restart` | Lifecycle | Standard controls to start, stop, or restart the systemd user service. |
| `status` | Status | Show the current runtime status of the systemd service. |
| `logs` | Logs | Tail the daemon stdout/stderr output using `journalctl --user -u <service> -f`. |
| `edit` | Edit Environment | Open the assistant's `.env` environment file in your `$EDITOR` and automatically restart the service upon exit to apply changes. |
| `exec <args...>` | Sandbox Execute | Run the assistant's CLI binary or command line inside a transient systemd user service inheriting the same sandboxing and environment. |
| `shell` | Sandbox Shell | Spawn an interactive shell inside the assistant's systemd user sandbox for debugging. |

### Common Paths & Redirections

- **Service File**: `~/.config/systemd/user/<assistant>.service` (or `hermes-gateway.service`)
- **Environment File**: `~/.config/systemd/user/<assistant>.env` (or `hermes-gateway.env`)
- **Data Home**: `~/.local/share/<assistant>` (the service forces an isolated `HOME` environment variable to this location to keep configurations and cached libraries contained).
- **Shared Space**: `~/agent-shared` is bind-mounted in read-write mode to enable inter-agent communication, workflow passing, and common file sharing.

