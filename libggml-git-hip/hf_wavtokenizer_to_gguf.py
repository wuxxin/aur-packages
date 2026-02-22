#!/usr/bin/env python3
import sys
import os
import torch
import numpy as np
from huggingface_hub import hf_hub_download
from gguf import GGUFWriter
import shutil
import re

def prepare_and_convert(model_id, output_name):
    print(f"Phase 1: Downloading decoder from {model_id}...")
    
    # Download decoder or use local file
    if os.path.isfile(model_id):
        local_pt = model_id
    else:
        # Try both the v1 and v2 filenames
        try:
            local_pt = hf_hub_download(repo_id=model_id, filename="decoder/decoder_model.pt")
        except:
            local_pt = hf_hub_download(repo_id=model_id, filename="wavtokenizer_large_speech_320_v2.ckpt")
    
    temp_dir = "temp_wavtokenizer"
    os.makedirs(temp_dir, exist_ok=True)

    print("Phase 2: Loading and remapping weights...")
    # Using weights_only=True for security, but we trust this source
    sd = torch.load(local_pt, map_location="cpu", weights_only=True)
    
    if "state_dict" in sd:
        sd = sd["state_dict"]
        
    # Flatten if nested
    flat_sd = {}
    def flatten(d, prefix=""):
        for k, v in d.items():
            if isinstance(v, torch.Tensor):
                flat_sd[prefix + k] = v
            elif isinstance(v, dict):
                flatten(v, prefix + k + ".")
    
    flatten(sd)

    processed_sd = {}
    for norm_key, val in flat_sd.items():
        # Remove common prefixes
        new_key = norm_key.replace("model_state_dict.", "").replace("state_dict.", "")
        
        # Mapping to llama.cpp WavTokenizer architecture expectations
        mapped = True
        if new_key == "codebook_weights":
            new_key = "token_embd.weight"
        elif new_key == "backbone.embed.weight":
            new_key = "conv1d.weight"
        elif new_key == "backbone.embed.bias":
            new_key = "conv1d.bias"
        elif new_key == "backbone.norm.scale.weight":
            new_key = "output_norm.weight"
            if val.ndim > 1: val = val[0]
        elif new_key == "backbone.norm.shift.weight":
            new_key = "output_norm.bias"
            if val.ndim > 1: val = val[0]
        elif new_key.startswith("backbone.convnext."):
            # backbone.convnext.0.dwconv.weight -> convnext.0.dw.weight
            parts = new_key.split('.')
            idx = parts[2]
            suffix = ".".join(parts[3:])
            if suffix == "dwconv.weight": sub = "dw.weight"
            elif suffix == "dwconv.bias": sub = "dw.bias"
            elif suffix == "norm.scale.weight": 
                sub = "norm.weight"
                if val.ndim > 1: val = val[0]
            elif suffix == "norm.shift.weight": 
                sub = "norm.bias"
                if val.ndim > 1: val = val[0]
            elif suffix == "pwconv1.weight": sub = "pw1.weight"
            elif suffix == "pwconv1.bias": sub = "pw1.bias"
            elif suffix == "pwconv2.weight": sub = "pw2.weight"
            elif suffix == "pwconv2.bias": sub = "pw2.bias"
            elif suffix == "gamma": sub = "gamma.weight"
            else: continue
            new_key = f"convnext.{idx}.{sub}"
        elif new_key.startswith("backbone.pos_net."):
            # backbone.pos_net.0.norm1.weight -> posnet.0.norm1.weight
            parts = new_key.split('.')
            idx = int(parts[2])
            suffix = ".".join(parts[3:])
            
            if idx == 2:
                # Attention layer
                if suffix == "norm.weight": sub = "attn_norm.weight"
                elif suffix == "norm.bias": sub = "attn_norm.bias"
                elif suffix == "q.weight": sub = "attn_q.weight"
                elif suffix == "q.bias": sub = "attn_q.bias"
                elif suffix == "k.weight": sub = "attn_k.weight"
                elif suffix == "k.bias": sub = "attn_k.bias"
                elif suffix == "v.weight": sub = "attn_v.weight"
                elif suffix == "v.bias": sub = "attn_v.bias"
                elif suffix == "proj_out.weight": sub = "attn_output.weight"
                elif suffix == "proj_out.bias": sub = "attn_output.bias"
                else: continue
            elif idx == 5:
                # Final norm - llama.cpp uses attn_norm enum for this index
                if suffix == "weight": sub = "attn_norm.weight"
                elif suffix == "bias": sub = "attn_norm.bias"
                else: continue
            else:
                # Standard posnet layers
                if suffix == "scale.weight": sub = "weight"
                elif suffix == "shift.weight": sub = "bias" # Wait, normalize.
                elif suffix == "norm1.weight": sub = "norm1.weight"
                elif suffix == "norm1.bias": sub = "norm1.bias"
                elif suffix == "norm2.weight": sub = "norm2.weight"
                elif suffix == "norm2.bias": sub = "norm2.bias"
                elif suffix == "conv1.weight": sub = "conv1.weight"
                elif suffix == "conv1.bias": sub = "conv1.bias"
                elif suffix == "conv2.weight": sub = "conv2.weight"
                elif suffix == "conv2.bias": sub = "conv2.bias"
                elif suffix == "weight" and "norm" in new_key: sub = "weight"
                elif suffix == "bias" and "norm" in new_key: sub = "bias"
                else: sub = suffix
            
            new_key = f"posnet.{idx}.{sub}"
        elif new_key == "head.out.weight":
            new_key = "output.weight"
        elif new_key == "head.out.bias":
            new_key = "output.bias"
        else:
            mapped = False
            continue

        if mapped:
            print(f"  Map: {norm_key} -> {new_key}")

        # Convert to numpy f32 for processing
        data = val.float().numpy()
        
        if new_key == "token_embd.weight":
            # [4096, 512] -> GGML d0=512, d1=4096. No transpose needed.
            pass 
        elif new_key == "conv1d.weight":
            # [OC=512, IC=512, KW=1] -> GGML ne={1, 512, 512}
            # Torch [OC, IC, KW] maps to GGML ne={KW, IC, OC} via Numpy shape (OC, IC, KW)
            if data.ndim == 2:
                data = data.reshape(data.shape[0], data.shape[1], 1)
        elif "posnet" in new_key and "conv" in new_key and "weight" in new_key:
            # [OC, IC, KW] -> GGML ne={KW, IC, OC}
            if data.ndim == 2:
                data = data.reshape(data.shape[0], data.shape[1], 1)
        elif "attn_q" in new_key or "attn_k" in new_key or "attn_v" in new_key or "attn_output" in new_key:
            if "weight" in new_key:
                if data.ndim == 2:
                    data = data.reshape(data.shape[0], data.shape[1], 1)
        elif ".dw.weight" in new_key:
            # [OC, 1, KW] -> GGML ne={KW, 1, OC}
            if data.ndim == 2:
                data = data.reshape(data.shape[0], data.shape[1], 1)
        elif ".pw1.weight" in new_key or ".pw2.weight" in new_key:
            # [OC, IC, KW=1] -> GGML ne={1, IC, OC}
            if data.ndim == 2:
                data = data.reshape(data.shape[0], data.shape[1], 1)
        
        # Biases and norms: Keep as 1D (GGUF ne=[N, 1, 1, 1])
        if data.ndim == 1:
            data = data.squeeze()
        
        processed_sd[new_key] = data

    # Ensure token_embd_norm is present (identity if missing)
    if "token_embd_norm.weight" not in processed_sd:
        print("  Adding dummy token_embd_norm.weight")
        processed_sd["token_embd_norm.weight"] = np.ones(768, dtype=np.float32)
    if "token_embd_norm.bias" not in processed_sd:
        print("  Adding dummy token_embd_norm.bias")
        processed_sd["token_embd_norm.bias"] = np.zeros(768, dtype=np.float32)

    # Ensure output_norm is present (identity if missing)
    if "output_norm.weight" not in processed_sd:
        print("  Adding dummy output_norm.weight")
        processed_sd["output_norm.weight"] = np.ones(768, dtype=np.float32)
    if "output_norm.bias" not in processed_sd:
        print("  Adding dummy output_norm.bias")
        processed_sd["output_norm.bias"] = np.zeros(768, dtype=np.float32)

    print(f"Processed {len(processed_sd)} tensors.")

    print(f"Phase 3: Writing GGUF to {output_name}...")
    writer = GGUFWriter(output_name, "wavtokenizer-dec")
    
    writer.add_name("WavTokenizer")
    writer.add_uint32("wavtokenizer-dec.vocab_size", 4096)
    writer.add_uint32("wavtokenizer-dec.context_length", 4096)
    writer.add_uint32("wavtokenizer-dec.features_length", 512)
    # n_embd_out() dimension: 
    # For OuteTTS 1.0 75token, the head.out is 1282 spectrogram bins.
    # llama.cpp sets n_embd_out_impl = LLM_KV_EMBEDDING_LENGTH.
    writer.add_uint32("wavtokenizer-dec.embedding_length", 1282) 
    
    writer.add_uint32("wavtokenizer-dec.block_count", 12)
    writer.add_uint32("wavtokenizer-dec.attention.head_count", 1)
    writer.add_uint32("wavtokenizer-dec.feed_forward_length", 2304)
    writer.add_float32("wavtokenizer-dec.attention.layer_norm_epsilon", 1e-6)
    writer.add_float32("wavtokenizer-dec.attention.group_norm_epsilon", 1e-6)
    writer.add_uint32("wavtokenizer-dec.attention.group_norm_groups", 32)
    
    writer.add_uint32("wavtokenizer-dec.posnet.embedding_length", 768)
    writer.add_uint32("wavtokenizer-dec.posnet.block_count", 6)
    writer.add_uint32("wavtokenizer-dec.convnext.embedding_length", 768)
    writer.add_uint32("wavtokenizer-dec.convnext.block_count", 12)
    writer.add_bool("wavtokenizer-dec.attention.causal", False)

    # Required for model loader to bypass vocabulary search
    writer.add_string("tokenizer.ggml.model", "none")
    writer.add_uint32("tokenizer.ggml.tokens", 0)
    
    writer.add_file_type(0) # F32
    writer.add_quantization_version(2)

    for name, data in processed_sd.items():
        # Use F32 for everything in the vocoder. 
        # Although larger, it ensures compatibility with all GGML CPU kernels (avoiding im2col_f16/binary_op_f16 issues).
        data_out = data.astype(np.float32)
        writer.add_tensor(name, data_out)

    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    print("--------------------------------------------------")
    print(f"Success! GGUF model created: {output_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python outetts-hf-wavtokenizer-to-gguf.py [model_id] [output_name]")
        sys.exit(1)
    model_id = sys.argv[1]
    output_name = sys.argv[2]
    prepare_and_convert(model_id, output_name)
