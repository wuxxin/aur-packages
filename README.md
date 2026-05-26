## AUR-Packages

Archlinux [AUR packages](https://aur.archlinux.org/) i currently maintain:

- [coreos-installer](coreos-installer)
    - Installer for CoreOS disk images
- [librefang-git](librefang-git)
    - Libre-source Agent Operating System built in Rust. One binary, sandboxed, secure (Git VCS version with all split packages: CLI, GUI, and WhatsApp gateway).
- [moltis-git](moltis-git)
    - A personal AI gateway written in Rust. One binary, sandboxed, secure. (Git VCS version)
- [pulumi-git](pulumi-git) - Modern Infrastructure as Code
    - build from the latest git tag with enabled python and nodejs dynamic provider
- [python-torchao-rocm](python-torchao-rocm)
    - PyTorch native quantization and sparsity for training and inference (with ROCM support)
- [python-torchaudio-rocm](python-torchaudio-rocm)
    - PyTorch Data manipulation and transformation for audio signal processing (with ROCM support)
- [python-torchvision-rocm](python-torchvision-rocm)
    - PyTorch Datasets, transforms, and models specific to computer vision (with ROCM support)
- [salt](salt)
    - Portable, distributed, remote execution and configuration management system
- [solo1](solo1)
    - Python tool and library for SoloKeys Solo 1
- [zeroclaw-git](zeroclaw-git)
    - Fast, small, and fully autonomous AI assistant infrastructure (Rust, Git VCS version with all features and embedded web dashboard).


---

### Private forks of Archlinux/AUR and other custom packages

Can be **broken or bitrotten at anytime**.

- [libggml-git-hip](libggml-git-hip) - HIP libggml git version shared library
    - builds `libggml`, `llama.cpp`, `whisper.cpp`, `python-llama-cpp`, and `stable-diffusion.cpp` with hip/rocm accel from latest git
    - with patches for RDNA2,  Python Bindings to support the latest git version,
    - all packages link dynamically against a single system-wide `libggml-git-hip`.
        - This ensures consistent backend behavior / bug compatibility across all tools.

- [python-bitsandbytes-rocm-git](python-bitsandbytes-rocm-git) - Lightweight wrapper around CUDA/HIP custom functions, in particular 8-bit optimizers, matrix multiplication (LLM.int8()), and quantization functions
    - switched to main branch, other branch is stale

- [signal-cli-rest-api-git](signal-cli-rest-api-git) - A small REST API around signal-cli (Go implementation) with polling support, currently not in AUR

- [python-vllm-rocm-git](python-vllm-rocm-git) - High-throughput and memory-efficient inference and serving engine for LLMs (ROCm support, Git VCS version)

- [python-vllm-omni-rocm-git](python-vllm-omni-rocm-git) - A framework for efficient model inference with omni-modality models (ROCm support, depends on python-vllm-rocm-git)

