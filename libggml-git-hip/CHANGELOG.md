# Curated changes — what each update window means for this system

Consumer-facing digest of upstream deltas between two `libggml-git-hip` builds, filtered to what is actionable on **this system**: an Arch Linux x86_64 workstation with two AMD RDNA GPUs (gfx1030 + gfx1100) driven by the HIP backend (Vulkan as fallback), running this package suite as local inference services — strata-engine serving a Qwen3.8-Flash-Next MoE (MTP drafter, web chat/agent tooling over `strata serve`), plus whisper/parakeet ASR, qwen3-tts TTS, stable-diffusion image gen, acestep music, llama-server embedding/rerank workloads. Other mypai infrastructure (service control scripts, benchmarks, docs) should read this file for features to adopt and breaking changes; it deliberately contains no hostnames or personal paths — "this system" means the deployment described above.

## Window: 2026-11-14 → 2026-11-18 (`12383.r1.g3549c27` → `12522.r0.g2cbfc3c`)

Complete per-source commit listings for this window: [full-changes.md](full-changes.md). The sections below are the filtered digest.

Pinned range per component:

| component | from (installed) | to (built, pending install) |
|---|---|---|
| llama.cpp / ggml | `3549c27` (b12383) | `2cbfc3c` (b12522), 138 commits |
| Strata | v0.2.13.1, engine 0.1.59.1 | **v0.2.15**, Control/Terminal 0.2.14–0.2.15, engines **0.1.60** (`c77572806`), +736 commits (range, no-merges) |
| whisper.cpp | pre-1.9.6-dev | `6680804f9`, 1.9.6-dev (llama pin 1.0.0), 110 commits |
| stable-diffusion.cpp | — | v0.3.37 (`532d2c15` opaque-API refactor #2365), 10 commits |
| llama-cpp-python / acestep.cpp | — | 0.3.37 bump + llama pin `a956a852c` (3); 4 commits |
| qwen3-tts.cpp, parakeet.cpp | unchanged upstream | unchanged |

### Breaking / adopt now

- **`CLEAR_CACHE` stays** — split out of the removed spill scaffold into `strata-clear-cache.patch`; the pre-suspend hook works unchanged (drops parked conversations, trims heap, answers `CLEARED <n>`). What is gone: the `--disk-spill*` flags (they never persisted anything; upstream #5697 now releases parked-conversation RAM on eviction and park pools are budget-accounted).
- **Strata CPU expert path changed**: engine 0.1.60 builds the expert pool and DeepSeek/Flash CPU lanes on Strata's own quant layer (`STRATA_OWN_CPU_QUANT`, default ON on x86) — ggml-cpu is out of the pool, bit-exact against it (AVX2/AVX-512-VNNI/Q4_0/Q5/IQ4_NL/MXFP4; NVFP4 scale decode 5× faster). Expect changed CPU-side decode throughput on our dynamic expert offloading; benchmark before/after on upgrade.
- **stable-diffusion.cpp C API refactor (#2365)**: opaque options/tensors/results. `sd-cli`/`sd-server` are unaffected, but any code linking `libsd` directly (custom tools) must migrate to the new handles. The v0.3.37 shim also calls llama.cpp's now-private `ggml_graph_view`; our `stable-diffusion-graph-view.patch` mirrors it locally — needed as long as we build SD against system ggml.

### Features worth wiring in

- **llama.cpp on our GPUs**: GDN (gated-delta-net) MMA kernel enabled on CDNA (#31327 — Qwen3-Next-family linear attention), MoE regression fix on HIP (#32344), `MUL_MAT_ID` abort with odd src0 columns on AMD fixed (#32385), stream_k tuning for GCN, K/V read-order rotation for L2 hits (#32407). Server: slot scheduler refactor (`server_slot_sched`, #32154), streaming connection-reuse fix (#30492) — relevant to keep-alive clients of llama-server.
- **Model correctness**: `qwen3next` output-projection weight scale applied (#32393), qwen4exp graph-realloc + FP8 checkpoint converter fixes — quality fixes for Qwen3/Next-family serving on all backends.
- **Strata serve/chat**: declared boolean tool arguments accept `True`/`False` (tool-calling agents), stop-without-timeout drains requests, parked-message routing and agent-question notifications fixed; Drafting on/off/auto control per model — our MTP-drafted Flash-Next setup can pin drafting from config instead of environment.
- **Strata vision**: upstream own Qwen ViT tower (`tools/vision/own`) now has a HIP build; our package builds it (`strata_vit_own` linked into `strata-vision`). Upstream default remains mtmd — try `--tower own|auto` when testing the multimodal reader.
- **Strix/integrated-GPU arena work** (unregistered expert arena, KFD quiet switches): not applicable to gfx1030/gfx1100 desktop cards; ignore unless a second machine joins.

### Verified in this build

- `strata --version` prints `strata version: 0.2.15 (c77572806)`; the built engine binary contains the `CLEAR_CACHE` handler (`CLEARED %zu`); `libwhisper.so.1.9.6` embeds `1.9.6-dev (6680804f9)`.
- All 9 packages build clean from a wiped cache via `updpkgsums && makepkg -Cf --nocheck` at `12522.r0.g2cbfc3c-1`, zero rejects, including the two new patches and the refreshed ones.

## How to regenerate this file (next iteration)

Append a new "Window:" section; never rewrite older ones. Procedure:

1. **Baseline pin**: the installed pkgver encodes llama.cpp (`<N>.r<k>.g<hex>` = tag b\<N\> + k commits + `h`); component pins come from embedded versions — `/usr/lib/strata/engine/BUILD.json` (Strata), `whisper-cli --version`, package install mtimes under `/var/lib/pacman/local/*ggml-hip*/desc`.
2. **Fetch**: run `updpkgsums` in the package dir (it refreshes the local git mirrors; slow first time). All VCS sums stay SKIP.
3. **Range logs** per mirror: `git -C <mirror> log --oneline <old-pin>..HEAD` (tags when available, e.g. Strata `v0.2.13.1..HEAD`; for components without a pin use the exact baseline `base=$(git -C <mirror> rev-list -1 --before=<window-start>T00:00 HEAD)` — a date-filtered `--since` log misses commits merged later). Save to `../scratch/chlog/`.
4. **Full enumeration**: append a new window section to [full-changes.md](full-changes.md) with the complete unfiltered lists (`git log --no-merges --date=short --pretty='%h %ad %an: %s' <range>` per mirror, incl. explicit `0 commits` for untouched components); use its counts in the table above.
5. **Filter** for this system: `hip|rocm|gfx|amd|kfd`, `serve|launch|engine|prefill|expert|quant|iq[0-9]|mtp|draft|cache|spill|nvme|vision|qwen3next|deepseek`, drop `windows|strix|arc|sycl|metal|arm|neon|780m|integrated` noise. Read the surviving lines fully for Strata and llama.cpp; summarize per component in the table + three sections (breaking / features / verified).
6. **Prove**: after building, re-check `strata --version`, whisper strings, and any new CLI surface before writing "Verified".
7. Record patch drift fixes in [PKG-CHANGELOG.md](PKG-CHANGELOG.md) (package history), consumer consequences here — keep the two roles separate.
