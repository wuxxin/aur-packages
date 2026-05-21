# Local Inference Management Guide

`local-inference.sh` manages a persistent `llama-server` instance in **router mode**, serving an LLM, an embedding model, and an optional reranker from a single process on one port. Optimized for AMD ROCm hardware (specifically tested on Radeon Pro W6800).

- **Source Code**: [GitHub - ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

## Usage

| Command | Description |
|---|---|
| `install` | Sets up the service, generates default configuration and models INI. |
| `uninstall` | Stops and removes the service. |
| `edit` | Edit model selection and server parameters. |
| `logs` | View the inference server output. |
| `exec` | Run `llama-server` in a transient unit with the same GPU access. |
| `shell` | Spawn an interactive shell in the inference sandbox (useful for `rocm-smi`). |

## Router Mode Architecture

The service uses `llama-server --models-preset` to serve multiple models from a single process. All models are kept warm simultaneously in VRAM (`--models-max 2` or `3`), eliminating swap delays.

### Endpoints (all on port 50080)

| Endpoint | Model Name | Purpose |
|---|---|---|
| `/v1/chat/completions` | `qwen3` | LLM chat completions |
| `/v1/embeddings` | `qwen3-embedding` | Text embedding generation |
| `/v1/rerank` | `qwen3-reranker` | Document reranking (if enabled) |

### Configuration Files

| File | Purpose |
|---|---|
| `~/.config/systemd/user/local-inference.env` | Model paths, aliases, toggle reranker |
| `~/.config/systemd/user/local-inference.ini` | Auto-generated models preset (do not edit manually) |
| `~/.config/systemd/user/local-inference.service` | Auto-generated systemd unit |

## VRAM Budget

Hardware: AMD Radeon Pro W6800 — **30,704 MiB** usable VRAM.

### Model Weights on GPU

| Component | File Size | GPU VRAM |
|---|---|---|
| [MoE LLM (Qwen3.6-35B-A3B-APEX-I-Compact)](https://huggingface.co/mudler/Qwen3.6-35B-A3B-APEX-GGUF/blob/main/Qwen3.6-35B-A3B-APEX-I-Compact.gguf) | 17 GiB | ~17,408 MiB |
| [MoE mmproj (vision)](https://huggingface.co/mudler/Qwen3.6-35B-A3B-APEX-GGUF/blob/main/mmproj.gguf) | 861 MiB | ~861 MiB |
| Dense LLM (Qwen3.6-27B Q5_K_L) | 20 GiB | ~19,013 MiB |
| [Embedding (Qwen3-Embedding-0.6B Q8_0)](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF/blob/main/Qwen3-Embedding-0.6B-Q8_0.gguf) | 610 MiB | ~700 MiB |
| [Reranker (Qwen3-Reranker-0.6B Q4_K_M)](https://huggingface.co/mradermacher/Qwen3-Reranker-0.6B-GGUF/resolve/main/Qwen3-Reranker-0.6B.Q4_K_M.gguf) | 379 MiB | ~450 MiB |
| Compute overhead (per LLM) | — | ~990 MiB |
| Dense recurrent state | — | ~299 MiB |

### Config A: MoE + Vision + Embedding + Reranker

| Item | MiB |
|---|---|
| Total VRAM | 30,704 |
| − MoE model | 17,408 |
| − mmproj | 861 |
| − compute | 990 |
| − embedding | 700 |
| − reranker | 450 |
| **Free for KV** | **10,295** |
| − KV @ 240,000 tok | 8,031 |
| **Free headroom** | **2,264** |

**n_ctx = 240,000** (per slot: 120,000)

### Config B: Dense + Embedding + Reranker

| Item | MiB |
|---|---|
| Total VRAM | 30,704 |
| − Dense model | 19,013 |
| − compute | 990 |
| − recurrent | 299 |
| − embedding | 700 |
| − reranker | 450 |
| **Free for KV** | **9,252** |
| − KV @ 240,000 tok | 8,031 |
| **Free headroom** | **1,221** |

**n_ctx = 240,000** (per slot: 120,000)

### Co-running Speech-to-Text (Whisper)

Running the `local-speech-to-text` service (`whisper-server` using `ggml-large-v3-turbo-q5_0.bin`) alongside `local-inference` requires an additional **~1,426 MiB** of GPU VRAM (weights + compute + HIP context overhead).

#### Co-running with Config A (MoE + Vision + Embedding + Reranker + Whisper)

| Item | MiB |
|---|---|
| Total VRAM | 30,704 |
| − Config A (weights + compute) | 20,409 |
| − KV @ 240,000 tok | 8,031 |
| − Whisper (local-speech-to-text) | 1,426 |
| **Free headroom** | **838** |

*Status*: **Safe**. The system has 838 MiB of remaining VRAM headroom, meaning all processes will remain fully offloaded to the GPU without risk of host memory fallbacks.

#### Co-running with Config B (Dense + Embedding + Reranker + Whisper)

| Item | MiB |
|---|---|
| Total VRAM | 30,704 |
| − Config B (weights + compute) | 21,452 |
| − KV @ 240,000 tok | 8,031 |
| − Whisper (local-speech-to-text) | 1,426 |
| **Free headroom** | **−205** |

*Status*: **Overallocated (Risk of system RAM fallback)**. The total required VRAM (30,909 MiB) exceeds the GPU's physical capacity (30,704 MiB) by 205 MiB.

*Mitigation*: If you need to run Whisper concurrently with the Dense LLM setup, you must reduce the LLM context limit `LI_N_CTX` from `240000` to `200000` in `local-inference.env` to free up ~1,340 MiB of VRAM:
- Reduced KV @ 200,000 tok: ~6,692 MiB
- Adjusted Free Headroom: **~1,134 MiB** (Safe)


## Implementation Considerations

### ROCm / GPU Access
Because `llama-server` requires direct access to GPU device nodes:
- `PrivateDevices=no` is set in the systemd unit.
- Access to `/dev/dri` and `/dev/kfd` is mandatory.
- The user must be in the `render` and `video` groups.

### Filesystem and Data Access
- **Models**: Read-write access to `/data/public/machine-learning` is configured.
- **Sandboxing**: Uses `ProtectSystem=strict`.
- **Isolation**: The user's home directory `%h` is bind-mounted to allow the server to read its configurations, while system paths are protected.

### Configuration & Ports
- **Default Port**: `50080` (llama-server OpenAI-compatible API — LLM, embeddings, reranking)
- **Configuration File**: Environment parameters and model settings are configured in `~/.config/systemd/user/local-inference.env`.

### Models Preset (INI)
The `local-inference.ini` file is **auto-generated** from the env file on every `install`, `start`, and `restart`. Do not edit it manually. It defines:
- The LLM model section with KV cache, batch, and context parameters
- The embedding model section with `embedding = true` and `pooling = mean`
- The optional reranker section with `embedding = true` and `pooling = rank`

### Reranker Toggle
Set `LI_RERANKER_ENABLED=true` in the env file to enable the `/v1/rerank` endpoint. When disabled, `--models-max` is reduced from 3 to 2, and the reranker model is not loaded.
