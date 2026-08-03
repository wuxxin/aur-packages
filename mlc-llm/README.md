# mlc-llm

Universal LLM deployment engine via ML compilation targeting ROCm and Vulkan (qwen3_5 fork).

- **Fork**: [alansrobotlab2/mlc-llm](https://github.com/alansrobotlab2/mlc-llm) branch `qwen3_5`
- **TVM/Relax**: [alansrobotlab2/relax](https://github.com/alansrobotlab2/relax) branch `mlc` (submodule)

## Supporting Models

Adds Qwen3.5/Qwen3.6 (GatedDeltaNet + MoE hybrid) model support:
- `model_type: qwen3_5` (dense variants)
- `model_type: qwen3_5_moe` (MoE, 256 experts + 1 shared)
- `conv_template: qwen3_5` / `qwen3_5_nothink`
- Quantization: `q4f16_1` (4.345 bits/param), `q4f16_g16e` (group=16)

## Patches

### hipblas-rocm72.patch
Fixes ROCm 7.2 hipblas API incompatibility:
- `hipblasDatatype_t` → `hipDataType`
- Adds `GetHipBlasComputeType()` helper for new `hipblasComputeType_t` parameter

### hipblas-cc-rocm72.patch
Updates `hipblas.cc` call sites to use corrected types and compute type mapping.

## Build Configuration

- `USE_ROCM=ON`, `USE_HIPBLAS=ON` — AMD GPU via HIP
- `USE_VULKAN=ON` — AMD GPU via Vulkan
- `USE_THRUST=ON` — GPU algorithms (sort, scan)
- `USE_LLVM=ON` — host codegen
- `USE_FLASHINFER=OFF` — FlashInfer JIT'd at model compile time via `flashinfer-python`
- `-DCMAKE_SHARED_LINKER_FLAGS=-lonig` — oniguruma regex library linking

## Memory

| Component | Size |
|---|---|
| Weights (q4f16_1) | 18,624 MB |
| Temp buffer (prefill_chunk=512) | 544 MB |
| KV cache per token | 0.08 MB |
| 4K ctx total | 19,488 MB |
| 24 GB headroom | ~5,000 MB (~62K more ctx tokens) |
