# Hermes Agent Management Guide

`hermes-ctl` is a management wrapper for the `hermes-agent` messaging gateway. It provides a standardized interface for installation, configuration, and service lifecycle management using `systemd` user units.

- **Source Code**: [GitHub - NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)

## Installation

```bash
./assistants/hermes-ctl install
```

## Commands

`hermes-ctl` supports all standard management operations. For detailed command reference and sandboxing path defaults, see [Standard Control Wrappers](file:///home/wuxxin/agent-shared/code/aur-packages/assistants/assistants.md#standard-control-wrappers-assistant-ctl).

## Configuration & Ports

- **Default Ports**:
  - **Gateway API (OpenAI-compatible)**: `8642`
  - **Dashboard Web UI**: `9119`
- **Configuration File**: Environment variables and key secrets are managed in `~/.config/systemd/user/hermes-gateway.env`.

## Signal Channel Configuration

Hermes includes native support for the Signal messaging channel, interfacing with a locally running `signal-cli` daemon.

### Configuration

Add the following environment variables to `~/.config/systemd/user/hermes-gateway.env` (via `./assistants/hermes-ctl edit`):

```bash
# Enable Signal by supplying the account phone number and daemon endpoint
SIGNAL_ACCOUNT="+1234567890"  # Your registered Signal phone number
SIGNAL_HTTP_URL="http://localhost:50888"  # Local signal-cli HTTP daemon port

# Optional Access Control Allowlists
SIGNAL_ALLOWED_USERS="+1987654321,+1555000111" # Comma-separated allowed numbers or UUIDs ("*" to allow all DMs)
SIGNAL_GROUP_ALLOWED_USERS="group_id_1,group_id_2" # Comma-separated allowed group IDs ("*" to allow all groups)
```

Ensure the local `signal-cli` daemon is running. Hermes will automatically connect, stream inbound messages via Server-Sent Events (SSE), and reply via JSON-RPC.

## Search, Retrieval & Embedding Configuration

Hermes supports built-in SQLite-based SessionDB/State management, Full-Text Search (FTS5), vector search using the `sqlite-vec` extension, and integrations with external vector databases and memory frameworks.

### Configuration

Add the following environment variables to `~/.config/systemd/user/hermes-gateway.env` (via `./assistants/hermes-ctl edit`):

```bash
# Vector Database & Memory Backend Selection
# Options: "sqlite" (default), "qdrant", "chroma"
HERMES_VECTOR_DB="sqlite"

# External Vector Database Credentials (if using qdrant/chroma)
QDRANT_URL="http://localhost:6333"
QDRANT_API_KEY=""
CHROMA_URL="http://localhost:8000"

# External Memory & RAG Frameworks (optional)
# Supports Mem0, Honcho, Supermemory, RetainDB
MEM0_API_KEY="your-mem0-key"
HONCHO_API_KEY="your-honcho-key"

# Embedding Provider Configuration
# Options: "openai", "cohere", "jina", "voyage", "local", "ollama"
HERMES_EMBEDDING_PROVIDER="local"
HERMES_EMBEDDING_MODEL="text-embedding-3-small"

# Local Inference Endpoint (llama.cpp or Ollama)
# Route to local-inference (port 50080) for system-wide local embeddings
EMBEDDING_API_BASE="http://localhost:50080/v1"
EMBEDDING_API_KEY="unused"
```

### Reranking Configuration

Hermes supports reranking via auxiliary model slots and the QMD hybrid retrieval engine. Configure the reranker endpoint to point to the local-inference server:

```bash
# Reranking Provider Configuration
# Options: "local", "cohere", "jina", "disabled"
HERMES_RERANK_PROVIDER="local"

# Local reranker endpoint (served by local-inference on port 50080)
HERMES_RERANK_URL="http://localhost:50080/v1/rerank"
HERMES_RERANK_MODEL="qwen3-reranker"

# Number of top candidates to rerank after initial retrieval
HERMES_RERANK_TOP_K=30
```

## Speech-to-Text Integration

Hermes automatically transcribes incoming voice messages (from Signal, Telegram, Discord, etc.) using its transcription tools. You can route these requests to the local `local-speech-to-text` service.

### Configuration

Add the following environment variables to `~/.config/systemd/user/hermes-gateway.env` (via `./assistants/hermes-ctl edit`):

```bash
# Set provider to openai and point base URL to local-speech-to-text service
STT_OPENAI_BASE_URL="http://localhost:50090/v1"
STT_OPENAI_MODEL="whisper"
VOICE_TOOLS_OPENAI_KEY="dummy"  # Required placeholder to activate the provider
```

Alternatively, you can configure the provider directly in your `config.yaml`:

```yaml
stt:
  enabled: true
  provider: "openai"
  openai:
    api_key: "dummy"
    base_url: "http://localhost:50090/v1"
    model: "whisper"
```

## Onboarding

1. **Install Service**: Run `./assistants/hermes-ctl install` to set up the home directory (`~/.local/share/hermes`) and generate/enable the systemd user service.
2. **Set Environment**: Run `./assistants/hermes-ctl edit` (or edit `~/.config/systemd/user/hermes-gateway.env`) to configure necessary provider environment variables (e.g. `OPENROUTER_API_KEY`).
3. **Setup Wizard**: Run `./assistants/hermes-ctl exec setup` to launch the interactive configuration setup.
4. **Start & Verify**: Start the service with `./assistants/hermes-ctl start`. Monitor its logs via `./assistants/hermes-ctl logs` and access the Web UI at `http://localhost:9119`.
5. **Switch to Local Inference & Qwen3**: Run `./assistants/hermes-ctl edit` to set `OPENAI_API_BASE=http://localhost:50080/v1` and `OPENAI_API_KEY=unused`. Run `./assistants/hermes-ctl exec setup` and configure the default model to `qwen3` (or whatever model name is served by your local instance).

### OpenClaw Migration

Hermes supports importing configuration from an existing OpenClaw setup. To migrate your setup, run:
```bash
./assistants/hermes-ctl exec claw migrate
```
This utility will parse your legacy config formats and migrate them to the Hermes gateway structure.

## Implementation Considerations

### Graceful Shutdown and Restarts
Hermes uses a graceful drain mechanism. The service is configured with:
- `KillMode=mixed`: Ensures that if the gateway is interrupted, child processes (like tool-call subshells) are correctly handled.
- `KillSignal=SIGTERM`: Standard termination signal.
- `ExecReload=/bin/kill -USR1 $MAINPID`: Triggers the gateway's internal graceful restart logic.
- `TimeoutStopSec=210`: Provides a budget for the 180s default drain timeout plus cleanup headroom.
- `RestartForceExitStatus=75`: Hermes exits with status 75 when a planned restart is requested; systemd is configured to always restart on this status.

### Security and Sandboxing
The service runs with `ProtectSystem=strict` and `TemporaryFileSystem=%h`. Only the following paths are writable:
- `~/.local/share/hermes`: The persistent home for config, logs, and state.
- `~/agent-shared`: Shared directory for agent-to-agent or agent-to-human integration.

### Environment and Isolation
- **Isolated HOME**: The `HOME` environment variable is redirected to `~/.local/share/hermes` within the service to ensure that any tools called by the agent (pip, git, etc.) do not leak state into the user's real home.
- **Secrets Management**: API keys and secrets are stored in `~/.config/systemd/user/hermes-gateway.env` and loaded via `EnvironmentFile`.

### Container Backend Support
If you plan to use `docker` or `podman` as a terminal backend from within the gateway:
- The default `NoNewPrivileges=yes` and `PrivateDevices=yes` may need to be relaxed.
- Rootless podman specifically requires access to `/dev/fuse` and certain namespaces that are restricted by default systemd hardening. See the comments in `hermes-ctl` for suggested overrides.
