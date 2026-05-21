# Assistants and Integrations

This document describes information about several AI assistants, their sandboxing requirements, default port allocations, and external integrations (Local Inference and Signal) managed within this repository.

## Integrations

### Local Inference
- **Description**: Manages a persistent `llama-server` instance optimized for local LLM serving, specifically tuned for AMD ROCm hardware (tested on Radeon Pro W6800). Designed for high context lengths (Qwen 35B/27B) with optimized memory access and KV cache.
- **Sandboxing**: Requires `PrivateDevices=no` to access `/dev/dri` and `/dev/kfd`. Enforces `ProtectSystem=strict` while bind-mounting the user's home configuration and granting read-write access to `/data/public/machine-learning`.
- **Features**: Flash Attention, layer GPU offloading, hardware-specific concurrency parameters.
- **Arch/AUR Packages**:
  - `llama.cpp` (Official extra repository, CPU-only/OpenBLAS fallback)
  - `llama.cpp-cuda` (AUR, with CUDA acceleration for NVIDIA GPUs)
  - `llama.cpp-hip` (AUR, with HIP/ROCm acceleration for AMD GPUs)
  - `llama.cpp-git` (AUR, latest git source build, CPU)
  - `llama.cpp-git-cuda` (AUR, latest git source build with CUDA)
  - `llama.cpp-git-hip` (AUR, latest git source build with HIP/ROCm)
  - Local package built in this workspace: `llama.cpp-git-ggml-hip` (depends on `libggml-git-hip`), providing and conflicting with `llama.cpp` and `llama.cpp-hip`.

