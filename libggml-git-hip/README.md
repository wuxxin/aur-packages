# libggml-git-hip

An optimized Git HEAD compilation of the GGML tensor library and associated tools (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp`, `qwen3-tts.cpp`) for Arch Linux. This package uses **dynamic backends** (`GGML_BACKEND_DL=ON`) to compile and package **CPU** (with auto-selected instruction set variants), **OpenBLAS**, **HIP/ROCm**, and **Vulkan** backends under a unified shared library.

## Split Packages

- **`libggml-git-hip`**: The core shared library (`libggml.so`, `libllama.so`) and dynamically loaded backend modules (`libggml-cpu.so`, `libggml-blas.so`, `libggml-hip.so`, `libggml-vulkan.so` under `/usr/lib/ggml/`).
- **`llama.cpp-git-ggml-hip`**: Main executables (`llama-cli`, `llama-server`, etc.) dynamically linking to the shared library.
- **`whisper.cpp-git-ggml-hip`**: Whisper speech-to-text tools (`whisper-cli`, `whisper-server`) dynamically linking to the shared library.
- **`python-llama-cpp-git-ggml-hip`**: Python bindings (`llama_cpp`) installed into site-packages, dynamically linking to the shared library.
- **`stable-diffusion.cpp-git-ggml-hip`**: Stable Diffusion Text-to-Image generation tools (`sd-cli`, `sd-server`) dynamically linking to the shared library.
- **`qwen3-tts.cpp-git-ggml-hip`**: Qwen3-TTS text-to-speech tools (`qwen3-tts-cli`, `qwen3-tts-server`) dynamically linking to the shared library.
- **`crispasr-git-ggml-hip`**: CrispASR speech-to-text tools (`crispasr`, `crispasr-server`, `crispasr-quantize`) dynamically linking to the shared library. Serves as a high-performance alternative to Whisper, enabling the use of Cohere Transcribe and other modern Conformer-based ASR/TTS architectures.

## Key Features

- **Git HEAD Version:** Builds directly from latest GIT HEAD to provide the latest features, optimizations, and model compatibility.
- **Dynamic Backend Loading:** `libggml.so` loads backends dynamically at runtime from `/usr/lib/ggml/`. This isolates dependencies and prevents applications from failing to load if a specific GPU runtime (like ROCm) is missing or broken.
- **Combined Backends:** Supports CPU (AVX/AVX2/AVX512), OpenBLAS, Vulkan, and HIP/ROCm in a single installation. Devices can be listed using `llama-cli --list-devices` and selected at runtime using `--device <name>` (e.g. `--device hip` or `--device vulkan`).
- **ROCm & Vulkan Support:** Accelerate workloads on AMD GPUs using the highly optimized native HIP backend, or fallback to the cross-vendor Vulkan backend.
- **CPU Backend Optimization:** Instead of a single static CPU build, compiling with `GGML_CPU_ALL_VARIANTS` builds optimized variants for multiple instruction sets (AVX, AVX2, AVX512, etc.). At runtime, the best matching variant for the host CPU is dynamically loaded (e.g. AVX2/FMA on Zen3+).
- **Qwen3 Optimizations:** See (Qwen3-TTS)[qwen3-tts-modifications.md]
- **shared libggml support in CrispASR:** Add the needed additional Conformer functions in libggml, so shared build is possible.
- **RDNA2 Optimization:** Includes `rdna2-optimized-tile.patch` to unlock more performant TILE Flash Attention on RDNA2 GPUs.
- **Python Bindings:** patched to support the latest git version of libggml and llama.cpp.
- **OpenBLAS CPU Fallback:** CPU-only layers are accelerated either via the standard CPU backend, or optional with the OpenBLAS CPU backend, providing alternative matrix operations to the standard CPU backend.

### Package Rationale

Of the current HIP/ROCm-accelerated Archlinux AUR packages for the GGML ecosystem (beside `llama.cpp-hip`) the following are outdated and orphaned:

- `llama.cpp-hipblas-git`
- `whisper.cpp-hip`
- `python-llama-cpp-hip`
- `stable-diffusion.cpp-hipblas-git`

This package provides up-to-date replacements for the outdated HIP/ROCm-accelerated builds of the GGML ecosystem on Arch Linux for `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp` and adds:

- `qwen3-tts.cpp` with HIP/ROCm acceleration.
- `crispasr` using the shared libggml library  `crispasr-git-ggml-hip`) with HIP, Vulkan, CPU, and BLAS acceleration.

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

### Unified System GGML with added Conformer operations for CrispASR shared libggml support (`patch-ggml.py`)
To enable dynamic linking of CrispASR to the system-wide `libggml.so` without missing Conformer functions, we apply a dynamic patching script during the `prepare()` phase:
- **Missing Functions Synced**: The script `patch-ggml.py` locates and injects the `GGML_OP_NORM_AFFINE` (fused LayerNorm + scale/shift) and `GGML_GLU_OP_SIGLU` (SiGLU activation) operations directly into the standard `llama.cpp/ggml` source tree (handling public headers, core symbol mapping, CPU compute kernels, and HIP/ROCm GPU kernel launchers).
- **CrispASR Dynamic Linkage**: CrispASR is built with `-DCRISPASR_USE_SYSTEM_GGML=ON`, enabling its binaries to link dynamically to `/usr/lib/libggml.so`. This avoids redundant compilation of massive GPU shaders/kernels.
- **Bypassing Sentencepiece**: We comment out the search for `libsentencepiece` in CrispASR (`src/CMakeLists.txt`), forcing a fallback to CrispASR's custom Viterbi tokenizer. This avoids linker failures caused by a broken system `sentencepiece` dynamic package on this system and is completely safe since sentencepiece is only utilized by the TTS component, which is unused for our local ASR Speech-to-Text pipeline.

### RDNA2 Flash Attention Optimization (`rdna2-optimized-tile.patch`)
This package applies a custom patch to maximize stability and performance on RDNA2 GPUs (gfx1030). It bypasses the unstable "VEC" kernel and forces an optimized "TILE" kernel with 256 threads for Head Dim 128.

| Configuration | Throughput (40k Ctx) | Max Stable Context |
| :--- | :--- | :--- |
| Stock (VEC) | ~660 Char/s | ~50k Chars |
| Stock (TILE) | ~280 Char/s | >145k Chars |
| **Optimized TILE** | **~1485 Char/s**| **>145k Chars** |

### Python Binding Fixes (`python-llama-cpp`)
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

### Qwen3-TTS Hybrid mode , offload Device selection, Voice Fallback & Built-in Voices 

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

