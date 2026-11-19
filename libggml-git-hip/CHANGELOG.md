# Curated changes — what each update window means for this system

Consumer-facing digest of upstream deltas between two `libggml-git-hip` builds, filtered to what is actionable on **this system**: an Arch Linux x86_64 workstation with two AMD RDNA GPUs (gfx1030 + gfx1100) driven by the HIP backend (Vulkan as fallback), running this package suite as local inference services — whisper/parakeet ASR, qwen3-tts TTS, stable-diffusion image gen, acestep music, llama-server embedding/rerank workloads. The Qwen3.8-Flash-Next MoE engine is Strata, served via `strata serve`; its update windows live in [../strata-engine-git-hip/CHANGELOG.md](../strata-engine-git-hip/CHANGELOG.md). Other mypai infrastructure (service control scripts, benchmarks, docs) should read this file for features to adopt and breaking changes; it deliberately contains no hostnames or personal paths — "this system" means the deployment described above.

## Window: 2026-11-14 → 2026-11-18 (`12383.r1.g3549c27` → `12522.r0.g2cbfc3c`)

Complete per-source commit listings for this window: [full-changes.md](full-changes.md). The sections below are the filtered digest.

Pinned range per component:

| component | from (installed) | to (built, pending install) |
|---|---|---|
| llama.cpp / ggml | `3549c27` (b12383) | `2cbfc3c` (b12522), 138 commits |
| whisper.cpp | pre-1.9.6-dev | `6680804f9`, 1.9.6-dev (llama pin 1.0.0), 110 commits |
| stable-diffusion.cpp | — | v0.3.37 (`532d2c15` opaque-API refactor #2365), 10 commits |
| llama-cpp-python / acestep.cpp | — | 0.3.37 bump + llama pin `a956a852c` (3); 4 commits |
| qwen3-tts.cpp, parakeet.cpp | unchanged upstream | unchanged |

Strata shipped as a split package in this window; its digest: [../strata-engine-git-hip/CHANGELOG.md](../strata-engine-git-hip/CHANGELOG.md).

### Breaking / adopt now

- **stable-diffusion.cpp C API refactor (#2365)**: opaque options/tensors/results. `sd-cli`/`sd-server` are unaffected, but any code linking `libsd` directly (custom tools) must migrate to the new handles. The v0.3.37 shim also calls llama.cpp's now-private `ggml_graph_view`; our `stable-diffusion-graph-view.patch` mirrors it locally — needed as long as we build SD against system ggml.

### Features worth wiring in

- **llama.cpp on our GPUs**: GDN (gated-delta-net) MMA kernel enabled on CDNA (#31327 — Qwen3-Next-family linear attention), MoE regression fix on HIP (#32344), `MUL_MAT_ID` abort with odd src0 columns on AMD fixed (#32385), stream_k tuning for GCN, K/V read-order rotation for L2 hits (#32407). Server: slot scheduler refactor (`server_slot_sched`, #32154), streaming connection-reuse fix (#30492) — relevant to keep-alive clients of llama-server.
- **stable-diffusion.cpp HIP perf** (found by full enumeration, not in the earlier filtered pass): `perf(hip)` INT8 SwiGLU quantization + gated-residual fusion (#2353) and flash-attention/INT8-projection acceleration (#2351), both 2026-11-14 — direct image-gen speedups on our gfx cards; plus upstream ggml-1.0.0 sync (#2354). acestep.cpp: VAE conv1d as implicit GEMM (Metal-oriented, no action for HIP).
- **Model correctness**: `qwen3next` output-projection weight scale applied (#32393), qwen4exp graph-realloc + FP8 checkpoint converter fixes — quality fixes for Qwen3/Next-family serving on all backends.

### Verified in this build

- `libwhisper.so.1.9.6` embeds `1.9.6-dev (6680804f9)`.
- All packages build clean from a wiped cache via `updpkgsums && makepkg -Cf --nocheck` at `12522.r0.g2cbfc3c-1`, zero rejects, including the two new patches and the refreshed ones (Strata split package included then; verified in its changelog).

## Window: 2026-11-18 → 2026-11-19 (`12522.r0.g2cbfc3c` → `12550.r2.g9a080f44b`)

Complete per-source commit listings for this window: [full-changes.md](full-changes.md). The sections below are the filtered digest.

Pinned range per component:

| component | from (installed) | to (built, pending install) |
|---|---|---|
| llama.cpp / ggml | `2cbfc3c` (b12522) | `9a080f44b` (b12550+2), 30 commits |
| whisper.cpp | `6680804f9` | `ca19af244`, 4 commits — CI-only, functionally unchanged |
| stable-diffusion.cpp / llama-cpp-python / acestep.cpp / qwen3-tts.cpp / parakeet.cpp / sdcpp-webui / libwebm | unchanged upstream | unchanged (0 commits) |

Strata v0.2.15 → v0.2.16+4 moved out of this suite in this window; its digest: [../strata-engine-git-hip/CHANGELOG.md](../strata-engine-git-hip/CHANGELOG.md).

### Breaking / adopt now

None on the libggml side.

### Features worth wiring in

- **llama.cpp**: sticky-NaN fix in recurrent state (#31913 — Qwen3-Next-family GDN quality), buffered-I/O fallback on EIO (robust model loading off mounts), IQ2 creation speedup via caching, `PATH_MAX` removal, cpp-httplib 0.67; Vulkan: stream-k MUL_MAT and MMQ with mixed-signness integer dots (fallback-path gains); mtmd voxcpm2 TTS support. No HIP-backend commits this window.
- **whisper.cpp**: CI/version bumps only (`1.9.6-dev` unchanged); no action.

### Verified in this build

Built at `12550.r4.g7fce543` — the llama.cpp mirror moved 2 commits past the analyzed tip `9a080f44b` during packaging; no new HIP-relevant commits in the drift (both were doc/test churn).

- Strata split out of this suite into [../strata-engine-git-hip](../strata-engine-git-hip) (`replaces=('strata-engine-git-ggml-hip')`); its standalone build verification is in that directory's changelog.
- ggml-diag-mask patch (fixed for the upstream SLEEP op, counts 100→102): compiled in — `SLEEP` and `sleep(x)` strings present in `libggml-base.so`.
- All libggml-suite packages build clean via `updpkgsums && makepkg -C --nocheck`, zero patch rejects (strata patches moved out; `strata-system-ggml.patch` deleted as no longer needed).
- The `'CUDA graph capture'` string check from the previous window's plan is N/A for this build: that string lives in `ggml-cuda.cu` and we ship HIP/Vulkan/CPU/BLAS backends.

## How to regenerate this file (next iteration):

Append a new "Window:" section; never rewrite older ones. Procedure:

1. **Baseline pin**: the installed pkgver encodes llama.cpp (`<N>.r<k>.g<hex>` = tag b\<N\> + k commits + `h`); component pins come from embedded versions — `whisper-cli --version`, package install mtimes under `/var/lib/pacman/local/*ggml-hip*/desc`. Strata's own changelog covers its window procedure.
2. **Fetch**: run `updpkgsums` in the package dir (it refreshes the local git mirrors; slow first time). All VCS sums stay SKIP.
3. **Range logs** per mirror: `git -C <mirror> log --oneline <old-pin>..HEAD`; for components without a pin use the exact baseline `base=$(git -C <mirror> rev-list -1 --before=<window-start>T00:00 HEAD)` — a date-filtered `--since` log misses commits merged later. Save to `../scratch/chlog/`.
4. **Full enumeration**: append a new window section to [full-changes.md](full-changes.md) with the complete unfiltered lists (`git log --no-merges --date=short --pretty='%h %ad %an: %s' <range>` per mirror, incl. explicit `0 commits` for untouched components); use its counts in the table above.
5. **Filter** for this system: `hip|rocm|gfx|amd`, `server|prefill|quant|cache|vision|mtmd|qwen3next`, drop `windows|strix|arc|sycl|metal|arm|neon|780m|integrated` noise. Read the surviving lines fully for llama.cpp, and **all** lines of any component with <20 commits (a keyword pass once missed two `perf(hip)` stable-diffusion commits). Summarize per component in the table + three sections (breaking / features / verified).
6. **Prove**: after building, re-check whisper strings, version stamps and any new CLI surface before writing "Verified".
7. Record patch drift fixes in [PKG-CHANGELOG.md](PKG-CHANGELOG.md) (package history), consumer consequences here — keep the two roles separate.
