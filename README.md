# AUR-Packages

Arch Linux [AUR packages](https://aur.archlinux.org/) repository for custom PKGBUILDs, utility scripts, and research.

## Repository Structure

- `libggml-git-hip/` — ROCm/HIP accelerated GGML, `llama.cpp`, and `whisper.cpp` packages
- `python-torch*-rocm/` — PyTorch ROCm packages
- `<package-dir>/` — Package directories containing PKGBUILDs
- `scripts/` — Repository utility scripts
- `research/` — Development stats, build notes, and research reports
- `scratch/` — Workspace for temporary build logs and checkout sources (`scratch/*-sources`)

Development activity tracking:

A Development activity tracking for a few selected packages is available in [research/weekly-devel-activity.md](research/weekly-devel-activity.md).

## AUR Maintained Packages 

Packages i currently maintain on AUR:

- [coreos-installer](coreos-installer)
    - Installer for CoreOS disk images
- [librefang-git](librefang-git)
    - Libre-source Agent Operating System built in Rust. One binary, sandboxed, secure (Git VCS version with split packages: CLI, GUI, and WhatsApp gateway).
- [python-librefang-sdk-git](python-librefang-sdk-git)
    - Python Client SDK for the LibreFang Agent OS (Git VCS version).
- [moltis-git](moltis-git)
    - A personal AI gateway written in Rust. One binary, sandboxed, secure. (Git VCS version)
- [picoclaw-git](picoclaw-git)
    - Ultra-Efficient AI Assistant in Go (Nightly Git build)
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


## Private forks of Archlinux/AUR and other custom packages

Can be **broken or bitrotten at anytime**.


### temporary forks of pkgs

- [groonga](groonga) - An open-source fulltext search engine and column store
    - Temporary private fork of AUR package with patch (`fix-blosc2-pkgconfig.patch`) fixing system `blosc2` CMake package detection.

- [python-peft](python-peft)
    - State-of-the-art Parameter-Efficient Fine-Tuning (v0.20.0, , updated, upstream aur is at 0.17)

### currently used private forks (different in AUR)

- [oh-my-pi-git-tag](oh-my-pi-git-tag) - AI coding agent for the terminal
    - Built from git latest tag with dynamically evaluated versioning and system libraries (opus, pcre2).
- [hermes-agent-git](hermes-agent-git) - Locally-run AI agent with tool use, web browsing, and automation (Git Main Branch)
    - System package adaptations: self-update disabled, runtime npm installs pre-built, PR patching mechanism
- [libggml-git-hip](libggml-git-hip) - HIP libggml git version shared library
    - builds `libggml`, `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, `stable-diffusion.cpp`, `qwen3-tts`, `parakeet.cpp` with hip/rocm accel from latest git
    - with patches and Python Bindings to support the latest git version,
    - all packages link dynamically against a single system-wide `libggml-git-hip`.
        - This ensures consistent backend behavior / bug compatibility across all tools.


### experimental packages (not in AUR)

- [amux-git](amux-git) - Multi-session agent orchestrator and control plane
    - Includes custom enhancements to support **Oh-My-Pi (`omp`)** as a first-class agent provider alongside Claude Code, Codex, and Gemini.

- [aoe-git-tag](aoe-git-tag) - Terminal session manager for AI coding agents
    - Built from git latest tag with all features enabled (embedded web dashboard, ACP structured view, cap-std sandboxing, full shell completions).

- Python Support Packages for HF.*, torch, sglang, vllm feature support
    - [python-optimum-amd](python-optimum-amd)
        - Hugging Face Optimum integration for AMD hardware build fixes
    - [python-optimum-rocm](python-optimum-rocm)
        - Accelerated inference and training with Hugging Face Optimum (with ROCm support)
    - [python-gptqmodel-rocm-git](python-gptqmodel-rocm-git)
        - Production ready LLM model compression and quantization toolkit (ROCm support, backend for Optimum)

- [python-infinity-emb](python-infinity-emb)
    - High-throughput, low-latency REST API for serving text-embeddings and reranking models
    - Needs torch, peft and optimum

- [vllm.cpp-git-hip](vllm.cpp-git-hip) - C++ engine for vLLM-alike serving (continuous batching, paged KV)
    - Python-free 1:1 C++ vLLM engine with ROCm/HIP and Vulkan hardware acceleration (`vllm-server`, `vllm-cli`, `vllm-bench`, `libvllm.so`).

- [mlc-llm](mlc-llm)
    - Universal LLM deployment engine via ML compilation (ROCm & Vulkan). Fork of [alansrobotlab2/mlc-llm](https://github.com/alansrobotlab2/mlc-llm) (qwen3_5 branch) adding Qwen3.5/Qwen3.6 (GatedDeltaNet + MoE) model support, with patches for ROCm 7.2 hipblas API compatibility.

- [crane-git](crane-git) - Pure Rust LLM, VLM, VLA, TTS, OCR Inference Engine powered by Candle
    - Custom build from latest git with OpenAI-compatible API server (`crane`), `onnx` features, and demo CLI tools (`crane-chat-simple`, `crane-chat-cli`, `crane-ornith-tools`).

- [tei-rocm](tei-rocm)
    - Hugging Face Text Embeddings Inference (TEI) A blazing fast inference solution for text embeddings models. (with ROCm/HIP support)
    - [python-grpc-interceptor](python-grpc-interceptor)
        - Simplified gRPC interceptors for Python (needed by TEI backend)
    - [python-grpcio-reflection](python-grpcio-reflection)
        - Standard Protobuf reflection service for gRPC Python (needed by TEI backend)

- [smg](smg)
    - High-performance model-routing gateway for large-scale LLM deployments


- [pocket-tts.cpp-git](pocket-tts.cpp-git) - Single-file C++ TTS runtime for Pocket TTS with ONNX Runtime
    - builds `pocket-tts` C++ executable and shared library `libpocket_tts.so` with support for voice cloning, streaming, HTTP server, and FFI C API.
    - [python-pocket-tts](python-pocket-tts) - A TTS that fits in your CPU (and pocket)
        - builds `pocket-tts` python package by Kyutai Labs.


