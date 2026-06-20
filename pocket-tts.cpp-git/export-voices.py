#!/usr/bin/env python
import argparse
import os
import struct
import sys

try:
    import torch
    import safetensors.torch
    from huggingface_hub import hf_hub_download
except ImportError as e:
    print(f"Error: missing required python package: {e}", file=sys.stderr)
    print("Please install: python-pytorch python-safetensors python-huggingface-hub", file=sys.stderr)
    sys.exit(1)

# Predefined voices mapping: voice_name -> (language_dir, hf_file_name)
VOICE_MAP = {
    "alba": ("english_2026-01", "alba"),
    "juergen": ("german", "juergen"),
    "giovanni": ("italian_24l", "giovanni"),
    "lola": ("spanish_24l", "lola"),
    "rafael": ("portuguese_24l", "rafael"),
    "estelle": ("french_24l", "estelle"),
}

ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT16 = 10
ONNX_TENSOR_ELEMENT_DATA_TYPE_INT64 = 7

def serialize_kv(safetensors_path, out_kv_path, out_emb_path):
    state = {}
    with safetensors.safe_open(safetensors_path, framework="pt") as f:
        for key in f.keys():
            state[key] = f.get_tensor(key)
            
    blob = bytearray()
    num_layers = 6
    for i in range(num_layers):
        cache_key = f"transformer.layers.{i}.self_attn/cache"
        offset_key = f"transformer.layers.{i}.self_attn/offset"
        
        cache_tensor = state[cache_key] # Shape: [2, 1, S, 16, 64]
        offset_tensor = state[offset_key] # Shape: [1]
        
        k_cache = cache_tensor[0] # Shape: [1, S, 16, 64]
        v_cache = cache_tensor[1] # Shape: [1, S, 16, 64]
        
        # State i*3 + 0: Key cache
        blob.extend(struct.pack("<i", 4))
        blob.extend(struct.pack("<4q", *k_cache.shape))
        blob.extend(struct.pack("<i", ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT16))
        k_fp16 = k_cache.to(torch.float16).numpy().tobytes()
        blob.extend(struct.pack("<q", len(k_fp16)))
        blob.extend(k_fp16)
        
        # State i*3 + 1: Value cache
        blob.extend(struct.pack("<i", 4))
        blob.extend(struct.pack("<4q", *v_cache.shape))
        blob.extend(struct.pack("<i", ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT16))
        v_fp16 = v_cache.to(torch.float16).numpy().tobytes()
        blob.extend(struct.pack("<q", len(v_fp16)))
        blob.extend(v_fp16)
        
        # State i*3 + 2: Offset
        blob.extend(struct.pack("<i", 1))
        blob.extend(struct.pack("<q", 1))
        blob.extend(struct.pack("<i", ONNX_TENSOR_ELEMENT_DATA_TYPE_INT64))
        offset_data = offset_tensor.to(torch.int64).numpy().tobytes()
        blob.extend(struct.pack("<q", len(offset_data)))
        blob.extend(offset_data)

    os.makedirs(os.path.dirname(out_kv_path), exist_ok=True)
    with open(out_kv_path, "wb") as f:
        f.write(struct.pack("<I", 0x3143564B)) # Magic "KVC1"
        payload_size = 4 + 4 + len(blob)
        f.write(struct.pack("<Q", payload_size))
        f.write(struct.pack("<i", 0)) # current_buf
        f.write(struct.pack("<i", 18)) # num_states
        f.write(blob)
        
    with open(out_emb_path, "wb") as f:
        f.write(struct.pack("<I", 0x31424D45)) # Magic "EMB1"
        f.write(struct.pack("<i", 3)) # ndims
        f.write(struct.pack("<3q", 1, 8, 1024)) # shape
        dummy_data = struct.pack("<8192f", *[0.0]*8192)
        f.write(dummy_data)

def main():
    parser = argparse.ArgumentParser(description="Export and compile predefined voices for PocketTTS.cpp")
    parser.add_argument("--voice", choices=list(VOICE_MAP.keys()) + ["all"], default="all",
                        help="Predefined voice to export (default: all)")
    parser.add_argument("--output", default="voices",
                        help="Output directory for voice caches (default: ./voices)")
    args = parser.parse_args()

    repo_id = "kyutai/pocket-tts-without-voice-cloning"
    revision = "e041936c75475d350b405bc870bcf7c22da4e9e6"

    to_download = []
    if args.voice == "all":
        to_download = list(VOICE_MAP.keys())
    else:
        to_download = [args.voice]

    for voice in to_download:
        lang_dir, name = VOICE_MAP[voice]
        filename = f"languages/{lang_dir}/embeddings/{name}.safetensors"
        
        print(f"Downloading predefined voice '{voice}' ({lang_dir})...")
        try:
            cached_file = hf_hub_download(repo_id=repo_id, filename=filename, revision=revision)
            
            out_kv_path = os.path.join(args.output, ".cache", f"{voice}.kv")
            out_emb_path = os.path.join(args.output, ".cache", f"{voice}.emb")
            
            print(f"Compiling caches for '{voice}'...")
            serialize_kv(cached_file, out_kv_path, out_emb_path)
            print(f"  ✓ {out_kv_path}")
            print(f"  ✓ {out_emb_path}")
        except Exception as e:
            print(f"Error exporting voice '{voice}': {e}", file=sys.stderr)
            sys.exit(1)

    print("\nExport completed successfully!")

if __name__ == "__main__":
    main()
