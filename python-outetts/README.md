# python-outetts AUR Package

This is the Arch User Repository (AUR) package for `outetts`, a Text-to-Speech library by OuteAI.

## Source
Upstream: [https://github.com/edwko/OuteTTS](https://github.com/edwko/OuteTTS)

## Variants

This package is split into multiple variants to support different hardware backends (via `llama.cpp`):

- `python-outetts-cpu`: Standard CPU inference. Refers to `python-llama-cpp`.
- `python-outetts-cuda`: CUDA (NVIDIA GPU) acceleration. Refers to `python-llama-cpp-cuda`.
- `python-outetts-hip`: HIP (AMD ROCm) acceleration. Refers to `python-llama-cpp-hip`.
- `python-outetts-vulkan`: Vulkan (Cross GPU) acceleration. Refers to `python-llama-cpp-vulkan`.

## Installation

Install the variant matching your hardware:

```bash
# For AMD GPUs (HIP)
makepkg -si --pkg python-outetts-hip

# For NVIDIA GPUs (CUDA)
makepkg -si --pkg python-outetts-cuda

# For CPU only
makepkg -si --pkg python-outetts-cpu
```

## Troubleshooting

If you encounter build errors, ensure all AUR dependencies are installed. You can verify available dependencies or build them yourself.

### Clean Build
If you face repeated errors or strange linking issues, try a clean build:

```bash
rm -rf src/ pkg/ *.pkg.tar.zst
makepkg -siC
```
