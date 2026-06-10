# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Last 7 Days Activity (June 4, 2026 – June 10, 2026) 

### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **libggml-git-hip** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 115,880 | 19,411 | `master` | 2026-06-10 | **35** | 0 | 28 | 113.7 | `b9587`, `b9586` | `9442.r0.gd4c8e2c-1` (built 2026-05-31) | 146 | **Active** |
| *└─ python-llama-cpp-git-ggml-hip* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,388 | 1,413 | `main` | 2026-06-10 | **13** | 0 | 13 | 20.2 | `v0.3.28` | `9442.r0.gd4c8e2c-1` (ref `fdf38b3`) | 70 | **Active** |
| *└─ stable-diffusion.cpp-git-ggml-hip* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,223 | 652 | `master` | 2026-06-08 | **3** | 0 | 3 | 22.2 | `master-685-19bdfe2` | `9442.r0.gd4c8e2c-1` (ref `d2797b8`) | 25 | **Active** |
| *└─ whisper.cpp-git-ggml-hip* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 50,611 | 5,652 | `master` | 2026-06-09 | **47** | 0 | 0 | 63.0 | — | `9442.r0.gd4c8e2c-1` (ref `2e045a9`) | 62 | **Highly Active** |
| *└─ qwen3-tts.cpp-git-ggml-hip* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) (Fork) | 14 | 3 | `main` | 2026-04-21 | **0** | 0 | 0 | 0.0 | — | `9442.r0.gd4c8e2c-1` (ref `2a41916`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 200 | 64 | `main` | 2026-06-03 | **0** | 0 | 0 | 0.2 | — | — | — | **Stale** |
| **python-bitsandbytes-rocm-git** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,264 | 866 | `main` | 2026-06-01 | **0** | 0 | 0 | 2.7 | — | `head.r1155.g2177945b-1` (built 2026-05-31) | 2 | **Active** |
| **python-vllm-rocm-git** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 82,396 | 17,879 | `main` | 2026-06-10 | **94** | 0 | 0 | 218.2 | — | not installed | — | **Highly Active** |
| **python-vllm-omni-rocm-git** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 5,065 | 1,091 | `main` | 2026-06-10 | **28** | 0 | 0 | 77.0 | — | not installed | — | **Highly Active** |

> [!NOTE]
> `vllm`, `bitsandbytes`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api-git** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,610 | 289 | `master` | 2026-06-01 | **0** | 0 | 0 | 6.0 | — | `0.100.pre.r0.g81efbd2-1` (built 2026-06-03) | 0 | **Active** |

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Active (35 commits, 28 tags in the last week, as of June 10).
* **Recent Focus**:
  - **Model Support & Core**: Supported Granite speech models under non-deepstack inference by applying embedding scaling (`d73cd0767`); added MTP support for Gemma-4 E2B and E4B assistants (`7d2b45b4f`); resolved Plamo2 attention key/value length regressions (`f0152efe4`). Introduced speculative decoding fixes for logging (`d2e22ed97`) and added the `GGML_OP_COL2IM_1D` operator (`26021699b`).
  - **Hardware Backends**:
    - *Vulkan*: Optimized memory by reducing shared memory usage in `iq1` `mul_mm` (`d6d0ce821`), added `v_dot2_f32_f16` matrix multiplication and Flash Attention support (`b4e3dc613`), and integrated `cm2` decode vectors for B matrix loading (`c74759a24`).
    - *HIP (AMD ROCm)*: Added RDNA3.5 support with architectures `gfx1152` and `gfx1153` (`19bba67c1`).
    - *Metal / WebGPU*: Fixed audio model `im2col` 1D indexing for Metal (`daf6bc9f2`). Refactored WebGPU k-quants matmul for better prefill speeds (`1e1aca09d`).
  - **Server & WebUI**: Implemented pinned conversations in the chat interface (`76da2450a`); added an opt-in `run_javascript` frontend tool (`483609509`); fixed mobile UI overflows and styled hover effects to decrease style recalculation overhead (`ae735b131`, `efbacf8d2`). Added local server prompt logging (`1e912561d`).

### llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Active (13 commits, 13 tags in the last week, as of June 10).
* **Recent Focus**:
  - **llama.cpp Sync**: Updated llama.cpp upstream dependency to commit `76da2450a` (`b5eefc8`).
  - **Features & Examples**: Enabled server video input and Gemma text tool calling examples (`051dda2`); added an OpenAI-compatible embeddings endpoint (`fe927bd`); aligned server MTP support with upstream (`fddee27`); corrected tool calling configs (`e8191f0`).
  - **Bugfixes & CI**: Repaired Linux accelerator wheel builds in CI (`7eb494d`); corrected duplicate streamed response deltas and aligned response schema parsing boundaries (`411e0f4`, `a72325b`). Bumped version to `v0.3.28`.

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (3 commits, 3 tags in the last week, as of June 10).
* **Recent Focus**:
  - **Features**: Added tensor name settings on block parameters (`19bdfe2`).
  - **APG & Optimizations**: Normalized `diff_norm` calculations by tensor size for Adaptive Projected Guidance (`138da14`); capped planning budget when model sizes disproportionately dwarf streaming budgets to optimize CPU offloading (`17a2b4a`).

### whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Highly Active (47 commits in the last week, as of June 10).
* **Recent Focus**:
  - **Sync & Versioning**: Substantially updated internal `ggml` dependency to `0.14.0` and integrated a large batch of backported `llama.cpp` optimizations and bugfixes.
  - **Platform-Specific Support**: CoreML backend fixed `--quantize` crashes for mlprogram format and corrected `--optimize-ane` labels (`ba573929`). Synced `talk-llama` helper tool implementation with recent upstream changes (`84bd03a4`).
  - **CI/CD**: Pinned all GitHub Actions workflow actions to exact commit SHAs (`df7638d8`).

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Status**: Stale (0 commits in the last week on both repos).
* **Fork & Feature Parity**:
  - Maintained downstream changes (Flash Attention, static KV cache, OpenAI-compatible TTS server). No new features or maintenance commits were registered this week.

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Stale (0 commits in the last week).
* **Recent Focus**:
  - No new commits since June 1. Maintainer focus remains on stabilization of nightly workflows.

### vLLM (`vllm-project/vllm`)
* **Status**: Highly Active (94 commits in the last week, as of June 10).
* **Recent Focus**:
  - **ROCm & AMD Optimizations**: Added fused AllReduce + RMSNorm + per-group FP8 quantization kernel to support DSv3.2 indexer fan-outs (`80e2c4462`); enabled fused softplus-sqrt-topk router under AITER fused-MoE (`01d8cd92d`); resolved Llama EAGLE compilation issues when `ROCM_AITER_FA` is enabled (`c9c1540e6`); stabilized sleep-mode memory release (`2385e140d`).
  - **Model Support & Kernels**: Unified Gemma4 FlashAttention-4 layers and mm_prefix support (`6deb05e0e`). Integrated DeepEP v2 for WideEP routing (`e2f993dc4`) and resolved DeepSeek V4 out-of-memory bugs (`d7607ad27`). Added online FP8 per-tensor parameter-wise calibration (PTPC) (`753e9d55e`). Fused QK RMSNorm + RoPE gate for Qwen 3.5 (`7a89b7256`).
  - **Rust Frontend & APIs**: Added API key authorization (`d841386d2`), `/tokenize` and `/detokenize` endpoints (`69fdaffbc`), Kimi K2 tool call ID mapping (`1c23c4203`), and engine control endpoints (`/pause`, `/resume`, `/is_paused`) (`3c0b4432b`).
  - **Security & Fixes**: Mitigated denial-of-service vulnerability from audio decompression bombs in speech endpoints (`1b1359c33`); fixed image EXIF orientation handling (`cf1c90672`).

### vllm-omni (`vllm-project/vllm-omni`)
* **Status**: Highly Active (28 commits in the last week, as of June 10).
* **Recent Focus**:
  - **TTS & Audio Optimizations**: Fused CosyVoice serving with TensorRT to optimize TTFP and throughput (`f1bf5442`). Patched Fish Speech prefix cache collision issues via missing `cache_salt` parameter (`d50bf1aa`). Introduced prefix-cache OOM guards and orchestrated micro-optimizations in Qwen3-TTS hot paths (`57227dc7`).
  - **Model Integrations**: Integrated `moriio` transfer engine (`e1b0b832`). Added LoRA support to SenseNova-U1 (`3753b21c`). Enabled parallel VAE decoding for LTX-2.3 models (`bf03413c`) and kept its auxiliary modules resident in GPU memory by default (`13f9ecae`).
  - **Quantization & Core**: Configured default Blackwell FP8 GEMMs to route through quack CuteDSL fused-bias kernels (`b5352a58`). Supported Cosmos3 video-to-video generation tasks (`2f251957`).

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
* **Status**: Stale (0 commits in the last week).
* **Recent Focus**:
  - No new commits since June 1.

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
| **signal-cli-rest-api** | `bbernhard/signal-cli-rest-api` | `signal-cli-rest-api-git` | AUR VCS (`-git`) |

### Step 2: Probe Installed System Versions

Run `pacman -Q` on the target package names to retrieve their current installed version and git commit hashes:

```bash
for pkg in libggml-git-hip python-llama-cpp-git-ggml-hip stable-diffusion.cpp-git-ggml-hip whisper.cpp-git-ggml-hip qwen3-tts.cpp-git-ggml-hip python-bitsandbytes-rocm-git python-vllm-rocm-git python-vllm-omni-rocm-git signal-cli-rest-api-git; do
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
for r in llama.cpp llama-cpp-python stable-diffusion.cpp whisper.cpp qwen3-tts.cpp qwen3-tts-upstream bitsandbytes vllm vllm-omni signal-cli-rest-api; do
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
  [signal-cli-rest-api]=signal-cli-rest-api-git
)

# Reference hashes corresponding to build date (2026-05-31 and 2026-06-03)
declare -A PKG_REFS=(
  [llama.cpp]="d4c8e2c"
  [llama-cpp-python]="fdf38b3"
  [stable-diffusion.cpp]="d2797b8"
  [whisper.cpp]="2e045a9"
  [qwen3-tts.cpp]="2a41916"
  [bitsandbytes]="2177945b"
  [vllm]="6bdabba"
  [vllm-omni]="5dfdf58"
  [signal-cli-rest-api]="81efbd2"
)

for d in llama.cpp llama-cpp-python stable-diffusion.cpp whisper.cpp qwen3-tts.cpp qwen3-tts-upstream bitsandbytes vllm vllm-omni signal-cli-rest-api; do
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
for repo in ggml-org/llama.cpp abetlen/llama-cpp-python leejet/stable-diffusion.cpp ggerganov/whisper.cpp khimaros/qwen3-tts.cpp predict-woo/qwen3-tts.cpp bitsandbytes-foundation/bitsandbytes vllm-project/vllm vllm-project/vllm-omni bbernhard/signal-cli-rest-api; do
  echo "=== $repo ==="
  curl -L -s "https://api.github.com/repos/$repo" | jq '{stargazers_count, forks_count}'
done
```
