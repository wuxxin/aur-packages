# libggml-git-hip

An optimized Git HEAD compilation of the GGML tensor library and associated tools (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`) for Arch Linux. This package focuses on **HIP/ROCm hardware acceleration** on RDNA architectures.

## Key Features

- **Git HEAD Version:** Builds directly from latest GIT HEAD to provide the latest features and improvements.
- **Unified Shared Library:** `llama.cpp`, `whisper.cpp`, and `python-llama-cpp` all link dynamically against a single system-wide `libggml-git-hip`. This ensures **consistent backend behavior** and bug compatibility across all tools.
- **RDNA2 Optimization:** Includes `rdna2-optimized-tile.patch` to unlock more performant TILE Flash Attention on RDNA2 GPUs.
- **Python Bindings:** patched to support the latest git version of libggml and llama.cpp.

## Package Structure

- **`libggml-git-hip`**: The core shared library (`libggml.so`, `libllama.so`) optimized for HIP.
- **`llama.cpp-git-ggml-hip`**: Main executables (`llama-cli`, `llama-server`, etc.) linking to the shared lib.
- **`whisper.cpp-git-ggml-hip`**: Whisper speech-to-text tools (`whisper-cli`, `whisper-server`) linking to the shared lib.
- **`python-llama-cpp-git-ggml-hip`**: Python bindings (`llama_cpp`) installed into site-packages, linking to the shared lib.

## Installation

```bash
# Build and install all packages
makepkg -i
```

## Patches & Modifications

### 1. RDNA2 Flash Attention Optimization (`rdna2-optimized-tile.patch`)
This package applies a custom patch to maximize stability and performance on RDNA2 GPUs (gfx1030). It bypasses the unstable "VEC" kernel and forces an optimized "TILE" kernel with 256 threads for Head Dim 128.

| Configuration | Throughput (40k Ctx) | Max Stable Context |
| :--- | :--- | :--- |
| Stock (VEC) | ~660 Char/s | ~50k Chars |
| Stock (TILE) | ~280 Char/s | >145k Chars |
| **Optimized TILE** | **~1485 Char/s**| **>145k Chars** |

**Note:** The build conditionally disables `GGML_HIP_ROCWMMA_FATTN` ONLY for single-target RDNA2 builds to trigger the patch logic, to keep ROCWMMA_FATTN enabled for other targets

### 2. Python Binding Fixes (`python-llama-cpp`)
To bridge the gap between latest `libllama.so` and the `llama-cpp-python` bindings, we apply functional shims and symbol aliasing.

#### Symbol Resolution Table

| Symbol Name | Resolution | Status |
| :--- | :--- | :--- |
| `llama_set_adapter_lora` | **Shimmed** | Re-implemented using `llama_set_adapters_lora` (plural API). Wraps single adapter into array. |
| `llama_adapter_lora_init` | **Shimmed** | Bound to C symbol with UTF-8 path encoding safety. |
| `llama_adapter_lora_free` | **Shimmed** | Bound to C symbol for manual memory management. |
| `llama_get_kv_self` | Aliased | Dummied to `llama_get_memory`. Deprecated in library. |
| `llama_rm_adapter_lora` | Aliased | Dummied to `llama_get_memory`. Unused by high-level API. |
| `llama_clear_adapter_lora`| Aliased | Dummied to `llama_get_memory`. Unused by high-level API. |
| `llama_apply_adapter_cvec`| Aliased | Dummied to `llama_get_memory`. Unused by high-level API. |
| `llama_kv_self_*` (13 variants)| Aliased | Dummied to `llama_get_memory`. Internal seq management replaced by library. |
| `llama_sampler_init_softmax`| Aliased | Dummied to `llama_get_memory`. Deprecated in library. |

**Implementation:** Shims are injected via `EOF` concatenation at the end of `llama_cpp/llama_cpp.py`. Aliases are applied via `sed` substitutions during the `prepare()` phase.

