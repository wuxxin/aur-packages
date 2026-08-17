# python-infinity-emb

High-throughput, low-latency REST API and engine for serving text embeddings, cross-encoder rerankers, vision-language models, and audio embeddings.

## Engine & Backend Feature Matrix

| Feature / Backend | Package | Role & Capabilities |
| :--- | :--- | :--- |
| **ROCm Hardware Acceleration** | `python-optimum` *(or `python-optimum-rocm`)* | Enables `--engine optimum` with `ROCMExecutionProvider` and `MIGraphXExecutionProvider` on AMD GPUs. |
| **GPTQ Quantization** | `python-gptqmodel` *(or `python-gptqmodel-rocm-git`)* | Unlocks serving large 4-bit/8-bit quantized embedding models (e.g. `Qwen2-7B-Embedding`, `bge-reranker-v2-m3`) via `optimum.gptq` with low VRAM footprint. |
| **Low-Bit `torch.compile`** | `python-torchao` *(or `python-torchao-rocm`)* | Unlocks native PyTorch low-bit linear quantization (`int8wo`, `int4wo`, `fp6`, `fp8`) fused directly with `--compile` kernel acceleration. |
| **8-bit / 4-bit Inference** | `python-bitsandbytes` *(or `python-bitsandbytes-rocm-git`)* | Enables 8-bit / 4-bit quantized weight loading in `--engine torch` (`load_in_8bit=True`). |
| **Domain-Adapted Adapters** | `python-peft` | Enables loading fine-tuned LoRA / PEFT adapter weights over base embedding models. |
| **Audio Embeddings** | `python-torchaudio` *(or `python-torchaudio-rocm`)* | Enables audio embedding models (CLAP, Wav2Vec, Whisper encoder) for audio similarity and classification. |
| **Vision-Language Embeddings** | `python-pillow` | Enables multi-modal vision-language embedding pipelines (ColPali, CLIP). |

---

## Supported Engine Modes

- **`--engine torch`**: PyTorch backend with dynamic request batching, mixed precision (`fp16`/`bf16`), and optional `--compile`.
- **`--engine optimum`**: Hugging Face Optimum backend for accelerated ONNX and ROCm/MIGraphX graph execution.
- **`--engine ctranslate2`**: CTranslate2 quantized CPU/GPU backend.
