# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Weekly Activity (May 23, 2026 – May 29, 2026)

### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **libggml-git-hip** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 113,629 | 18,914 | `master` | 2026-05-29 | **121** | 0 | 59 | 104.7 | `b9406`, `b9405` | `9320.r13.g35c9b1f-1` (built 2026-05-26) | 80 | **Highly Active** |
| *└─ python-llama-cpp-git-ggml-hip* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,348 | 1,411 | `main` | 2026-05-24 | **2** | 0 | 0 | 4.7 | `v0.3.23` | `9320.r13.g35c9b1f-1` (ref `3bda091`) | 0 | **Active** |
| *└─ stable-diffusion.cpp-git-ggml-hip* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,116 | 631 | `master` | 2026-05-27 | **14** | 0 | 12 | 15.7 | `master-656-0e4ee04` | `9320.r13.g35c9b1f-1` (ref `1ceb5bd`) | 6 | **Active** |
| *└─ whisper.cpp-git-ggml-hip* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 50,243 | 5,583 | `master` | 2026-05-29 | **108** | 0 | 1 | 51.0 | `v1.8.5` | `9320.r13.g35c9b1f-1` (ref `e0fd1f67`) | 44 | **Highly Active** |
| *└─ qwen3-tts.cpp-git-ggml-hip* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) (Fork) | 14 | 3 | `main` | 2026-04-21 | **0** | 0 | 0 | 0.0 | — | `9320.r13.g35c9b1f-1` (ref `2a41916`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 184 | 61 | `main` | 2026-03-09 | **0** | 0 | 0 | 0.0 | — | — | — | **Stale** |
| **python-bitsandbytes-rocm-git** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,236 | 856 | `main` | 2026-05-28 | **4** | 0 | 1 | 3.0 | `continuous-release_main` | `head.r1054.g17d32f15-1` (built 2026-01-22) | 92 | **Active** |
| **python-vllm-rocm-git** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 81,346 | 17,389 | `main` | 2026-05-29 | **218** | 0 | 5 | 209.7 | `v0.22.0`, `v0.22.0rc3` | `0.21.1rc0.r301.g445ded1-1` (built 2026-05-26) | 132 | **Highly Active** |
| **python-vllm-omni-rocm-git** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 4,834 | 1,014 | `main` | 2026-05-29 | **78** | 0 | 1 | 78.7 | `v0.21.0rc2` | `0.21.0rc2.r13.ge459fdb-1` (built 2026-05-26) | 54 | **Highly Active** |

> [!NOTE]
> `vllm`, `bitsandbytes`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api-git** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,586 | 283 | `master` | 2026-05-28 | **10** | 1 | 0 | 9.0 | — | `0.99.r38.g5c0bd05-2` (built 2026-05-17) | 10 | **Active** |

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Highly Active (121 commits, 59 tags in the last week).
* **Recent Focus**:
  - **CUDA & GPU Optimizations**: Disabled `launch_fattn` PDL enrollment due to compiler bugs; auto-applied iGPU flags for integrated CUDA/HIP devices; added Vulkan Release-build adjustments to minimize ccache bloat.
  - **Multi-Modal Support**: Corrected `n_head_kv` default settings in MiniCPM-V-like architectures (MTMD); resolved pre-normalization issues in the Gemma 4 projector; fixed audio RMS-norm epsilon parameters.
  - **Backend Integrations**: Introduced basic/generic operator fusion and RMS_NORM+MUL fusion on Hexagon processors; resolved a missing buffer set in the fallback clearing routine for allreduce operations.
  - **Usability & Build Improvements**: Relocated application licenses to the `llama-app` package; enhanced help interface output; fixed audio and video modality detection in the Web UI.

### llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Active (2 commits in the last week).
* **Recent Focus**:
  - **Submodule Maintenance**: Updated `llama.cpp` dependency submodules to latest versions (`c0c7e147e` and `b9a2170fc`).
  - **Migration**: Moved upstream `llama.cpp` submodule tracking from `ggerganov/llama.cpp` to the new `ggml-org` organization.
  - **Embedding Refactors**: Auto-configured `kv_unified=True` when running embeddings to allow correct batch processing; configured `n_seq_max` specifically for batched embedding jobs.

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (14 commits in the last week).
* **Recent Focus**:
  - **New Architectures**: Added native support for Longcat-Image and Longcat-Image-Edit; supported Microsoft Lens model loads.
  - **Image Generation Pipeline**: Enabled temporal and rational latent upscaling for LTX video pipelines; optimized VAE decode by stripping trailing latent channels; corrected VAE loading defaults (TAE) for models running Flux2 VAE.
  - **BLAS & CPU/GPU Bindings**: Restructured and simplified parameter bindings in the main diffusion runner; resolved host symbol naming checks; ensured ROCm BLAS runtime dlls package correctly inside Windows distributions.

### whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Highly Active (108 commits, 1 tag in the last week).
* **Recent Focus**:
  - **Synchronization**: Regularly pulled modifications from the upstream `ggml` library and bumped `ggml` versioning parameters to 0.13.1.
  - **Hardware acceleration updates**: Inherited CUDA/HIP integrated device identification configurations from llama.cpp; implemented faster Vulkan paths for Walsh-Hadamard transforms.
  - **Speech-specific patches**: Synchronized internal `talk-llama` sub-applications against newer llama.cpp interfaces.

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Status**: Stale (0 commits in the last week on both repos).
* **Fork & Feature Parity**:
  - The split package `qwen3-tts.cpp-git-ggml-hip` is built from **`khimaros/qwen3-tts.cpp`**, which is a downstream fork of **`predict-woo/qwen3-tts.cpp`** (the original author's repository, which has 184 stars but has not received updates since March 9, 2026).
  - The downstream `khimaros` fork was created to address several performance regressions and add integration patches: it introduces **Flash Attention** support, implements a **static KV cache**, caches the vocoder graph to prevent re-compilation latency, refactors C FFI embeddings extraction, and implements an **OpenAI-compatible TTS server** with batch conversion support. Its last commit was on April 21, 2026 (`2a41916`), implementing streaming vocoder decodes using chunked KV/tail state.

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Active (4 commits in the last week).
* **Recent Focus**:
  - **Compiler Fixes**: Resolved OpenMP loop-inlining target option mismatches under GCC 16.
  - **Quantization & Kernels**: Integrated a per-device `cudaFuncSetAttribute` cache to mitigate GEMM launch overheads; rolled out new 4-bit GEMM inference kernels; cleaned up deprecated code and CPU activation check mutations.
  - **Platform & PyTorch Support**: Lifted the minimum PyTorch requirement to 2.4 and optimized validation warnings; bumped supported Linux ROCm targets to 7.2.3 and enabled Windows compilation workflows for ROCm 7.2.1; added Intel XPU support for blockwise quantization.

### vLLM (`vllm-project/vllm`)
* **Status**: Highly Active (218 commits in the last week).
* **Recent Focus**:
  - **AMD ROCm Backend**: Cleaned up decode-step orchestration for the MI355X architecture (achieving several performance micro-opts); resolved AITER MXFP4 MoE weight loading/shuffling issues; added native W4A16 kernels for AMD RDNA3 (gfx1100).
  - **Intel XPU Backend**: Implemented Multi-Token Prediction (MTP) for gdn attention models; expanded XPU support to Gelu Tanh activation in MoE layers.
  - **Attention & Kernel Core**: Debugged corrupted MLA + linear attention paths; proceeded with the transition of attention and caching kernels to PyTorch's stable ABI; introduced Triton-based top-k/top-p sampling on CPU.
  - **Engine & Scheduling**: Fixed pipeline parallel KeyErrors for residual tensors; excluded decode-phase blocks from CPU KV offloading; optimized CPU core binding (PCT priority) on DGX B300.

### vllm-omni (`vllm-project/vllm-omni`)
* **Status**: Highly Active (78 commits in the last week).
* **Recent Focus**:
  - **Audio & Speech Modeling**: Supported voice cloning (zero-shot) for omnivoice in online endpoints; introduced CosyVoice3Model support on Intel XPUs; consolidated Code2Wav CUDA Graph bucket configurations for Qwen3-TTS.
  - **Diffusion & Graphics**: Integrated prompt embedding caching for diffusion pipelines; added SageAttention3 diffusion backend support on NVIDIA Blackwell (GB200/B200) architectures.
  - **Distributed & Cache Optimization**: Fixed DistributedVaeExecutor IndexErrors when the parallel size is smaller than the world size; resolved prefix-caching behavior issues; stabilized FP8 Z-Image quality gates in CI.

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
* **Status**: Active (10 commits in the last week).
* **Recent Focus**:
  - **Build Integrity**: Fixed Gradle integration and manual download hooks in CI; resolved Docker image packaging bugs and updated Go dependencies (`go.sum`).
  - **Core Updates**: Upgraded the underlying `signal-cli` to `v0.14.4.1`; restructured the JSON schema generation pipelines to build directly from signal-cli source trees.
  - **Extensibility**: Improved the plugin interface architecture and bundled a native SQLite3 plugin.
  - **Bugfixes**: Added safeguards against slice out-of-range crashes occurring during base64 attachment extraction.

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

# Reference hashes corresponding to build date (2026-05-26 02:02:15)
declare -A PKG_REFS=(
  [llama.cpp]="35c9b1f"
  [llama-cpp-python]="3bda091"
  [stable-diffusion.cpp]="1ceb5bd"
  [whisper.cpp]="e0fd1f67"
  [qwen3-tts.cpp]="2a41916"
  [bitsandbytes]="17d32f15"
  [vllm]="445ded1"
  [vllm-omni]="e459fdb"
  [signal-cli-rest-api]="5c0bd05"
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
