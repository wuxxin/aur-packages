# Changelog — libggml-git-hip

Package-level change history for the `libggml-git-hip` split-package build. Per-update ecosystem deltas relevant to consumers of this system are tracked separately in `curated-changes.md`.

### `12522.r0.g2cbfc3c-1` (Current, built 2026-11-18; not yet installed)
Replaces the installed `12383.r1.g3549c27-1` (2026-11-14).
- **Upstream sync**: llama.cpp b12383→b12522, Strata v0.2.13.1→v0.2.15 (Control/Terminal 0.2.14/0.2.15, engines 0.1.60), whisper.cpp 1.9.6-dev, stable-diffusion.cpp v0.3.37, llama-cpp-python bump; qwen3-tts.cpp and parakeet.cpp unchanged upstream.
- **Patch refresh**: `whisper-version-commit.patch` re-pinned to the new upstream context (`find_package(llama 1.0.0)` stripped); `strata-system-ggml.patch` vision hunk rewritten onto upstream's own-ViT-tower layout — system-mode `strata-vision` now links the new `strata_vit_own` target (built via `STRATA_VISION_HIP`, same gfx archs).
- **Added**: `strata-clear-cache.patch` — the engine's `CLEAR_CACHE` stdin command (drop parked conversations + `malloc_trim`) split out of the old spill scaffold; verified in the built binary. Added `stable-diffusion-graph-view.patch` — llama.cpp b12521+ keeps `ggml_graph_view` private (defined in ggml.c, not exported from libggml); stable-diffusion v0.3.37's system-ggml compat shim calls it, so the patch mirrors it locally inside the `SD_GGML_GRAPH_COMPAT` block.
- **Removed**: `strata-nvme-spill.patch` (kept unreferenced in this directory; design parked at `strata-spill-plan.md`). The patch was a scaffold: it logged evictions and wired `--disk-spill*` flags, never persisted KV. Upstream supersedes its memory half (#5697 RAM release on eviction, segment/checkpoint park pools with budget accounting).
- **Docs**: changelog split out of `README.md` into this file; added `curated-changes.md` with a reusable per-window extraction procedure.

### `12284.r12.g1648d64-1`
- **acestep.cpp Subpackage (`acestep.cpp-git-ggml-hip`)**:
  - Added subpackage for ACE-Step 1.5 text-and-lyrics music generation (`ace-lm`, `ace-synth`, `ace-server`, `ace-understand`, `neural-codec`, `mp3-codec`, `quantize`).
  - Dynamic linking against system shared `libggml.so` via `acestep-system-ggml.patch`.
  - Runtime device offloading (HIP/ROCm, Vulkan, CPU) through GGML dynamic backend plugin discovery.
- **Patch Refresh & Upstream Sync**:
  - Refreshed `strata-system-ggml.patch` to support upstream Strata CMake reorganization (`cmake/strata_ggml.cmake`, including `src/platform/ggml_cpu_shim.cpp` and system `mtmd`/`llama` vision linking) and updated Strata packaging for `cmake/`, `strata_cli/`, `strata.py`, and `tools/chat.py`.
  - Refreshed `strata-version-commit.patch`, `jina-reranker-v3.patch`, and `whisper-version-commit.patch` with zero offsets.
  - Added `strata-nvme-spill.patch`: engine `CLEAR_CACHE` stdin protocol command for zero-turnaround S3 suspend memory reclamation and opt-in `--disk-spill` lazy NVMe KV offload for long conversations.
  - Updated all components to latest git HEAD.

### `11937.r7.g1b4554e-1`
- **Strata Documentation & Packaging Fixes**:
  - Resolved `install` file conflict in `package_strata-engine-git-ggml-hip()` by preserving `docs/*.md` under `/usr/share/doc/strata-engine-git-ggml-hip/docs/` alongside root `README.md` and `SECURITY.md`, maintaining markdown inter-doc relative link structures.
  - Added `/usr/share/doc/strata` compatibility symlink.
  - Added `hipblaslt` direct runtime dependency to `strata-engine-git-ggml-hip`.
  - Added `-DCMAKE_SKIP_RPATH=ON` and `patchelf --remove-rpath` to remove ephemeral staging directory paths from the compiled `strata` binary.
  - Passed `--no-same-owner` during embedded `llama.cpp` tar extraction for reliable rootless and sandboxed builds.
- **Strata Git Versioning (`strata-version-commit.patch`)**:
  - Implemented Git tag and commit identification in `strata --version` (e.g. `strata version: 0.2.7 (5e8a4cca7)`).
- **Upstream Sync**: Updated all submodules and component repositories to latest git HEAD.

### `11753.r0.gd8d9297-1`
- **Strata Engine Subpackage (`strata-engine-git-ggml-hip`)**:
  - Integrated Strata inference engine for large MoE models (Qwen 3.8-Flash-Next, DeepSeek-V4.1-Flash, Qwen 3.6-35B).
  - Native AMD ROCm/HIP wave32 compilation (`gfx1010`–`gfx1201`).
  - Dynamic linking against system shared `libggml.so`, `libllama.so`, and `libmtmd.so` via CPU traits shim (`strata-system-ggml.patch`).
  - Multimodal vision reader (`strata-vision-hip`) and `/usr/bin/strata` runtime launcher.

### `10524.r8.g70aff25-1`
- **Patch Modernization & Cleanup**:
  - Replaced outdated / fuzzy patches with clean diffs matching latest upstream Git HEADs (zero fuzz, zero offsets, zero rejects).
  - Dropped `llama-cmake-include.patch`: upstream `llama.cpp` has integrated `INTERFACE_INCLUDE_DIRECTORIES` into `ggml-config.cmake.in`.
  - Dropped `llama-patch-abi.py` & `llama-shims.py`: upstream `llama-cpp-python` Git HEAD now natively supports modern `llama.h` ABI and functions.
  - Refreshed `jina-reranker-v3.patch` cleanly against latest `llama.cpp` `src/llama-graph`, `src/llama-model`, and Qwen3 architectures.
  - Refreshed `whisper-version-commit.patch` cleanly against latest `whisper.cpp`.
  - Added `sd-system-ggml.patch`: fixed `stable-diffusion.cpp` linear I8 matrix multiplication and quantization compatibility when building against shared system GGML.
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
