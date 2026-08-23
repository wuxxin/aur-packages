# amux-git

Arch Linux PKGBUILD for [amux](https://github.com/mixpeek/amux) — the multi-session AI agent orchestrator and control plane.

This package includes the following custom enhancements:
- `aoe-backend.patch`: support **Agent of Empires (`aoe`)** as additional process execution and dispatch backend
- `omp-provider.patch`: support **Oh-My-Pi (`omp`)** ([can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)) as additional agent provider
- `disable-no-apikey-banner.patch`: Suppresses the persistent "No Anthropic API key set" warning banner

## Running `amux-server`

To start `amux-server` in standalone / cognitive-bus mode:

### Environment Variables

| Variable | Recommended Value | Purpose |
| :--- | :--- | :--- |
| `AMUX_BACKEND` | `aoe` | Selects AoE as the default process execution and dispatch backend (deactivates `herdr` & local tmux). |
| `AMUX_HOME` | `/path/to/.amux` | Custom base directory for `amux.db`, server config, and auth tokens. |
| `AMUX_DATA_DIR` | `/path/to/.amux/data` | Working data directory for SQLite storage and session state. |
| `AMUX_PORT` | `28824` | HTTPS server listening port. |
| `AMUX_ALLOW_AGENT_SESSION_DELETE` | `1` | Allows automated session cleanup from agents and scripts. |
| `AOE_DAEMON_URL` | `http://127.0.0.1:28080` | URL of the running `aoe` execution cockpit / ACP host. |
| `AOE_DAEMON_TOKEN` | `set-to-long-random` | Bearer token for authenticating requests sent to the AoE daemon REST API. |

### Usage with AoE Example

```bash
#!/usr/bin/env bash
set -euo pipefail

export AMUX_HOME="${HOME}/.amux"
export AMUX_DATA_DIR="${HOME}/.amux/data"
export AMUX_BACKEND="aoe"
export AOE_DAEMON_URL="http://127.0.0.1:28080"
export AOE_DAEMON_TOKEN="set-to-long-random"
export AMUX_ALLOW_AGENT_SESSION_DELETE=1

# Ensure data directories exist
mkdir -p "${AMUX_HOME}/sessions" "${AMUX_DATA_DIR}"

# Start amux-server daemon
exec amux-server
```

### Configuring AoE Lifecycle Hooks for Amux Auto-Discovery

When using AoE (`agent-of-empires`) as the supervisor/cockpit, sessions created directly in AoE (via TUI, ACP, or Web PWA) can automatically register and deregister with `amux-server` using AoE's lifecycle hooks.

Add the following to your global AoE configuration (`~/.config/agent-of-empires/config.toml`) or a specific profile `config.toml`:

```toml
[hooks]
# Register newly created sessions in amux
on_create = [
    'u="${AMUX_API_URL:-https://localhost:28824}"; u="${u%/}"; curl -sk -X POST "$u/api/sessions" -H "Authorization: Bearer ${AMUX_AUTH_TOKEN:-}" -H "Content-Type: application/json" -d "{\"name\": \"$AOE_SESSION_TITLE\", \"dir\": \"$AOE_PROJECT_PATH\", \"provider\": \"${AOE_TOOL:-omp}\"}" 2>/dev/null || true'
]
# Ensure existing or resumed sessions are registered upon start/launch
on_launch = [
    'u="${AMUX_API_URL:-https://localhost:28824}"; u="${u%/}"; curl -sk -X POST "$u/api/sessions" -H "Authorization: Bearer ${AMUX_AUTH_TOKEN:-}" -H "Content-Type: application/json" -d "{\"name\": \"$AOE_SESSION_TITLE\", \"dir\": \"$AOE_PROJECT_PATH\", \"provider\": \"${AOE_TOOL:-omp}\"}" 2>/dev/null || true'
]
# Clean up session metadata in amux when deleted in AoE
on_destroy = [
    'u="${AMUX_API_URL:-https://localhost:28824}"; u="${u%/}"; curl -sk -X DELETE "$u/api/sessions/$AOE_SESSION_TITLE" -H "Authorization: Bearer ${AMUX_AUTH_TOKEN:-}" 2>/dev/null || true'
]
```

> **Note:** Ensure `AMUX_ALLOW_AGENT_SESSION_DELETE=1` is set in `~/.amux/server.env` so that `on_destroy` can unregister sessions via the REST API without interactive dashboard prompts.

---


### Usage with Oh-My-Pi Example

1. **Creating an Oh-My-Pi Worker via Web Dashboard:**
   - Open WebUI at `https://127.0.0.1:28824`.
   - Click **New worker**.
   - Select the **Oh-My-Pi** provider button.
   - Enter worker name and working directory, then click **Create**.

2. **Creating an Oh-My-Pi Worker via REST API:**
   ```bash
   curl -k -X POST https://127.0.0.1:28824/api/sessions \
     -H "Content-Type: application/json" \
     -d '{"name": "worker-1", "dir": "/path/to/project", "provider": "omp", "model": "llama.cpp/qwen3"}'
   ```


## Included Patches & Technical Breakdown

### 1. `aoe-backend.patch`
Adds native **Agent of Empires (`aoe`)** backend execution and REST delegation support to `amux-server`.

- **Backend Routing (`CC_BACKEND=aoe` or `AMUX_BACKEND=aoe`)**:
  - Directs `amux-server` to route process status checks, terminal screen captures, prompt deliveries, and worker terminations to the `aoe` REST API instead of local tmux or herdr subprocesses.
- **REST Dispatch Functions**:
  - `aoe_agent_running`: Checks `GET ${AOE_DAEMON_URL}/api/sessions?state=live` for active worker status.
  - `aoe_capture`: Reads `GET ${AOE_DAEMON_URL}/api/sessions/{name}/output?lines={N}&format=text` for remote pane peeking.
  - `aoe_send`: Issues `POST ${AOE_DAEMON_URL}/api/sessions/{name}/send` with `{"message": text}` to push turn-boundary prompts and scheduled cron sweeps without terminal screen scraping.
  - `aoe_stop`: Calls `POST ${AOE_DAEMON_URL}/api/sessions/{name}/stop` to cleanly terminate agent workers.
- **Configurable Endpoint & Auth (`AOE_DAEMON_URL` / `AOE_DAEMON_TOKEN`)**:
  - Endpoint defaults to upstream standard `http://localhost:8080` (overridden to `http://127.0.0.1:28080` in MyPAI's unified port map).
  - Automatically attaches `Authorization: Bearer <AOE_DAEMON_TOKEN>` header to all outgoing requests when `AOE_DAEMON_TOKEN` is configured.

#### Backend Feature Matrix (`tmux` vs `herdr` vs `aoe`)

| Capability | `tmux` Backend | `herdr` Backend | `aoe` Backend |
| :--- | :--- | :--- | :--- |
| **Transport** | Unix socket / CLI (`tmux`) | Subprocess CLI (`herdr agent ...`) | **HTTP REST API** |
| **Prompt Delivery (`send`)** | Keystrokes (`tmux send-keys`) | CLI prompt (`herdr agent prompt`) | **HTTP POST (`/api/sessions/{name}/send`)** |
| **Liveness Check (`is_running`)** | PID inspection (`pgrep -P`) | CLI query (`herdr agent get`) | **HTTP GET (`/api/sessions?state=live`)** |
| **Screen Output (`capture`)** | `tmux capture-pane -S -N` | CLI read (`herdr agent read`) | **HTTP GET (`/api/sessions/{name}/output`)** |
| **Worker Stop (`stop`)** | Injects `/exit` / `C-c` | CLI prompt (`/exit`) | **HTTP POST (`/api/sessions/{name}/stop`)** |
| **Worker Start (`start`)** | `tmux new-session` | ❌ *Not ported in Rust (501)* | **Delegated to AoE / Pre-configured** |
| **Structured Events / ACP** | ❌ None (raw text) | ❌ None (raw text) | **✅ Native JSON-RPC tool cards & diffs** |

#### Comparison & Architectural Analysis

- **What `aoe` adds over `herdr`**:
  - **Zero Subprocess Overhead:** Replaces constant CLI shell executions (`herdr agent get`, `herdr agent prompt`) with persistent, async HTTP REST calls.
  - **Structured ACP Interface:** Agents communicate via typed Agent Client Protocol JSON-RPC, removing terminal scraping artifacts and false-positive generating state transitions.
  - **Mobile PWA & TUI Cockpit:** Native integration with AoE's mobile structured view, diff inspector, and approval gates.
- **Operational Nuances**:
  - **Lifecycle Hosting:** Worker processes are hosted and supervised inside `aoe` (`omp acp`). `amux` acts as the cognitive event and task plane, pushing turns to `aoe` at turn boundaries.
  - **Attachment:** Direct keyboard inspection is handled via `aoe`'s TUI or Web PWA instead of `amux attach`.


### 2. `omp-provider.patch`
Adds full end-to-end integration for the **Oh-My-Pi (`omp`)** CLI provider across the CLI harness, Rust server daemon, and Web Dashboard.

#### A. CLI Script (`/usr/bin/amux`)
- **Native Provider Dispatch (`amux start <name>`)**:
  - Adds an `elif [[ "$provider" == "omp" ]]` branch that builds `cmd="omp"` directly instead of falling back to `claude`.
  - Honors `CC_FLAGS` from `<name>.env` and inline arguments passed after `--`.
  - Appends `--model ${CC_MODEL:-llama.cpp/qwen3}` if no `--model` flag is present in flags or inline arguments.
  - Skips Claude-specific default flags (`CC_DEFAULT_FLAGS`) and preserves environment credentials without unsetting OAuth/API key variables.
- **Environment Discovery**:
  - Sets `CC_HOME="${AMUX_HOME:-${CC_HOME:-$HOME/.amux}}"` so CLI commands seamlessly detect session configurations located in `$AMUX_HOME/sessions`.

#### B. Server Backend (`crates/amux-server/`)
- **Provider Adapter & Registry (`src/provider/`)**:
  - Implements `OmpAdapter` conforming to `ProviderAdapter`:
    - `id()` $\rightarrow$ `ProviderId::new("omp")`
    - `capabilities()` $\rightarrow$ `ProviderCapabilities { hot_model_switch: false, reports_usage: false, structured_events: false, hooks: false }`
    - `usage()` $\rightarrow$ `ProviderUsage::unknown(self.id())`
    - `build_command(prompt_mode)` $\rightarrow$ `vec!["omp".into()]` (Interactive) or `vec!["omp".into(), "exec".into()]` (Headless)
  - Registers `OmpAdapter` in `default_registry()` with alias normalization (`oh-my-pi` $\rightarrow$ `omp`), updates registry provider counts, and adds conformance tests (`conformance_omp`).
- **Session Verbs & Launch Engine (`src/api/session_verbs.rs`)**:
  - Extends `SESSION_PROVIDERS` to `["claude", "codex", "gemini", "iterm2", "ollama", "omp"]` so worker configs (`CC_PROVIDER=omp`) and API endpoints (`POST /api/sessions`, `PATCH /api/sessions/<name>`) recognize `omp` as a valid provider without defaulting to Claude.
  - `launch_base_binary("omp")` $\rightarrow$ `"omp"`
  - `default_model_for_provider("omp")` $\rightarrow$ `"llama.cpp/qwen3"`
  - `provider_label("omp")` $\rightarrow$ `"Oh-My-Pi"`
  - `provider_yolo_flag("omp")` $\rightarrow$ `"--approval-mode=yolo"`
  - `start_session`: Constructs the `omp` launch command with quoted flags, injecting `--model ${CC_MODEL:-llama.cpp/qwen3}` if omitted, and isolates shell setup from Claude OAuth unsetting.
- **Fleet Signal & Model Routing (`src/api/sessions_legacy.rs`)**:
  - `tmux list-sessions`: Suppresses false-positive `tracing::warn!` log messages when tmux reports `"no server"` / `"No such file or directory"` / `"error connecting to"` (idle state / 0 active workers).
  - `worker_model_env`: Routes `omp` models without inheriting Claude default models, setting `CC_MODEL` and defaulting to `llama.cpp/qwen3`.

#### C. Web Dashboard (`crates/amux-dashboard/static/`)
- **New Worker Modal (`index.html`)**: Adds the **Oh-My-Pi** selection button (`#create-provider-omp`) to the provider button group.
- **Custom Model Input & Preset Picker (`app.js`)**:
  - Interactive custom model input with autofocus when clicking "Change model" on worker cards.
  - For `omp`, pre-fills `llama.cpp/qwen3` with quick presets (`llama.cpp/qwen3`, `auto`), allowing typing or pasting any custom model identifier without static restrictions.
- **Settings Modal (`index.html`, `app.js`)**: Adds an `Oh-My-Pi / Local` optgroup (`qwen3`, `auto`, `llama.cpp/qwen3`, `deepseek-r1`) to the default model dropdown.
- **Styling (`app.css`)**: Adds `.badge.omp` and `.archived-card-chip.provider-omp` badges.

---

### 3. `disable-no-apikey-banner.patch`
- Suppresses the persistent "No Anthropic API key set — Claude workers won't work" warning banner in `amux-dashboard` (`app.js`) for local instances.
- Prevents UI clutter when running local LLMs, Ollama, Gemini, or Oh-My-Pi without Anthropic API keys.

