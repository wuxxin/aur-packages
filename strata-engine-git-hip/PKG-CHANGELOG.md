# Changelog — strata-engine-git-hip

Package-level history for this package. Ecosystem-wide update digests stay in [../libggml-git-hip/CHANGELOG.md](../libggml-git-hip/CHANGELOG.md).

### `0.2.21.1.r0.g2af30cc-1` (Current, built 2026-11-25; pending install)
Upstream `v0.2.21.1` (Control `0.1.68`, engines `0.1.67`, +770 commits over `0.2.16.r4.g58ee322`).
- **Expanded build targets (B1):** now builds and installs `strata`, `strata-q36`, `strata-inkling` (`-DSTRATA_BUILD_INKLING=ON -DSTRATA_BUILD_INKLING2=ON`), `strata-hy4` (`-DSTRATA_BUILD_HY4=ON`, added `'zstd'` to `depends`), CPU fallback `strata-vision` alongside GPU `strata-vision-hip` (replaces symlink), and CLI tools (`strata-gguf`, `strata-dequant`, `strata-plan`). `/usr/bin/strata` symlinks all shipped binaries into `$app/terminal/engine/`; `BUILD.json` records `vision_cpu` and `vision_gpu`.
- **Upgraded `strata-clear-cache.patch`:** re-anchored to `v0.2.21.1` and upgraded from drop-only (`conversations.clear()`) to **spill-then-clear** (`while (conversations.evict_oldest())` → `spill_writer->wait_idle()` → `spill_reclaim()` → `conversations.clear()` → `pools_budget.shrink()` → `release_free_heap()`), so idle/pre-suspend RAM reclamation flushes parked conversations to `--conversation-spill-persist` instead of discarding them.
- **Re-anchored `strata-version-commit.patch`:** zero-offset clean apply on `engine/CMakeLists.txt` + `engine/src/program/generate.cpp`.
- **PKGBUILD hygiene:** removed redundant `'python'` from `makedepends` (`namcap PKGBUILD` now reports 0 warnings/errors).
- **Verified:** `strata --version` = `0.2.21.1 (2af30ccaa)`, `--expert-support 22,20,2560,640` = `supported`, `strata-hy4`/`strata-inkling` = `0.1.67`, zero `libggml`/`libllama` linkage, `CLEAR_CACHE` spill-then-clear strings present, `namcap` clean, `.SRCINFO` regenerated.

### `0.2.16.r4.g58ee322-1` (Installed 2026-11-19)
First build as a standalone package; split out of `libggml-git-hip`'s `strata-engine-git-ggml-hip` split package (`replaces=` that name; `provides`/`conflicts`: `strata-engine`, `strata-engine-git`).
- **Why**: Strata 0.2.16 ("own-stack" steps 1–10) links no ggml, llama.cpp, or mtmd — verified: `ldd strata` shows no such libs; a release configure prints `Strata: no ggml in this build`. The picture reader is upstream's self-contained own Qwen tower.
- **pkgver** now derives from the project's own tags (`git describe --tags`: `0.2.16.r4.g58ee322`), not the llama.cpp version of the base package.
- **Layout migration (0.2.16)**: build `-S Strata/engine` (engine) and `-S Strata/terminal/tools/vision` (vision); install to `/usr/share/strata/{terminal,engine,tools}` + compiled binaries under `/usr/lib/strata/engine`; launcher materializes the new app layout (`app/terminal`, `app/engine`) and migrates pre-0.2.16 state by symlink.
- **Removed**: `strata-system-ggml.patch` (system ggml/llama/mtmd linkage, CPU traits shim) — no longer needed; build flags `STRATA_USE_SYSTEM_GGML`/`STRATA_NO_PREFILL_MMQ` dropped.
- **Carried over, reanchored**: `strata-version-commit.patch` (now on `engine/CMakeLists.txt` + `engine/src/program/generate.cpp`; prints e.g. `strata version: 0.2.16 (58ee32277)`), `strata-clear-cache.patch` (`CLEAR_CACHE` stdin command).
- **Verified**: `strata --version` = `0.2.16 (58ee32277)`; no ggml/llama linkage in the engine binary; `CLEAR_CACHE` handler strings present; launcher + app-tree install layout exercised on the pkg tree.

### Provenance
Built as a split package of `libggml-git-hip` from its initial release (`11753.r0.gd8d9297-1`, Strata subpackage added) through `12522.r0.g2cbfc3c-1` (Strata v0.2.15); full history in [../libggml-git-hip/PKG-CHANGELOG.md](../libggml-git-hip/PKG-CHANGELOG.md).
