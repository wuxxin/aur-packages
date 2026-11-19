# Curated changes — Strata update windows for this system

Consumer-facing digest of upstream Strata deltas between two `strata-engine-git-hip` builds, filtered to what is actionable on **this system**: an Arch Linux x86_64 workstation with two AMD RDNA GPUs (gfx1030 + gfx1100), running strata-engine serving a Qwen3.8-Flash-Next MoE (MTP drafter, web chat/agent tooling over `strata serve`). The llama.cpp-suite digest lives in [../libggml-git-hip/CHANGELOG.md](../libggml-git-hip/CHANGELOG.md); complete per-source commit listings for all components (incl. Strata) in [../libggml-git-hip/full-changes.md](../libggml-git-hip/full-changes.md). "This system" means the deployment described above — no hostnames, no personal paths.

Up to 2026-11-18 Strata shipped as the split package `strata-engine-git-ggml-hip` of `libggml-git-hip`; from v0.2.16 it is this standalone package (the engine links no ggml/llama.cpp at all).

## Window: 2026-11-14 → 2026-11-18 (`v0.2.13.1` → `v0.2.15`, built as split package)

| from (installed) | to (built, pending install) |
|---|---|
| v0.2.13.1, engine 0.1.59.1 | **v0.2.15**, Control/Terminal 0.2.14–0.2.15, engines **0.1.60** (`c77572806`), +736 commits (range, no-merges) |

### Breaking / adopt now

