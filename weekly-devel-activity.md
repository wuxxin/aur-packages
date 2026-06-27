# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Last 7 Days Activity (June 20, 2026 – June 27, 2026)

<!-- START_TABLES -->
### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **llama.cpp** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 118,322 | 19,972 | `master` | 2026-06-27 | **93** | 0 | 58 | 99.0 | ` b9735`, ` b9736` | `9771.r4.gbe4a6a6-1` (ref `be4a6a6`) | 51 | **Highly Active** |
| *└─ llama-cpp-python* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,440 | 1,423 | `main` | 2026-06-24 | **3** | 0 | 0 | 23.0 | — | `9771.r4.gbe4a6a6-1` (ref `4bee85b`) | 1 | **Active** |
| *└─ stable-diffusion.cpp* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,388 | 679 | `master` | 2026-06-27 | **16** | 0 | 11 | 17.5 | ` master-711-e8e012e`, ` master-712-e9e9524` | `9771.r4.gbe4a6a6-1` (ref `f440ad9`) | 7 | **Active** |
| *└─ whisper.cpp* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 51,084 | 5,705 | `master` | 2026-06-26 | **34** | 0 | 0 | 42.5 | — | `9771.r4.gbe4a6a6-1` (ref `43d78af`) | 31 | **Active** |
| *└─ qwen3-tts.cpp* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) | 0 | 0 | `main` | 2026-06-16 | 0 | 0 | 0 | 0.2 | — | `9771.r4.gbe4a6a6-1` (ref `0c8b2ba`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 0 | 0 | `main` | 2026-06-03 | 0 | 0 | 0 | 0.0 | — | not installed | - | **Stale** |
| **bitsandbytes** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 0 | 0 | `main` | 2026-06-22 | **1** | 0 | 0 | 3.0 | — | `0.49.2.r91.g435b8b33-1` (ref `435b8b33`) | 1 | **Active** |
| **vllm** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 0 | 0 | `main` | 2026-06-27 | **313** | 0 | 0 | 255.2 | — | not installed | - | **Highly Active** |
| **vllm-omni** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 0 | 0 | `main` | 2026-06-26 | **73** | 0 | 0 | 73.0 | — | not installed | - | **Highly Active** |
| **pockettts.cpp** | [VolgaGerm/PocketTTS.cpp](https://github.com/VolgaGerm/PocketTTS.cpp) | 0 | 0 | `master` | 2026-03-29 | 0 | 0 | 0 | 0.0 | — | `0.1.0.r18.ge801e7d-1` (ref `e801e7d`) | 0 | **Stale** |
| **pocket-tts** | [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 0 | 0 | `main` | 2026-06-23 | **1** | 0 | 0 | 0.5 | — | `2.1.0-1` (ref `v2.1.0`) | 6 | **Active** |

> [!NOTE]
> `vllm`, `bitsandbytes`, `pocket-tts`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 0 | 0 | `master` | 2026-06-25 | 0 | 1 | 0 | 1.5 | — | `0.100.r0.ga4f5855-1` (ref `a4f5855`) | 1 | **Stale** |

> [!NOTE]
> `zeroclaw-git` (upstream: [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)) > `ironclaw-git` (upstream: [nearai/ironclaw](https://github.com/nearai/ironclaw)) are hosted and tracked separately under the `agents-shared` repository.
<!-- END_TABLES -->

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
<!-- START_BD_LLAMA_CPP -->
* **Status**: Highly Active (93 commits, 58 tags/releases in the last week). **51 commits since installed 9771.r4.gbe4a6a6-1 (ref `be4a6a6`).**
<!-- END_BD_LLAMA_CPP -->
<!-- START_RF_LLAMA_CPP -->
* **Recent Focus**:
  - `9bebfcb4` sycl : fix failed ut cases of norm (#25044)
  - `0b6529d8` vulkan: fix step operator for 0 input (#25036)
  - `c299a92c` binaries : Improve rpc-server and export-graph-ops names. (#25045)
  - `0275c0f8` ci : add windows-openvino to check-release (#25022)
  - `83d385b4` tests : fix test-chat-template --no-common option (#25075)
  - `050ee92d` app : allow --version, --licenses & --help (#25054)
  - `3fc4e105` sched : reintroduce less synchronizations during split compute (#20793)
  - `5d8ccdf9` devops : add llama in all docker images (#25035)
  - `024930c6` arg: fix handling --spec-draft-hf and --hf-repo-v (#25043)
  - `5397c361` openvino: Update to OV 2026.2.1, self-contained release packages, operator improvements (#24974)
  - `e7ea94af` sync : ggml
  - `96183e98` ggml : bump version to 0.15.3 (ggml/1550)
  - `487a6cc1` vulkan: opt mul_mat_vecq for mi50 (#22933)
  - `5a6a0dd7` vulkan: add INTEL_XE1 arch enum and enable coopmat1 on Intel Xe-LPG Plus (#24404)
  - `ded1561b` ui: fix accessibility for hover-gated interactive elements assisted by claude(in debugging and tests) (#24727)
  - `9df06805` vulkan: Workaround compiler bug in conv2d coopmat2 path (#24924)
  - `2f18fe13` CUDA: add cublasSgemmBatched mapping for HIP/MUSA vendor headers (#25033)
  - `c16c35b8` ggml-cpu: fix SVE leftover path in ggml_vec_dot_f32 (#24699)
  - `1a87dcdc` server + ui: SSE Replay Buffer (#23226)
  - `e7e3f350` sycl : clamp softmax input to avoid underflow (#24941)
  - `b11f7c16` mtmd: add more validations (#25013)
  - `f818065d` CUDA: batch out_prod broadcast (dps2>1) path with cublasSgemmBatched (#24426)
  - `960d628f` mamba2: remove hardcoded 2x expansion factor and invalid d_inner % d_state check (#23082)
  - `5c7c22c3` opencl: flush profiling batch at shutdown for incomplete batches (#25016)
  - `beac5309` xcframework : disable mtmd video on i/tv/visionos (#25018)
  - `9d5d882d` model : Add label for LFM2.5-230M (#25008)
  - `1ec44d17` CUDA: Various fixes to 'cpy.cu' (#25000)
  - `c7cddefc` misc: fix labeler (#25012)
  - `e9d1b76d` server: use status code 403 for disabled features (#24970)
  - `099bf069` misc: update lables (#24920)
  - `60bc8866` common: refactor model handling (#24980)
  - `e8ecce53` docs : Eagle3 qwen3 draft model support (#24977)
  - `683b04cc` app : add the llama download subcommand (#24982)
  - `f728adab` ggml : address integer overflows in binary ops CUDA implementation (#24706)
  - `3e61ea0e` ui: fix always-show-sidebar-on-desktop setting after navigation refactor (#24979)
  - `fdbd6abe` tests : synchronize contexts at end of test-thread-safety (#24935)
  - `e12a0128` build: include libmtmd in Apple XCFramework (#21935)
  - `b3ce5ced` quant : fix quantizing moe with mtp (#24986)
  - `e9fb3b3f` sycl : support --split-mode tensor (#24152)
  - `9c109548` sycl : fix the failed UT cases of conv_3d (#24900)
  - `fdb2c11c` opencl: support non-contig rows in norm (#24965)
  - `09cedfd6` chat: harden caps check (#24973)
  - `8be759e6` hexagon: MUL_MAT and MUL_MAT_ID rework : 32x32 tiled weight repack, kernel-params, cached graphs (#24954)
  - `894bb27a` mtmd: model: unlimited-ocr: converter + parity test (#24969)
  - `fb401045` common: remove unused json-partial (#24968)
  - `51eae8cf` vulkan: allow reducing the graph submission batches to avoid timeouts (#24872)
  - `1191758c` vulkan: fail the build when a shader fails to compile (#24450)
  - `00139b66` ui: loading bar below the model picker (#24931)
  - `ef9c13d4` ui: New Logo + Navigation cleanup & Mobile UI/UX improvements (#24897)
  - `88636e17` model : Add LFM2.5-ColBERT-350M and LFM2.5-Embedding-350M (#24913)
  - `ac4105d6` vulkan: Apply bias before softmax in FA, to avoid overflow (#24909)
<!-- END_RF_LLAMA_CPP -->

### llama-cpp-python (`abetlen/llama-cpp-python`)
<!-- START_BD_LLAMA_CPP_PYTHON -->
* **Status**: Active (3 commits, 0 tags/releases in the last week). **1 commits since installed 9771.r4.gbe4a6a6-1 (ref `4bee85b`).**
<!-- END_BD_LLAMA_CPP_PYTHON -->
<!-- START_RF_LLAMA_CPP_PYTHON -->
* **Recent Focus**:
  - `4ff48f0` feat(example): support chained NextN server MTP (#2319)
<!-- END_RF_LLAMA_CPP_PYTHON -->

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
<!-- START_BD_STABLE_DIFFUSION_CPP -->
* **Status**: Active (16 commits, 11 tags/releases in the last week). **7 commits since installed 9771.r4.gbe4a6a6-1 (ref `f440ad9`).**
<!-- END_BD_STABLE_DIFFUSION_CPP -->
<!-- START_RF_STABLE_DIFFUSION_CPP -->
* **Recent Focus**:
  - `9956436` refactor: consolidate WAN VAE version checks (#1712)
  - `ec4cb81` fix: correct TAEHV encoding for image models (#1711)
  - `3973015` sync: update ggml and revert vulkan workarounds for Anima and Ernie (#1710)
  - `9ee77fc` fix(ci): disable dynamic CPU backends for arm64 CUDA image (#1709)
  - `39f7962` ci: adopt dynamic cpu backends on released binaries (#1704)
  - `8caa3f9` feat: add krea2 support (#1705)
  - `2938272` feat: add logit-normal scheduler (#1669)
<!-- END_RF_STABLE_DIFFUSION_CPP -->

### whisper.cpp (`ggerganov/whisper.cpp`)
<!-- START_BD_WHISPER_CPP -->
* **Status**: Active (34 commits, 0 tags/releases in the last week). **31 commits since installed 9771.r4.gbe4a6a6-1 (ref `43d78af`).**
<!-- END_BD_WHISPER_CPP -->
<!-- START_RF_WHISPER_CPP -->
* **Recent Focus**:
  - `0ae02cdb` talk-llama : sync llama.cpp
  - `0279b538` sync : ggml
  - `974db58c` ggml : bump version to 0.15.3 (ggml/1550)
  - `df03e266` vulkan: Workaround compiler bug in conv2d coopmat2 path (llama/24924)
  - `b564d536` CUDA: add cublasSgemmBatched mapping for HIP/MUSA vendor headers (llama/25033)
  - `5e7ef7e4` ggml-cpu: fix SVE leftover path in ggml_vec_dot_f32 (llama/24699)
  - `02be8712` sycl : clamp softmax input to avoid underflow (llama/24941)
  - `96996579` CUDA: batch out_prod broadcast (dps2>1) path with cublasSgemmBatched (llama/24426)
  - `7ce3616a` opencl: flush profiling batch at shutdown for incomplete batches (llama/25016)
  - `9cad7959` CUDA: Various fixes to 'cpy.cu' (llama/25000)
  - `82686b51` ggml : address integer overflows in binary ops CUDA implementation (llama/24706)
  - `ffd5b0b5` sycl : support --split-mode tensor (llama/24152)
  - `c4ba5e2e` sycl : fix the failed UT cases of conv_3d (llama/24900)
  - `fe37d2e4` opencl: support non-contig rows in norm (llama/24965)
  - `e0a0f125` hexagon: MUL_MAT and MUL_MAT_ID rework : 32x32 tiled weight repack, kernel-params, cached graphs (llama/24954)
  - `a201c205` vulkan: allow reducing the graph submission batches to avoid timeouts (llama/24872)
  - `f081d84a` vulkan: fail the build when a shader fails to compile (llama/24450)
  - `792da0ec` vulkan: Apply bias before softmax in FA, to avoid overflow (llama/24909)
  - `3fc2c57a` vulkan: support all backend tests for SQR/SQRT/SIN/COS/CLAMP/LEAKY_RELU/NORM (llama/24582)
  - `1fdbfb19` vulkan: Support GET_ROWS_BACK (llama/24883)
  - `c25eb26c` vulkan: support CONV_3D (llama/24612)
  - `cc0d00f6` vulkan: make mul_mm ALIGNED a spec constant (llama/24689)
  - `e3c18388` vulkan: link ggml-cpu when GGML_VULKAN_CHECK_RESULTS / RUN_TESTS are enabled (llama/24444)
  - `2955e84e` ggml-webgpu: improve MTP inference by using mat-vec path for small batches (llama/24811)
  - `0badff27` opencl: q8_0 gemv precision improvement (llama/24923)
  - `1b3f8434` support bf16 on bin_bcast OP and unary OPs (llama/24838)
  - `556d900c` fix(hexagon): use padded stride for ssm-conv weights (llama/24470)
  - `420518d8` ggml : optimize AMX (llama/24806)
  - `75b90fb0` ggml-webgpu: add adapter toggles for F16 on Vulkan + NVIDIA
  - `adbcfa0d` mtmd, arg: fix utf8 handling on windows (llama/24779)
  - `e3ab3110` examples : fix argument flag for min speech duration in VAD (#3907)
<!-- END_RF_WHISPER_CPP -->

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Downstream Fork**:
<!-- START_BD_QWEN3_TTS_CPP -->
* **Status**: Stale (0 commits, 0 tags/releases in the last week). **0 commits since installed 9771.r4.gbe4a6a6-1 (ref `0c8b2ba`).**
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
* **Status**: Active (1 commits, 0 tags/releases in the last week). **1 commits since installed 0.49.2.r91.g435b8b33-1 (ref `435b8b33`).**
<!-- END_BD_BITSANDBYTES -->
<!-- START_RF_BITSANDBYTES -->
* **Recent Focus**:
  - `9da7109` Reduce CUDA build matrix, better fallback for lib loading (#1980)
<!-- END_RF_BITSANDBYTES -->

### vLLM (`vllm-project/vllm`)
<!-- START_BD_VLLM -->
* **Status**: Highly Active (313 commits, 0 tags/releases in the last week).
<!-- END_BD_VLLM -->
<!-- START_RF_VLLM -->
* **Recent Focus**:
  - `9fd00ee0` [ROCm][CI] Move remaining mi250_2 tests out of the MI250 queue (#46905)
  - `091d1397` [ROCm][CI] Add TRITON_ATTN score absolute tolerance floor (#46891)
  - `b588f66d` [GLM5.2 Perf] 'fused_indexer_q_rope_quant' triton kernel, 1.9% ~ 3.3% E2E Throughput improvement. (#46862)
  - `455f25aa` [CLI] Add flag to print TTFT and TPS in 'vllm chat' (#46775)
  - `d706dec9` fix: Correct reasoning-end detection for prompt history (#44551)
  - `68ee8300` [ROCm][CI]Fix test_concat_and_cache_mla_rope_fused on ROCm (#46409)
  - `ddd3855a` [MoE Backend] add HPC-Ops MoE backend (#45924)
  - `00e045b7` [ROCm][CI TG] refactor and fix deepep_moe test group (#46758)
  - `17a71d87` [ROCm][CI] Relax fused layernorm quant test tolerances for one-ULP outliers (#46658)
  - `2e058851` fix(docker): eliminate race conditions in shared buildkit cache mounts (#44984)
  - `1a92dfcc` [Build] Show error message when using ROCm with LTO and different compilers (#35232)
  - `d0f80081` [Build] Update vllm to point to vllm-project/flash-attention commit that builds FA3 with torch stable API.  (#46644)
  - `c6dd32a8` [ModelRunner V2] Support realtime embeddings (#46762)
  - `af16446b` Vram semaphore infra (#44465)
  - `3f674774` [CI] Don't try and download files that we already know don't exist (#46854)
<!-- END_RF_VLLM -->

### vllm-omni (`vllm-project/vllm-omni`)
<!-- START_BD_VLLM_OMNI -->
* **Status**: Highly Active (73 commits, 0 tags/releases in the last week).
<!-- END_BD_VLLM_OMNI -->
<!-- START_RF_VLLM_OMNI -->
* **Recent Focus**:
  - `05a86ed1` [Test] Un-skip Qwen3-TTS batch E2E; match documented omit-null response shape (#4757) (#4759)
  - `c6ee3f7c` [Test] Skip Qwen3-TTS batch E2E tests (#4758)
  - `327e9dca` [Feature] Spatially-sharded (SP) decode for the Wan VAE (#4620)
  - `47871d5e` Updated Cosmos3 docstrings (#4727)
  - `b66cd024` [Bugfix] Fix /v1/audio/speech usage token accounting for Qwen3-TTS (#4646) (#4673)
  - `c582805e` Revert "[Bugfix] Use MediaConnector for image/video URL fetching to prevent SSRF" (#4751)
  - `908e7d32` [CI][Bugfix] Fix nightly L2/L3 E2E-only upload and Buildkite EXTRA escaping (#4734)
  - `d6f1d3d6` [Doc] Add code-quality dimension to precheck-pr skill (#4697)
  - `c39ac9ff` [Bugfix] Stream Qwen3-TTS WebSocket input as one request (#4731)
  - `580a0efe` [Bugfix] Add back resolving from deploy config written pipeline in StageConfigFactory (#4729)
  - `329c98ff` Wan2.2: Fix the bug of using cache-dit with ulysses in t2v and i2v (#3927)
  - `36a5e9cf` [skip ci][Misc] LVSA showcase (training-free block-sparse attention) (#4192)
  - `0b04f2a0` [Model] Add Ming-omni-tts MoE 16.8B-A3B + CFM CUDAGraph (#4341)
  - `5db89b41` [Core] hunyuan-image prefetch kv (#4448)
  - `e500c005` [Bugfix][NPU] Register vllm-ascend custom ops in NPUOmniPlatform.set_device (#4712)
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

### ironclaw (`nearai/ironclaw`)
<!-- START_BD_IRONCLAW -->
* **Status**: Highly Active (96 commits, 1 tag/release in the last week). **43 commits since installed ironclaw_skill_learning.v0.1.0.r21.g4f28feb-1 (ref `44f063d`).**
<!-- END_BD_IRONCLAW -->
<!-- START_RF_IRONCLAW -->
* **Recent Focus**:
  - `f0f46a52e` [codex] Port Reborn Responses API input handling (#5347)
  - `5298504a1` feat(approvals): default "Always allow eligible tools" to on (#5366)
  - `c8a51ada5` [codex] Align Reborn runtime tool surface (#5346)
  - `1a01a0942` [codex] test llm loop failures (#5367)
  - `0eccde571` feat(reborn): env-configurable turn-runner concurrency (0 = unlimited) (#5265)
  - `a1b7f80b2` build(deps-dev): bump js-yaml in /docs/architecture-video (#4934)
  - `2fe061f3c` fix(reborn): unblock parallel-thread sends and new chats during active runs (#5352)
  - `a16b67a2a` test(e2e): add reborn webui legacy harness (#5345)
  - `667e3cc63` fix(ci): gate skills io/Read import to unix (fixes Clippy Windows ripple from #5325) (#5351)
  - `185ce889d` fix(reborn): discourage disabled tool workarounds (#5307)
  - `f344180a5` fix(webui-v2): anchor run failure messages (#5299)
  - `0e492365e` fix(reborn): persist always-allow for shared registry tools (#5309)
  - `aeaee50e4` fix(ci): green up main + cargo/non-cargo network resilience (#5325)
  - `535c29c34` Fix hosted-volume scoped tool service resolution (#5321)
  - `26a5f902e` fix(reborn): deliver triggered Slack runs after settlement (#5318)
  - `f7c82f5b3` fix(reborn): duplicate logs header (#5324)
  - `e2742bb97` [codex] harden agent loop chaos handling (#5296)
  - `0c79a2d28` Add hosted single-tenant volume profile (#5259)
  - `4e1e816b4` Move legacy tests to nightly CI (#5308)
  - `c785ca2e9` fix(ci): unblock main and cut flake (libsql feature, apt retry, fail-fast, .codegraph) (#5281)
  - `bc4cc6e5c` fix(reborn): align external tool provider names (#5303)
  - `54ca2108e` [codex] Type provider tool names at model protocol boundaries (#5292)
  - `7e191be3f` feat(reborn): /v1/models, model validation, external-tool gate foundation (#5094)
  - `0c00929b6` perf(reborn): batch durable event-log appends (write-behind coalescing) (#5257)
  - `e37772f94` fix(webui-v2): move active run logs link out of composer (#5284)
  - `6985e6347` docs(reborn): design — native hot-store primitives on the unified RootFilesystem trait (#5269)
  - `e67882e55` fix(webui-v2): make logs page scrollable (#5278)
  - `46ed73f53` fix(filesystem): fold CAS put directory pre-check into one statement (3→1 round-trip) (#5255)
  - `031f2e2fd` add a seam for download_file to extract binary docs (PDF/PPTX/DOCX/XLSX) as text (#4997)
  - `bf29e0508` fix(reborn): treat parked Blocked* triggered runs as terminal-for-delivery (#5222)
  - `799eb1540` fix(reborn): stop WASM execution from starving the tokio worker pool (#5206)
  - `24faee72e` fix(turns): exempt certified skill content from prompt content denylist (#5169) (#5258)
  - `9ce47c4d7` feat(reborn): expose user-scoped tool settings (#5256)
  - `afa549508` fix(reborn): keep approval gates visible on busy sends (#5241)
  - `ef729fc00` fix(triggers): recover stale claim-only fires (#5245)
  - `6af6b9318` fix(webui): keep streamed chat responses in view (#5248)
  - `81dd13abe` fix(webui-v2): keep chat composer editable while running (#5235)
  - `92e77640f` fix(reborn): persist approval-card always allow as tool settings (#5195)
  - `a38119f59` fix(reborn): chat timestamp hover actions (#5226)
  - `9632f9093` [codex] Fix durable preview owner scope (#5230)
  - `fbb85eee5` fix(reborn): show NEAR AI default base URL in provider card (#5217)
  - `c02f73dad` fix(reborn): allow web ui logs for multi-tenancy users (#5199)
  - `163d594b3` feat(reborn-webui): tool permissions + global auto-approve settings surface (#4960) (#5068)
<!-- END_RF_IRONCLAW -->

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
  - **PocketTTS Integration**: Added support for VolgaGerm's C++ PocketTTS wrapper (`pocket-tts.cpp-git` at `0.1.0.r18.ge801e7d`) and the python binding (`python-pocket-tts` at `2.1.0`).
  - **libggml-git-hip**: Updated to build version `9743.r0.gc576070` to align with upstream changes and updated patches.
  - **zeroclaw-git**: Upgraded package to version `0.8.1.r16.g13a8a857ae` to package the newly tagged `v0.8.1` release.
  - **AGENTS.md**: Updated styling guidelines and command examples for shell and python scripts.

---

## 📋 Instruction Guide: Recreating this Analysis

**Fully Automated Update**: You can run the automation script `scripts/update-activity.py` with the `--write` (or `-w`) flag to automatically pull all repository updates, calculate the statistics, and optionally write the updated tables directly back into this file:
```bash
python scripts/update-activity.py [--write]
```
