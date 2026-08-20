# vllm.cpp-git-hip

An optimized Git HEAD compilation of [vllm.cpp](https://github.com/mudler/vllm.cpp) for Arch Linux with **HIP/ROCm** and **Vulkan** acceleration.

`vllm.cpp` is a Python-free, lightweight C++ serving engine providing 1:1, vLLM-alike features (continuous batching, paged KV cache) with zero PyTorch runtime dependencies.

## Binaries & Features Included

- **`vllm-server`**: OpenAI-compatible HTTP API server for LLM inference.
- **`vllm-cli`**: Command-line interactive prompt and inference runner.
- **`vllm-bench`**: Engine benchmark tool (throughput, latency, TTFT evaluation).
- **`libvllm.so` / `vllm.h`**: Shared C++ library and public C ABI header for embedding `vllm.cpp` into downstream applications.

## Backends

- **HIP/ROCm**: Native AMD GPU kernel execution (automatically targets host ROCm GPU architecture e.g. `gfx1030`, `gfx1100`, `gfx90a`).
- **Vulkan**: Portable cross-vendor GPU execution backend.
- **CPU**: Optimized fallback backend.

## Installation

```bash
cd vllm.cpp-git-hip
makepkg -si
```

## Quick Start

```bash
# Run OpenAI-compatible API server
vllm-server --model /path/to/model.gguf --port 28080

# Interactive CLI inference
vllm-cli --model /path/to/model.gguf --prompt "Hello!"

# Benchmark throughput & latency
vllm-bench --model /path/to/model.gguf
```
