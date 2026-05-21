# ZeroClaw Agent Management Guide

`zeroclaw-ctl` manages the ZeroClaw Gateway and agent runtime, providing a hardened execution environment that supports Bubblewrap/Landlock isolation.

- **Source Code**: [GitHub - zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)

## Installation

```bash
./assistants/zeroclaw-ctl install
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

## Search, Retrieval & Embedding Configuration

ZeroClaw contains a self-contained, native SQLite-based hybrid memory system. It integrates Full-Text Search (FTS5) and vector search directly into its SQLite datastore, removing the need for external vector database servers. The persistent memory system automatically handles context compression, conversation history limits, and user preference storage.

### Configuration

Add the following to your `config.toml` configuration file (located in the sandboxed home directory at `~/.local/share/zeroclaw/.zeroclaw/config.toml`):

```toml
[memory]
# Native hybrid (keyword FTS + vector similarity) SQLite backend
backend = "sqlite-hybrid"
db_path = "~/.zeroclaw/memory.db"

# Enable automatic context compression when reaching limit
context_compression = true

# Maximum conversational turns to hold in active context before compressing
history_limit = 100

[embeddings]
# Embedding provider (OpenAI-compatible)
provider = "openai"
model = "text-embedding-3-small"

# Local Inference (llama-server) or Ollama endpoint mapping
api_base = "http://localhost:50080/v1"
api_key = "unused"
```

### Reranking Configuration

ZeroClaw includes a built-in weighted hybrid search (0.7 vector similarity / 0.3 keyword FTS) that does not require an external reranker. However, you can optionally integrate an external reranker for improved precision on large retrieval sets. Add the following to `~/.local/share/zeroclaw/.zeroclaw/config.toml`:

```toml
[reranker]
# External reranker: "local" (OpenAI-compatible /v1/rerank), or "disabled" (use built-in hybrid)
provider = "local"
model = "qwen3-reranker"

# Local reranker endpoint (served by local-inference on port 50080)
api_base = "http://localhost:50080/v1"
api_key = "unused"

# Number of top candidates to rerank
top_k = 30
```

## Onboarding

1. **Install Service**: Run `./assistants/zeroclaw-ctl install` to initialize `~/.local/share/zeroclaw` and register the systemd user service.
2. **Interactive Onboarding**: Run the onboarding setup wizard with `./assistants/zeroclaw-ctl exec onboard`. This will guide you through providers, models, channels, and agent configuration, outputting a minimal four-section configuration to `~/.local/share/zeroclaw/.zeroclaw/config.toml`.
3. **Verify Connection**: Run `./assistants/zeroclaw-ctl exec auth status` to check credentials and model fallback status. Test chat via `./assistants/zeroclaw-ctl exec agent -a <agent_alias>`.
4. **Start Gateway**: Start the service via `./assistants/zeroclaw-ctl start` to launch the background daemon (listening on port `42617`). Watch logs with `./assistants/zeroclaw-ctl logs`.
5. **Switch to Local Inference & Qwen3**: Edit `~/.local/share/zeroclaw/.zeroclaw/config.toml` and configure the local provider:
   ```toml
   [providers.models.openai.local]
   model = "qwen3"
   uri = "http://localhost:50080/v1"
   api_key = "unused"
   ```
   Point the target agent at this provider using `model_provider = "openai.local"` under `[agents.<alias>]`.

### OpenClaw Migration

ZeroClaw supports importing history and conversation memory logs from an existing OpenClaw installation. To perform the migration, run:
```bash
./assistants/zeroclaw-ctl exec migrate openclaw
```
This command imports the legacy SQLite database memory logs directly into ZeroClaw's memory format.

## Implementation Considerations

### Sandboxing Profile
ZeroClaw utilizes the **Relaxed Namespaces Profile** in its systemd unit. This is necessary because ZeroClaw supports nested sandboxing mechanisms (Bubblewrap) for its tool executions.
- `ProtectProc=invisible`, `ProcSubset=pid`, and `RestrictNamespaces=yes` are omitted.
- Provides standard system filesystem isolation while preserving the ability for the agent to spawn secure sub-sandboxes via `bwrap`.
