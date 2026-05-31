# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Weekly Activity (May 25, 2026 – May 31, 2026)

### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **libggml-git-hip** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 113,921 | 18,981 | `master` | 2026-05-31 | **134** | 0 | 72 | 107.2 | `b9441`, `b9439` | `9406.r7.g6ed481e-1` (built 2026-05-29) | 28 | **Highly Active** |
| *└─ python-llama-cpp-git-ggml-hip* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,355 | 1,411 | `main` | 2026-05-30 | **4** | 0 | 0 | 4.0 | — | `9406.r7.g6ed481e-1` (ref `3bda091`) | 4 | **Active** |
| *└─ stable-diffusion.cpp-git-ggml-hip* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,132 | 636 | `master` | 2026-05-30 | **12** | 0 | 10 | 16.7 | `master-660-d2797b8` | `9406.r7.g6ed481e-1` (ref `0e4ee04`) | 4 | **Active** |
| *└─ whisper.cpp-git-ggml-hip* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 50,293 | 5,591 | `master` | 2026-05-29 | **108** | 0 | 1 | 48.2 | `v1.8.5` | `9406.r7.g6ed481e-1` (ref `f24588a`) | 0 | **Highly Active** |
| *└─ qwen3-tts.cpp-git-ggml-hip* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) (Fork) | 14 | 3 | `main` | 2026-04-21 | **0** | 0 | 0 | 0.0 | — | `9406.r7.g6ed481e-1` (ref `2a41916`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 186 | 61 | `main` | 2026-03-09 | **0** | 0 | 0 | 0.0 | — | — | — | **Stale** |
| **python-bitsandbytes-rocm-git** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,243 | 858 | `main` | 2026-05-30 | **4** | 0 | 1 | 3.2 | `continuous-release_main` | `head.r1054.g17d32f15-1` (built 2026-02-12) | 93 | **Active** |
| **python-vllm-rocm-git** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 81,475 | 17,458 | `main` | 2026-05-31 | **199** | 0 | 5 | 210.5 | `v0.22.1rc0`, `v0.22.0` | `0.21.1rc0.r433.g0585b5b-1` (built 2026-05-29) | 34 | **Highly Active** |
| **python-vllm-omni-rocm-git** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 4,852 | 1,022 | `main` | 2026-05-31 | **93** | 0 | 1 | 79.7 | `v0.21.0rc2` | `0.21.0rc2.r67.g8c4a42b-1` (built 2026-05-29) | 22 | **Highly Active** |

> [!NOTE]
> `vllm`, `bitsandbytes`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api-git** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,591 | 284 | `master` | 2026-05-28 | **6** | 1 | 0 | 8.7 | — | `0.99.r38.g5c0bd05-2` (built 2026-05-23) | 10 | **Active** |

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Highly Active (134 commits, 72 tags in the last week).
* **Recent Focus**:
  - **Vulkan & OpenCL GPU Optimizations**: Added support for Flash Attention in Vulkan for BFloat16 KV cache; enabled BF16 support in OpenCL by converting to F16.
  - **Metal Backend**: Restored the `im2col` implementation for large kernels.
  - **Hardware Integration**: Added support for LSX (Loongson vector extensions); improved device identification logic to prevent skipping integrated GPUs when only RPC devices are present.
  - **Speculative Decoding & Benchmarking**: Introduced a new `speed-bench` utility in server-bench specifically for speculative decoding benchmarking.
  - **Usability & Server updates**: Implemented server self-updater feature; configured the server to send HTTP headers when slots start in SSE mode; enabled custom CSS injection via config in WebUI; improved tokenizer support for LFM2.5-8B-A1B.

### llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Active (4 commits in the last week).
* **Recent Focus**:
  - **Documentation**: Added a comprehensive contributing guide.

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (12 commits, 10 tags in the last week).
* **Recent Focus**:
  - **New Architecture Support**: Added support for Gemma3 rope settings and vram limit propagation; added microsoft lens support.
  - **Generation & Model Pipelines**: Excluded F8, F64, and I64 tensors explicitly from mmap; resolved LLM norm tensor names dynamically by architecture; corrected TAE defaults for models utilizing the Flux2 VAE; used flux flow prediction for LTXAV.
  - **Performance & Reliability**: Split tokens before normalization; simplified parameters for the diffusion model runner; prevented crashes in the event of memory allocation errors with a graceful exit; fixed ROCm CI builds by preserving frontend tooling.

### whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Highly Active (108 commits, 1 tag in the last week).
* **Recent Focus**:
  - **Sync & Versioning**: Regularly pulled changes from the ggml library, bumping the ggml dependency version to 0.13.1.
  - **Hardware-Specific Optimizations**: Disabled `launch_fattn` PDL enrollment on CUDA due to compiler bugs; routed batch>=4 quantized matmuls to MMQ on AMD MFMA hardware; auto-applied iGPU flags for CUDA/HIP integrated devices; implemented faster Vulkan paths for Walsh-Hadamard transform.
  - **General Fixes & Backends**: Fixed KQ mask offset integer overflow in CUDA fattn MMA kernel; resolved vector usage bug in ARM SVE; fixed unsafe iterator accesses in Vulkan memory logger; updated Hexagon OP_GATED_DELTA_NET support for K>1 and added OpenCL support.

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Status**: Stale (0 commits in the last week on both repos).
* **Fork & Feature Parity**:
  - The split package `qwen3-tts.cpp-git-ggml-hip` is built from **`khimaros/qwen3-tts.cpp`**, which is a downstream fork of **`predict-woo/qwen3-tts.cpp`** (the original author's repository, which has 186 stars but has not received updates since March 9, 2026).
  - The downstream `khimaros` fork was created to address several performance regressions and add integration patches: it introduces **Flash Attention** support, implements a **static KV cache**, caches the vocoder graph to prevent re-compilation latency, refactors C FFI embeddings extraction, and implements an **OpenAI-compatible TTS server** with batch conversion support. Its last commit was on April 21, 2026 (`2a41916`), implementing streaming vocoder decodes using chunked KV/tail state.

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Active (4 commits, 1 tag in the last week).
* **Recent Focus**:
  - **Build & Platform Support**: Added Windows ARM64 wheel build support with NEON optimization; resolved GCC 16 target specific option mismatches during OpenMP loop inlining.
  - **Usability & Performance**: Reduced Python CPU overhead and improved validation messages; fixed GEMV tests on AVX-512 BF16 CPUs.

### vLLM (`vllm-project/vllm`)
* **Status**: Highly Active (199 commits, 5 tags in the last week).
* **Recent Focus**:
  - **AMD & Hardware Backends**: Added attention sink support to the AITer flash attention backend for AMD ROCm; routed W8A8 and W4A16 linear inference through `zentorch` on AMD Zen CPUs; added native cmake PYTORCH_FOUND_HIP support for torch 2.13.
  - **Attention & Kernel Core**: Fixed Gemma4 MTP IMA issue when TP > 1 causing illegal memory access errors; resolved RMSNorm kernel bugs by multiplying in weight's native dtype; optimized expert mapping by removing expertExpertMap method and expertExpertMethod configurations.
  - **Execution & Scheduling**: Introduced support for breakable CUDA graphs in MRV2 engine; offloaded prompt embeddings decode in `render_prompts_async` to prevent blocking the engine loop.

### vllm-omni (`vllm-project/vllm-omni`)
* **Status**: Highly Active (93 commits, 1 tag in the last week).
* **Recent Focus**:
  - **Model Support**: Added Voxtral TTS recipe from MistralAI; added SenseNova-U1 Cache-DiT deployment configurations.
  - **Qwen3-TTS Optimizations**: Extracted a reusable prompt embeddings builder and made `tts_pad_embed` a persistent buffer; restored Code2Wav cross-request batching; fixed length estimation issue where 2D reference code list was collapsed.
  - **Performance & Distributed**: Supported USP and VAE patch parallel architectures for HunyuanVideo 1.5; resolved DistributedVaeExecutor IndexErrors when patch parallel sizes are smaller than world sizes; enabled AITER backend with ring attention on AMD ROCm.

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
* **Status**: Active (6 commits in the last week).
* **Recent Focus**:
  - **Build & Dependencies**: Fixed Dockerfile build issues; resolved CI gradle download hangs by switching to manual Gradle download; updated go.sum.
  - **Features & Safety**: Upgraded underlying `signal-cli` to v0.14.4.1; configured JSON schema generation to build directly from the signal-cli source tree; added safe slicing checks to prevent crashes when processing base64 attachment data.

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

# Reference hashes corresponding to build date (2026-05-29 15:59:16)
declare -A PKG_REFS=(
  [llama.cpp]="6ed481e"
  [llama-cpp-python]="3bda091"
  [stable-diffusion.cpp]="0e4ee04"
  [whisper.cpp]="f24588a"
  [qwen3-tts.cpp]="2a41916"
  [bitsandbytes]="17d32f15"
  [vllm]="0585b5b"
  [vllm-omni]="8c4a42b"
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
