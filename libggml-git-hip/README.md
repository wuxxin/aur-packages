# libggml-git-hip

An optimized Git-based compilation of the GGML tensor library and associated tools (`llama.cpp`, `whisper.cpp`, `python-llama-cpp`) for Arch Linux. This package focuses on **HIP/ROCm hardware acceleration** for delivering maximum performance and stability on RDNA architectures.

## Key Features

- **Bleeding Edge:** Builds directly from latest GIT to provide the latest features and scheduler improvements.
- **Unified Shared Library:** `llama.cpp`, `whisper.cpp`, and Python bindings all link dynamically against a single system-wide `libggml-git-hip`. This reduces disk usage and ensures consistent backend behavior across all tools.
- **RDNA2 Optimization Patch:** Includes `vec-wmma-boost.patch` to resolve critical performance regressions on RDNA2 (gfx103[0-6]) GPUs.

## RDNA2 Optimization (`vec-wmma-boost.patch`)

This package applies a custom patch to increase Flash Attention performance on RDNA2 GPUs, which suffered slowdown due to regression in upstream kernel selection logic.

### The Problem
Upstream `llama.cpp` prevents the optimized "VEC" Flash Attention kernel from running on memory that isn't 32-byte aligned. Since token generation involves single-token increments (unaligned), RDNA2 GPUs fell back to the unoptimized "TILE" kernel.

**Impact:**
- **Before Patch:** ~300 tokens/sec generation (TILE kernel)
- **After Patch:** ~500 tokens/sec generation (VEC kernel)

### The Fix
The included patch:
1.  **Unlocks VEC Kernel (Safe):** Removes the alignment restriction **conditionally** for RDNA2 only. Other architectures (RDNA3, NVIDIA) retain the original strict check, ensuring safety in multi-arch builds.
    ```cpp
    // ggml/src/ggml-cuda/fattn.cu

    // 1. Move 'cc' definition to top of function (fix scope):
    const int cc = ggml_cuda_info().devices[device].cc;

    // 2. Relax stride checks ONLY if running on RDNA2 (affects use_gqa_opt, gqa_opt_applies, can_use_vector_kernel):
    bool use_gqa_opt = ... && (K->ne[1] % FATTN_KQ_STRIDE == 0 || GGML_CUDA_CC_IS_RDNA2(cc));
    
    // 3. Added explicit RDNA2 check to force VEC kernel:
    if (GGML_CUDA_CC_IS_RDNA2(cc) && Q->ne[0] <= 256 && Q->ne[0] % 64 == 0 && Q->ne[1] <= 4096) {
        return BEST_FATTN_KERNEL_VEC;
    }
    ```
2.  **Fixes TILE Stability:** Caps thread counts to 128 in the fallback TILE kernel.
    *   **Scope:** Affects all RDNA architectures (RDNA 1, 2, 3, 4).
    *   **Safety:** This is a safe stability improvement. It prevents occupancy crashes on RDNA2 and provides a stable fallback configuration for RDNA3/4. Nvidia and CDNA architectures use separate config paths and are **unaffected**.
    *   **Performance (RDNA3/4):** Unmodified RDNA3/4 GPUs may see a slight reduction in *fallback* performance (when VEC/WMMA **cannot** be used) due to the reduced thread count (128 vs 256). However, this affects only the slow path and guarantees stability across the entire RDNA family.
    ```cpp
    // ggml/src/ggml-cuda/fattn-tile.cuh
    // Cap threads to 128 for specific RDNA TILE configs (was 256)
    GGML_CUDA_FATTN_TILE_CONFIG_CASE(128, 128, 16, 128, 3, 128, 128)
    GGML_CUDA_FATTN_TILE_CONFIG_CASE(128, 128, 32, 128, 3, 128,  64)
    // ...
    GGML_CUDA_FATTN_TILE_CONFIG_CASE(256, 256, 16, 128, 5,  32, 256)
    GGML_CUDA_FATTN_TILE_CONFIG_CASE(256, 256, 32, 128, 3,  64, 128)
    ```
3.  **Boosts Threshold:** Increases the batch size threshold for the VEC kernel to 128, improving prefill performance for small-to-medium batches.

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

## Performance Verification (`cache_test.py`)

This package includes the `cache_test.py` utility (installed to `/usr/share/doc/llama.cpp-git-ggml-hip/examples/`) to benchmark throughput and cache hit latency.

### Usage
Start the server:
```bash
llama-server -m /path/to/model.gguf \
    --ctx-size 262144 \
    --parallel 2 \
    --port 18080 \
    --n-gpu-layers 999 \
    --cache-type-k q4_0 \
    --cache-type-v q4_0 \
    --flash-attn on \
    --no-mmap \
    --cache-prompt \
    -b 2048 -ub 2048 \
    --cont-batching
```

Run the benchmark:
```bash
python cache_test.py \
  --url http://127.0.0.1:18080/v1 \
  --payload ~/AntigravityWorkspace/caching-local-inference/noben-context.md  \
  --step 10000 \
  --skip-linearity \
  --min-cps 600
```

Output:
```log
# LLM Benchmark Report

- **URL:** `http://127.0.0.1:18080/v1`
- **Model:** `default`
- **Payload:** 145916 chars
- **Vision:** DISABLED
- **Fail-Fast:** Enabled (< 600.0 Char/s)

### Incremental Prefill & Warmup

**Step size:** 10000 chars

| Chars | Delta (ms) | Char/s |
| ---: | ---: | ---: |
| 10000 | 4488 | 2228.05 |
| 20000 | 5006 | 1997.75 |
| 30000 | 5453 | 1833.70 |
| 40000 | 6721 | 1487.85 |
| 50000 | 6839 | 1462.20 |
| 60000 | 7368 | 1357.27 |
| 70000 | 8051 | 1242.12 |
| 80000 | 8649 | 1156.16 |
| 90000 | 8491 | 1177.65 |
| 100000 | 9042 | 1105.99 |
| 110000 | 9259 | 1080.01 |
| 120000 | 11001 | 909.03 |
| 130000 | 11497 | 869.82 |
| 140000 | 11026 | 906.96 |
| 145916 | 8760 | 675.33 |

### Cache Hit Latency Test (8 Loops)

| Loop | Distractor (ms) | Target Hit (ms) | Status |
| :--- | :--- | :--- | :--- |
| 01 | 81.1 | 119.5 | **HIT** |
| 02 | 75.1 | 111.0 | **HIT** |
| 03 | 76.2 | 113.6 | **HIT** |
| 04 | 77.6 | 110.7 | **HIT** |
| 05 | 79.7 | 110.6 | **HIT** |
| 06 | 79.9 | 112.0 | **HIT** |
| 07 | 79.5 | 109.1 | **HIT** |
| 08 | 79.9 | 110.7 | **HIT** |

### Summary

- **Cache Hit Rate:** 100.0% (8/8)
```
