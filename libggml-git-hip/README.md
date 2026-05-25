# libggml-git-hip

An optimized Git HEAD compilation of the GGML tensor library and associated tools (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp`) for Arch Linux. This package focuses on **HIP/ROCm hardware accelerated** builds, and uses libggml and libllama as shared libraries instead of static linking.

## Split Packages

- **`libggml-git-hip`**: The core shared library (`libggml.so`, `libllama.so`) built for HIP/ROCm.
- **`llama.cpp-git-ggml-hip`**: Main executables (`llama-cli`, `llama-server`, etc.) linking to the shared lib.
- **`whisper.cpp-git-ggml-hip`**: Whisper speech-to-text tools (`whisper-cli`, `whisper-server`) linking to the shared lib.
- **`python-llama-cpp-git-ggml-hip`**: Python bindings (`llama_cpp`) installed into site-packages, linking to the shared lib.
- **`stable-diffusion.cpp-git-ggml-hip`**: Stable Diffusion Text-to-Image generation tools (`sd-cli`, `sd-server`) linking to the shared lib.
- **`qwen3-tts.cpp-git-ggml-hip`**: Qwen3-TTS text-to-speech tools (`qwen3-tts-cli`, `qwen3-tts-server`) linking to the shared lib.

## Key Features

- **Git HEAD Version:** Builds directly from latest GIT HEAD to provide the latest features and improvements.
- **Unified Shared Library:** `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp` and `qwen3-tts.cpp` all link dynamically against a single system-wide `libggml-git-hip`. This ensures **consistent backend behavior** and bug compatibility across all tools.
- **RDNA2 Optimization:** Includes `rdna2-optimized-tile.patch` to unlock more performant TILE Flash Attention on RDNA2 GPUs.
- **Python Bindings:** patched to support the latest git version of libggml and llama.cpp.
- **OpenBLAS CPU Fallback**: CPU-only layers are uniformly accelerated via a shared linkage to OpenBLAS.

### Package Rationale

Of the current HIP/ROCm-accelerated Archlinux AUR packages for the GGML ecosystem (beside `llama.cpp-hip`) the following are outdated and orphaned:

- `llama.cpp-hipblas-git`
- `whisper.cpp-hip`
- `python-llama-cpp-hip`
- `stable-diffusion.cpp-hipblas-git`

This package provides up-to-date replacements for the outdated HIP/ROCm-accelerated builds of the GGML ecosystem on Arch Linux for `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp` and adds:

- `qwen3-tts.cpp` with HIP/ROCm acceleration.

In contrast to the listed AUR packages above, each of which contains their own static compilation of `libggml`, this package compiles `libggml` as a single system-wide shared library (`libggml-git-hip`) and dynamically links all downstream packages against it, we achieve:

- **Disk, Compute & Memory Savings**: We compile the heavy HIP/ROCm GPU kernels only once.
- **Unified Backend Upgrades**: A single update to `libggml-git-hip` automatically upgrades GPU kernel performance, RDNA optimizations, and model support across all 5 downstream tools.
- **OpenBLAS CPU Fallback**: CPU-only layers are uniformly accelerated via a shared linkage to OpenBLAS, providing faster CPU fallback matrix operations than the standard unaccelerated CPU backend.

### Avoiding Namespace Conflicts
To prevent conflicts with existing standalone AUR packages (such as `llama.cpp-hip`, `stable-diffusion.cpp-git`, or `qwen3-tts.cpp`), this repository uses the naming suffix `-git-ggml-hip` for all downstream split packages (e.g. `stable-diffusion.cpp-git-ggml-hip` or `qwen3-tts-git-ggml-hip`).
They explicitly declare their dynamic linkage to the shared `libggml-git-hip` package, while declaring correct `conflicts` and `provides` arrays so they can act as drop-in replacements for standard packages without namespace pollution or file conflicts.


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

**Note:** The build conditionally disables `GGML_HIP_ROCWMMA_FATTN` ONLY for single-target RDNA2 builds to trigger the patch logic, and keeps ROCWMMA_FATTN enabled for other targets

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
