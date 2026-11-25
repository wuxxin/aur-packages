# strata-engine-git-hip

Git HEAD build of [Strata](https://github.com/Niko1221/Strata) — the inference engine for large MoE models (Qwen3.8-Flash-Next, DeepSeek-V4.1-Flash, Qwen3.6-35B, Inkling-2-Mini, Hy4-Flash) with dynamic CPU expert offloading, MTP/DFlash2 drafting, web chat + agent tooling over `strata serve`, and the self-contained multimodal picture readers (`strata-vision-hip` GPU + `strata-vision` CPU fallback) — compiled for AMD RDNA GPUs via HIP/ROCm on Arch Linux.

## Shipped Binaries (`/usr/lib/strata/engine/`)

- `strata` — main HIP engine (Qwen3.8-Flash-Next, DeepSeek, etc.)
- `strata-q36` — dedicated HIP engine for Qwen3.6-35B-A3B
- `strata-inkling` — standalone HIP engine for Inkling-2-Mini (`.strata` v1.1) with in-process vision and 1..64 continuous batching
- `strata-hy4` — standalone HIP engine for Tencent Hy4-Flash 220B-A12B (`.strata`, linked against system `zstd`)
- `strata-vision-hip` / `strata-vision` — self-contained GPU (HIP) and CPU fallback Qwen ViT picture readers
- `strata-gguf`, `strata-dequant`, `strata-plan` — CLI artifact and planning utilities

## Why a separate package

Since Strata 0.2.16 ("own-stack" steps 1–10) the engine links **no ggml, llama.cpp, or mtmd at all**: expert quantization and prompt kernels are Strata's own code (`Strata: no ggml in this build` is what a release configure prints), and the picture reader is its own Qwen vision tower. It shares nothing with `libggml-git-hip` beyond the ROCm toolchain, so it builds here instead of as a split package of that base.

The AUR already has `strata-engine-git`; this package is named `strata-engine-git-hip` and declares `provides`/`conflicts` for `strata-engine`, `strata-engine-git`, `strata-engine-git-ggml-hip` (its former name as a split package of `libggml-git-hip`) and `replaces=('strata-engine-git-ggml-hip')`.

## Patches & Modifications

### Git commit-hash versioning (`strata-version-commit.patch`)

Adds the tag + build-commit stamp to the engine's CMake (the upstream project's own `STRATA_VERSION` define is extended with `STRATA_TAG_VERSION` / `STRATA_BUILD_COMMIT`, read from git) and makes `strata --version` print e.g. `strata version: 0.2.16 (58ee32277)`.

### Strata `CLEAR_CACHE` stdin command (`strata-clear-cache.patch`)

Adds a serve-protocol command to the engine's stdin loop: writing `CLEAR_CACHE` evicts all parked RAM conversations through `evict_sink` (flushing them to Strata's persistent SSD spill tier when `--conversation-spill-dir` / `--conversation-spill-persist` is enabled), waits for the background spill writer to finish, shrinks idle segment pools, and trims the host heap, answering `CLEARED <n>`. Used by both the idle RAM-cache-clear timer and the S3 pre-suspend hook to reclaim ~8–16 GiB of host RAM without unloading VRAM weights or losing parked conversations.

### Layout note (0.2.16)

Upstream moved its tree to `engine/`, `terminal/`, `app/`. The package installs a read-only copy under `/usr/share/strata`; the launcher (`/usr/bin/strata`) materializes a user-writable app dir at `${STRATA_HOME:-~/.local/share/strata}/app` with symlinks (`terminal/`, `engine/`) plus the built binaries in `app/terminal/engine/`. Old-layout state (pre-0.2.16 app dirs, `Strata-data` next to it) is migrated by symlink on first start.

## Build

```bash
makepkg -si          # builds engine + vision reader for this machine's gfx targets
```

HIP architectures come from `rocm-supported-gfx` (override with `AMDGPU_TARGETS=`); the RDNA whitelist in the PKGBUILD mirrors what Strata's kernels support. Update windows for our deployment: [CHANGELOG.md](CHANGELOG.md) (Strata digest), ecosystem-wide: [../libggml-git-hip/CHANGELOG.md](../libggml-git-hip/CHANGELOG.md).
