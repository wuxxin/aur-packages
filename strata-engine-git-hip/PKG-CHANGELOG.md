# Changelog — strata-engine-git-hip

Package-level history for this package. Ecosystem-wide update digests stay in [../libggml-git-hip/CHANGELOG.md](../libggml-git-hip/CHANGELOG.md).

### `0.2.16.r4.g58ee322-1` (Current, built 2026-11-19; not yet installed)
First build as a standalone package; split out of `libggml-git-hip`'s `strata-engine-git-ggml-hip` split package (`replaces=` that name; `provides`/`conflicts`: `strata-engine`, `strata-engine-git`).
- **Why**: Strata 0.2.16 ("own-stack" steps 1–10) links no ggml, llama.cpp, or mtmd — verified: `ldd strata` shows no such libs; a release configure prints `Strata: no ggml in this build`. The picture reader is upstream's self-contained own Qwen tower.
- **pkgver** now derives from the project's own tags (`git describe --tags`: `0.2.16.r4.g58ee322`), not the llama.cpp version of the base package.
- **Layout migration (0.2.16)**: build `-S Strata/engine` (engine) and `-S Strata/terminal/tools/vision` (vision); install to `/usr/share/strata/{terminal,engine,tools}` + compiled binaries under `/usr/lib/strata/engine`; launcher materializes the new app layout (`app/terminal`, `app/engine`) and migrates pre-0.2.16 state by symlink.
- **Removed**: `strata-system-ggml.patch` (system ggml/llama/mtmd linkage, CPU traits shim) — no longer needed; build flags `STRATA_USE_SYSTEM_GGML`/`STRATA_NO_PREFILL_MMQ` dropped.
- **Carried over, reanchored**: `strata-version-commit.patch` (now on `engine/CMakeLists.txt` + `engine/src/program/generate.cpp`; prints e.g. `strata version: 0.2.16 (58ee32277)`), `strata-clear-cache.patch` (`CLEAR_CACHE` stdin command).
- **Verified**: `strata --version` = `0.2.16 (58ee32277)`; no ggml/llama linkage in the engine binary; `CLEAR_CACHE` handler strings present; launcher + app-tree install layout exercised on the pkg tree.

### Provenance
Built as a split package of `libggml-git-hip` from its initial release (`11753.r0.gd8d9297-1`, Strata subpackage added) through `12522.r0.g2cbfc3c-1` (Strata v0.2.15); full history in [../libggml-git-hip/PKG-CHANGELOG.md](../libggml-git-hip/PKG-CHANGELOG.md).