- **`CLEAR_CACHE` stays** — split out of the removed spill scaffold into `strata-clear-cache.patch`; the pre-suspend hook works unchanged (drops parked conversations, trims heap, answers `CLEARED <n>`). What is gone: the `--disk-spill*` flags (they never persisted anything; upstream #5697 now releases parked-conversation RAM on eviction and park pools are budget-accounted).
- **CPU expert path changed**: engine 0.1.60 builds the expert pool and DeepSeek/Flash CPU lanes on Strata's own quant layer (`STRATA_OWN_CPU_QUANT`, default ON on x86) — ggml-cpu is out of the pool, bit-exact against it (AVX2/AVX-512-VNNI/Q4_0/Q5/IQ4_NL/MXFP4; NVFP4 scale decode 5× faster). Expect changed CPU-side decode throughput on our dynamic expert offloading; benchmark before/after on upgrade.

### Features worth wiring in

- **Serve/chat**: declared boolean tool arguments accept `True`/`False` (tool-calling agents), stop-without-timeout drains requests, parked-message routing and agent-question notifications fixed; Drafting on/off/auto control per model — our MTP-drafted Flash-Next setup can pin drafting from config instead of environment.
- **Vision**: upstream own Qwen ViT tower (`tools/vision/own`) now has a HIP build; our package built it (`strata_vit_own` linked into `strata-vision`). Upstream default was mtmd — try `--tower own|auto` when testing the multimodal reader.
- **Strix/integrated-GPU arena work** (unregistered expert arena, KFD quiet switches): not applicable to gfx1030/gfx1100 desktop cards; ignore unless a second machine joins.

### Verified in this build

- `strata --version` printed `strata version: 0.2.15 (c77572806)`; the built engine binary contained the `CLEAR_CACHE` handler (`CLEARED %zu`).

## Window: 2026-11-18 → 2026-11-19 (`v0.2.15` → `v0.2.16+4`, split out into this package)

| from (installed) | to (built, pending install) |
|---|---|
| v0.2.15 (`c77572806`) | **v0.2.16+4** (`58ee32277`), Control/Terminal 0.2.16, engines 0.1.61–0.1.62, +609 commits (range, no-merges) |

### Breaking / adopt now

- **Strata 0.2.16 layout move**: the top level is now `app/`, `engine/`, `terminal/`, `docs/`, `tools/` (commit `4058aa782`). Every path our PKGBUILD and patches reference has moved — this build carries the patch/packaging migration. A clone's first run renames old state into `terminal/`; `setup.py --update` now self-updates via git pull.
- **Engine fully leaves llama.cpp** ("own-stack" steps 1–10): the MMQ build path and vendored ggml-cuda are removed, x86 CUDA/HIP builds link no ggml-base/ggml-cpu, quant format headers are Strata's own, docs state "the engine build does not fetch or use llama.cpp". The picture reader `strata-vision` runs without mtmd/llama/ggml (mtmd fallback and the "Picture reader" setting removed; our tower under `auto` on every GPU). Consequence: `strata-system-ggml.patch` deleted, package split out of `libggml-git-hip` into this directory.
- **Conversation cache SSD tier** (#5697 P2): evicted parked conversations are written to disk as session files in the background, matched and read back; one budgeted folder per engine process (dead ones cleaned); a park that cannot fit is refused before anything is evicted, and the RAM gate stops evicting when memory does not come back. This is upstream's answer to our parked `strata-spill-plan.md` — conversation-level persistence, not raw KV bytes; `CLEAR_CACHE` stays ours.
- **Serving API security default**: without an API key, web pages from other origins cannot use `/v1` (Origin check incl. empty Origin and GET /v1). Local browser-based clients must send the key or be same-origin.
- `/v1/models` now reports each model's context window (`meta.n_ctx`, `context_length`) — clients can drop engine-private port probes (#3931, #5893).

### Features worth wiring in

- **HIP on our cards**: RX 6000 (gfx103x) reads prompts with FP16 GEMMs by default and PcieAuto is on by default (#5151, #4007 — measured on gfx103x); the start-up tip asking for `STRATA_HIP_PROMPT_F16=1` is gone on gfx103x. RX 7000 (gfx1100–1102) takes Gyro trellis experts on fused prompt kernels (#6067). Package-side: HIP builds against kpack ROCm carry rocBLAS device code in-package and point the loader at it (#5060); setup finds the HIP compiler under `lib/llvm/bin` (rocm-core 10.1, #6071); engine test-starts only see cards the package has code for (#6015). RX 6600-class (gfx1032) joins the RX 6000 package and setup vocabulary (#5174).
- **Tool-calling robustness** (agents on `strata serve`): full recovery parser family for damaged/malformed tool calls (`#6032 R1–R6`, Claude `<invoke>/<parameter>` dialect, XML-element parameters, `anyOf/oneOf` types, >4 KB streamed string values made linear-time #4686); a reply ending in unrunnable tool markup is retried once and marked `strata_unread_tool_markup`; failed tool calls feed the model a tool error (max twice) instead of dead turns; `/v1/responses` honors `tool_choice: required`, accepts Codex multi-agent v2 items, answers Anthropic-shaped errors, streams usage in its own final chunk on `include_usage`.
- **Drafting**: DFlash2 confidence priced at the pack's real slot size (IQ3_S and above), stock-pack-missing falls back to the tuned pack not to no drafter, explicit `--draft-model` files are kept, DFlash2 downloads honour `HF_ENDPOINT`, drafting decisions follow the config's card family on mixed NVIDIA+AMD machines.
- **Engine ops**: `--expert-support` reports GPU expert-kernel support without a GPU (#6059); `--ple-gguf` recognizes PLE-table-only files (#6026); `STRATA_CKPT_ASYNC` single-owner checkpoint staging; `--prompt-cache-every` checkpoints sit on the resumed request's grid; refused parks counted by reason in `/metrics`; `run-defaults.json` for user-wide launch defaults.

### Verified in this build

- Built standalone at `0.2.16.r4.g58ee322`: `strata --version` prints `strata version: 0.2.16 (58ee32277)`; `ldd` on the engine shows **no libggml/libllama linkage**; the `CLEAR_CACHE` handler strings are present; `/usr/bin/strata`, `/usr/share/strata/{terminal,engine,tools}` install as designed.
- Package split verified: `replaces=('strata-engine-git-ggml-hip')`, provides/conflicts `strata-engine`/`strata-engine-git`; builds clean via `updpkgsums && makepkg -C --nocheck`, zero patch rejects (`strata-system-ggml.patch` deleted as no longer needed).

## How to regenerate this file (next iteration):

Append a new "Window:" section; never rewrite older ones. Procedure:

1. **Baseline pin**: the installed pkgver encodes Strata directly (`0.2.x.rN.gHASH` = tag + N commits + `HASH`); live pins from `strata --version` and `/usr/lib/strata/engine/BUILD.json`.
2. **Fetch**: run `updpkgsums` in this package dir (refreshes the local Strata git mirror). VCS sum stays SKIP.
3. **Range log**: `git -C Strata log --no-merges --date=short --pretty='%h %ad %an: %s' <old-tag-or-hash>..HEAD`. Save to `../scratch/chlog/`; append the complete listing to a "Strata" section in [../libggml-git-hip/full-changes.md](../libggml-git-hip/full-changes.md).
4. **Filter** for this system: `hip|rocm|gfx|amd|kfd`, `serve|launch|engine|prefill|expert|quant|iq[0-9]|mtp|draft|cache|spill|nvme|vision|qwen3|deepseek`; drop `windows|strix|arc|sycl|metal|arm|neon|780m|integrated` noise. Read every surviving line fully — this component is the workload, not a dependency.
5. **Prove**: after building, re-check `strata --version`, `ldd` on the engine (must stay ggml/llama-free), the `CLEAR_CACHE` strings, and any new CLI surface before writing "Verified".
6. Record patch drift fixes in [PKG-CHANGELOG.md](PKG-CHANGELOG.md) (package history), consumer consequences here — keep the two roles separate.
