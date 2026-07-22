# TEI and MLC-LLM Packaging and Build Research

This document outlines the build plan, hardware target information, and dependency constraints for building Text Embeddings Inference (TEI) and MLC-LLM sequentially on ROCm/Vulkan.

## Hardware & OS Environment
* **CPU/Host Platform:** Arch Linux x86_64
* **Python Stack:** Default python is **3.14.5**.
* **GPU Profiles:**
  * Discrete GPU (dGPU): `AMD Radeon Pro W6800` / `RX 7900 XTX` (RDNA3, `gfx1100`), using `rocm-hip-sdk` (7.2.4-1) and `vulkan-radeon` (Mesa RADV Vulkan).
  * Integrated GPU (iGPU): `AMD Radeon Renoir` (GCN5, `gfx90c`), using Mesa RADV Vulkan.
* **FlashInfer Status:** `python-flashinfer-rocm` version `0.5.3-2` has been successfully compiled and installed as a system package.

## Packaging Plans

### 1. `python-grpc-interceptor` (Status: Built)
* **Metadata:** Pure Python package, version `0.15.4`.
* **Build tool:** `python-build` + `python-installer` (with setuptools/poetry backend support).
* **Package File:** `python-grpc-interceptor-0.15.4-1-any.pkg.tar.zst` (needs manual installation prior to building `tei`).

### 2. `python-grpcio-reflection` (Status: Built)
* **Metadata:** Pure Python package, version `1.81.0`.
* **Build tool:** `python-build` + `python-installer` (with setuptools backend).
* **Package File:** `python-grpcio-reflection-1.81.0-1-any.pkg.tar.zst` (needs manual installation prior to building `tei`).

### 3. `tei` (Text Embeddings Inference - ROCm)
* **Description:** Hugging Face server for text embedding models, accelerated via ROCm.
* **Build Strategy:**
  1. Rust router binary compiled using `cargo` with `python,http` features enabled, targeting AMD Instinct / RDNA3 architectures.
  2. Python gRPC backend server packages (generated stubs + backend code) compiled and installed into `/usr/lib/python3.14/site-packages`.
* **System Dependencies:**
  * Build-time: `rust`, `cargo`, `protobuf`, `python-grpcio-tools`, `git`.
  * Runtime: `python-pytorch-opt-rocm`, `python-safetensors`, `python-einops`, `python-packaging`, `python-grpcio`, `python-grpcio-status`, `python-grpcio-reflection`, `python-grpc-interceptor`.

### 4. `mlc-llm` (Universal LLM serving engine)
* **Description:** Multi-backend LLM execution engine compiled with TVM Unity Relax support.
* **Build Strategy:**
  1. Compiles the internal `3rdparty/tvm` submodule (pointing to `mlc-ai/relax` fork) inline.
  2. Submodule TVM build options: `USE_ROCM=ON`, `USE_VULKAN=ON`, `USE_CUDA=OFF`.
  3. Package split:
     * `mlc-llm`: C++ libraries (`libmlc_llm.so`) and command line executables.
     * `python-mlc-llm`: Python compilation bindings (`mlc_llm` package).
* **System Dependencies:**
  * Build-time: `cmake`, `git`, `python-scikit-build-core`, `rocm-hip-sdk`, `vulkan-headers`.
  * Runtime: `python-flashinfer-rocm` (already installed), `python-shortuuid`, `python-ml-dtypes`, `python-tiktoken`, `python-transformers`, `python-fastapi`, `uvicorn`, `python-safetensors`, `python-sentencepiece`, `python-tqdm`, `python-openai`.

## Sequential Build Execution Path
Rather than a concurrent build scheduler, the packages will be compiled sequentially:
1. **`python-grpc-interceptor`** (Done).
2. **`python-grpcio-reflection`** (Done).
3. **`tei`** (Build from source Rust+Python).
4. **`mlc-llm`** (Build C++ shared library + TVM submodule + Python bindings).

