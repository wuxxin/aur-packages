import re
import sys
import os

path = sys.argv[1] if len(sys.argv) > 1 else 'llama_cpp/llama_cpp.py'

if not os.path.exists(path):
    print(f"Error: {path} not found")
    sys.exit(1)

with open(path, 'r') as f:
    content = f.read()

# Helper definitions for types that might be missing or wrongly defined
# (In this case, we rely on existing definitions in llama_cpp.py or add them if needed)

# llama_context_params
c_pat = r'class llama_context_params\(ctypes\.Structure\):.*?_fields_ = \[(.*?)\]'
c_rep = """class llama_context_params(ctypes.Structure):
    _fields_ = [
        ("n_ctx", ctypes.c_uint32), ("n_batch", ctypes.c_uint32), ("n_ubatch", ctypes.c_uint32),
        ("n_seq_max", ctypes.c_uint32), ("n_threads", ctypes.c_int32), ("n_threads_batch", ctypes.c_int32),
        ("rope_scaling_type", ctypes.c_int), ("pooling_type", ctypes.c_int), ("attention_type", ctypes.c_int),
        ("flash_attn_type", ctypes.c_int), ("rope_freq_base", ctypes.c_float), ("rope_freq_scale", ctypes.c_float),
        ("yarn_ext_factor", ctypes.c_float), ("yarn_attn_factor", ctypes.c_float), ("yarn_beta_fast", ctypes.c_float),
        ("yarn_beta_slow", ctypes.c_float), ("yarn_orig_ctx", ctypes.c_uint32), ("defrag_thold", ctypes.c_float),
        ("cb_eval", ggml_backend_sched_eval_callback), ("cb_eval_user_data", ctypes.c_void_p),
        ("type_k", ctypes.c_int), ("type_v", ctypes.c_int), ("abort_callback", ggml_abort_callback),
        ("abort_callback_data", ctypes.c_void_p), ("embeddings", ctypes.c_bool), ("offload_kqv", ctypes.c_bool),
        ("no_perf", ctypes.c_bool), ("op_offload", ctypes.c_bool), ("swa_full", ctypes.c_bool),
        ("kv_unified", ctypes.c_bool), ("samplers", ctypes.c_void_p), ("n_samplers", ctypes.c_size_t),
    ]"""
content = re.sub(c_pat, c_rep, content, flags=re.DOTALL)

# llama_model_params
m_pat = r'class llama_model_params\(ctypes\.Structure\):.*?_fields_ = \[(.*?)\]'
m_rep = """class llama_model_params(ctypes.Structure):
    _fields_ = [
        ("devices", ctypes.c_void_p), ("tensor_buft_overrides", ctypes.c_void_p), ("n_gpu_layers", ctypes.c_int32),
        ("split_mode", ctypes.c_int), ("main_gpu", ctypes.c_int32), ("tensor_split", ctypes.POINTER(ctypes.c_float)),
        ("progress_callback", llama_progress_callback), ("progress_callback_user_data", ctypes.c_void_p),
        ("kv_overrides", ctypes.POINTER(llama_model_kv_override)), ("vocab_only", ctypes.c_bool),
        ("use_mmap", ctypes.c_bool), ("use_direct_io", ctypes.c_bool), ("use_mlock", ctypes.c_bool),
        ("check_tensors", ctypes.c_bool), ("use_extra_bufts", ctypes.c_bool), ("no_host", ctypes.c_bool),
        ("no_alloc", ctypes.c_bool),
    ]"""
content = re.sub(m_pat, m_rep, content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)
print(f"Successfully patched ABI in {path}")
