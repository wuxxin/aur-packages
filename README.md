## AUR-Packages

Archlinux [AUR packages](https://aur.archlinux.org/) i currently maintain:

- [coreos-installer](coreos-installer)
    - Installer for CoreOS disk images
- [librefang-git](librefang-git)
    - Libre-source Agent Operating System built in Rust. One binary, sandboxed, secure (Git VCS version with split packages: CLI, GUI, and WhatsApp gateway).
- [python-librefang-sdk-git](python-librefang-sdk-git)
    - Python Client SDK for the LibreFang Agent OS (Git VCS version).
- [moltis-git](moltis-git)
    - A personal AI gateway written in Rust. One binary, sandboxed, secure. (Git VCS version)
- [pulumi-git](pulumi-git) - Modern Infrastructure as Code
    - build from the latest git tag with enabled python and nodejs dynamic provider
- [python-bitsandbytes-rocm-git](python-bitsandbytes-rocm-git)
    - Accessible large language models via k-bit quantization for PyTorch (GIT Version, with ROCm support)
- [python-torchao-rocm](python-torchao-rocm)
    - PyTorch native quantization and sparsity for training and inference (with ROCM support)
- [python-torchaudio-rocm](python-torchaudio-rocm)
    - PyTorch Data manipulation and transformation for audio signal processing (with ROCM support)
- [python-torchvision-rocm](python-torchvision-rocm)
    - PyTorch Datasets, transforms, and models specific to computer vision (with ROCM support)
- [salt](salt)
    - Portable, distributed, remote execution and configuration management system
- [signal-cli-rest-api-git](signal-cli-rest-api-git) - A small REST API around signal-cli 
    - GIT version with patches for unix socket, token auth and polling support
- [solo1](solo1)
    - Python tool and library for SoloKeys Solo 1
- [zeroclaw-git](zeroclaw-git)
    - Fast, small, and fully autonomous AI assistant infrastructure (Rust, Git VCS version with all features and embedded web dashboard).


### Private forks of Archlinux/AUR and other custom packages

Can be **broken or bitrotten at anytime**.


Currently using:

- [groonga](groonga) - An open-source fulltext search engine and column store
    - Temporary private fork of AUR package with patch (`fix-blosc2-pkgconfig.patch`) fixing system `blosc2` CMake package detection.
- [oh-my-pi-git-tag](oh-my-pi-git-tag) - AI coding agent for the terminal
    - Built from git latest tag with dynamically evaluated versioning and system libraries (opus, pcre2).
- [hermes-agent-git](hermes-agent-git) - Locally-run AI agent with tool use, web browsing, and automation (Git Main Branch)
    - System package adaptations: self-update disabled, runtime npm installs pre-built, PR patching mechanism
- [libggml-git-hip](libggml-git-hip) - HIP libggml git version shared library
    - builds `libggml`, `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, and `stable-diffusion.cpp` with hip/rocm accel from latest git
    - with patches for RDNA2,  Python Bindings to support the latest git version,
    - all packages link dynamically against a single system-wide `libggml-git-hip`.
        - This ensures consistent backend behavior / bug compatibility across all tools.

testing:

- [smg](smg)
    - High-performance model-routing gateway for large-scale LLM deployments

- [crane-git](crane-git) - Pure Rust LLM, VLM, VLA, TTS, OCR Inference Engine powered by Candle
    - Custom build from latest git with OpenAI-compatible API server (`crane`), `onnx` features, and demo CLI tools (`crane-chat-simple`, `crane-chat-cli`, `crane-ornith-tools`).

- [python-grpc-interceptor](python-grpc-interceptor)
    - Simplified gRPC interceptors for Python (needed by TEI backend)
- [python-grpcio-reflection](python-grpcio-reflection)
    - Standard Protobuf reflection service for gRPC Python (needed by TEI backend)
- [tei-rocm](tei-rocm)
    - Hugging Face Text Embeddings Inference (TEI) A blazing fast inference solution for text embeddings models. (with ROCm/HIP support)

- [mlc-llm](mlc-llm)
    - Universal LLM deployment engine via ML compilation (ROCm & Vulkan). Fork of [alansrobotlab2/mlc-llm](https://github.com/alansrobotlab2/mlc-llm) (qwen3_5 branch) adding Qwen3.5/Qwen3.6 (GatedDeltaNet + MoE) model support, with patches for ROCm 7.2 hipblas API compatibility.

- [python-peft](python-peft)
    - State-of-the-art Parameter-Efficient Fine-Tuning (v0.20.0, , updated, upstream aur is at 0.17)
- [python-optimum-amd](python-optimum-amd)
    - Hugging Face Optimum integration for AMD hardware build fixes
- [python-optimum-rocm](python-optimum-rocm)
    - Accelerated inference and training with Hugging Face Optimum (with ROCm support)
- [python-infinity-emb](python-infinity-emb)
    - High-throughput, low-latency REST API for serving text-embeddings and reranking models


- [pocket-tts.cpp-git](pocket-tts.cpp-git) - Single-file C++ TTS runtime for Pocket TTS with ONNX Runtime
    - builds `pocket-tts` C++ executable and shared library `libpocket_tts.so` with support for voice cloning, streaming, HTTP server, and FFI C API.
- [python-pocket-tts](python-pocket-tts) - A TTS that fits in your CPU (and pocket)
    - builds `pocket-tts` python package by Kyutai Labs.


### Workspace & Scratch Directory Usage

All temporary files, build logs, intermediate test outputs, and source checkouts (`scratch/*-sources`) must be stored in `scratch/`:
- **Standalone Repository**: Use `./scratch/` at the root of `aur-packages/`.
- **Submodule Checkout**: Always defer to the top-level parent repository's root `scratch/` directory.

### Weekly development activity tracking

Development activity tracking for a few selected packages are available in [research/weekly-devel-activity.md](research/weekly-devel-activity.md).


### Notes/Todo

- update salt (3008.1)
- rebuild signal-cli-res-api-git


