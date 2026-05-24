# libggml-git-hip

An optimized Git HEAD compilation of the GGML tensor library and associated tools (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp`) for Arch Linux. This package focuses on **HIP/ROCm hardware acceleration** on RDNA architectures.

## Key Features

- **Git HEAD Version:** Builds directly from latest GIT HEAD to provide the latest features and improvements.
- **Unified Shared Library:** `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, and `stable-diffusion.cpp` all link dynamically against a single system-wide `libggml-git-hip`. This ensures **consistent backend behavior** and bug compatibility across all tools.
- **RDNA2 Optimization:** Includes `rdna2-optimized-tile.patch` to unlock more performant TILE Flash Attention on RDNA2 GPUs.
- **Python Bindings:** patched to support the latest git version of libggml and llama.cpp.
- **OpenBLAS**: build to use OpenBLAS for optimized CPU performance layer.

### Package Rationale

Many of the HIP/ROCm-accelerated Archlinux AUR packages for the GGML ecosystem (beside `llama.cpp-hip`) are outdated and/or orphaned:

- **`llama.cpp-hipblas-git`**: Orphaned and outdated (`b5123.r1.bc091a4dc-1`). It lacks all modern refactors, multi-GPU optimizations, and new model support.
- **`whisper.cpp-hip`**: Orphaned and flagged out of date (`1.8.3-1`). ROCm-accelerated transcription is currently unavailable via an active/maintained AUR package.
- **`python-llama-cpp-hip`**: Orphaned (`0.3.16-1`) and outdated, making python bindings unusable with ROCm out-of-the-box.
- **`stable-diffusion.cpp-hipblas-git`**: Orphaned, flagged out of date (`r256.5900ef6-1`). Missing support for SDXL, Flux, SD3, and other modern architectures.

### Shared Library Architecture
Normally, each of these packages (`llama.cpp`, `whisper.cpp`, `stable-diffusion.cpp`, and the Python bindings) includes its own static compilation of `libggml`. This results in **Inconsistent Backend Behavior**: Each tool may run on a slightly different version of GGML, leading to inconsistent model support, bugs, and mismatched features.

By compiling `libggml` as a single unified system-wide shared library (`libggml-git-hip`) and dynamically linking all downstream packages (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`, and `stable-diffusion.cpp`) against it, we achieve:
- **Disk, CPU & Memory Savings**: We compile the heavy HIP/ROCm GPU kernels exactly once.
- **Unified Backend Upgrades**: A single update to `libggml-git-hip` automatically upgrades GPU kernel performance, RDNA optimizations, and model support across all 4 downstream tools.
- **OpenBLAS CPU Fallback**: CPU-only layers are uniformly accelerated via a shared linkage to OpenBLAS, providing faster CPU fallback matrix operations than the standard unaccelerated CPU backend.

### Avoiding Namespace Conflicts
To prevent conflicts with existing standalone AUR packages (such as `llama.cpp-hip` or `stable-diffusion.cpp-git`), this repository uses the naming suffix `-git-ggml-hip` for all downstream split packages (e.g. `stable-diffusion.cpp-git-ggml-hip`).
They explicitly declare their dynamic linkage to the shared `libggml-git-hip` package, while declaring correct `conflicts` and `provides` arrays so they can act as drop-in replacements for standard packages without namespace pollution or file conflicts.


## Package Structure

- **`libggml-git-hip`**: The core shared library (`libggml.so`, `libllama.so`) optimized for HIP.
- **`llama.cpp-git-ggml-hip`**: Main executables (`llama-cli`, `llama-server`, etc.) linking to the shared lib.
- **`whisper.cpp-git-ggml-hip`**: Whisper speech-to-text tools (`whisper-cli`, `whisper-server`) linking to the shared lib.
- **`python-llama-cpp-git-ggml-hip`**: Python bindings (`llama_cpp`) installed into site-packages, linking to the shared lib.
- **`stable-diffusion.cpp-git-ggml-hip`**: Stable Diffusion Text-to-Image generation tools (`sd-cli`, `sd-server`) linking to the shared lib.

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
