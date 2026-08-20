# libggml-git-hip

An optimized Git HEAD compilation of the GGML tensor library and associated tools (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp`, `qwen3-tts.cpp`, `parakeet.cpp`) for Arch Linux. This package uses **dynamic backends** (`GGML_BACKEND_DL=ON`) to compile and package **CPU** (with auto-selected instruction set variants), **OpenBLAS**, **HIP/ROCm**, and **Vulkan** backends under a unified shared library.

## Split Packages

- **`libggml-git-hip`**: The core shared library (`libggml.so`, `libllama.so`) and dynamically loaded backend modules (`libggml-cpu.so`, `libggml-blas.so`, `libggml-hip.so`, `libggml-vulkan.so` under `/usr/lib/ggml/`).
- **`llama.cpp-git-ggml-hip`**: Main executables (`llama-cli`, `llama-server`, etc.) dynamically linking to the shared library.
- **`whisper.cpp-git-ggml-hip`**: Whisper speech-to-text tools (`whisper-cli`, `whisper-server`) dynamically linking to the shared library.
- **`python-llama-cpp-git-ggml-hip`**: Python bindings (`llama_cpp`) installed into site-packages, dynamically linking to the shared library.
- **`stable-diffusion.cpp-git-ggml-hip`**: Stable Diffusion Text-to-Image generation tools (`sd-cli`, `sd-server`) dynamically linking to the shared library.
- **`qwen3-tts.cpp-git-ggml-hip`**: Qwen3-TTS text-to-speech tools (`qwen3-tts-cli`, `qwen3-tts-server`) dynamically linking to the shared library.
- **`parakeet.cpp-git-ggml-hip`**: FastConformer and TDT ASR tools (`parakeet-cli`, `parakeet-server`) dynamically linking to the shared library.

## Key Features

- **Git HEAD Version:** Builds directly from latest GIT HEAD to provide the latest features, optimizations, and model compatibility.
- **Dynamic Backend Loading:** `libggml.so` loads backends dynamically at runtime from `/usr/lib/ggml/`. This isolates dependencies and prevents applications from failing to load if a specific GPU runtime (like ROCm) is missing or broken.
- **Combined Backends:** Supports CPU (AVX/AVX2/AVX512), OpenBLAS, Vulkan, and HIP/ROCm in a single installation. Devices can be listed using `llama-cli --list-devices` and selected at runtime using `--device <name>` (e.g. `--device hip` or `--device vulkan`).
- **ROCm & Vulkan Support:** Accelerate workloads on AMD GPUs using the highly optimized native HIP backend, or fallback to the cross-vendor Vulkan backend.
- **CPU Backend Optimization:** Instead of a single static CPU build, compiling with `GGML_CPU_ALL_VARIANTS` builds optimized variants for multiple instruction sets (AVX, AVX2, AVX512, etc.). At runtime, the best matching variant for the host CPU is dynamically loaded (e.g. AVX2/FMA on Zen3+).
- **Qwen3 Optimizations:** See (Qwen3-TTS)[qwen3-tts-modifications.md]
- **RDNA2 Optimization:** Includes `rdna2-optimized-tile.patch` to unlock more performant TILE Flash Attention on RDNA2 GPUs.
- **Python Bindings:** patched to support the latest git version of libggml and llama.cpp.
- **OpenBLAS CPU Fallback:** CPU-only layers are accelerated either via the standard CPU backend, or optional with the OpenBLAS CPU backend, providing alternative matrix operations to the standard CPU backend.

### Package Rationale

Of the current HIP/ROCm-accelerated Archlinux AUR packages for the GGML ecosystem (beside `llama.cpp-hip`) the following are outdated and orphaned:

- `llama.cpp-hipblas-git`
- `whisper.cpp-hip`
- `python-llama-cpp-hip`
- `stable-diffusion.cpp-hipblas-git`

This package provides up-to-date replacements for the outdated HIP/ROCm-accelerated builds of the GGML ecosystem on Arch Linux for `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp`.

It adds the following new packages:

- `qwen3-tts.cpp` with HIP/ROCm acceleration.
- `parakeet.cpp` with HIP/ROCm acceleration.

In contrast to the listed AUR packages above, each of which contains their own static compilation of `libggml`, this package compiles `libggml` as a single system-wide shared library (`libggml-git-hip`) and dynamically links all downstream packages against it, we achieve:

- **Disk, Compute & Memory Savings**: We compile the heavy HIP/ROCm GPU kernels only once.
- **Unified Backend Upgrades**: A single update to `libggml-git-hip` automatically upgrades GPU kernel performance, RDNA optimizations, and model support across all 5 downstream tools.

### Avoiding Namespace Conflicts
To prevent conflicts with existing standalone AUR packages (such as `llama.cpp-hip`, `stable-diffusion.cpp-git`, or `qwen3-tts.cpp`), this repository uses the naming suffix `-git-ggml-hip` for all downstream split packages (e.g. `stable-diffusion.cpp-git-ggml-hip` or `qwen3-tts-git-ggml-hip`).
They explicitly declare their dynamic linkage to the shared `libggml-git-hip` package, while declaring correct `conflicts` and `provides` arrays so they can act as drop-in replacements for standard packages without namespace pollution or file conflicts.


## Installation

```bash
# Build and install all packages
makepkg -i
```

## Patches & Modifications


### RDNA2 Flash Attention Optimization (`rdna2-optimized-tile.patch`)
This package applies a custom patch to maximize stability and performance on RDNA2 GPUs (gfx1030). It bypasses the unstable "VEC" kernel and forces an optimized "TILE" kernel with 256 threads for Head Dim 128.

| Configuration | Throughput (40k Ctx) | Max Stable Context |
| :--- | :--- | :--- |
| Stock (VEC) | ~660 Char/s | ~50k Chars |
| Stock (TILE) | ~280 Char/s | >145k Chars |
| **Optimized TILE** | **~1485 Char/s**| **>145k Chars** |

### Python Binding System Library Integration (`llama-cpp-system.patch`)
With modern `llama-cpp-python` git HEAD, the binding layer natively matches upstream `llama.h` ABI structures and exports (including `llama_context_params`, `llama_model_params`, and modern LoRA / sampler functions).

Previously required symbol aliasing and runtime monkey-patching scripts (`llama-patch-abi.py`, `llama-shims.py`) have been retired. The package now only applies a clean one-line patch (`llama-cpp-system.patch`) to configure the Python binding to load the system-wide `/usr/lib/libllama.so` and dynamic backend libraries by default.

### Qwen3-TTS Hybrid mode, offload Device selection, Voice Fallback & Built-in Voices 

#### Additional Environment Variables

In addition to the upstream khimaros fork, which adds the following environment variables:
- `QWEN3_TTS_FORCE_CPU`: Force all computations to run on the CPU.
- `QWEN3_TTS_LOW_MEM`: Enable memory-mapped file loading (mmap) and lazy buffer allocations to keep the VRAM/RAM footprint minimal.

This patch series adds:
- `QWEN3_TTS_TRANSFORMER_FORCE_CPU`: Force only the TTSTransformer (Code Generation) stage to run on the CPU. When combined with running Vocoder Decode on the GPU, this unlocks **Hybrid Split Mode** (the optimal performance and VRAM sweet spot).
- `QWEN3_TTS_VOCODER_FORCE_CPU`: Force only the Vocoder Decode (AudioTokenizerDecoder) stage to run on the CPU.
- `QWEN3_TTS_DEVICE`: Specify a custom backend device by name (e.g. `cpu`, `hip0`, `rocm0`, etc.) to offload the computations.

We also introduce a new command line parameter to select the preferred offloading device:
- `-dev`, `--device <name>`: Used in both `qwen3-tts-cli` and `qwen3-tts-server` to specify the offloading device (which sets the `QWEN3_TTS_DEVICE` environment variable internally). Set to `none` (or `cpu`) to disable offloading.


#### Voice Fallback & Built-in Voices

Standard OpenAI text-to-speech clients default to requesting standard voices (e.g. `alloy`). 

To prevent `400 Bad Request` errors on unmapped voice names, this patch adds an automatic voice fallback in `qwen3-tts-server`:
- If the requested voice is not found, the server prints a warning and falls back to the first built-in speaker (if available) or the default zero-embedding voice.

The built-in voice names for the `Qwen3-TTS-12Hz-0.6B-CustomVoice-Q8_0.gguf` model are:
- `default` (zero-embedding baseline voice)
- `serena`
- `vivian`
- `uncle_fu`
- `ryan`
- `aiden`
- `ono_anna`
- `sohee`
- `eric`
- `dylan`


### Git Commit-Hash Versioning for whisper and qwen3-tts

- patches: `whisper-version-commit.patch` and `qwen3-tts-version-commit.patch`

To assist with version identification and debugging of Git-HEAD packages:
- **Whisper**: Appends the specific Git commit hash of the whisper.cpp repository to the output of `whisper-cli --version` (e.g., `whisper.cpp version: 1.9.1 (commithash)`).
- **Qwen3-TTS**: Implements the `--version` flag for `qwen3-tts-cli` to output `qwen3-tts version 0.1-main-commithash` where the branch name (`main`) and short commit hash of the qwen3-tts.cpp repository are dynamically resolved at configure time.

### Jina Reranker v3 Cross-Encoder Support (`jina-reranker-v3.patch`)

Adds upstream support for the [jina-reranker-v3](https://huggingface.co/jinaai/jina-reranker-v3) cross-encoder reranking model to llama.cpp. This model is based on Qwen3 with a dense projector MLP for cosine similarity scoring.

- **Architecture**: Qwen3 base (hidden_size=1024) with a 2-layer projector MLP (1024 → 512 → 512 with ReLU activation)
- **Pooling**: LAST token pooling
- **Output**: 512-dimensional embeddings for cosine similarity scoring
- **Converter**: `JinaForRankingModel` class registered for GGUF conversion of HuggingFace models
- **Dense tensor support**: Adds `DENSE_2_OUT`/`DENSE_3_OUT` tensor mappings to QWEN3-family architectures
- **Usage**:
  ```bash
  llama-server -m jina-reranker-v3.gguf --embeddings --pooling last
  ```
  Then POST to `/v1/embeddings` to get 512-dim projected embeddings; compute cosine similarity client-side for reranking.

---

## Changelog

### `10524.r8.g70aff25-1` (Current)
- **Patch Modernization & Cleanup**:
  - Replaced outdated / fuzzy patches with clean diffs matching latest upstream Git HEADs (zero fuzz, zero offsets, zero rejects).
  - Dropped `llama-cmake-include.patch`: upstream `llama.cpp` has integrated `INTERFACE_INCLUDE_DIRECTORIES` into `ggml-config.cmake.in`.
  - Dropped `llama-patch-abi.py` & `llama-shims.py`: upstream `llama-cpp-python` Git HEAD now natively supports modern `llama.h` ABI and functions.
  - Refreshed `jina-reranker-v3.patch` cleanly against latest `llama.cpp` `src/llama-graph`, `src/llama-model`, and Qwen3 architectures.
  - Refreshed `whisper-version-commit.patch` cleanly against latest `whisper.cpp`.
- **Build System**: Updated all source checksums via `updpkgsums` and validated compilation of all 7 split packages.

### `10344.r14.g030ebb5-1`
- **Jina Reranker v3 Integration**: Added `jina-reranker-v3.patch` for Qwen3 cross-encoder embeddings and dense projection layers.
- **Python Bindings Compatibility**: Introduced ABI shims for LoRA and sampler functions to bridge `llama-cpp-python` with dynamic `libllama.so`.
- **Dynamic Backend Loading**: Hardened `GGML_BACKEND_DL=ON` across CPU variants, OpenBLAS, HIP/ROCm, and Vulkan.

### `9700.r12.g41bf982-1`
- **New Split Packages**:
  - Added `qwen3-tts.cpp-git-ggml-hip` with hybrid CPU/GPU split execution, device selection, and automatic voice fallback.
  - Added `parakeet.cpp-git-ggml-hip` (FastConformer and TDT ASR).
  - Added `stable-diffusion.cpp-git-ggml-hip` with web UI and system ggml integration.
- **Version Identification**: Implemented commit-hash tagging patches for `whisper.cpp` and `qwen3-tts.cpp`.

### `7974.r6.g262364e-1`
- **Initial Release**: Unified shared library `libggml-git-hip` with split packages `llama.cpp-git-ggml-hip`, `whisper.cpp-git-ggml-hip`, and `python-llama-cpp-git-ggml-hip`.
- **RDNA2 Acceleration**: HIP compilation with ROCm toolchain targeting modern AMD architectures (gfx1030+).





