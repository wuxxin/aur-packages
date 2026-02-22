# libggml-git-hip

An optimized Git-based compilation of the GGML tensor library and associated tools (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`) for Arch Linux. This package focuses on **HIP/ROCm hardware acceleration** on RDNA architectures.

## Key Features

- **Git Version:** Builds directly from latest GIT to provide the latest features and improvements.
- **Unified Shared Library:** `llama.cpp`, `whisper.cpp`, and `python-llama-cpp` all link dynamically against a single system-wide `libggml-git-hip`. This ensures consistent backend behavior / bug compatibility across all tools.
- **RDNA2 Optimization:** Includes `rdna2-optimized-tile.patch` to unlock more performant TILE Flash Attention on RDNA2 GPUs.
- **OuteTTS 1.0 Support:** Added support in `llama-tts`for the latest OuteTTS 1.0 (v3) models with interleaved DAC tokens and audio feature injection for high-fidelity voice cloning.
- **Python Bindings:** patched to support the latest git version of libggml and llama.cpp.


## Package Structure

- **`libggml-git-hip`**: The core shared library (`libggml.so`, `libllama.so`) optimized for HIP.
- **`llama.cpp-git-ggml-hip`**: Main executables (`llama-cli`, `llama-server`, etc.) linking to the shared lib.
- **`whisper.cpp-git-ggml-hip`**: Whisper speech-to-text tools (`whisper-cli`, `whisper-server`) linking to the shared lib.
- **`python-llama-cpp-git-ggml-hip`**: Python bindings (`llama_cpp`) installed into site-packages, linking to the shared lib.

## Installation

```bash
# Build and install all packages
makepkg -i
```

## Patches & Modifications

### 1. RDNA2 Flash Attention Optimization (`rdna2-optimized-tile.patch`)
This package applies a custom patch to maximize stability and performance on RDNA2 GPUs (gfx1030). It bypasses the unstable "VEC" kernel and forces an optimized "TILE" kernel with 256 threads for Head Dim 128.

| Configuration | Throughput (40k Ctx) | Max Stable Context |
| :--- | :--- | :--- |
| Stock (VEC) | ~660 Char/s | ~50k Chars |
| Stock (TILE) | ~280 Char/s | >145k Chars |
| **Optimized TILE** | **~1485 Char/s**| **>145k Chars** |

**Note:** The build conditionally disables `GGML_HIP_ROCWMMA_FATTN` ONLY for single-target RDNA2 builds to trigger the patch logic, to keep ROCWMMA_FATTN enabled for other targets

### 2. Python Binding Fixes (`python-llama-cpp`)
To bridge the gap between latest `libllama.so` and the `llama-cpp-python` bindings, we apply functional shims and symbol aliasing.

#### Symbol Resolution Table

| Symbol Name | Resolution | Status |
| :--- | :--- | :--- |
| `llama_set_adapter_lora` | **Shimmed** | Re-implemented using `llama_set_adapters_lora` (plural API). Wraps single adapter into array. |
| `llama_adapter_lora_init` | **Shimmed** | Bound to C symbol with UTF-8 path encoding safety. |
| `llama_adapter_lora_free` | **Shimmed** | Bound to C symbol for manual memory management. |
| `llama_get_kv_self` | Aliased | Dummied to `llama_get_memory`. Deprecated in library. |
| `llama_rm_adapter_lora` | Aliased | Dummied to `llama_get_memory`. Unused by high-level API. |
| `llama_clear_adapter_lora`| Aliased | Dummied to `llama_get_memory`. Unused by high-level API. |
| `llama_apply_adapter_cvec`| Aliased | Dummied to `llama_get_memory`. Unused by high-level API. |
| `llama_kv_self_*` (13 variants)| Aliased | Dummied to `llama_get_memory`. Internal seq management replaced by library. |
| `llama_sampler_init_softmax`| Aliased | Dummied to `llama_get_memory`. Deprecated in library. |

**Implementation:** Shims are injected via `EOF` concatenation at the end of `llama_cpp/llama_cpp.py`. Aliases are applied via `sed` substitutions during the `prepare()` phase.


### 3. OuteTTS 1.0 (v3) Support
 
This package includes a series of patches for `llama-tts` to support the latest OuteTTS 1.0 models and provides standalone tools for model conversion and speaker profile creation. 

- **Dynamic Version Detection:** Automatically recognizes "1.0" or "3" versions in `speaker.json`.
- **Interleaved Tokens:** Native support for the `<|c1_xxx|><|c2_xxx|>` DAC token format used in the 1B model. DAC operates at 75 frames per second, with each frame represented by two codebook tokens, resulting in a total generation rate of 150 tokens per second.
- **Audio Feature Injection:** Incorporates energy, pitch, and spectral centroid data for higher-fidelity voice cloning. The prompt system is version-aware and adjusts buffer sizes based on these injected features.
- **Optimized Prompting:** Handles ChatML padding and Qwen-style separators. Correctly identifies special tokens for different OuteTTS versions.

- **GGML Core & CPU Backend**
    - Snake Activation: Implemented the $f(x) = x + \frac{1}{\alpha + 10^{-9}} \sin^2(\alpha x)$ activation function (GGML_OP_SNAKE) in both the core GGML library and the CPU backend.
    - Per-Channel Alpha: The implementation correctly handles per-channel alpha parameters, which is critical for DAC model fidelity.
- **Llama Architecture**
    - LLM_ARCH_DAC_DEC: Registered the new DAC decoder architecture.
    - Tensor Mapping: Added mappings for DAC-specific tensors (`DAC_SNAKE`, `DAC_OUTPUT_SNAKE`, `DAC_UPSAMPLE`, `DAC_RU_*`).
    - Metadata Handling: Updated the model loader to recognize DAC-specific metadata like features_length.
- **TTS Tooling**
    - OuteTTS 1.0 Support: Updated tts.cpp to support OuteTTS version 1.0.
    - Dual-Stream Tokens: Implemented logic to process interleaved tokens (e.g., <|c1_xxx|><|c2_xxx|>) used by DAC-based OuteTTS models.
    - Dynamic Filtering: Updated the token filter to handle the expanded token space of OuteTTS 1.0.
- **Conversion & Packaging**
    - hf_dac_to_gguf.py: Developed a script to convert DAC models from Hugging Face to GGUF format, mapping weights and Snake parameters.
    - PKGBUILD Automation: Updated the PKGBUILD to use a sed-style integration script (outetts-v1-integration-patch.sh), ensuring a clean and automated build process.

#### Current Integration Status (February 20, 2026)

- [x] **GGML Build:** Success (Snake operator and OP_COUNT fix confirmed).
- [x] **Installation:** Success (User-confirmed system-wide installation).
- [x] **Architecture Registration:** Success. `LLM_ARCH_DAC_DEC` registered in all 5 required `llama-model.cpp` switches.
- [x] **Tensor Name Mapping:** Fixed — templates, `LLM_TENSOR_INFOS`, bias shapes (2D `{1, channels}`), conv transpose padding.
- [x] **Runtime Verification (WavTokenizer):** **Success.** Resolved the CPU and HIP crashes during `im2col` building by patching `ggml.c` to use the dynamic `a->type` rather than hardcoding `GGML_TYPE_F16`. Tensor dimension mismatch in posnet was fixed by explicitly flattening biases in the converter.
- [x] **Runtime Verification (DAC):** **Success.** The `sched_reserve()` crash for the DAC 24kHz model was resolved by identifying that `llama-model.cpp` needs specific 2D `{1, C}` biases for proper tensor broadcasting. The segmentation fault during graph building was resolved by exporting `dac.ones` explicitly as a float32 tensor from python rather than allocating it dynamically via `ggml_new_tensor` in C++ context logic.

#### Next Steps

1.  **Full System Build:** Run `makepkg -Cf` to cleanly regenerate the build with all final F32 and broadcasting tensor fixes.
2.  **Verify Quantization Profiles:** Quantize the models (Q8_0, Q5_K_M, Q4_K_M) using the system `llama-quantize` and verify standard inference synthesis stability.


#### Usage Example

##### 1. Download the Base Model (one-time)
Download the OuteTTS GGUF models (Q5_K_M or better recommended):
```bash
hf download OuteAI/OuteTTS-1.0-0.6B-GGUF OuteTTS-1.0-0.6B-Q6_K.gguf --local-dir .
hf download OuteAI/Llama-OuteTTS-1.0-1B-GGUF Llama-OuteTTS-1.0-1B-Q5_K_M.gguf --local-dir .
```

##### 2. Prepare the Vocoder (one-time)
You must convert the original PyTorch weights to GGUF.

```bash
# A. Download and Convert WavTokenizer (0.6B)
outetts-hf-wavtokenizer-to-gguf

# B. Download and Convert DAC (1B) 
uv venv --system-site-packages --seed
echo "torch torchvision torchaudio bitsandbytes triton torchao nvidia-cublas-cu12 nvidia-cuda-cupti-cu12 nvidia-cuda-nvrtc-cu12 nvidia-cuda-runtime-cu12 nvidia-cudnn-cu12 nvidia-cufft-cu12 nvidia-cufile-cu12 nvidia-curand-cu12 nvidia-cusolver-cu12 nvidia-cusparse-cu12 nvidia-cusparselt-cu12 nvidia-nccl-cu12 nvidia-nvjitlink-cu12 nvidia-nvshmem-cu12 nvidia-nvtx-cu12" | tr " " "\n" > .venv/excluded_packages.txt
uv pip install --excludes .venv/excluded_packages.txt "git+https://github.com/descriptinc/descript-audio-codec#egg=descript-audio-codec"
.venv/bin/python $(which outetts-hf-dac-to-gguf)


```

##### 3. Create a Speaker Profile
```bash
outetts-create-speaker --audio reference-30-42sec.wav --output my_speaker.json
```

##### 4. Generate Speech

The `llama-tts` tool includes a hardcoded default speaker, but this is currently optimized for **OuteTTS 0.2/0.3**. For **OuteTTS 1.0**, it is highly recommended to explicitly provide a OuteTTS 1.0 speaker JSON file.

You can use the official default female speaker provided by OuteAI, which is installed by this package at: `/usr/share/llama.cpp/outetts-default-v3-female.json`

If no speaker is provided, the model will fall back to the internal 0.2 profile, which may result in lower quality or unexpected artifacts when used with 1.0 models.


```bash
# Using WavTokenizer
llama-tts \
-m OuteTTS-1.0-0.6B-Q6_K.gguf \
-mv wavtokenizer-75-f32.gguf \
--tts-speaker-file /usr/share/llama.cpp/outetts-default-v3-female.json \
-p "The future of speech technology is open and accessible." \
-o output_wav.wav

# Using DAC
llama-tts \
-m Llama-OuteTTS-1.0-1B-Q5_K_M.gguf \
-mv dac-dec-24khz-f32.gguf \
--tts-speaker-file /usr/share/llama.cpp/outetts-default-v3-female.json \
-p "The future of speech technology is open and accessible." \
-o output_dac.wav
```

### Troubleshooting & Optimization

#### 14. WavTokenizer Norm Shape Alignment
The upstream C++ WavTokenizer `load_tensors` expects many 1D-looking tensors as 2D `{1, n_embd}`, including `posnet.*.norm1.weight`, `posnet.*.norm2.weight`, `posnet.*.attn_norm.*`, and `conv1d.bias`. The GGUF converter must reshape numpy arrays to `[channels, 1]` (GGUF reverses to `ne=[1, channels]`). The `build_norm` crash in WavTokenizer suggests additional tensors may need this treatment.


## Lessons Learned (Dev Log):

- The OuteTTS 1.0 1B model uses the **Descript Audio Codec (DAC)** instead of WavTokenizer. 
    - **Backbone:** Llama-3.1-1B (vs. GPT-2 style in 0.6B).
    - **Vocoder Architecture:** DAC uses a symmetrical encoder-decoder with Snake activations. The decoder consists of a series of `UpsampleBlock`s, each containing a sequence: `Snake -> ConvTranspose1d -> [ResidualUnit1, ResidualUnit2, ResidualUnit3]`.
    - **Indexing (state_dict):** Found that `UpsampleBlock` is implemented as an `nn.Sequential` where `block.0` is the initial Snake, `block.1` is the upsample convolution, and `block.2..4` are the three ResidualUnits. Correctly mapping these indices is vital for GGUF conversion.
    - **Weight Normalization Fusion:** All convolutional layers in the DAC decoder (initial, upsample, and residual) use Weight Normalization. These must be fused (`w = v * (g / ||v||)`) into static weight tensors for efficient GGML execution.
    - **Snake Activation (GGML_OP_SNAKE):** Implemented a custom GGML operator to handle $x + \frac{1}{\alpha} \sin^2(\alpha x)$. The `alpha` parameters are per-channel and are exported as block-specific tensors (e.g., `blk.N.ru.M.snake1.alpha`).
    - **3D Tensor Layout:** Standardized 1D convolution weights on the `[KW, IC, OC]` layout to ensure compatibility with GGML's `im2col` kernels. This corresponds to Torch's `[OC, IC, KW]` after a `transpose(2, 1, 0)`.
    - **Architectural Builder:** Discovered that `LLM_ARCH_DAC_DEC` in `llama.cpp` was initially a placeholder aliased to WavTokenizer. Fixing this required implementing a dedicated `llm_build_dac_dec` graph builder with proper upsampling logic.

- **Hugging Face Integration (DAC):** The `outetts-hf-dac-to-gguf` script supports repo IDs (defaulting to `ibm-research/DAC.speech.v1.0`).
    - **Resolution:** Corrected filename mapping for official weights (e.g., `weights_24khz_3kbps_v1.0.pth` is used instead of `3.0kbps`).
- **WavTokenizer vs DAC Tokenization:** 
    - WavTokenizer: Single codebook stream (75 tokens/s).
    - DAC: Dual codebook stream (150 tokens/s) interleaved as `[C1, C2, C1, C2...]`.
- **Snake Activation (GGML_OP_SNAKE):** 
    - Implemented as $x + \frac{1}{\alpha} \sin^2(\alpha x)$ to match the original DAC implementation.
    - Exported as per-channel `alpha` tensors at each upsample/residual level.
- **GGUF Tensor Layout & `gguf-py` Shape Reversal:** Discovered a critical behavior in the `gguf` Python library where it automatically reverses numpy shapes (e.g., a numpy array of `(OC, IC, KW)` is written to the GGUF file as `ne=[KW, IC, OC]`). 
    - **Resolution:** Removed manual `transpose(2, 1, 0)` calls in conversion scripts. Previously, manual transposing moved the large channel dimension into the `ne[0]` (kernel width) slot, causing `im2col` calculations to result in a negative output width (`OW <= 0`) during model warmup.
- **IM2COL Hardware Validation Pass (Fit Phase):** Discovered that `llama_params_fit` uses a dummy input of 1 token (or 512 in our patched version). 
    - **Resolution:** Corrected the layout to ensure `ne[0]` correctly represents the kernel width (e.g., 7 or 9). This ensures the convolution formula results in a positive output width even with small inputs. Additionally, patched `llama-model.cpp` to provide a safe minimum input length.
- **Multi-Model Buffer Stability:** Fixed a crash where tool-level `fit_params` conflicted with secondary model initialization. Standardized on `n_ubatch = n_batch` and explicitly managed context sharing for dual-model tools like `tts.cpp`.

- **Robust Speaker Creation (`outetts-create-speaker`):**
    - **Audio Decoding:** Migrated from `transformers` default decoding to native `torchcodec` & `torchaudio` for better support of varied sample rates and formats without ffmpeg dependency issues.
    - **ROCm Stability:** Implemented early environment variable injection (`HIP_VISIBLE_DEVICES`, `HSA_OVERRIDE_GFX_VERSION`) before importing `torch` to prevent initialization-time core dumps on unsupported architectures.
    - **Hydra Suppression:** Manually disabled Hydra's extensive log-capturing to keep the CLI output clean and focused on speaker JSON generation.

- **Integrated Patching Strategy (February 2026):** Transitioned from standalone `PKGBUILD` patches to script-injected patching via `outetts-v1-integration-patch.sh`. 
    - **Rationale:** The integration script performs a `git checkout` reset at the start to ensure idempotency. Standalone patches applied before the script were being wiped; patches applied after often failed context matches due to script modifications.
- **WavTokenizer Tensor Alignment:** Discovered persistent `1, 768, 1, 1` shape mismatches in `posnet` bias tensors. 
    - **Cause:** Original PyTorch biases are 4D (NCHW). GGUF conversion usually squeezes these, but `llama.cpp`'s `im2col` operations sometimes struggle with mapping across the Python-to-C++ barrier.
    - **Resolution:** Standardized on 1D flattening in conversion scripts and letting `llama.cpp` dynamically handle 1D layouts.
- **WavTokenizer F32 Context Crash:** Discovered `ggml_conv_1d` statically enforced `GGML_TYPE_F16` during im2col layout generation, crashing F32 WavTokenizer vocoders.
    - **Resolution:** Modified `ggml_conv_1d` parameter injection to dynamically inherit `a->type` via standard patch inclusion.
- **DAC Tensor Alignment (Broadcast bug):** Modifying 1D bias arrays into `[1, Channels]` explicitly inside converter scripts bypassing `ggml_add` assertions which were stalling generation graphs during `llama_params_fit`.
- **DAC `ones` graph mapping (Segfault):** Calling `ggml_new_tensor` during graph initialization causes immediate pointer evaluation errors because graph variables do not persist natively like mapped `LLM_TENSOR_*` buffers do. Reverted Python GGUF scripts to output standard numpy buffers via `writer.add_tensor` instead.
- **Build Verification:** 
    - [x] `libggml-git-hip` builds successfully with `makepkg`.
    - [x] OuteTTS 1.0 tensors registered and graph builder integrated.
