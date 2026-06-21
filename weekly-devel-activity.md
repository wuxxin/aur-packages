# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Last 7 Days Activity (June 14, 2026 – June 21, 2026)

<!-- START_WEEKLY_ACTIVITY_TABLES -->
### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **llama.cpp** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 117,501 | 19,777 | `master` | 2026-06-21 | **116** | 0 | 86 | 110.2 | ` b9632`, ` b9637` | `9742.r1.gc576070-1` (ref `c576070`) | 0 | **Highly Active** |
| *└─ llama-cpp-python* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,423 | 1,418 | `main` | 2026-06-20 | **7** | 0 | 27 | 22.5 | ` v0.3.30`, ` v0.3.30-cu118` | `9742.r1.gc576070-1` (ref `b11fe07`) | 0 | **Active** |
| *└─ stable-diffusion.cpp* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,323 | 671 | `master` | 2026-06-17 | **9** | 0 | 7 | 15.5 | ` master-703-bb90bfa`, ` master-704-6e66a1a` | `9742.r1.gc576070-1` (ref `7f0e728`) | 0 | **Active** |
| *└─ whisper.cpp* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 50,915 | 5,683 | `master` | 2026-06-19 | **71** | 0 | 3 | 61.0 | ` v1.8.7`, ` v1.9.0` | `9742.r1.gc576070-1` (ref `5ed76e9`) | 0 | **Highly Active** |
| *└─ qwen3-tts.cpp* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) | 16 | 5 | `main` | 2026-06-16 | **1** | 0 | 0 | 0.2 | — | `9742.r1.gc576070-1` (ref `0c8b2ba`) | 0 | **Active** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 205 | 71 | `main` | 2026-06-03 | 0 | 0 | 0 | 0.2 | — | not installed | - | **Stale** |
| **bitsandbytes** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,279 | 873 | `main` | 2026-06-18 | **3** | 0 | 0 | 3.8 | — | `0.49.2.r91.g435b8b33-1` (ref `435b8b33`) | 0 | **Active** |
| **vllm** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 83,452 | 18,278 | `main` | 2026-06-21 | **233** | 0 | 1 | 230.8 | ` v0.23.1rc0` | not installed | - | **Highly Active** |
| **vllm-omni** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 5,223 | 1,148 | `main` | 2026-06-21 | **68** | 0 | 0 | 77.8 | — | not installed | - | **Highly Active** |
| **pockettts.cpp** | [VolgaGerm/PocketTTS.cpp](https://github.com/VolgaGerm/PocketTTS.cpp) | 38 | 8 | `master` | 2026-03-29 | 0 | 0 | 0 | 0.0 | — | `0.1.0.r18.ge801e7d-1` (ref `e801e7d`) | 0 | **Stale** |
| **pocket-tts** | [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 4,637 | 515 | `main` | 2026-06-03 | 0 | 0 | 0 | 0.5 | — | `2.1.0-1` (ref `v2.1.0`) | 0 | **Stale** |

> [!NOTE]
> `vllm`, `bitsandbytes`, `pocket-tts`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,653 | 296 | `master` | 2026-06-11 | 0 | 0 | 0 | 3.5 | — | `0.100.r0.ga4f5855-1` (ref `a4f5855`) | 0 | **Stale** |

> [!NOTE]
> `zeroclaw-git` (upstream: [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw)) is hosted and tracked separately under the `agents-shared` repository.
<!-- END_WEEKLY_ACTIVITY_TABLES -->

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Highly Active (116 commits, 86 tags in the last week, as of June 21).
* **Recent Focus**:
  - **Server**: Added real-time model load progress tracking via `/models/sse` (`d6d89958`), refactored child-to-router communication (`2b686a91`), optimized `get_token_probabilities` (`4b48a53b`), and consolidated slot selection (`80452d65`).
  - **Models & Speculative Decoding**: Supported Step3.5/3.7 flash mtp3 speculative decoding (`d7895274`), supported Eagle3 for Qwen3.5 & 3.6 (`b14e3fb9`), made DSA indexer tensors optional for GLM-DSA (`796f41be`), and added batching support for InternVL in MTMD (`db52540f`).
  - **GGML & System Sync**: Bumped GGML version to `0.15.2` (`1868af13`, `5fd2dc2c`).
  - **Grammar & Parsing**: Refactored `common/peg` until gbnf grammar generation (`063d9c15`) and aligned spacing rules with parsers in `common/json-schema-to-grammar` (`c5760701`).
  - **Hardware Backends & Kernels**:
    - *CPU*: Added support for K tails in power10 Q8/Q4 MMA matmul (`587f602e`). Conditionally enabled power11 backend based on compiler support (`6aff09ac`).
    - *CUDA*: Integrated CUDA col2im 1d kernel (`50fd261d`).
    - *Hexagon*: Added support for fine-grain op-trace logging of HVX/HMX/DMA events (`5cbc2153`), and used padded stride for ssm-conv weights (`4a809431`).
    - *Metal*: Added BF16 support check in concat kernel (`c39dd2db`), implemented `rope_back` operator (`d9115692`), and f16/bf16 support for concat operator (`ad19c982`).
    - *Vulkan*: Recorded actual memory properties during buffer creation (`ae09736e`), prefer host-visible memory buffers on UMA devices (`69457918`), and supported `gated_delta_net` with S_v=16 (`93c02083`).
    - *SYCL*: Renamed `GGML_SYCL_SUPPORT_LEVEL_ZERO` (`4c4f6eac`). Supported MUL_MAT and OUT_PROD with Q1_0 (`69a9798a`). Supported `conv_2d`, `conv_2d_dw`, `conv2d_transpose` (`31203378`). Added dev2dev memcpy by SYCL API (`6772827b`). Supported Conv3D (`01b1c3ad`). Enabled fp16 support for SQR, SQRT, LOG, SIN, COS, CLAMP (`da66f048`). Fixed use-after-free bug in MoE prefill (`fddcda58`). Supported USM system allocations (`dd1a6ca8`).
    - *OpenCL*: Optimized `mul_mat_f16_f32_l4` for decode (`9f785839`).
    - *OpenVINO*: Added OpenVINO 2026.2, context-shift, Q5_1 support, gemma4 dense/embedding, and `-fa off` (`5fa14e99`).
    - *WebGPU*: Added adapter toggles for F16 on Vulkan + NVIDIA (`f449e055`).
  - **Quantization & Metadata**: Used `LLM_KV` for `quantization_version` and `file_type` (`84de01a1`), and handled rope parameters more consistently during conversion (`f4043fec`).

### llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Active (7 commits, 27 tags in the last week, as of June 21).
* **Recent Focus**:
  - **llama.cpp Sync**: Updated llama.cpp to `6e9007ae6` (`541b08c`), `6eab47181` (`824565a`), `e3a74b299` (`822146b`), and `f449e0553` (`7440aaa`).
  - **Features**: Added Pyodide wheel support (`a804233`).
  - **CI & Releases**: Bumped package release version to `v0.3.31` (`b11fe07`) and `v0.3.30` (`ddb6a05`).

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (9 commits, 7 tags in the last week, as of June 21).
* **Recent Focus**:
  - **Features**: Added support for cancelling generations (`5a34bc7`), added PuLID-Flux identity-injection support (`93527fd`), and supported backend-specific max-VRAM budgets (`bb90bfa`).
  - **Fixes**: Normalize CLIP prompts before special-token splitting (`7f0e728`), correct conversion from sd_type_t to ggml_type (`710bc91`), simplify PuLID ID extraction setup (`146b6cc`), and allow oversized Vulkan parameter tensors (`6e66a1a`).
  - **Sync**: Updated `sdcpp-webui` (`92a3b73`) and synced upstream `ggml` commits (`517abc7`).

### whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Highly Active (71 commits, 3 tags in the last week, as of June 21).
* **Recent Focus**:
  - **Release**: Released `v1.9.1` (`f049fff9`) and `v1.9.0`.
  - **Sync & GGML**: Synced talk-llama with latest llama.cpp (`5ed76e9a`), bumped GGML version to `0.15.2` (`f92382f1`), and synced upstream ggml commits (`41cf1278`).
  - **CI**: Added `GGML_NATIVE=OFF` and `GGML_BMI2=OFF` to `windows-blas` CI matrix (`200b1197`).

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Status**: Active (1 commit on downstream fork, 0 commits on origin, as of June 21).
* **Fork Focus**:
  - Downstream fork added support for more audio formats using ffmpeg/libavcodec (`0c8b2ba`).

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Active (3 commits, as of June 21).
* **Recent Focus**:
  - **CI & Fixes**: Fixed CI matrices, pinned GitHub Actions to SHA, and added Dependabot for automatic updates (`435b8b3`). Performed miscellaneous cleanup/improvements (`78a8478`) and added compatibility for Windows 2025 + VS2026 (`aee0ebb`).

### vLLM (`vllm-project/vllm`)
* **Status**: Highly Active (233 commits, 1 tag in the last week, as of June 21).
* **Recent Focus**:
  - **Performance & Scheduler**: Optimized scheduler by skipping/shrinking `all_token_ids` copies for non-async and V2 runners (`6e919960`). Optimized Qwen3-VL multi-video prompt processing (`d272418f`). Exposed CPU cache usage metric for KV offloading (`3b4a76b6`).
  - **KV Connector & Offloading**: Compacted chunk-hash keys and introduced zero-copy lookup wire format for Mooncake (`ab7fcbdd`). Supported packed HMA KV cache layout (`cc22621b`). Added SimpleCPUOffloadConnector with PCP + DCP support (`c88d3d47`). Supported packing KV caches into contiguous per-block allocations for DeepSeek V4 (`01192139`).
  - **Models & Emulation**: Supported block-FP8 shared expert TEP=16 in DeepSeek-V4 (`2a6c6b94`), fixed NVFP4/OCP MX MoE emulation (`a346d589`), and fixed memory pointer overflow in Mamba state buffers (`b5495cc5`).
  - **Frontend & API**: Added cache usage reporting to Anthropic `/v1/messages` API endpoint (`891cc4b9`).
  - **ROCm/AMD GPU Backend**: Fixed ROCm Sparse Indexer bug (`1bdf9810`). Unlocked AITER hipBLASLt accuracy tests using vLLM's fp8 quant max (`dec860fb`). Fixed VRAM leaks in Phi3V testing (`0fbf42af`).
  - **Bugfixes**: Prevented `U+FFFD` leaks at reasoning-to-content transition in engine parsers (`859e4d43`), avoided `gridDim.y` overflow for large row counts (`93bad119`), fixed `min_tokens` off-by-one in V2 GPU sampler (`183a430c`), and added OpenAI schema validation fixes.

### vllm-omni (`vllm-project/vllm-omni`)
* **Status**: Highly Active (68 commits, as of June 21).
* **Recent Focus**:
  - **Audio & TTS Models**: Fixed Qwen3-Omni `Code2Wav` CUDA-graph output length surplus (`cead6152`). Batched matmul and embedding gather in MOSS-TTS talker (`63ba11b8`). Fixed MOSS-TTS cross-request audio corruption under batching (`1228a109`). Added Voxtral TTS recipe details for 1x RTX A6000 48GB (`13e9094b`).
  - **Diffusion Models & Pipelines**: Added GR00T-N1.7 pipeline with OpenPI serving (`2d0b1d8a`), simplified CacheDiT integration (`6ff246bf`), configured video storage backends with TTL (`951ae28e`), enabled regional compilation for Cosmos3 HSDP blocks (`14d70d98`), supported NVFP4 W4A4 serving on Blackwell (`2f64c712`), and fixed diffusion profile RPC None results (`1292c478`).
  - **Multimodal & Interaction**: Added JoyAI-VL-Interaction streaming serving layer (`e241005a`), migrated helios example (`950e66a4`), and added Cosmos3 transfer (`a1e1ac01`).
  - **Core & Integration**: Aligned vLLM Omni Request input signature with upstream vLLM (`17cf60a6`). Fixed HSDP + FP8 online quantization compatibility (`7e152ca6`). Supported CUDA graph, torch.compile, and DiT Caching for DreamZero (`f05e03ae`).
  - **Testing**: Added `vllm-omni-test` agent skill for CI-aligned test generation (`dff8cda8`).

### PocketTTS.cpp (`VolgaGerm/PocketTTS.cpp` & `kyutai-labs/pocket-tts`)
* **Status**: Stale (0 commits in the last week, as of June 21).
* **Recent Focus**:
  - No new commits in the last week. `pocket-tts.cpp-git` (upstream clone version `0.1.0.r18.ge801e7d`) and `python-pocket-tts` (upstream version `2.1.0`) remain stable with no new upstream changes.

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
* **Status**: Active (0 commits in the last week, as of June 21).
* **Recent Focus**:
  - No new commits in the last week. The package is running signal-cli v0.14.5.

### Custom AUR Repository Updates
* **Recent Focus**:
  - **PocketTTS Integration**: Added support for VolgaGerm's C++ PocketTTS wrapper (`pocket-tts.cpp-git` at `0.1.0.r18.ge801e7d`) and the python binding (`python-pocket-tts` at `2.1.0`).
  - **libggml-git-hip**: Updated to build version `9743.r0.gc576070` to align with upstream changes and updated patches.
  - **zeroclaw-git**: Upgraded package to version `0.8.1.r16.g13a8a857ae` to package the newly tagged `v0.8.1` release.
  - **AGENTS.md**: Updated styling guidelines and command examples for shell and python scripts.

---

## 📋 Instruction Guide: Recreating this Analysis

> [!TIP]
> **Fully Automated Update**: You can run the automation script `scripts/update-activity.py` with the `--write` (or `-w`) flag to automatically pull all repository updates, calculate the statistics, and write the updated tables directly back into this file:
> ```bash
> python scripts/update-activity.py --write
> ```
> For manual reproduction steps, follow the guide below.

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

# Robustly resolve the installed commit reference hash
get_installed_ref() {
  local d="$1"
  local pkg="$2"
  local src_path=""
  case "$d" in
    llama.cpp) src_path="libggml-git-hip/src/llama.cpp" ;;
    llama-cpp-python) src_path="libggml-git-hip/src/llama-cpp-python" ;;
    stable-diffusion.cpp) src_path="libggml-git-hip/src/stable-diffusion.cpp" ;;
    whisper.cpp) src_path="libggml-git-hip/src/whisper.cpp" ;;
    qwen3-tts.cpp) src_path="libggml-git-hip/src/qwen3-tts.cpp" ;;
    bitsandbytes) src_path="python-bitsandbytes-rocm-git/src/bitsandbytes" ;;
    pockettts.cpp) src_path="pocket-tts.cpp-git/src/pockettts.cpp" ;;
    signal-cli-rest-api) src_path="signal-cli-rest-api-git/src/signal-cli-rest-api" ;;
  esac

  # 1. Attempt to read from build tree checkout if present
  if [ -n "$src_path" ] && [ -d "$src_path/.git" ]; then
    git -C "$src_path" rev-parse --short=7 HEAD 2>/dev/null
    return
  fi
  
  # 2. Attempt to parse git hash from pacman package version suffix
  if [ -n "$pkg" ]; then
    local pkg_ver
    pkg_ver=$(pacman -Q "$pkg" 2>/dev/null | awk '{print $2}')
    if [ -n "$pkg_ver" ]; then
      local parsed_ref
      parsed_ref=$(echo "$pkg_ver" | sed -nE 's/.*\.g([0-9a-f]{7,})(-.*)?$/\1/p')
      if [ -n "$parsed_ref" ]; then
        echo "$parsed_ref"
        return
      fi
    fi
  fi
  
  # 3. Fallback default hashes (June 21, 2026 baseline)
  case "$d" in
    llama.cpp) echo "c576070" ;;
    llama-cpp-python) echo "b11fe07" ;;
    stable-diffusion.cpp) echo "7f0e728" ;;
    whisper.cpp) echo "5ed76e9a" ;;
    qwen3-tts.cpp) echo "0c8b2ba" ;;
    bitsandbytes) echo "435b8b3" ;;
    vllm) echo "6bdabba" ;;
    vllm-omni) echo "5dfdf58" ;;
    pockettts.cpp) echo "e801e7d" ;;
    pocket-tts) echo "v2.1.0" ;;
    signal-cli-rest-api) echo "a4f5855" ;;
  esac
}

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
      installed_ref=$(get_installed_ref "$d" "$pkg")
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
```
