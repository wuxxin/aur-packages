# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Last 7 Days Activity (August 02, 2026 – August 09, 2026)

<!-- START_TABLES -->
### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **oh-my-pi** | [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) | 23,171 | 2,199 | `main` | 2026-08-09 | **503** | 192 | 9 | 759.2 | ` v17.2.10`, ` v17.2.11` | `17.2.10.r120.g39477ba-1` (ref `39477ba`) | 71 | **Highly Active** |
| **llama.cpp** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 123,175 | 21,477 | `master` | 2026-08-09 | **106** | 0 | 81 | 89.2 | ` b10228`, ` b10229` | `10154.r0.g0e4a036-1` (ref `0e4a036`) | 179 | **Highly Active** |
| *└─ llama-cpp-python* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,537 | 1,444 | `main` | 2026-07-11 | 0 | 0 | 0 | 0.0 | — | `10154.r0.g0e4a036-1` (ref `629bd1b`) | 0 | **Stale** |
| *└─ stable-diffusion.cpp* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,693 | 727 | `master` | 2026-08-06 | **4** | 0 | 3 | 9.8 | ` master-811-b4e67d1`, ` master-812-ea7f0c8` | `10154.r0.g0e4a036-1` (ref `2251699`) | 16 | **Active** |
| *└─ whisper.cpp* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 52,728 | 6,043 | `master` | 2026-08-07 | **50** | 0 | 1 | 13.5 | ` v1.9.2` | `10154.r0.g0e4a036-1` (ref `080bbbe`) | 54 | **Active** |
| *└─ qwen3-tts.cpp* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) | 17 | 5 | `main` | 2026-06-16 | 0 | 0 | 0 | 0.0 | — | `10154.r0.g0e4a036-1` (ref `0c8b2ba`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 226 | 82 | `main` | 2026-07-18 | 0 | 0 | 0 | 0.2 | — | not installed | - | **Stale** |
| **bitsandbytes** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 0 | 0 | `main` | 2026-07-29 | 0 | 0 | 0 | 5.5 | — | `0.50.0.r5.ga2b90e6e-1` (ref `a2b90e6e`) | 0 | **Stale** |
| **infinity_emb** | [michaelfeil/infinity](https://github.com/michaelfeil/infinity) | 0 | 0 | `main` | 2026-03-23 | 0 | 0 | 0 | 0.0 | — | `0.0.75-2` (ref `0.0.75`) | 45 | **Stale** |
| **pockettts.cpp** | [VolgaGerm/PocketTTS.cpp](https://github.com/VolgaGerm/PocketTTS.cpp) | 0 | 0 | `master` | 2026-03-29 | 0 | 0 | 0 | 0.0 | — | `0.1.0.r18.ge801e7d-1` (ref `e801e7d`) | 0 | **Stale** |
| **pocket-tts** | [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 0 | 0 | `main` | 2026-07-16 | 0 | 0 | 0 | 0.2 | — | `2.1.0-1` (ref `v2.1.0`) | 7 | **Stale** |

> [!NOTE]
> `bitsandbytes`, `pocket-tts`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 0 | 0 | `master` | 2026-08-01 | 0 | 0 | 0 | 2.2 | — | `0.100.r2.gfe9df01-1` (ref `fe9df01`) | 12 | **Stale** |

> [!NOTE]
> `zeroclaw-git` (upstream: [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)) > `ironclaw-git` (upstream: [nearai/ironclaw](https://github.com/nearai/ironclaw)) are hosted and tracked separately under the `agents-shared` repository.
<!-- END_TABLES -->

---

## 🔍 Repository Focus & Developments

### oh-my-pi (`can1357/oh-my-pi`)
<!-- START_BD_OH_MY_PI -->
* **Status**: Highly Active (503 commits, 9 tags/releases in the last week). **71 commits since installed 17.2.10.r120.g39477ba-1 (ref `39477ba`).**
<!-- END_BD_OH_MY_PI -->
<!-- START_RF_OH_MY_PI -->
* **Recent Focus**:
  - `45e12e5bb` test(mnemopi): awaited detached shared-bank flush in lock-wait test
  - `311c32eaf` fix(natives): repaired win32 build and bazel feature drift
  - `896bf5f33` fix(natives): repaired linux pi-builtins release build
  - `6fb07028f` chore: bump version to 17.2.12
  - `60d4cb997` test(catalog): pinned copilot grok-4.5 migration to the responses route
  - `bf04fbfc8` fix(catalog): routed opencode-go deepseek-v4-flash through the responses api
  - `d85dde52c` fix(session): fence in-flight disk work behind the terminal seal
  - `22b5ccd97` test(coding-agent): assert exact transcript contents in seal regression
  - `63aa8cf6f` fix(session): seal the manager at terminal release against revival races
  - `31d765547` fix(agent): re-finalize dispose after the drain deadline
  - `b9ddc81f0` test(coding-agent): assert dispose-persisted state from the reopened file
  - `cab4c4520` test(coding-agent): reopen persisted session after terminal dispose
  - `a85e23d15` chore(changelog): normalized unreleased spacing after merges
  - `3cf1e42a0` fix(tui): preserve unbraced math continuations
  - `b2d0ade66` fix(agent): finish session disposal after event drain
  - `ac55ea769` fix(catalog): toggle qwen3.8 max thinking on wire
  - `7ca140f66` fix(ai): routed policy-rejected accounts through sibling rotation
  - `abf80e4f7` feat(hashline): secured boundary repairs with parse checks and added warnings
  - `506f57fbf` fix(task): recorded subagent model performance
  - `c0eda613c` fix(catalog): kept qwen3.8 max preview on enable_thinking
  - `4d2c6e37f` fix(catalog): preserved token plan preview vision
  - `155fdaedb` fix(catalog): corrected qwen3.8 max discovery metadata
  - `731c05173` feat(pi-shell/minimizer): implemented length threshold and empty preservation
  - `a30cbbb75` feat(hashline): implemented syntax validation and veto checks for patch application
  - `2728675ba` docs: documented provider compatibility flags and specific quirks
  - `a6aa462a6` fix(tui): bounded WSL idle animation CPU
  - `88021b90e` fix(agent): drained in-flight session event handlers on dispose
  - `a7a32f35d` fix(agent): settled active turn before clearing session memory
  - `4ca6c376b` fix(agent): detached append-only context on dispose
  - `ed6300b35` fix(agent): release parked subagent session memory on dispose
  - `a709a6604` fix(web-search): parsed double-encoded zai results
  - `fe8651226` fix(tui): parsed spaced nested command arguments
  - `7914e7c45` fix(session): preserved harness handoff abort reasons
  - `9757a7b16` fix(tui): preserved outer arity through command arguments
  - `d1eafe7a6` feat(pi-builtins): prevented kill builtin from targeting ancestor processes
  - `2504800a4` fix(tui): only suppress a math row break when a command owes an argument
  - `0f7e37900` fix(tui): keep display-math fractions intact across source newlines
  - `92e574cb0` fix(session): surface empty handoff generation as failure not cancel
  - `2ee994356` refactor: unify builtins in one place
  - `08819b279` ci(test): budgeted bun test parallelism across the chunk pool
  - `7cebe901b` refactor(coding-agent): narrowed over-exported internal symbols
  - `cd4e04e8e` refactor(coding-agent): reduced lsp index to a composition barrel
  - `0f3e45f07` refactor(coding-agent): extracted model registry helper modules
  - `e0ec404de` refactor(coding-agent): split theme module by responsibility
  - `0697e7f68` refactor(coding-agent): split secret obfuscator into domain modules
  - `cafe52cd9` refactor(coding-agent): split github tool into domain modules
  - `7454b6e78` refactor(coding-agent): split read tool into per-source modules
  - `8cf3dce6f` refactor(coding-agent): split builtin slash commands by domain
  - `71af89cba` refactor(coding-agent): extracted generic kernel session registry
  - `c80a53122` refactor(catalog): deduplicated openai-compatible manager builders
  - `2efbdeaab` refactor(ai): deduplicated usage provider coercion helpers
  - `5fa578fa3` refactor(ai): migrated hand-rolled api-key logins to shared factory
  - `a0efb56b6` feat: cleanup command
  - `4dc97f89a` fix(natives): backticked RemoteDesktop in portal doc comments
  - `81e0c3f6b` fix(voice): dropped redundant pub(crate) in private device module
  - `055a5d4f2` chore: bump version to 17.2.11
  - `7cae7ef3f` feat(voice): replaced miniaudio with native platform audio backends
  - `bc5eee4e2` fix(build): activated zune-jpeg log feature and widened test compat type - zune-jpeg 0.5.15 (image 0.25's JPEG decoder) cannot compile with its   non-default log feature off: zune-core's no-log warn! stub is not   expression-safe. A feature-activation-only workspace dep on   zune-jpeg { features = ["log"] } fixes the cold build; log stays 0.4.33. - model-registry-default-config's local ModelSnapshot type gains the optional   streamIdleTimeoutMs the Bedrock watchdog compat now emits.
  - `34af136c6` test(utils): dropped flaky concurrent logger rotation test - The two-child fs.watch/poll choreography deadlocked under parallel test load   (runner killed a dangling probe); the PID-namespace pruning test still covers   the multiprocess audit/rotation file contract.
  - `a9dcf0f8d` chore: update changelogs
  - `38b61ae34` fix(session): honored explicit retry-after over reason backoff - A provider-supplied retry-after now bypasses the transient rate/concurrency   heuristic window instead of being overridden by it (regression from the   subscription-cap retry change). - Updated event-controller/ui-helpers test doubles for provenance-gated   renderer selection (hasBuiltInTool), aggregated retryErrors on   auto_retry_end, and Bedrock override compat gaining streamIdleTimeoutMs.
  - `5b3bed18b` fix(launch): accepted empty daemon regex matches
  - `a09dfd0ba` fix(extensions): restored provider unregistration
  - `336975c46` fix(mnemopi): recover from partially-extracted embedding model cache
  - `216fc3ca2` fix(computer): waited for all granted libei devices
  - `4981eba1c` fix(task): refreshed agent definitions without restart
  - `7d4b2e799` fix(agent): re-check context on cooldown-expiry revert in auto-continue path
  - `2567db01d` fix(computer): removed orphaned wayland remote-desktop token
  - `539906e25` fix(computer): bounded consent-denied portal close inline
  - `1865afb7c` fix(hashline): recovered pipe-numbered read rows
  - `1e6638d8c` fix(session): surfaced real handoff errors instead of false cancel
<!-- END_RF_OH_MY_PI -->

### llama.cpp (`ggml-org/llama.cpp`)
<!-- START_BD_LLAMA_CPP -->
* **Status**: Highly Active (106 commits, 81 tags/releases in the last week). **179 commits since installed 10154.r0.g0e4a036-1 (ref `0e4a036`).**
<!-- END_BD_LLAMA_CPP -->
<!-- START_RF_LLAMA_CPP -->
* **Recent Focus**:
  - `08659901` ggml-cpu : fix missing Q5_0 dispatch in SpaceMiT backend (#26792)
  - `61141f14` ci: rm 'GGML_HIP_ROCWMMA_FATTN' (#26760)
  - `7ba604f1` server: report the isolate working directory from get_info (#26773)
  - `687e7789` CUDA: fuse rms_norm + mul + rope (+ view + set_rows) (#26767)
  - `18f7ad7f` server, ui: only offer a working directory when a tool reads it (#26762)
  - `dd2c7c44` server: add initial tool isolation support (via docker) (#26507)
  - `69bf6437` CUDA: fix thread/block count in quantized cpy kernel launches (#26731)
  - `3653e6d6` tts: account for the vocoder pass in the timings line (#26733)
  - `fc6545d3` allozaur/feat/chat form contenteditable (#26717)
  - `1621a3d3` tests : speed-up server test suite 3x (#26734)
  - `6de1b634` allozaur/feat/chat slash commands (#26716)
  - `f8e30266` sycl: coalesce the ssm_conv window loads (#26612)
  - `a194a75b` metal : fix NORM/RMS_NORM for row lengths that leave a partial simdgroup (#26708)
  - `23634783` ui: Filesystem '@mentions' for Chat Form (#26715)
  - `4cb22cd5` mtmd: fix longest_edge ignoring min/max pixels (#26638)
<!-- END_RF_LLAMA_CPP -->

### llama-cpp-python (`abetlen/llama-cpp-python`)
<!-- START_BD_LLAMA_CPP_PYTHON -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 10154.r0.g0e4a036-1 (ref `629bd1b`).**
<!-- END_BD_LLAMA_CPP_PYTHON -->
<!-- START_RF_LLAMA_CPP_PYTHON -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_LLAMA_CPP_PYTHON -->

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
<!-- START_BD_STABLE_DIFFUSION_CPP -->
* **Status**: Active (4 commits, 3 tags/releases in the last week). **16 commits since installed 10154.r0.g0e4a036-1 (ref `2251699`).**
<!-- END_BD_STABLE_DIFFUSION_CPP -->
<!-- START_RF_STABLE_DIFFUSION_CPP -->
* **Recent Focus**:
  - `c6beeef` fix: map Qwen3-VL DeepStack GGUF tensor names (#1858)
  - `bfbef5b` feat: trained Minimax VAE Latent2rgb proj (#1856)
  - `ea7f0c8` feat: add minimax-h3 support (#1854)
  - `b4e67d1` fix(cmake): only apply /MP to the MSVC compiler, not icx (#1846)
<!-- END_RF_STABLE_DIFFUSION_CPP -->

### whisper.cpp (`ggerganov/whisper.cpp`)
<!-- START_BD_WHISPER_CPP -->
* **Status**: Active (50 commits, 1 tag/release in the last week). **54 commits since installed 10154.r0.g0e4a036-1 (ref `080bbbe`).**
<!-- END_BD_WHISPER_CPP -->
<!-- START_RF_WHISPER_CPP -->
* **Recent Focus**:
  - `592feef0` talk-llama : sync llama.cpp
  - `87704926` sync : ggml
  - `84cdcad3` ggml : bump version to 0.19.0 (ggml/1581)
  - `8587ad3b` ggml : add aarch64 HWCAP fallbacks and fix fp16 variant detection (llama/25554)
  - `56cb1547` sycl: fix UE4M3 parsing (llama/25608)
  - `077c5d42` sycl: *glu flat path (llama/26354)
  - `9faa9ee7` sycl : Support DSv4 OPs: LIGHTNING_INDEXER,DSV4_HC_COMB,DSV4_HC_POST,DSV4_HC_PRE (llama/26568)
  - `fb9e8ca9` sycl : fix error Error OP FLASH_ATTN_EXT on arc770 (llama/26441)
  - `89d45afe` sycl : enhance OP set_rows to support all missed data types (llama/26515)
  - `79ab70c9` cuda: fix warnings for unused variable/function (llama/26688)
  - `56933786` metal : avoid 'threadgroup' matrix array instantiation in kernel_lightning_indexer (llama/26646)
  - `69bd0a9a` ci : onboard AMD ROCm CI with gfx1151 fixes (llama/26544)
  - `5a80d0ad` vulkan: fix submission batching size, add debug tools for diagnosing causes of DeviceLost drivers errors (llama/26371)
  - `60894f1e` mtmd/ggml: add ggml_build_forward_order (llama/26649)
  - `87310219` vulkan backend ops: implemented GATED_LINEAR_ATTN (llama/25601)
<!-- END_RF_WHISPER_CPP -->

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Downstream Fork**:
<!-- START_BD_QWEN3_TTS_CPP -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 10154.r0.g0e4a036-1 (ref `0c8b2ba`).**
<!-- END_BD_QWEN3_TTS_CPP -->
<!-- START_RF_QWEN3_TTS_CPP -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_QWEN3_TTS_CPP -->

* **Upstream Origin**:
<!-- START_BD_QWEN3_TTS_UPSTREAM -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week).
<!-- END_BD_QWEN3_TTS_UPSTREAM -->
<!-- START_RF_QWEN3_TTS_UPSTREAM -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_QWEN3_TTS_UPSTREAM -->

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
<!-- START_BD_BITSANDBYTES -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 0.50.0.r5.ga2b90e6e-1 (ref `a2b90e6e`).**
<!-- END_BD_BITSANDBYTES -->
<!-- START_RF_BITSANDBYTES -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_BITSANDBYTES -->

### infinity_emb (`michaelfeil/infinity`)
<!-- START_BD_INFINITY_EMB -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **45 commits since installed 0.0.75-2 (ref `0.0.75`).**
<!-- END_BD_INFINITY_EMB -->
<!-- START_RF_INFINITY_EMB -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_INFINITY_EMB -->

### PocketTTS.cpp (`VolgaGerm/PocketTTS.cpp` & `kyutai-labs/pocket-tts`)
* **PocketTTS C++ Wrapper**:
<!-- START_BD_POCKETTTS_CPP -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 0.1.0.r18.ge801e7d-1 (ref `e801e7d`).**
<!-- END_BD_POCKETTTS_CPP -->
<!-- START_RF_POCKETTTS_CPP -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_POCKETTTS_CPP -->

* **PocketTTS Python Bindings**:
<!-- START_BD_POCKET_TTS -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **7 commits since installed 2.1.0-1 (ref `v2.1.0`).**
<!-- END_BD_POCKET_TTS -->
<!-- START_RF_POCKET_TTS -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_POCKET_TTS -->

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
<!-- START_BD_SIGNAL_CLI_REST_API -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **12 commits since installed 0.100.r2.gfe9df01-1 (ref `fe9df01`).**
<!-- END_BD_SIGNAL_CLI_REST_API -->
<!-- START_RF_SIGNAL_CLI_REST_API -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_SIGNAL_CLI_REST_API -->

### Custom AUR Repository Updates
* **Recent Focus**:


---

## 📋 Instruction Guide: Recreating this Analysis

**Fully Automated Update**: You can run the automation script `scripts/update-activity.py` with the `--write` (or `-w`) flag to automatically pull all repository updates, calculate the statistics, and optionally write the updated tables directly back into this file:
```bash
python scripts/update-activity.py [--write]
```
