# 📊 Custom AUR Packages: Weekly Development Activity

This document tracks repository activity, commit counts, merge frequency, and release cycles for custom, private, or experimental AUR packages hosted in this repository.

---

## 📅 Summary of Weekly Activity (June 1, 2026 – June 7, 2026)

### AI Backend & Inference Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **libggml-git-hip** | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 115,076 | 19,265 | `master` | 2026-06-07 | **106** | 0 | 70 | 113.0 | `b9547`, `b9544` | `9442.r0.gd4c8e2c-1` (built 2026-05-31) | 105 | **Highly Active** |
| *└─ python-llama-cpp-git-ggml-hip* | [abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | 10,370 | 1,411 | `main` | 2026-06-07 | **56** | 0 | 29 | 17.2 | `v0.3.26`, `v0.3.25` | `9442.r0.gd4c8e2c-1` (ref `fdf38b3`) | 55 | **Highly Active** |
| *└─ stable-diffusion.cpp-git-ggml-hip* | [leejet/stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | 6,182 | 645 | `master` | 2026-06-07 | **19** | 0 | 19 | 20.7 | `master-679-f3fd359` | `9442.r0.gd4c8e2c-1` (ref `d2797b8`) | 19 | **Active** |
| *└─ whisper.cpp-git-ggml-hip* | [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) | 50,519 | 5,625 | `master` | 2026-06-06 | **18** | 0 | 1 | 52.5 | `v1.8.6` | `9442.r0.gd4c8e2c-1` (ref `2e045a9`) | 15 | **Active** |
| *└─ qwen3-tts.cpp-git-ggml-hip* | [khimaros/qwen3-tts.cpp](https://github.com/khimaros/qwen3-tts.cpp) (Fork) | 14 | 3 | `main` | 2026-04-21 | **0** | 0 | 0 | 0.0 | — | `9442.r0.gd4c8e2c-1` (ref `2a41916`) | 0 | **Stale** |
| *   └─ [Fork Origin]* | [predict-woo/qwen3-tts.cpp](https://github.com/predict-woo/qwen3-tts.cpp) | 196 | 64 | `main` | 2026-06-03 | **0** | 1 | 0 | 0.2 | — | — | — | **Stale** |
| **python-bitsandbytes-rocm-git** | [bitsandbytes-foundation/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) | 8,261 | 861 | `main` | 2026-06-01 | **2** | 0 | 0 | 2.7 | — | `head.r1155.g2177945b-1` (built 2026-05-31) | 2 | **Active** |
| **python-vllm-rocm-git** | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 82,115 | 17,738 | `main` | 2026-06-07 | **231** | 0 | 3 | 220.0 | `v0.22.1`, `v0.22.1rc2` | `0.22.1rc0.r23.g6bdabba-1` (built 2026-05-31) | 231 | **Highly Active** |
| **python-vllm-omni-rocm-git** | [vllm-project/vllm-omni](https://github.com/vllm-project/vllm-omni) | 4,975 | 1,064 | `main` | 2026-06-06 | **72** | 0 | 2 | 78.0 | `v0.22.0`, `v0.22.0rc1` | `0.21.0rc2.r89.g5dfdf58-1` (built 2026-05-31) | 72 | **Highly Active** |

> [!NOTE]
> `vllm`, `bitsandbytes`, and most split sub-repositories of the `libggml-git-hip` package squash-merge PRs directly into their primary branch instead of creating merge commits, which is why the "Merges" column displays `0`.

### Other Custom Packages

| Package | Upstream Repo | Stars | Forks | Main Branch | Last Commit | Commits (Last Wk) | Merges (Last Wk) | Releases/Tags (Last Wk) | Avg Commits/Wk (4 Wks) | Recent Tags / Versions | Installed Pkg Version | Commits Since Installed | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **signal-cli-rest-api-git** | [bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) | 2,605 | 288 | `master` | 2026-06-01 | **4** | 1 | 1 | 6.7 | `0.100-pre` | `0.100.pre.r0.g81efbd2-1` (built 2026-06-03) | 0 | **Active** |

---

## 🔍 Repository Focus & Developments

### llama.cpp (`ggml-org/llama.cpp`)
* **Status**: Highly Active (106 commits, 70 tags in the last week).
* **Recent Focus**:
  - **Model Support**: Added Granite4 Vision support; fixed Gemma4 conversion (with no audio encoder, unified conversion); improved tokenizer support and chat integration for LFM2/LFM2.5 (including fixing reasoning round-trip and `<think>` leaks, and unifying tool parser).
  - **Multimodal & Server**: Added "placeholder bitmap" for counting tokens and introduced a new `*/input_tokens` API; supported "frame merge" for Qwen-VL based models; optimized server checkpointing by disabling on-device speculative checkpoints and avoiding unnecessary restores.
  - **Hardware Backends**:
    - *Vulkan*: Added checking of `coopmat2` features before reporting support; added Walsh-Hadamard Transform (FWHT) support for Intel with shared-memory reduction.
    - *OpenCL*: Improved performance for get_rows, cpy, concat, and flat GEMV in Q6_K.
    - *CUDA / SYCL / KleidiAI*: Enrolled `mul_mat_vec_q_moe` into Profile-Driven Loop (PDL) for CUDA; ported multi-column Matrix-Vector Quantized (MMVQ) from CUDA to SYCL; integrated dynamic chunk-based scheduling for hybrid execution in KleidiAI.
  - **WebUI**: Solved keyboard navigation (accessibility) issues in chat interface and sidebar; automated `npm install` when `package-lock.json` is newer than `node_modules`; added single-line reasoning preview in the UI.

### llama-cpp-python (`abetlen/llama-cpp-python`)
* **Status**: Highly Active (56 commits, 29 tags in the last week).
* **Recent Focus**:
  - **llama.cpp Sync**: Regularly pulled in upstream llama.cpp updates up to commit `5a69c9743`.
  - **Features**: Introduced a **Generic Multimodal Chat Handler**; updated the server example to support batch processing, response parsing, and the `/v1/responses` API.
  - **CI & Releases**: Added **ROCm** and **Vulkan** wheel builds to the CI pipeline; repaired release wheel workflows, RISC-V 64 wheel builds, and CUDA wheel variant indexing. Bumped version to `v0.3.26`.
  - **Documentation**: Added Gemma 4 QAT Colab notebooks.

### stable-diffusion.cpp (`leejet/stable-diffusion.cpp`)
* **Status**: Active (19 commits, 19 tags in the last week).
* **Recent Focus**:
  - **New Model Architectures**: Added support for Ideogram4; refactored Wan VAE implementation and unified model config detection; made Wan2.2 5B FLF2V work.
  - **Execution Options**: Added `--stream-layers` flag for streaming weights from CPU during generation; allocated CPU-offloaded parameters from runtime device pinned host buffer.
  - **Optimizations**: Reorganized model layout in `src/`; ratcheted streaming budget to prevent re-merging planning every step; kept chunk-K residency engaged with runtime LoRA; added Adaptive Projected Guidance (APG) and unconditional SLG support.
  - **Platform Fixes**: Built HIP backend with PIC (Position Independent Code) to allow static-lib PIE links to succeed (ROCm specific fix).

### whisper.cpp (`ggerganov/whisper.cpp`)
* **Status**: Active (18 commits, 1 tag in the last week).
* **Recent Focus**:
  - **Releases**: Released version `v1.8.6`.
  - **General Functionality**: Improved FFmpeg audio decoding by passing sample rate to `ffmpeg_decode_audio` and refactoring `ffmpeg-transcode.cpp`; caught C++ exceptions in `whisper_init_with_params_no_state` for safer initialization.
  - **Server Improvements**: Merged split UTF-8 token texts in verbose JSON output.
  - **Build Systems & CI**: Modified CMake to avoid assuming `/usr/lib` library installation; optimized and slimmed down CI workflows (ccache, setup action commit SHAs).

### qwen3-tts.cpp (`khimaros/qwen3-tts.cpp` and fork origin `predict-woo/qwen3-tts.cpp`)
* **Status**: Stale (0 commits in the last week on both repos).
* **Fork & Feature Parity**:
  - Maintained downstream changes (Flash Attention, static KV cache, OpenAI-compatible TTS server). The original repository (`predict-woo/qwen3-tts.cpp`) had 1 merge commit (maintenance) but remains functionally stale with no active features developed.

### bitsandbytes (`bitsandbytes-foundation/bitsandbytes`)
* **Status**: Active (2 commits in the last week).
* **Recent Focus**:
  - **CI/CD Platform Support**: Added Windows CPU ARM64 nightlies to tests and PR workflows.

### vLLM (`vllm-project/vllm`)
* **Status**: Highly Active (231 commits, 3 tags in the last week).
* **Recent Focus**:
  - **ROCm / AMD Optimizations**: Enabled `permute_cols` for ROCm; replaced `torch.cat` in sparse-MLA `forward_mqa` with fused `concat_mla_q` kernel; added fused MoE W4A16 HIP kernel for AMD RDNA3 (gfx1100); handled rotary embedding grid boundaries by falling back to native when limits are exceeded.
  - **Performance & Quantization**: Fused RoPE + static Q FP8 quantization on fused RoPE+KV path; fixed RMSNorm big-fuse miscompilations for hidden sizes other than 4096; resolved deadlocks in multiple async KV loads; split mixed prefill/decode batches for Qwen 3.5 routing decodes to recurrent kernels.
  - **Model Support**: Implemented GLM-4-6V video loader; enabled Cohere Mini Code model and Command A-plus support; added Phi-4 mini JSON tool parser to Rust frontend; added index sharing feature for DSA MTP.

### vllm-omni (`vllm-project/vllm-omni`)
* **Status**: Highly Active (72 commits, 2 tags in the last week).
* **Recent Focus**:
  - **Model & Feature Additions**: Supported `bosonai/higgs-audio-v3-tts-4b`; added Cosmos3 action modality; added ModelOpt FP8 serving under batched diffusion serving.
  - **Higgs-Audio-V3 Optimizations**: Turned on Stage-0 prefix caching by default; added LRU cache for voice-cloned reference audio encoding.
  - **Qwen3-Omni & Diffusion improvements**: Optimized TTFP using `initial_codec_chunk_frames`; updated thinker's sampling parameters; fixed qwen3-tts code2wav bugs; enabled fused RMSNorm for HunyuanImage3; optimized Wan2.2 S2V video generation on Intel XPU.
  - **Bugfixes**: Corrected GPU device mapping in multi-replica environments; guarded against transformers v5 shard-resolution race condition in prefetching.

### signal-cli-rest-api (`bbernhard/signal-cli-rest-api`)
* **Status**: Active (4 commits, 1 tag in the last week).
* **Recent Focus**:
  - **Releases & CI**: Tagged `0.100-pre` release; resolved check-docs CI workflows to use Java 25.

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
