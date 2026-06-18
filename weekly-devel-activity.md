# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---## 📅 Summary of Last 7 Days Activity (June 11, 2026 – June 17, 2026) 

### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **libggml-git-hip** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 117,038 | 19,681 | `master` | 2026-06-17 | **100** | 0 | 67 | 107.5 | `b9692`, `b9691` | `9627.r0.g53bd47e-1` (built 2026-06-14) | 65 | **Highly Active** |
| *└─ python-llama-cpp-git-ggml-hip* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,409 | 1,418 | `main` | 2026-06-16 | **12** | 0 | 26 | 22.2 | `v0.3.30`, `v0.3.29` | `9627.r0.g53bd47e-1` (ref `e807092`) | 6 | **Active** |
| *└─ stable-diffusion.cpp-git-ggml-hip* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,296 | 665 | `master` | 2026-06-17 | **25** | 0 | 20 | 18.2 | `master-709-92a3b73` | `9627.r0.g53bd47e-1` (ref `276025e`) | 16 | **Active** |
| *└─ whisper.cpp-git-ggml-hip* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 50,812 | 5,671 | `master` | 2026-06-17 | **28** | 0 | 2 | 50.7 | `v1.9.0`, `v1.8.7` | `9627.r0.g53bd47e-1` (ref `df7638d8`) | 28 | **Active** |
| *└─ qwen3-tts.cpp-git-ggml-hip* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) (Fork) | 16 | 3 | `main` | 2026-06-16 | **1** | 0 | 0 | 0.2 | — | `9627.r0.g53bd47e-1` (ref `2a41916`) | 1 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 205 | 66 | `main` | 2026-06-03 | **0** | 0 | 0 | 0.2 | — | — | — | **Stale** |
| **python-bitsandbytes-rocm-git** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,277 | 873 | `main` | 2026-06-12 | **2** | 0 | 0 | 3.5 | — | `head.r1155.g2177945b-1` (built 2026-05-31) | 8 | **Active** |
| **python-vllm-rocm-git** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 83,190 | 18,158 | `main` | 2026-06-17 | **275** | 0 | 1 | 235.5 | `v0.23.1rc0` | not installed | — | **Highly Active** |
| **python-vllm-omni-rocm-git** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 5,179 | 1,130 | `main` | 2026-06-17 | **74** | 0 | 1 | 76.2 | `v0.23.0rc1` | not installed | — | **Highly Active** |
| **pocket-tts.cpp-git** | [VolgaGerm/PocketTTS.cpp](https://github.com/VolgaGerm/PocketTTS.cpp) | 37 | 8 | `master` | 2026-03-29 | **0** | 0 | 0 | 0.0 | — | `0.1.0.r18.ge801e7d-1` (built 2026-06-17) | 0 | **Stale** |
| **python-pocket-tts** | [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 4,621 | 512 | `main` | 2026-06-03 | **0** | 0 | 0 | 0.7 | — | `2.1.0-1` (built 2026-06-17) | 5 | **Stale** |

> [!NOTE]
> `vllm`, `bitsandbytes`, `pocket-tts`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api-git** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,640 | 292 | `master` | 2026-06-11 | **1** | 0 | 1 | 4.0 | `0.100` | `0.100.pre.r0.g81efbd2-1` (built 2026-06-03) | 1 | **Active** |

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Highly Active (100 commits, 67 tags in the last week, as of June 17).
* **Recent Focus**:
  - **Server & WebUI**: Added model management API (`b4024af6`). Added SVG block rendering (`2a6c391a`), source toggle to mermaid and svg blocks (`c1304d7b`), conversation export as jsonl (`8086439a`), and SSE transport/CORS proxy fixes (`bae36efa`).
  - **Hardware Backends & Kernels**:
    - *Metal*: Implemented `rope_back` operator (`0843245c`), f16/bf16 support for concat operator (`8d2e5806`), and repeat bf16 support (`272088b9`).
    - *Vulkan*: Recorded actual memory properties during buffer creation (`558e221b`), prefer host-visible memory buffers on UMA devices (`32120c10`), supported gated_delta_net with S_v=16 (`d5fb1042`), added `col2im_1d` op (`ad39ccaa`), and supported more CONCAT types (`9dbc6621`).
    - *SYCL*: Added dev2dev memcpy by SYCL API (`74a80dd9`), Conv3D support (`d1759e41`), fp16 support for various ops (SQR, SQRT, LOG, SIN, COS, CLAMP) (`58728bdb`), fixed use-after-free bug in MoE prefill (`ebbc1e51`), supported optional USM system allocations (`9b260fc9`), supported reordered Q4_K/Q5_K/Q6_K MoE MUL_MAT_ID (`ac79caa7`), supported OP EXPM1, and supported FLOOR, TRUNC, ROUND UT cases (`fdd10988`). Made `GGML_SYCL_F16=ON` default (`4196b477`).
  - **Models & Speculative Decoding**: Added backend sampling support for Eagle3 speculative decoding (`a1824902`), fixed Eagle3 segfaults on long prompts (`1a2dea29`), and added spec metrics (`635b65ad`). Fixed and restricted NVFP4 edge-cases in llama-graph (`02810c7a`). Conditionally enabled Power11 backend on CPU (`2e88c49c`).
  - **APIs & Dependencies**: Updated BoringSSL to 0.20260616.0 (`74ade527`). Added support for OpenVINO 2026.2, context-shift, Q5_1 support, gemma4 dense/embedding, and -fa off (`890f1a27`).

### llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Active (12 commits, 26 tags in the last week, as of June 17).
* **Recent Focus**:
  - **llama.cpp Sync**: Updated llama.cpp dependency to `6e9007ae6` (`541b08c`), `6eab47181` (`824565a`), and `e3a74b299` (`822146b`).
  - **Features**: Added Pyodide wheel support (`a804233`).
  - **CI & Build System**: Skips MTMD CLI wrappers in package builds (`e807092`) and resolved Docker compiler issues by using a C++ compiler (`3850aff`). Bumped release version to `v0.3.30` and `v0.3.29`.

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (25 commits, 20 tags in the last week, as of June 17).
* **Recent Focus**:
  - **Features**: Support for cancelling generations (`5a34bc7`), add PuLID-Flux identity-injection support (`93527fd`), support backend-specific max-vram budgets (`bb90bfa`), and add disk params backend (`bdb431a`).
  - **Fixes**: Normalize CLIP prompts before special-token splitting (`7f0e728`), correct conversion from sd_type_t to ggml_type (`710bc91`), simplify PuLID ID extraction setup (`146b6cc`), and allow oversized Vulkan parameter tensors (`6e66a1a`).
  - **Refactoring & Optimization**: Centralized controlnet output caching (`9838264`), remove `vae_decode_only` context flag (`749186c`).
  - **Sync**: Update `sdcpp-webui` (`92a3b73`), update ggml (`517abc7`).

### whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Active (28 commits, 2 tags in the last week, as of June 17).
* **Recent Focus**:
  - **Release**: Tagged and released `v1.9.0` and `v1.8.7`.
  - **Features & Models**: Added support for NVIDIA Parakeet models (`9efddafb`), and added support to Ruby bindings (`0d147569`). Added `--version` flag to CLI (`db5a84bd`).
  - **Hardware Backends**: Added OpenCL Adreno `q5_0`/`q5_1` kernels (`2dcfd49d`), Vulkan build fixes and optimizations (fast path for contiguous transfers, medium tile on Asahi Linux, Flash Attention optimizations, iq1 shared memory reduction), CUDA fixes (`ef85b26d`). WebGPU performance improvements (`aa42b483`).
  - **Sync**: Bumped internal ggml version to `0.15.1` (`f35f47b5`) and `0.15.0` (`b04008fc`), synced ggml and llama.cpp for `talk-llama` (`0ec08451`).

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Status**: Stale (1 commit in the last week on downstream fork, 0 commits on origin).
* **Fork & Feature Parity**:
  - Downstream added support for more audio formats using ffmpeg/libavcodec (`0c8b2ba`). Upstream had no updates.

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Active (2 commits in the last week, as of June 17).
* **Recent Focus**:
  - **Fixes & Kernel**: Ensured `absmax_offset` is of type float32 before passing to `gemm_4bit` (`99e0b0c`), and updated kernel usage (`936f60b`).

### vLLM (`vllm-project/vllm`)
* **Status**: Highly Active (275 commits, 1 tag in the last week, as of June 17).
* **Recent Focus**:
  - **Hardware & ROCm Backend**:
    - *MiniMax-M3 AMD*: Added `packed_modules_mapping` and pass `swiglu` (`091386a9`), enable fp8_per_channel for bf16 weights on mi300x (`e28e8c87`), and fallback GFX942 sparse MLA ops to Triton (`d5371223`).
    - *Fixes*: Fix FP8 per-tensor scale rank mismatch for Inductor (`2785a5e0`), fix MiniMax-M3 FP8 KV cache dtype (`efd15e19`), and tune `mxfp8` moe/linear on gfx950 for MiniMax-M3 (`f2beaa80`).
    - *AITER/Quark*: Tag per-channel FP8 weights as PER_CHANNEL so AITER pre-shuffled GEMM is selected (`0b131b16`).
  - **Models & Core**:
    - *MiniMax-M3*: Added MiniMax-M3-MXFP4 support (`d112eb1a`), and enabled FP8 sparse GQA (`4c626633`), tuning Triton indexer score decode (`5bdc01bc`).
    - *Gemma4*: Render reasoning on assistant turns without tool_calls (`58b2e896`), pre-initialise streaming reasoning state (`3c6084bb`), fix parsing when thinking is disabled (`b831374c`), and skip forced JSON for required/named tool choice (`b9684d99`).
    - *Other Models*: Support ViT full CUDA graph for Kimi-VL (`fa85ead2`). Support GLM-5 dimensions for TRT-LLM ragged MLA prefill (`9d4dc4ca`). Enforced audio decode duration limit in chat completions security path (`3d20275b`).
  - **KV Connector / Offloading**: Avoid blocking engine to flush offloads on idle (`6d8fff56`), added cache_prefix to Mooncake namespace store keys (`44b25127`), and added selective offload documentation (`ee0fd698`).
  - **Rust Frontend**: Added `/abort_requests` endpoint (`295232a2`), and supported prompt-only completions (`56e43452`).
  - **Kernels**: Added Helion kernel for `rms_norm_dynamic_per_token_quant` (`46f74e14`). Enabled Flashinfer non-gated MoE bf16 (`8b2b566e`). Added weightless RMSNorm CUDA kernels (`93bbe94d`).

### vllm-omni (`vllm-project/vllm-omni`)
* **Status**: Highly Active (74 commits, 1 tag in the last week, as of June 17).
* **Recent Focus**:
  - **Refactoring & Platform Architecture**: Extracted `OmniStreamingVideoHandler` base and `QwenOmniStreamingVideoHandler` (`d744940b`). Omni Stage Runtime and Distributed Replica Control Plane refactored (`64a5bb92`), and migrated pipelines to `SupportsComponentDiscovery` for offload discovery (`e957d16f`).
  - **Audio & TTS Models**: Qwen3-TTS: trim reference audio in `no_async_chunk` voice clone (`a693ae67`). Shim `PreTrainedModel._tp_plan` to fix `MOSS-TTS-Nano` load crash (`d78a92ec`). Lazy load codec for `higgs-audio-v3` under `load_format=dummy` (`dc143807`).
  - **Diffusion Models (Image/Video)**:
    - *Wan2.2*: Fixed uninitialized nn.Module RotaryEmbeddingWan graph break (`890803ca`), and skip attention mask for zero-padded SP sequences (`20b7a67b`).
    - *HunyuanImage3*: Added grouped step batching (`ae937320`), removed sync logic (`a86c333c`), size match issue fixes (`6c6fde3e`), and added more resolution support for HunyuanImage3.0 (`1be1a711`).
    - *LTX-2.3*: Fixed tensor-parallel gated attention (`11829ccd`).
    - *Other Models*: Supported SDXL model enabling (`e7f0db10`).
  - **Performance & Cache**: Avoid per-step blocking write in `OmniTensorPrefixCache` (`dff757da`). Fix DFlash prefix cache corruption due to missing lookahead block (`864d2216`). Restore parallel stage initialization for AR+DiT pipelines (`10404e4c`).
  - **Triton & Kernels**: Introduced High-Performance MoT (Mixture-of-Tokens) Kernels in Triton (`46ed7c14` / `#3960`).
  - **Metrics**: Wire `log_stats` to `AsyncOmni` and add missing token metrics for non-text requests (`8fa0394d`).

### PocketTTS.cpp (`VolgaGerm/PocketTTS.cpp` & `kyutai-labs/pocket-tts`)
* **Status**: Stale (0 commits in the last week, as of June 17).
* **Recent Focus**:
  - No new commits in the last week. `pocket-tts.cpp-git` (upstream clone version `0.1.0.r18.ge801e7d`) and `python-pocket-tts` (upstream version `2.1.0`) were newly packaged and integrated into the repository. Upstream `kyutai-labs/pocket-tts` had some recent cleanup commits (last commit June 3) including seshat-tts references. Upstream `PocketTTS.cpp` had its last commit on March 29 implementing ScatterElements buffer mismatch fixes for fp16 KV caches.

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
* **Status**: Active (1 commit, 1 tag in the last week, as of June 17).
* **Recent Focus**:
  - No new commits since June 11. The last update on June 11 bumped signal-cli version to `v0.14.5` (`a4f5855`) and released version `0.100`.


---

## 📋 Instruction Guide: Recreating this Analysis

To re-perform this development activity analysis, follow the steps below.

### Step 1: Repository Reference Map

Here is the list of tracked upstream GitHub repositories and their corresponding local Arch packages:

| Directory Name | GitHub Upstream Repo | System Package | Package Type |
| :--- | :--- | :--- | :--- |
| **llama.cpp** | `ggml-org/llama.cpp` | `libggml-git-hip` | AUR VCS (`-git`) |
| **llama-cpp-python** | `abetlen/llama-cpp-python` | `python-llama-cpp-git-ggml-hip` | AUR VCS (`-git` split) |
| **stable-diffusion.cpp** | `leejet/stable-diffusion.cpp` | `stable-diffusion.cpp-git-ggml-hip` | AUR VCS (`-git` split) |
| **whisper.cpp** | `ggerganov/whisper.cpp` | `whisper.cpp-git-ggml-hip` | AUR VCS (`-git` split) |
| **qwen3-tts.cpp** | `khimaros/qwen3-tts.cpp` (Fork) | `qwen3-tts.cpp-git-ggml-hip` | AUR VCS (`-git` split) |
| **qwen3-tts-upstream** | `predict-woo/qwen3-tts.cpp` (Origin) | — | not installed |
| **bitsandbytes** | `bitsandbytes-foundation/bitsandbytes` | `python-bitsandbytes-rocm-git` | AUR VCS (`-git`) |
| **vllm** | `vllm-project/vllm` | `python-vllm-rocm-git` | AUR VCS (`-git`) |
| **vllm-omni** | `vllm-project/vllm-omni` | `python-vllm-omni-rocm-git` | AUR VCS (`-git`) |
| **pockettts.cpp** | `VolgaGerm/PocketTTS.cpp` | `pocket-tts.cpp-git` | AUR VCS (`-git`) |
| **pocket-tts** | `kyutai-labs/pocket-tts` | `python-pocket-tts` | AUR Tagged Release |
| **signal-cli-rest-api** | `bbernhard/signal-cli-rest-api` | `signal-cli-rest-api-git` | AUR VCS (`-git`) |

### Step 2: Probe Installed System Versions

Run `pacman -Q` on the target package names to retrieve their current installed version and git commit hashes:

```bash
for pkg in libggml-git-hip python-llama-cpp-git-ggml-hip stable-diffusion.cpp-git-ggml-hip whisper.cpp-git-ggml-hip qwen3-tts.cpp-git-ggml-hip python-bitsandbytes-rocm-git python-vllm-rocm-git python-vllm-omni-rocm-git pocket-tts.cpp-git python-pocket-tts signal-cli-rest-api-git; do
  ver=$(pacman -Q "$pkg" 2>/dev/null | awk '{print $2}')
  if [ -n "$ver" ]; then
    echo "$pkg: $ver"
  else
    echo "$pkg: not installed"
  fi
done
```

### Step 3: Fetch Upstream Repository History

Update the local checkouts stored under `scratch/` by fetching the latest changes and resetting to the tracking branch:

```bash
# Clone any missing repositories using shallow clone depth
for r in llama.cpp llama-cpp-python stable-diffusion.cpp whisper.cpp qwen3-tts.cpp qwen3-tts-upstream bitsandbytes vllm vllm-omni pockettts.cpp pocket-tts signal-cli-rest-api; do
  if [ ! -d "scratch/$r" ]; then
    case "$r" in
      llama.cpp) url="https://github.com/ggml-org/llama.cpp.git" ;;
      llama-cpp-python) url="https://github.com/abetlen/llama-cpp-python.git" ;;
      stable-diffusion.cpp) url="https://github.com/leejet/stable-diffusion.cpp.git" ;;
      whisper.cpp) url="https://github.com/ggerganov/whisper.cpp.git" ;;
      qwen3-tts.cpp) url="https://github.com/khimaros/qwen3-tts.cpp.git" ;;
      qwen3-tts-upstream) url="https://github.com/predict-woo/qwen3-tts.cpp.git" ;;
      bitsandbytes) url="https://github.com/bitsandbytes-foundation/bitsandbytes.git" ;;
      vllm) url="https://github.com/vllm-project/vllm.git" ;;
      vllm-omni) url="https://github.com/vllm-project/vllm-omni.git" ;;
      pockettts.cpp) url="https://github.com/VolgaGerm/PocketTTS.cpp.git" ;;
      pocket-tts) url="https://github.com/kyutai-labs/pocket-tts.git" ;;
      signal-cli-rest-api) url="https://github.com/bbernhard/signal-cli-rest-api.git" ;;
    esac
    git clone --depth 2000 "$url" "scratch/$r"
  fi
done

# Fetch and reset checkouts (note default branch differences)
git -C scratch/llama.cpp fetch origin && git -C scratch/llama.cpp checkout master && git -C scratch/llama.cpp reset --hard origin/master
git -C scratch/llama-cpp-python fetch origin && git -C scratch/llama-cpp-python checkout main && git -C scratch/llama-cpp-python reset --hard origin/main
git -C scratch/stable-diffusion.cpp fetch origin && git -C scratch/stable-diffusion.cpp checkout master && git -C scratch/stable-diffusion.cpp reset --hard origin/master
git -C scratch/whisper.cpp fetch origin && git -C scratch/whisper.cpp checkout master && git -C scratch/whisper.cpp reset --hard origin/master
git -C scratch/qwen3-tts.cpp fetch origin && git -C scratch/qwen3-tts.cpp checkout main && git -C scratch/qwen3-tts.cpp reset --hard origin/main
git -C scratch/qwen3-tts-upstream fetch origin && git -C scratch/qwen3-tts-upstream checkout main && git -C scratch/qwen3-tts-upstream reset --hard origin/main
git -C scratch/bitsandbytes fetch origin && git -C scratch/bitsandbytes checkout main && git -C scratch/bitsandbytes reset --hard origin/main
git -C scratch/vllm fetch origin && git -C scratch/vllm checkout main && git -C scratch/vllm reset --hard origin/main
git -C scratch/vllm-omni fetch origin && git -C scratch/vllm-omni checkout main && git -C scratch/vllm-omni reset --hard origin/main
git -C scratch/pockettts.cpp fetch origin && git -C scratch/pockettts.cpp checkout master && git -C scratch/pockettts.cpp reset --hard origin/master
git -C scratch/pocket-tts fetch origin && git -C scratch/pocket-tts checkout main && git -C scratch/pocket-tts reset --hard origin/main
git -C scratch/signal-cli-rest-api fetch origin && git -C scratch/signal-cli-rest-api checkout master && git -C scratch/signal-cli-rest-api reset --hard origin/master
```

### Step 4: Batch Statistics Compilation

Run the following script from the root of the `aur-packages` repository to compile the raw statistical metrics:

```bash
declare -A PKG_MAP=(
  [llama.cpp]=libggml-git-hip
  [llama-cpp-python]=python-llama-cpp-git-ggml-hip
  [stable-diffusion.cpp]=stable-diffusion.cpp-git-ggml-hip
  [whisper.cpp]=whisper.cpp-git-ggml-hip
  [qwen3-tts.cpp]=qwen3-tts.cpp-git-ggml-hip
  [qwen3-tts-upstream]=""
  [bitsandbytes]=python-bitsandbytes-rocm-git
  [vllm]=python-vllm-rocm-git
  [vllm-omni]=python-vllm-omni-rocm-git
  [pockettts.cpp]=pocket-tts.cpp-git
  [pocket-tts]=python-pocket-tts
  [signal-cli-rest-api]=signal-cli-rest-api-git
)

# Reference hashes corresponding to build date (2026-06-14, 2026-05-31, 2026-06-17, and 2026-06-03)
declare -A PKG_REFS=(
  [llama.cpp]="53bd47e"
  [llama-cpp-python]="e807092"
  [stable-diffusion.cpp]="276025e"
  [whisper.cpp]="df7638d8"
  [qwen3-tts.cpp]="2a41916"
  [bitsandbytes]="2177945b"
  [vllm]="6bdabba"
  [vllm-omni]="5dfdf58"
  [pockettts.cpp]="e801e7d"
  [pocket-tts]="v2.1.0"
  [signal-cli-rest-api]="81efbd2"
)

for d in llama.cpp llama-cpp-python stable-diffusion.cpp whisper.cpp qwen3-tts.cpp qwen3-tts-upstream bitsandbytes vllm vllm-omni pockettts.cpp pocket-tts signal-cli-rest-api; do
  echo "=== $d ==="
  cd "scratch/$d" 2>/dev/null || continue
  
  commits=$(git log --since="7 days ago" --no-merges --oneline | wc -l)
  merges=$(git log --since="7 days ago" --merges --oneline | wc -l)
  last_commit=$(git log -1 --format="%ad" --date=short)
  commits_28=$(git log --since="28 days ago" --no-merges --oneline | wc -l)
  avg_commits=$(echo "scale=1; $commits_28 / 4" | bc)
  tags=$(git log --tags --since="7 days ago" --simplify-by-decoration --pretty="format:%d" | tr -d '()' | tr '\n' ',' | sed 's/,$//')
  
  pkg="${PKG_MAP[$d]}"
  pkg_info="not installed" since_commits="-"
  if [ -n "$pkg" ]; then
    pkg_ver=$(pacman -Q "$pkg" 2>/dev/null | awk '{print $2}')
    if [ -n "$pkg_ver" ]; then
      installed_ref="${PKG_REFS[$d]}"
      since_commits=$(git log --no-merges --oneline "${installed_ref}..HEAD" 2>/dev/null | wc -l)
      pkg_info="$pkg_ver (ref=$installed_ref)"
    fi
  fi
  
  echo "commits=$commits merges=$merges last_commit=$last_commit avg_commits=$avg_commits tags=[$tags]"
  echo "pkg=$pkg_info since_installed=$since_commits"
  cd - &>/dev/null
done
```

### Step 5: Gather GitHub Metadata (Stars & Forks)

To update the Stars and Forks metrics, query the GitHub API endpoints:

```bash
for repo in ggml-org/llama.cpp abetlen/llama-cpp-python leejet/stable-diffusion.cpp ggerganov/whisper.cpp khimaros/qwen3-tts.cpp predict-woo/qwen3-tts.cpp bitsandbytes-foundation/bitsandbytes vllm-project/vllm vllm-project/vllm-omni VolgaGerm/PocketTTS.cpp kyutai-labs/pocket-tts bbernhard/signal-cli-rest-api; do
  echo "=== $repo ==="
  curl -L -s "https://api.github.com/repos/$repo" | jq '{stargazers_count, forks_count}'
done
```epo" | jq '{stargazers_count, forks_count}'
done
```
