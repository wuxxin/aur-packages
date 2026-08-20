# Qwen3-Next (Qwen3.6-35B-A3B-APEX-I-Compact.gguf) vLLM Integration Research

This document outlines the findings, architecture, and monkey-patches required to load and serve `Qwen3.6-35B-A3B-APEX-I-Compact.gguf` under vLLM using AMD ROCm without system-wide modifications.

## 1. Model Architecture Overview

The model is a hybrid architecture combining multiple state-of-the-art layers:
- **Standard Attention Layers:** Traditional self-attention.
- **GDN (Gated DeltaNet) Linear Attention Layers:** Specialized linear attention using Triton/FLA.
- **SSM (MambaMixer2) Layers:** State Space Model layers.
- **MoE (Mixture of Experts) MLP Layers:** Gated expert layers for token routing.
- **Tied Word Embeddings:** `lm_head` shares weights with `embed_tokens`.

In the GGUF metadata, it is identified as `qwen35moe`, which maps to `Qwen3NextForCausalLM` in vLLM.

---

## 2. Issues Encountered & Solutions (Monkey-Patches)

### Issue 1: Unrecognized `qwen35moe` Architecture
- **Symptom:** `transformers` and `vllm` fail to load GGUF checkpoints with architecture `qwen35moe`.
- **Solution:** Patched `transformers.modeling_gguf_pytorch_utils` mapping `qwen35moe` -> `qwen3_moe` and overriding `model_type` to `qwen3_next` and `architectures` to `Qwen3NextForCausalLM`.

### Issue 2: Vision Config Extraction Error
- **Symptom:** Numpy scalar conversion error in `extract_vision_config_from_gguf`.
- **Solution:** Patched `gguf_utils.extract_vision_config_from_gguf` to return a dummy `SiglipVisionConfig()`.

### Issue 3: Unmapped GGUF Parameters
- **Symptom:** `RuntimeError: Failed to map GGUF parameters (...)` due to SSM and MoE expert parameters.
- **Solution:** Overrode `GGUFModelLoader._get_gguf_weights_map` to include explicit mapping definitions for:
  - SSM variables (e.g. `conv1d.weight`, `A_log`, `dt_bias`, `norm.weight`, `out_proj.weight`).
  - Virtual split projections for attention (`attn_qkv.weight`, `attn_gate.weight`) and SSM (`ssm_beta.weight`, `ssm_alpha.weight`).
  - MoE shared experts and gate inputs.

### Issue 4: `lm_head` Quantization Registration
- **Symptom:** `There is no module or parameter named lm_head.qweight_type` when loading GGUF.
- **Solution:** Patched `Qwen3NextForCausalLM.__init__` to recreate `lm_head` with `quant_config` so the GGUF-specific quantization attributes are registered. Assigned it to `self.model.embed_tokens` when `tie_word_embeddings=True`.

### Issue 5: Linear Attention Projection Layout & Quantization Mismatch
- **Symptom:** `in_proj_qkvz` and `in_proj_ba` are sharded as separate GGUF tensors (`attn_qkv`/`attn_gate` and `ssm_beta`/`ssm_alpha`) with mismatched quantization formats (`Q8_0` vs `Q4_K`). View-splitting or concatenating raw quantized byte tensors corrupts the weights, causing the model to output scrambled text.
- **Solution:** 
  1. Add GDN projection layers (`layers.{i}.linear_attn.in_proj_qkvz` and `layers.{i}.linear_attn.in_proj_ba`) to `vllm_config.quant_config.unquantized_modules`. This forces vLLM to instantiate them as standard unquantized float16 parallel linear layers.
  2. Intercept the quantized GGUF shards in `load_weights`.
  3. Dequantize the shards to float16 on the GPU using `vllm._custom_ops.ggml_dequantize`.
  4. Interleave the dequantized float16 heads to match the head-interleaved GQA layout expected by the model.
  5. Load the final interleaved float16 tensor directly into the standard parallel linear parameter.

### Issue 6: 1D to 2D / 2D to 3D Tensor Shapes
- **Symptom:** 
  - `conv1d.weight` expected 3D `[conv_dim, 1, kernel]` but GGUF provided 2D `[conv_dim, kernel]`.
  - `shared_expert_gate` expected 2D `[1, hidden]` but GGUF provided 1D `[hidden]`.
- **Solution:** Added shape corrections (`unsqueeze`) in a customized `load_weights` loop.

---

## 3. Current Running Status
- The server is being executed via `launch_vllm_chat.py` on port `20080` with AMD ROCm acceleration.
- Attention backend overridden to `ROCM_ATTN` out of potential backends `['ROCM_ATTN', 'TRITON_ATTN']`.
- Prefill kernel uses Triton/FLA GDN.