### Signal Integration
- **Description**: Connects agents to Signal. Runs a `signal-cli` daemon exposing both TCP and HTTP JSON-RPC interfaces. It also provides an optional Go-based REST API wrapper for robust, HTTP-based polling/webhook integrations (like linking OpenFang).
- **Sandboxing**: Standard filesystem hardening, but disables `MemoryDenyWriteExecute` because the underlying JVM (Java) requires it for JIT compilation. 
- **Features**: Account linking via QR code, dual daemon interfaces, and isolated home directory execution to prevent contamination.
- **Arch/AUR Packages**:
  - `signal-cli` (AUR / Official, Java-based commandline interface)
  - `signal-cli-bin` (AUR, precompiled binary distribution)
  - `signal-cli-git` (AUR, latest git build)
  - `signal-cli-rest-api` (AUR, Go-based REST API wrapper)
  - Local package built in this workspace: `signal-cli-rest-api-git` (custom patch for HTTP polling).

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
| **OpenFang** | [4200](http://localhost:4200) | OpenFang daemon API (HTTP) |
| **Moltis** | [13131](https://localhost:13131) | Moltis agent server Web UI/API (HTTPS) |
| **PicoClaw** | [18790](http://localhost:18790), [18800](http://localhost:18800) | Gateway (HTTP/Webhook) & Launcher Web UI |
| **NanoBot** | [8790](http://localhost:8790) | NanoBot Gateway API |
| **Hermes** | [8000](http://localhost:8000), [8642](http://localhost:8642), [9119](http://localhost:9119) | Hermes Messaging Gateway (API: 8642, UI: 9119) |
| **ZeroClaw** | [42617](http://localhost:42617) | ZeroClaw Gateway |
| **NanoClaw** | [3000](http://localhost:3000) | Webhook Server |
| **Signal-CLI** | `50887`, [50888](http://localhost:50888), [50889](http://localhost:50889) | TCP JSON-RPC, HTTP JSON-RPC, REST API |
| **Local-Inference** | [50080](http://localhost:50080) | Llama-server local instance |

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
- **Arch/AUR Packages**: `hermes-agent` (AUR, standard source), `hermes-agent-git` (AUR, latest git source), `hermes-agent-desktop-bin` (AUR, desktop prebuilt binary).
- **Search & Retrieval**: Built-in SQLite-based SessionDB and State management. Full-text search (FTS5) for keyword-based search. Built-in `sqlite-vec` extension support for vector search. Native integration with external vector/RAG databases (Qdrant, Chroma) and memory frameworks (Mem0, Honcho, Supermemory, RetainDB). Maintains localized context via `MEMORY.md` and `USER.md` prompt injections.
- **Embedding Options**: Supports remote embedding API providers (OpenAI, Cohere, Jina, Voyage AI) and local embedding models served via `llama.cpp` (local-inference) or Ollama.
- **Detailed Guide & Onboarding**: [hermes-ctl.md](hermes-ctl.md)

### Moltis
- **Major Features**: Agent server based on the openfang-ctl architecture. Web-based configuration and administration, persistent plugin/provider support, capable of privileged port binding.
- **Language/Runtime**: Compiled binary.
- **Requirements**: Needs a setup code on initial run to unlock the web UI. Uses `~/.local/share/moltis` for data.
- **Sandboxing**: Uses a mostly strict configuration but relies on specific network capability bounding (`CAP_NET_BIND_SERVICE`) and `PrivateDevices=no` if hardware-backed plugins are used. Isolated `HOME`.
- **Arch/AUR Packages**: `moltis` (AUR package built from the current workspace directory, source compilation). Alternatives: `moltis-bin` (AUR, precompiled binary) or `moltis-git` (AUR, latest git source build).
- **Search & Retrieval**: Built-in SQLite database with Full-Text Search (FTS5) for keyword search. Direct vector embedding storage inside SQLite. Supports an optional **QMD** sidecar that adds high-performance **BM25** keyword search, vector similarity search, and hybrid retrieval with LLM reranking. Automatically extracts facts and summarizes history when approaching context limits.
- **Embedding Options**: Remote OpenAI-compatible embedding API endpoints. Local vector search using local GGUF models served via local inference servers or Ollama, or built-in QMD model processing.
- **Detailed Guide & Onboarding**: [moltis-ctl.md](moltis-ctl.md)

### NanoBot
- **Major Features**: Lightweight python service built with `uv`. Features an onboarding wizard for simple configuration.
- **Language/Runtime**: Python. Uses isolated virtual environments managed by `uv`.
- **Requirements**: `uv` package manager installed.
- **Sandboxing**: Relies on the **Relaxed Namespaces Profile** because it natively spawns agent code wrapped in nested `bwrap` isolation. Isolated `HOME`.
- **Arch/AUR Packages**: No system-wide AUR packages are available for NanoBot. It is a lightweight Python framework designed to be installed inside a virtual environment using `uv` (pip package: `nanobot-ai`).
- **Search & Retrieval**: Structured two-stage memory system ("Dream") that separates active conversation buffers from long-term memory. Long-term memory store uses vector similarity search (RAG) to remember facts across sessions. Built-in Document Store allows indexing, chunking, and retrieving context from local files (PDFs, TXT, markdown). Model Context Protocol (MCP) integrations can execute external search tools (e.g. Brave Search) dynamically.
- **Embedding Options**: OpenAI-compatible embedding endpoints or local embeddings. Integrates with local embedding models via Ollama or `llama.cpp` / local-inference instances.
- **Detailed Guide & Onboarding**: [nanobot-ctl.md](nanobot-ctl.md)

### NanoClaw
- **Major Features**: Webhook server capable of securely executing containers for runtime tools.
- **Language/Runtime**: Container-based (`nanoclaw-agent:latest`).
- **Requirements**: Requires Docker/Podman running locally to spawn tool environments.
- **Sandboxing**: **Relaxed Namespaces Profile** with `PrivateDevices=no`. Strict profiles are dropped to allow the agent to launch local Docker/Podman containers successfully.
- **Arch/AUR Packages**: `nanoclaw-git` (AUR, git-based source compilation). Alternatives: `nanoclaw`, `nanoclaw-bin`.
- **Search & Retrieval**: Uses SQLite databases within the Node.js process to maintain state. Maintains `CLAUDE.md` and related markdown files in isolated agent group directories. RAG or vector retrieval is typically handled by custom agent tools or external MCP databases.
- **Embedding Options**: Uses APIs (e.g. Anthropic, OpenAI) for remote embeddings. Local embeddings can be fetched via tools querying `local-inference` or Ollama servers.
- **Detailed Guide & Onboarding**: [nanoclaw-ctl.md](nanoclaw-ctl.md)

### OpenFang
- **Major Features**: Agent OS daemon that provides a hardened execution environment and orchestrates complex agentic workloads.
- **Language/Runtime**: Compiled binary.
- **Requirements**: `~/.local/share/openfang` and `~/agent-shared`.
- **Sandboxing**: **Relaxed Namespaces Profile** to support bubblewrap (`bwrap`) nested sandboxing for sub-agents. Read-only system paths and strict filesystem protection for the host.
- **Arch/AUR Packages**: `openfang-cli` (AUR, provides both CLI client and the main server binary `/usr/bin/openfang`). Alternatives: `openfang-cli-git` (AUR, git-based).
- **Search & Retrieval**: Native integration of SQLite and vector storage for persistent agent memories and knowledge retrieval. Built-in scheduling and task memory, which allows agents to run 24/7 and store OSINT/research search results in the native database. Can connect to external databases via MCP (Model Context Protocol).
- **Embedding Options**: Supports embedding generation via 27 supported LLM/embedding providers (OpenAI-compatible, Cohere, Anthropic, etc.). Can leverage system-wide local embeddings via the `local-inference` server.
- **Detailed Guide & Onboarding**: [openfang-ctl.md](openfang-ctl.md)

### PicoClaw
- **Major Features**: HTTP/Webhook gateway and a dedicated Web UI launcher. Built-in web console and CLI integration.
- **Language/Runtime**: Compiled binary (`picoclaw`).
- **Requirements**: `~/.local/share/picoclaw` for persistent configuration.
- **Sandboxing**: **Strict Confinement Profile**. It hides other processes, prevents new namespaces, and denies writable/executable memory mappings. 
- **Arch/AUR Packages**: `picoclaw` (AUR, source-based Go compilation). Alternatives: `picoclaw-bin` (AUR, pre-built binary), `picoclaw-git` (AUR, git-based).
- **Search & Retrieval**: No native built-in vector database or complex memory engine due to its ultra-lightweight design (<10MB memory). Local state and conversation histories are stored in simple JSON files. Supports the Model Context Protocol (MCP) to delegate search and retrieval tasks to external databases or RAG servers (e.g. SQLite-vec MCP, Qdrant MCP, Chroma MCP).
- **Embedding Options**: No native embedding models. Leverages external embedding API endpoints (OpenAI, Anthropic) or local embedding models via Ollama/llama-server via MCP tools or API routing.
- **Detailed Guide & Onboarding**: [picoclaw-ctl.md](picoclaw-ctl.md)

### ZeroClaw
- **Major Features**: Gateway and agent runtime supporting multiple sandbox backends (auto-prefers Landlock or Bubblewrap).
- **Language/Runtime**: Compiled binary.
- **Requirements**: Support for Linux namespace isolation or Landlock.
- **Sandboxing**: **Relaxed Namespaces Profile** is enforced via the systemd unit so that ZeroClaw can spawn secure nested sub-sandboxes via `bwrap` internally.
- **Arch/AUR Packages**: `zeroclaw` (AUR, Rust source compilation), `zeroclaw-bin` (AUR, prebuilt binary distribution), `zeroclaw-git` (AUR, git-based).
- **Search & Retrieval**: Native SQLite-based hybrid memory system. Integrates vector search and Full-Text Search (FTS) directly into SQLite. No external database infrastructure (like Pinecone or Elasticsearch) is required, keeping the runtime completely self-contained. Persistent memory handles context compression, conversation history, and user preferences.
- **Embedding Options**: Supports OpenAI-compatible embedding APIs. Can route to local embedding models using system-wide local inference (`local-inference`) or Ollama.
- **Detailed Guide & Onboarding**: [zeroclaw-ctl.md](zeroclaw-ctl.md)

---

## Standard Control Wrappers (assistant-ctl)

Each assistant in this repository is managed by a dedicated shell wrapper script (`assistants/<assistant>-ctl`) adhering to standard design and lifecycle management guidelines.

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
- **Shared Space (`agent-shared`)**: `~/agent-shared` is bind-mounted in read-write mode to the sandbox of all assistants by default. This enables cross-assistant sharing of outputs, databases, and logs.
- **Private Submounts (`agent-private`)**: To easily share specific directories from your host's private workspace (`~/agent-private/*`) to an assistant's sandbox without exposing the entire home directory, configure the `AGENT_PRIVATE_MOUNTS` environment variable inside the assistant's `.env` environment file.
  - **Syntax**: `AGENT_PRIVATE_MOUNTS="health diary"`
  - **Behavior**: The control wrapper will dynamically parse this list, ensure that the target directories (e.g. `~/agent-private/health` and `~/agent-private/diary`) exist on the host, inject the corresponding `BindPaths=` rules into the systemd service file, reload the user daemon, and dynamically mount them in all `start`, `restart`, `exec`, and `shell` wrapper commands.

