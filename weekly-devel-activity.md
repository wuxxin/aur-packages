# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Last 7 Days Activity (June 22, 2026 – June 29, 2026)

<!-- START_TABLES -->
### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **llama.cpp** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 118,595 | 20,059 | `master` | 2026-06-29 | **81** | 0 | 51 | 95.2 | ` b9763`, ` b9765` | `9842.r0.g6f4f53f-1` (ref `6f4f53f`) | 0 | **Highly Active** |
| *└─ llama-cpp-python* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,447 | 1,423 | `main` | 2026-06-28 | **4** | 0 | 14 | 17.8 | ` v0.3.32`, ` v0.3.32-cu118` | `9842.r0.g6f4f53f-1` (ref `346853c`) | 0 | **Active** |
| *└─ stable-diffusion.cpp* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,400 | 681 | `master` | 2026-06-30 | **18** | 0 | 8 | 17.8 | ` master-720-2938272`, ` master-721-8caa3f9` | `9842.r0.g6f4f53f-1` (ref `3b6c9ca`) | 0 | **Active** |
| *└─ whisper.cpp* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 51,139 | 5,707 | `master` | 2026-06-26 | **33** | 0 | 0 | 40.8 | — | `9842.r0.g6f4f53f-1` (ref `0ae02cd`) | 0 | **Active** |
| *└─ qwen3-tts.cpp* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) | 16 | 6 | `main` | 2026-06-16 | 0 | 0 | 0 | 0.2 | — | `9842.r0.g6f4f53f-1` (ref `0c8b2ba`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 211 | 76 | `main` | 2026-06-03 | 0 | 0 | 0 | 0.0 | — | not installed | - | **Stale** |
| **bitsandbytes** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,295 | 873 | `main` | 2026-06-29 | **2** | 0 | 0 | 3.2 | — | `0.49.2.r91.g435b8b33-1` (ref `435b8b33`) | 2 | **Active** |
| **vllm** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 84,802 | 18,654 | `main` | 2026-06-29 | **307** | 0 | 0 | 264.5 | — | not installed | - | **Highly Active** |
| **vllm-omni** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 5,348 | 1,189 | `main` | 2026-06-30 | **63** | 0 | 0 | 70.5 | — | not installed | - | **Highly Active** |
| **pockettts.cpp** | [VolgaGerm/PocketTTS.cpp](https://github.com/VolgaGerm/PocketTTS.cpp) | 38 | 8 | `master` | 2026-03-29 | 0 | 0 | 0 | 0.0 | — | `0.1.0.r18.ge801e7d-1` (ref `e801e7d`) | 0 | **Stale** |
| **pocket-tts** | [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 4,691 | 522 | `main` | 2026-06-23 | **1** | 0 | 0 | 0.5 | — | `2.1.0-1` (ref `v2.1.0`) | 6 | **Active** |

> [!NOTE]
> `vllm`, `bitsandbytes`, `pocket-tts`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,675 | 295 | `master` | 2026-06-25 | 0 | 1 | 0 | 1.5 | — | `0.100.r0.ga4f5855-1` (ref `a4f5855`) | 1 | **Stale** |

> [!NOTE]
> `zeroclaw-git` (upstream: [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)) > `ironclaw-git` (upstream: [nearai/ironclaw](https://github.com/nearai/ironclaw)) are hosted and tracked separately under the `agents-shared` repository.
<!-- END_TABLES -->

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
<!-- START_BD_LLAMA_CPP -->
* **Status**: Highly Active (81 commits, 51 tags/releases in the last week). **0 commits since installed 9842.r0.g6f4f53f-1 (ref `6f4f53f`).**
<!-- END_BD_LLAMA_CPP -->
<!-- START_RF_LLAMA_CPP -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_LLAMA_CPP -->

### llama-cpp-python (`abetlen/llama-cpp-python`)
<!-- START_BD_LLAMA_CPP_PYTHON -->
* **Status**: Active (4 commits, 14 tags/releases in the last week). **0 commits since installed 9842.r0.g6f4f53f-1 (ref `346853c`).**
<!-- END_BD_LLAMA_CPP_PYTHON -->
<!-- START_RF_LLAMA_CPP_PYTHON -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_LLAMA_CPP_PYTHON -->

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
<!-- START_BD_STABLE_DIFFUSION_CPP -->
* **Status**: Active (18 commits, 8 tags/releases in the last week). **0 commits since installed 9842.r0.g6f4f53f-1 (ref `3b6c9ca`).**
<!-- END_BD_STABLE_DIFFUSION_CPP -->
<!-- START_RF_STABLE_DIFFUSION_CPP -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_STABLE_DIFFUSION_CPP -->

### whisper.cpp (`ggerganov/whisper.cpp`)
<!-- START_BD_WHISPER_CPP -->
* **Status**: Active (33 commits, 0 tags/releases in the last week). **0 commits since installed 9842.r0.g6f4f53f-1 (ref `0ae02cd`).**
<!-- END_BD_WHISPER_CPP -->
<!-- START_RF_WHISPER_CPP -->
* **Recent Focus**:
  - No new commits in this period.
<!-- END_RF_WHISPER_CPP -->

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Downstream Fork**:
<!-- START_BD_QWEN3_TTS_CPP -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 9842.r0.g6f4f53f-1 (ref `0c8b2ba`).**
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
* **Status**: Active (2 commits, 0 tags/releases in the last week). **2 commits since installed 0.49.2.r91.g435b8b33-1 (ref `435b8b33`).**
<!-- END_BD_BITSANDBYTES -->
<!-- START_RF_BITSANDBYTES -->
* **Recent Focus**:
  - `bd35b6a` chore(deps): bump the actions group with 2 updates (#1982)
  - `9da7109` Reduce CUDA build matrix, better fallback for lib loading (#1980)
<!-- END_RF_BITSANDBYTES -->

### vLLM (`vllm-project/vllm`)
<!-- START_BD_VLLM -->
* **Status**: Highly Active (307 commits, 0 tags/releases in the last week).
<!-- END_BD_VLLM -->
<!-- START_RF_VLLM -->
* **Recent Focus**:
  - `8ad4a018` [ModelRunner V2] Simplify recent UnlimitedOCR-related changes (#46975)
  - `7be58269` [Bugfix] Fix DeepseekV2Model hidden_size (#46986)
  - `030c9523` [Perf][1/N] Expand Triton kernel warmup coverage, DSv4 (#46634)
  - `4708292d` Bump flashinfer version to 0.6.13 (#46683)
  - `debec644` Add MiniMax-M3 modelopt nvfp4 support (#46756)
  - `c8fb2963` [FS-Offloading] Batch Lookup in C  (#46713)
  - `379acd4e` [Bugfix][Quantization] Fix W8A8 int-quantized scheme selection regression (#46860)
  - `07d33e57` [MyPy] Fix mypy incompatible assignment errors in LRUCacheLoRAModelManager (#44657)
  - `36bbecd6` [BugFix] Revert "[KV Offload] Use background thread for mmap / cpu_tensors pinning" (#46958)
  - `6149187a` [Kernel] Triton MLA logits workspace (#46819)
  - `49e28e8e` [Kernel][Helion][1/N] Add Helion kernel for fused_qk_norm_rope (#44010)
  - `0ca39c4f` [Bugfix] Capture final-layer aux hidden state in deepseek_v2 backbone (#46973)
  - `6185d738` [Rust Frontend] Keep literal "null" string for string-typed tool params (#46827)
  - `bc8481af` [MoE Refactor] Standardize Humming MoE experts + utilities (#43373)
  - `59575da4` [XPU] exclude unsupported models for test_tensor_sechma.py (#47008)
<!-- END_RF_VLLM -->

### vllm-omni (`vllm-project/vllm-omni`)
<!-- START_BD_VLLM_OMNI -->
* **Status**: Highly Active (63 commits, 0 tags/releases in the last week).
<!-- END_BD_VLLM_OMNI -->
<!-- START_RF_VLLM_OMNI -->
* **Recent Focus**:
  - `c45ac74d` [Core][Frontend] Support request-level batching for diffusion pipelines (#4079)
  - `504698de` [Core] Performance fix for orchestrator bottleneck: separates inter-stage from client outputs (#4527)
  - `724f5d13` [BugFix] Restore pre-#9572 NPU graph behavior (cap cudagraph_mode to PIECEWISE) (#4674)
  - `deb9bd4e` Fix Qwen2.5-Omni AutoRound loading (#4781)
  - `7619ed6b` [CI] Reducing mithril-h100-pool in ready&merge CI, optimize ready CI duration (#4354)
  - `e4026a50` Update WeChat QR code asset (#4778)
  - `e9d49317` [Core] Remove dead custom_process_input_func hooks in stage input processors (#4531)
  - `cd355720` [CI]Add Cosmos3 L2 serving tests (#4535)
  - `1b318d11` [Refactor] Reuse CFGParallelMixin in Bagel for CFG-parallel denoising (#4768)
  - `be60d7c7` [CI][Bugfix]Split nightly Diffusion X2V function tests by T2V/I2V to fix timeout (#4744)
  - `60ccadfb` [WAN_S2V] Enable HSDP for wan s2v (#4458)
  - `92f72085` [Bugfix] CosyVoice3: wrap ref_text in instruction template (#4644) (#4756)
  - `05a86ed1` [Test] Un-skip Qwen3-TTS batch E2E; match documented omit-null response shape (#4757) (#4759)
  - `c6ee3f7c` [Test] Skip Qwen3-TTS batch E2E tests (#4758)
  - `327e9dca` [Feature] Spatially-sharded (SP) decode for the Wan VAE (#4620)
<!-- END_RF_VLLM_OMNI -->

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
* **Status**: Active (1 commits, 0 tags/releases in the last week). **6 commits since installed 2.1.0-1 (ref `v2.1.0`).**
<!-- END_BD_POCKET_TTS -->
<!-- START_RF_POCKET_TTS -->
* **Recent Focus**:
  - `9514983` added project LocalVocal.ai to README.md (#200)
<!-- END_RF_POCKET_TTS -->

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
<!-- START_BD_SIGNAL_CLI_REST_API -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **1 commits since installed 0.100.r0.ga4f5855-1 (ref `a4f5855`).**
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
