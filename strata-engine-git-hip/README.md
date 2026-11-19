# strata-engine-git-hip

Git HEAD build of [Strata](https://github.com/Niko1221/Strata) — the inference engine for large MoE models (Qwen3.8-Flash-Next, DeepSeek-V4.1-Flash, Qwen3.6-35B) with dynamic CPU expert offloading, MTP/DFlash2 drafting, web chat + agent tooling over `strata serve`, and the self-contained multimodal picture reader (`strata-vision-hip`) — compiled for AMD RDNA GPUs via HIP/ROCm on Arch Linux.

## Why a separate package

Since Strata 0.2.16 ("own-stack" steps 1–10) the engine links **no ggml, llama.cpp, or mtmd at all**: expert quantization and prompt kernels are Strata's own code (`Strata: no ggml in this build` is what a release configure prints), and the picture reader is its own Qwen vision tower. It shares nothing with `libggml-git-hip` beyond the ROCm toolchain, so it builds here instead of as a split package of that base.

The AUR already has `strata-engine-git`; this package is named `strata-engine-git-hip` and declares `provides`/`conflicts` for `strata-engine`, `strata-engine-git`, `strata-engine-git-ggml-hip` (its former name as a split package of `libggml-git-hip`) and `replaces=('strata-engine-git-ggml-hip')`.

## Patches & Modifications

### Git commit-hash versioning (`strata-version-commit.patch`)

Adds the tag + build-commit stamp to the engine's CMake (the upstream project's own `STRATA_VERSION` define is extended with `STRATA_TAG_VERSION` / `STRATA_BUILD_COMMIT`, read from git) and makes `strata --version` print e.g. `strata version: 0.2.16 (58ee32277)`.

### Strata `CLEAR_CACHE` stdin command (`strata-clear-cache.patch`)

Adds a serve-protocol command to the engine's stdin loop: writing `CLEAR_CACHE` drops all parked conversation slots and trims the heap, answering `CLEARED <n>`. Used as the pre-suspend hook (reclaims host RAM without unloading VRAM weights). Upstream's 0.2.16 SSD tier persists evicted conversations to disk; this command stays complementary — see `strata-spill-plan.md` for the KV-spill design that remains parked.

### Layout note (0.2.16)

Upstream moved its tree to `engine/`, `terminal/`, `app/`. The package installs a read-only copy under `/usr/share/strata`; the launcher (`/usr/bin/strata`) materializes a user-writable app dir at `${STRATA_HOME:-~/.local/share/strata}/app` with symlinks (`terminal/`, `engine/`) plus the built binaries in `app/terminal/engine/`. Old-layout state (pre-0.2.16 app dirs, `Strata-data` next to it) is migrated by symlink on first start.

## Build

```bash
makepkg -si          # builds engine + vision reader for this machine's gfx targets
```

HIP architectures come from `rocm-supported-gfx` (override with `AMDGPU_TARGETS=`); the RDNA whitelist in the PKGBUILD mirrors what Strata's kernels support. Ecosystem-wide update notes for our deployment: see [../libggml-git-hip/CHANGELOG.md](../libggml-git-hip/CHANGELOG.md).
