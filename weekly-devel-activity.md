# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Last 7 Days Activity (June 4, 2026 – June 10, 2026) 

### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **libggml-git-hip** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 116,019 | 19,459 | `master` | 2026-06-10 | **96** | 0 | 69 | 111.7 | `b9592`, `b9591` | `9590.r0.gd2462f8-1` (built 2026-06-10) | 5 | **Highly Active** |
| *└─ python-llama-cpp-git-ggml-hip* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,394 | 1,414 | `main` | 2026-06-10 | **38** | 0 | 38 | 20.2 | `v0.3.28` | `9590.r0.gd2462f8-1` (ref `b5eefc8`) | 1 | **Active** |
| *└─ stable-diffusion.cpp-git-ggml-hip* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,228 | 653 | `master` | 2026-06-08 | **13** | 0 | 13 | 22.2 | `master-685-19bdfe2` | `9590.r0.gd2462f8-1` (ref `19bdfe2`) | 0 | **Active** |
| *└─ whisper.cpp-git-ggml-hip* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 50,635 | 5,652 | `master` | 2026-06-09 | **55** | 0 | 0 | 63.0 | — | `9590.r0.gd2462f8-1` (ref `df7638d8`) | 0 | **Highly Active** |
| *└─ qwen3-tts.cpp-git-ggml-hip* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) (Fork) | 14 | 3 | `main` | 2026-04-21 | **0** | 0 | 0 | 0.0 | — | `9590.r0.gd2462f8-1` (ref `2a41916`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 200 | 65 | `main` | 2026-06-03 | **0** | 0 | 0 | 0.2 | — | — | — | **Stale** |
| **python-bitsandbytes-rocm-git** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,264 | 868 | `main` | 2026-06-10 | **4** | 0 | 1 | 3.7 | `continuous-release_main` | `head.r1155.g2177945b-1` (built 2026-05-31) | 6 | **Active** |
| **python-vllm-rocm-git** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 82,503 | 17,923 | `main` | 2026-06-10 | **227** | 0 | 0 | 219.2 | — | not installed | — | **Highly Active** |
| **python-vllm-omni-rocm-git** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 5,088 | 1,096 | `main` | 2026-06-11 | **71** | 0 | 1 | 78.5 | `v0.22.0` | not installed | — | **Highly Active** |

> [!NOTE]
> `vllm`, `bitsandbytes`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api-git** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,618 | 290 | `master` | 2026-06-01 | **0** | 0 | 0 | 6.0 | — | `0.100.pre.r0.g81efbd2-1` (built 2026-06-03) | 0 | **Active** |

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Highly Active (96 commits, 69 tags in the last week, as of June 10).
* **Recent Focus**:
  - **Vocab & Tokenization**: Adopted the leading `TemplateProcessing` special token as BOS (`1bfbdb13`). Refactored normalizer flags into a structured option configuration and added `strip_accents` (`68f30663`).
  - **Server & WebUI**: Added checkpoint skipping functionality in the server when beyond `pos_next` (`db94854f`). Implemented pinned conversations in the chat interface (`76da2450`). Added an opt-in `run_javascript` frontend tool (`48360950`). Styled hover effects to decrease style recalculation overhead (`ae735b13`) and resolved mobile UI form layout overflows (`efbacf8d`).
  - **Hardware Backends & Kernels**:
    - *Vulkan*: Optimized shared memory utilization in `iq1` `mul_mm` kernels (`d6d0ce82`), and added matrix multiplication and Flash Attention support via `v_dot2_f32_f16` (`b4e3dc61`).
    - *CUDA*: Fixed data-races in `ssm_scan_f32` (`fb83cc9a`).
    - *Core & Speech*: Resolved Granite speech model inference errors by scaling embeddings when not using deepstack (`d73cd076`). Removed duplicate device-to-device (D2D) memory copies in MTP pipelines (`e95dae18`).
  - **Dependencies**: Updated the LibreSSL vendor code base to version 4.3.2 (`ac4cddeb`).

### llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Active (38 commits, 38 tags in the last week, as of June 10).
* **Recent Focus**:
  - **llama.cpp Sync**: Regularly bumped the upstream llama.cpp dependency commit, culminating in syncs with `ac4cddeb0` (`19ea70c`) and `76da2450a` (`b5eefc8`).
  - **Features & Endpoints**: Added support for server video input streams and Gemma text tool call execution (`051dda2`). Enabled an OpenAI-compatible `/v1/embeddings` endpoint (`fe927bd`). Aligned server speculative MTP settings with upstream updates (`fddee27`).
  - **Bugfixes & CI**: Corrected GPT-OSS tool calling configurations (`e8191f0`). Derived streaming response parser boundaries from the input schema (`411e0f4`). Repaired Linux accelerator wheel build tasks in CI pipelines (`7eb494d`). Bumped release version to `v0.3.28`.

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (13 commits, 13 tags in the last week, as of June 10).
* **Recent Focus**:
  - **Features**: Integrated support for Ideogram v4 models (`b9254dd`). Organized model config detection logic (`cfbc19d`) and model source layout files (`f3fd359`).
  - **Optimizations & Architecture**: Extracted the Wan VAE implementation into dedicated components (`dfb2390`). Ratcheted streaming budgets to stop planners from re-merging model weights at every step (`0648f44`). Optimized parameter loading by allocating CPU-offloaded weights from pinned device host buffers (`064001b`). Enabled custom tensor names on block parameters (`19bdfe2`).

### whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Highly Active (55 commits in the last week, as of June 10).
* **Recent Focus**:
  - **Backend & Sync**: Bumped the internal ggml dependency version to `0.14.0` (`b31466b4`). Synced the `talk-llama` helper tool implementation with recent upstream modifications (`84bd03a4`).
  - **Hardware Backends**: Patched the CoreML backend to resolve crashes during mlprogram `--quantize` operations, and aligned `--optimize-ane` label options (`ba573929`). Enabled support for RDNA 3.5 architectures (specifically `gfx1152` and `gfx1153`) under ROCm HIP (`4669631d`). Fixed Metal audio model `im2col` 1D indexing bugs (`2c139c2e`).
  - **CI/CD**: Hardened workflows by pinning all GitHub Actions to exact commit SHA references (`df7638d8`).

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Status**: Stale (0 commits in the last week on both repos).
* **Fork & Feature Parity**:
  - Downstream remains synchronized. No new feature commits or maintenance updates were registered during this weekly cycle.

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Active (4 commits, 1 tag in the last week, as of June 10).
* **Recent Focus**:
  - **Performance**: Optimized CPU performance paths for x64 and arm64 architectures (`f82277b`). Enhanced default/fallback backend components for blockwise quantization operations (`f0e5b85`).
  - **CI/CD**: Resolved failures in the continuous-release GitHub Actions workflow (`9dad665`).

### vLLM (`vllm-project/vllm`)
* **Status**: Highly Active (227 commits in the last week, as of June 10).
* **Recent Focus**:
  - **Hardware & ROCm Backend**: Configured intermediate padding variables to be TP-aware in `rocm_aiter_fused_experts` (`5b6b536f`). Migrated MI300 ROCm CI test suites to MI325 configurations (`16282a9c`). Added a scalar fallback implementation for CPU-based W4A8 INT4 GEMM (`f06aefb4`). Enabled RISC-V targets to execute oneDNN W8A8 INT8 kernels (`f31bc2ea`).
  - **Security & Bugfixes**: Guarded endpoints against denial-of-service threats by explicitly rejecting non-finite values for temperature and repetition penalty settings (`d598d239`). Patched an information disclosure vector caused by int32 truncation bugs in GGUF dequantizer routines (`f219788f`).
  - **APIs & Features**: Implemented support for the prompt parameter in `v1/audio/transcriptions` for `qwen3-asr` model workflows (`12f3f19c`). Populated `cached_token_count` metrics in Rust completion responses (`5d5591d9`). Integrated a Mooncake prefix-cache retention interval for sparse attention patterns (`f272dfdc`).

### vllm-omni (`vllm-project/vllm-omni`)
* **Status**: Highly Active (71 commits, 1 tag in the last week, as of June 10).
* **Recent Focus**:
  - **TTS & Audio Models**: Fixed prefix cache corruption on qwen3-tts by dropping the per-key size limit (`0342827d`). Enabled VoxCPM2 support on NPUs (`0d3c259a`) and fixed VoxCPM2 concurrent speech quality bugs (`1fe267d6`). Optimized TTFP and inference throughput for CosyVoice pipelines using TensorRT (`f1bf5442`). Integrated Voxtral TTS and Ming-omni-tts dense 0.5B pipelines (`aa92a3a3`, `2fa4c7a4`).
  - **Optimizations & Engine**: Enabled parallel VAE decoding for LTX-2.3 models (`bf03413c`). Purged chunk-transfer zombie processes on every scheduling tick to keep engine cores stable upon client-side abort actions (`73df8326`).
  - **Release**: Released version `v0.22.0` (`v0.22.0`).

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

# Reference hashes corresponding to build date (2026-06-10, 2026-05-31, and 2026-06-03)
declare -A PKG_REFS=(
  [llama.cpp]="d2462f8"
  [llama-cpp-python]="b5eefc8"
  [stable-diffusion.cpp]="19bdfe2"
  [whisper.cpp]="df7638d8"
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
