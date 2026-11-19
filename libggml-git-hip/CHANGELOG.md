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
- **stable-diffusion.cpp HIP perf** (found by full enumeration, not in the earlier filtered pass): `perf(hip)` INT8 SwiGLU quantization + gated-residual fusion (#2353) and flash-attention/INT8-projection acceleration (#2351), both 2026-11-14 — direct image-gen speedups on our gfx cards; plus upstream ggml-1.0.0 sync (#2354). acestep.cpp: VAE conv1d as implicit GEMM (Metal-oriented, no action for HIP).
- **Model correctness**: `qwen3next` output-projection weight scale applied (#32393), qwen4exp graph-realloc + FP8 checkpoint converter fixes — quality fixes for Qwen3/Next-family serving on all backends.
- **Strata serve/chat**: declared boolean tool arguments accept `True`/`False` (tool-calling agents), stop-without-timeout drains requests, parked-message routing and agent-question notifications fixed; Drafting on/off/auto control per model — our MTP-drafted Flash-Next setup can pin drafting from config instead of environment.
- **Strata vision**: upstream own Qwen ViT tower (`tools/vision/own`) now has a HIP build; our package builds it (`strata_vit_own` linked into `strata-vision`). Upstream default remains mtmd — try `--tower own|auto` when testing the multimodal reader.
- **Strix/integrated-GPU arena work** (unregistered expert arena, KFD quiet switches): not applicable to gfx1030/gfx1100 desktop cards; ignore unless a second machine joins.

### Verified in this build

- `strata --version` prints `strata version: 0.2.15 (c77572806)`; the built engine binary contains the `CLEAR_CACHE` handler (`CLEARED %zu`); `libwhisper.so.1.9.6` embeds `1.9.6-dev (6680804f9)`.
- All 9 packages build clean from a wiped cache via `updpkgsums && makepkg -Cf --nocheck` at `12522.r0.g2cbfc3c-1`, zero rejects, including the two new patches and the refreshed ones.

## Window: 2026-11-18 → 2026-11-19 (`12522.r0.g2cbfc3c` → `12550.r2.g9a080f44b`)

Complete per-source commit listings for this window: [full-changes.md](full-changes.md). The sections below are the filtered digest.

Pinned range per component:

| component | from (installed) | to (built, pending install) |
|---|---|---|
| llama.cpp / ggml | `2cbfc3c` (b12522) | `9a080f44b` (b12550+2), 30 commits |
| Strata | v0.2.15 (`c77572806`) | **v0.2.16+4** (`58ee32277`), Control/Terminal 0.2.16, engines 0.1.61–0.1.62, +609 commits (range, no-merges) |
| whisper.cpp | `6680804f9` | `ca19af244`, 4 commits — CI-only, functionally unchanged |
| stable-diffusion.cpp / llama-cpp-python / acestep.cpp / qwen3-tts.cpp / parakeet.cpp / sdcpp-webui / libwebm | unchanged upstream | unchanged (0 commits) |

### Breaking / adopt now

- **Strata 0.2.16 layout move**: the top level is now `app/`, `engine/`, `terminal/`, `docs/`, `tools/` (commit `4058aa782`). Every path our PKGBUILD and patches reference has moved — this build carries the patch/packaging migration. A clone's first run renames old state into `terminal/`; `setup.py --update` now self-updates via git pull.
- **Strata engine fully leaves llama.cpp** ("own-stack" steps 1–10): the MMQ build path and vendored ggml-cuda are removed, x86 CUDA/HIP builds link no ggml-base/ggml-cpu, quant format headers are Strata's own, docs state "the engine build does not fetch or use llama.cpp". The picture reader `strata-vision` runs without mtmd/llama/ggml (mtmd fallback and the "Picture reader" setting removed; our tower under `auto` on every GPU). Our `strata-system-ggml.patch` shrinks to what still links system libs — verified per build below.
- **Conversation cache SSD tier** (#5697 P2): evicted parked conversations are written to disk as session files in the background, matched and read back; one budgeted folder per engine process (dead ones cleaned); a park that cannot fit is refused before anything is evicted, and the RAM gate stops evicting when memory does not come back. This is upstream's answer to our parked `strata-spill-plan.md` — conversation-level persistence, not raw KV bytes; `CLEAR_CACHE` stays ours.
- **Serving API security default**: without an API key, web pages from other origins cannot use `/v1` (Origin check incl. empty Origin and GET /v1). Local browser-based clients must send the key or be same-origin.
- `/v1/models` now reports each model's context window (`meta.n_ctx`, `context_length`) — clients can drop engine-private port probes (#3931, #5893).

### Features worth wiring in

- **HIP on our cards**: RX 6000 (gfx103x) reads prompts with FP16 GEMMs by default and PcieAuto is on by default (#5151, #4007 — measured on gfx103x); the start-up tip asking for `STRATA_HIP_PROMPT_F16=1` is gone on gfx103x. RX 7000 (gfx1100–1102) takes Gyro trellis experts on fused prompt kernels (#6067). Package-side: HIP builds against kpack ROCm carry rocBLAS device code in-package and point the loader at it (#5060); setup finds the HIP compiler under `lib/llvm/bin` (rocm-core 10.1, #6071); engine test-starts only see cards the package has code for (#6015). RX 6600-class (gfx1032) joins the RX 6000 package and setup vocabulary (#5174).
- **Tool-calling robustness** (agents on `strata serve`): full recovery parser family for damaged/malformed tool calls (`#6032 R1–R6`, Claude `<invoke>/<parameter>` dialect, XML-element parameters, `anyOf/oneOf` types, >4 KB streamed string values made linear-time #4686); a reply ending in unrunnable tool markup is retried once and marked `strata_unread_tool_markup`; failed tool calls feed the model a tool error (max twice) instead of dead turns; `/v1/responses` honors `tool_choice: required`, accepts Codex multi-agent v2 items, answers Anthropic-shaped errors, streams usage in its own final chunk on `include_usage`.
- **Drafting**: DFlash2 confidence priced at the pack's real slot size (IQ3_S and above), stock-pack-missing falls back to the tuned pack not to no drafter, explicit `--draft-model` files are kept, DFlash2 downloads honour `HF_ENDPOINT`, drafting decisions follow the config's card family on mixed NVIDIA+AMD machines.
- **Engine ops**: `--expert-support` reports GPU expert-kernel support without a GPU (#6059); `--ple-gguf` recognizes PLE-table-only files (#6026); `STRATA_CKPT_ASYNC` single-owner checkpoint staging; `--prompt-cache-every` checkpoints sit on the resumed request's grid; refused parks counted by reason in `/metrics`; `run-defaults.json` for user-wide launch defaults.
- **llama.cpp**: sticky-NaN fix in recurrent state (#31913 — Qwen3-Next-family GDN quality), buffered-I/O fallback on EIO (robust model loading off mounts), IQ2 creation speedup via caching, `PATH_MAX` removal, cpp-httplib 0.67; Vulkan: stream-k MUL_MAT and MMQ with mixed-signness integer dots (fallback-path gains); mtmd voxcpm2 TTS support. No HIP-backend commits this window.
- **whisper.cpp**: CI/version bumps only (`1.9.6-dev` unchanged); no action.

### Verified in this build

Built at `12550.r4.g7fce543` — the llama.cpp mirror moved 2 commits past the analyzed tip `9a080f44b` during packaging; no new HIP-relevant commits in the drift (both were doc/test churn).

- Strata split into its own package dir [../strata-engine-git-hip](../strata-engine-git-hip) (`strata-engine-git-hip`, provides/conflicts `strata-engine`/`strata-engine-git`, replaces `strata-engine-git-ggml-hip`). Built standalone at `0.2.16.r4.g58ee322`: `strata --version` prints `strata version: 0.2.16 (58ee32277)`; `ldd` on the engine shows **no libggml/libllama linkage**; the `CLEAR_CACHE` handler strings are present; `/usr/bin/strata`, `/usr/share/strata/{terminal,engine,tools}` install as designed.
- ggml-diag-mask patch (fixed for the upstream SLEEP op, counts 100→102): compiled in — `SLEEP` and `sleep(x)` strings present in `libggml-base.so`.
- All libggml-suite packages build clean via `updpkgsums && makepkg -C --nocheck`, zero patch rejects (strata patches moved out; `strata-system-ggml.patch` deleted as no longer needed).
- The `'CUDA graph capture'` string check from the previous window's plan is N/A for this build: that string lives in `ggml-cuda.cu` and we ship HIP/Vulkan/CPU/BLAS backends.

## How to regenerate this file (next iteration):

Append a new "Window:" section; never rewrite older ones. Procedure:

1. **Baseline pin**: the installed pkgver encodes llama.cpp (`<N>.r<k>.g<hex>` = tag b\<N\> + k commits + `h`); component pins come from embedded versions — `/usr/lib/strata/engine/BUILD.json` (Strata), `whisper-cli --version`, package install mtimes under `/var/lib/pacman/local/*ggml-hip*/desc`.
2. **Fetch**: run `updpkgsums` in the package dir (it refreshes the local git mirrors; slow first time). All VCS sums stay SKIP.
3. **Range logs** per mirror: `git -C <mirror> log --oneline <old-pin>..HEAD` (tags when available, e.g. Strata `v0.2.13.1..HEAD`; for components without a pin use the exact baseline `base=$(git -C <mirror> rev-list -1 --before=<window-start>T00:00 HEAD)` — a date-filtered `--since` log misses commits merged later). Save to `../scratch/chlog/`.
4. **Full enumeration**: append a new window section to [full-changes.md](full-changes.md) with the complete unfiltered lists (`git log --no-merges --date=short --pretty='%h %ad %an: %s' <range>` per mirror, incl. explicit `0 commits` for untouched components); use its counts in the table above.
5. **Filter** for this system: `hip|rocm|gfx|amd|kfd`, `serve|launch|engine|prefill|expert|quant|iq[0-9]|mtp|draft|cache|spill|nvme|vision|qwen3next|deepseek`, drop `windows|strix|arc|sycl|metal|arm|neon|780m|integrated` noise. Read the surviving lines fully for Strata and llama.cpp, and **all** lines of any component with <20 commits (a keyword pass once missed two `perf(hip)` stable-diffusion commits). Summarize per component in the table + three sections (breaking / features / verified).
6. **Prove**: after building, re-check `strata --version`, whisper strings, and any new CLI surface before writing "Verified".
7. Record patch drift fixes in [PKG-CHANGELOG.md](PKG-CHANGELOG.md) (package history), consumer consequences here — keep the two roles separate.
