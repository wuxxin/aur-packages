#!/usr/bin/env python3
import sys
import torch
import argparse
import numpy as np
from gguf import GGUFWriter
from dac.model import DAC
from huggingface_hub import hf_hub_download

def convert_dac_to_gguf(repo_id, model_type, output_path, dtype_str="f16"):
    print(f"Loading DAC model from {repo_id} ({model_type})")
    
    # Map dtype string to numpy type
    dt = np.float16 if dtype_str == "f16" else np.float32
    print(f"Target tensor type: {dtype_str} ({dt})")
    
    # Map standard model names to specific weight files in ibm-research/DAC.speech.v1.0
    # or handle custom cases.
    filename = None
    if repo_id == "ibm-research/DAC.speech.v1.0":
        if "24khz" in model_type:
            filename = "weights_24khz_3kbps_v1.0.pth"
        elif "44khz" in model_type:
            filename = "weights_44khz_8kbps_v1.0.pth"
        elif "16khz" in model_type:
            filename = "weights_16khz_3kbps_v1.0.pth"
    
    if filename:
        print(f"Downloading {filename} from {repo_id}...")
        model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    else:
        # If it's a direct path or unknown, try it as is
        model_path = model_type

    print(f"Loading weights from {model_path}...")
    model = DAC.load(model_path)
    model.eval()

    # We only need the decoder for OuteTTS
    decoder = model.decoder
    state_dict = decoder.state_dict()

    writer = GGUFWriter(output_path, "dac-dec")

    # Metadata
    # DAC 24kHz:
    # d_model (features_length) = 1024
    # embedding_dim = 1024 -> 512 (compressed)
    
    # Add dac.ones for Snake activation (1/alpha)
    # This avoids ggml_new_f32() crash in no_alloc context during graph build
    # Add dac.ones for Snake activation (1/alpha)
    # This avoids ggml_new_f32() crash in no_alloc context during graph build
    writer.add_tensor("dac.ones.weight", np.array([1.0], dtype=np.float32))

    # We can infer these from state_dict
    features_length = state_dict['model.0.weight_v'].shape[1] 
    d_model = state_dict['model.0.weight_v'].shape[0]
    # Architecture and Metadata
    writer.add_architecture()
    writer.add_string("general.architecture", "dac-dec")
    writer.add_uint32("dac-dec.vocab_size", 2048) # 1024 * 2 codebooks
    writer.add_uint32("dac-dec.context_length", 4096)
    writer.add_uint32("dac-dec.features_length", features_length)
    writer.add_uint32("dac-dec.feed_forward_length", 1536) # For 1D conv intermediate
    writer.add_uint32("dac-dec.embedding_length", 512)
    writer.add_uint32("dac-dec.block_count", 4)
    writer.add_float32("dac-dec.attention.layer_norm_epsilon", 1e-6)
    writer.add_float32("dac-dec.attention.group_norm_epsilon", 1e-6)
    writer.add_uint32("dac-dec.attention.group_norm_groups", 32)
    writer.add_bool("dac-dec.attention.causal", False)

    # Required for model loader to bypass vocabulary search
    writer.add_string("tokenizer.ggml.model", "none")
    writer.add_uint32("tokenizer.ggml.tokens", 0)

    print("Mapping and fusing tensors...")
    
    # Extract and pre-compute embeddings from quantizer
    q_sd = model.quantizer.state_dict()
    
    def get_fused_out_proj(idx):
        v = q_sd[f'quantizers.{idx}.out_proj.weight_v']
        g = q_sd[f'quantizers.{idx}.out_proj.weight_g']
        b = q_sd[f'quantizers.{idx}.out_proj.bias']
        
        # v: [1024, 8, 1], g: [1024, 1, 1]
        norm = torch.norm(v, p=2, dim=(1, 2), keepdim=True)
        w = v * (g / (norm + 1e-8))
        return w.squeeze(-1), b

    # Codebooks are [1024, 8]
    cb0 = q_sd['quantizers.0.codebook.weight']
    cb1 = q_sd['quantizers.1.codebook.weight']
    
    # Projections
    w0, b0 = get_fused_out_proj(0)
    w1, b1 = get_fused_out_proj(1)
    
    # Compute embeddings: [1024, 1024]
    # z = xW^T + b -> cb [1024, 8] * w^T [8, 1024] -> [1024, 1024]
    emb0 = torch.matmul(cb0, w0.t()) + b0
    emb1 = torch.matmul(cb1, w1.t()) + b1
    
    # Concatenate: [2048, 1024]
    token_embd = torch.cat([emb0, emb1], dim=0)
    
    # GGML expects [n_embd, n_vocab] -> [1024, 2048]
    # Torch [2048, 1024] -> reshape/transpose? 
    # Actually, GGUFWriter expects [N, M] and will handle it.
    writer.add_tensor("token_embd.weight", token_embd.float().numpy())

    # Fusing weight_g and weight_v (Weight Normalization) for decoder
    fused_weights = {}
    
    def fuse_wn(sd, prefix):
        v = sd[f'{prefix}.weight_v']
        g = sd[f'{prefix}.weight_g']
        b = sd.get(f'{prefix}.bias')
        
        # v shape: [O, I, K], g shape: [O, 1, 1]
        norm = torch.norm(v, p=2, dim=(1, 2), keepdim=True)
        w = v * (g / (norm + 1e-8))
        return w, b

    print("Iterating model layers...")
    # Layer 0: Initial Conv
    w, b = fuse_wn(state_dict, 'model.0')
    fused_weights['conv1d.weight'] = w
    if b is not None: fused_weights['conv1d.bias'] = b

    # Upsample blocks 1..4
    for i in range(4): # 24kHz has 4 upsample blocks
        block_prefix = f'model.{i+1}.block'
        
        # block.0: Snake (before upsample)
        fused_weights[f'blk.{i}.snake.alpha'] = state_dict[f'{block_prefix}.0.alpha']

        # block.1: Upsample conv (ConvTranspose1d)
        w, b = fuse_wn(state_dict, f'{block_prefix}.1')
        fused_weights[f'blk.{i}.dac_upsample.weight'] = w
        if b is not None: fused_weights[f'blk.{i}.dac_upsample.bias'] = b
        
        # Residual Units 2..4 (indices in block)
        for j in range(3):
            # j=0 -> index 2, j=1 -> index 3, j=2 -> index 4
            ru_prefix = f'{block_prefix}.{j+2}.block'
            
            # Snake 1
            fused_weights[f'blk.{i}.dac_ru.{j}.snake1.alpha'] = state_dict[f'{ru_prefix}.0.alpha']
            
            # Conv 1
            w, b = fuse_wn(state_dict, f'{ru_prefix}.1')
            fused_weights[f'blk.{i}.dac_ru.{j}.conv1.weight'] = w
            if b is not None: fused_weights[f'blk.{i}.dac_ru.{j}.conv1.bias'] = b
            
            # Snake 2
            fused_weights[f'blk.{i}.dac_ru.{j}.snake2.alpha'] = state_dict[f'{ru_prefix}.2.alpha']
            
            # Conv 2
            w, b = fuse_wn(state_dict, f'{ru_prefix}.3')
            fused_weights[f'blk.{i}.dac_ru.{j}.conv2.weight'] = w
            if b is not None: fused_weights[f'blk.{i}.dac_ru.{j}.conv2.bias'] = b

    # Final Activation and Conv
    fused_weights['output_snake.alpha'] = state_dict['model.5.alpha']
    w, b = fuse_wn(state_dict, 'model.6')
    fused_weights['output.weight'] = w
    if b is not None: fused_weights['output.bias'] = b

    for name, tensor in fused_weights.items():
        data = tensor.float().numpy()
        
        # Biases: reshape to numpy [channels, 1] → GGUF ne=[1, channels] for broadcasting
        # with conv output ne=[OW, channels]. GGUF reverses numpy shape order.
        # Snake alphas: keep as-is (already 3D [1, N, 1])
        if 'bias' in name:
            data = data.reshape(-1, 1) # 2D [channels, 1] -> GGUF ne=[1, channels]
        elif 'alpha' in name and data.ndim == 1:
            data = data.reshape(1, -1, 1)  # [1, N, 1] for snake alpha

        # All tensors in the vocoder are F32 for compatibility.
        # This ensures compatibility with all GGML CPU kernels.
        # Note: The gguf library reverses the numpy shape, so Torch [OC, IC, KW] 
        # naturally becomes ne=[KW, IC, OC]. NO manual transpose is needed.
        # writer.add_tensor(name, data.astype(np.float32))
        writer.add_tensor(name, data.astype(dt))

    print(f"Writing GGUF to {output_path}...")
    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert DAC model to GGUF")
    parser.add_argument("--repo", type=str, default="ibm-research/DAC.speech.v1.0", help="Hugging Face repo ID")
    parser.add_argument("--model", type=str, default="24khz", help="DAC model type or local path")
    parser.add_argument("--output", type=str, default="dac-dec-24khz-f32.gguf", help="Output GGUF path")
    parser.add_argument("--dtype", type=str, choices=["f16", "f32"], default="f32", help="Data type for tensors (default: f32)")
    args = parser.parse_args()
    
    convert_dac_to_gguf(args.repo, args.model, args.output, args.dtype)
