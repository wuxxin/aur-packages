# Assistants and Integrations

This document describes information about all AI assistants, their sandboxing requirements, default port allocations, and external integrations (Local Inference and Signal) managed within this repository.

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

## Sandboxing Architecture Overview

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

### Moltis
- **Major Features**: Agent server based on the openfang-ctl architecture. Web-based configuration and administration, persistent plugin/provider support, capable of privileged port binding.
- **Language/Runtime**: Compiled binary.
- **Requirements**: Needs a setup code on initial run to unlock the web UI. Uses `~/.local/share/moltis` for data.
- **Sandboxing**: Uses a mostly strict configuration but relies on specific network capability bounding (`CAP_NET_BIND_SERVICE`) and `PrivateDevices=no` if hardware-backed plugins are used. Isolated `HOME`.

### NanoBot
- **Major Features**: Lightweight python service built with `uv`. Features an onboarding wizard for simple configuration.
- **Language/Runtime**: Python. Uses isolated virtual environments managed by `uv`.
- **Requirements**: `uv` package manager installed.
- **Sandboxing**: Relies on the **Relaxed Namespaces Profile** because it natively spawns agent code wrapped in nested `bwrap` isolation. Isolated `HOME`.

### NanoClaw
- **Major Features**: Webhook server capable of securely executing containers for runtime tools.
- **Language/Runtime**: Container-based (`nanoclaw-agent:latest`).
- **Requirements**: Requires Docker/Podman running locally to spawn tool environments.
- **Sandboxing**: **Relaxed Namespaces Profile** with `PrivateDevices=no`. Strict profiles are dropped to allow the agent to launch local Docker/Podman containers successfully.

### OpenFang
- **Major Features**: Agent OS daemon that provides a hardened execution environment and orchestrates complex agentic workloads.
- **Language/Runtime**: Compiled binary.
- **Requirements**: `~/.local/share/openfang` and `~/agent-shared`.
- **Sandboxing**: **Relaxed Namespaces Profile** to support bubblewrap (`bwrap`) nested sandboxing for sub-agents. Read-only system paths and strict filesystem protection for the host.

### PicoClaw
- **Major Features**: HTTP/Webhook gateway and a dedicated Web UI launcher. Built-in web console and CLI integration.
- **Language/Runtime**: Compiled binary (`picoclaw`).
- **Requirements**: `~/.local/share/picoclaw` for persistent configuration.
- **Sandboxing**: **Strict Confinement Profile**. It hides other processes, prevents new namespaces, and denies writable/executable memory mappings. 

### ZeroClaw
- **Major Features**: Gateway and agent runtime supporting multiple sandbox backends (auto-prefers Landlock or Bubblewrap).
- **Language/Runtime**: Compiled binary.
- **Requirements**: Support for Linux namespace isolation or Landlock.
- **Sandboxing**: **Relaxed Namespaces Profile** is enforced via the systemd unit so that ZeroClaw can spawn secure nested sub-sandboxes via `bwrap` internally.

---

## Integrations

### Local Inference
- **Description**: Manages a persistent `llama-server` instance optimized for local LLM serving, specifically tuned for AMD ROCm hardware (tested on Radeon Pro W6800). Designed for high context lengths (Qwen 35B/27B) with optimized memory access and KV cache.
- **Sandboxing**: Requires `PrivateDevices=no` to access `/dev/dri` and `/dev/kfd`. Enforces `ProtectSystem=strict` while bind-mounting the user's home configuration and granting read-write access to `/data/public/machine-learning`.
- **Features**: Flash Attention, layer GPU offloading, hardware-specific concurrency parameters.

### Signal Integration
- **Description**: Connects agents to Signal. Runs a `signal-cli` daemon exposing both TCP and HTTP JSON-RPC interfaces. It also provides an optional Go-based REST API wrapper for robust, HTTP-based polling/webhook integrations (like linking OpenFang).
- **Sandboxing**: Standard filesystem hardening, but disables `MemoryDenyWriteExecute` because the underlying JVM (Java) requires it for JIT compilation. 
- **Features**: Account linking via QR code, dual daemon interfaces, and isolated home directory execution to prevent contamination.
