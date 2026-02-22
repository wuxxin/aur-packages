
# --- SHIMS INJECTED BY PKGBUILD ---
# Re-implement or shim missing/deprecated symbols to avoid crashes with newest libllama.so
import sys
import ctypes

try:
    # 1. Bind llama_adapter_lora_init
    _llama_adapter_lora_init = _lib.llama_adapter_lora_init
    _llama_adapter_lora_init.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    _llama_adapter_lora_init.restype = ctypes.c_void_p

    def llama_adapter_lora_init(model, path_lora):
        if isinstance(path_lora, str):
            path_lora = path_lora.encode('utf-8')
        return _llama_adapter_lora_init(model, path_lora)

    # 2. Bind llama_adapter_lora_free
    _llama_adapter_lora_free = _lib.llama_adapter_lora_free
    _llama_adapter_lora_free.argtypes = [ctypes.c_void_p]
    _llama_adapter_lora_free.restype = None

    def llama_adapter_lora_free(adapter):
        return _llama_adapter_lora_free(adapter)

    # 3. Re-implement llama_set_adapter_lora using llama_set_adapters_lora
    _llama_set_adapters_lora = _lib.llama_set_adapters_lora
    _llama_set_adapters_lora.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_float)
    ]
    _llama_set_adapters_lora.restype = ctypes.c_int32

    def llama_set_adapter_lora(ctx, adapter, scale):
        adapters = (ctypes.c_void_p * 1)(adapter)
        scales = (ctypes.c_float * 1)(scale)
        return _llama_set_adapters_lora(ctx, adapters, 1, scales)

    # 4. Shim llama_sampler_init_softmax -> llama_sampler_init_dist
    try:
        _llama_sampler_init_dist = _lib.llama_sampler_init_dist
        _llama_sampler_init_dist.argtypes = [ctypes.c_uint32]
        _llama_sampler_init_dist.restype = ctypes.c_void_p

        def llama_sampler_init_softmax():
            # dist sampler with random seed (identity for softmax purposes in chain)
            return _llama_sampler_init_dist(1234)
    except AttributeError:
        # Fallback to a no-op greedy sampler if dist is also missing (unlikely)
        def llama_sampler_init_softmax():
            return _lib.llama_sampler_init_greedy()

    # 5. Dummy for missing symbols to avoid import-time breakage
    def llama_missing_symbol_dummy(*args, **kwargs):
        raise RuntimeError("This llama.cpp symbol is missing in system libllama.so. It was bridged to a dummy to allow import. If you see this, your llama-cpp-python version is too new for the installed libllama.so.")

    # Explicitly override the symbols that we aliased to llama_get_memory in the PKGBUILD
    _MISSING_SYMBOLS = [
        "llama_get_kv_self",
        "llama_rm_adapter_lora",
        "llama_clear_adapter_lora",
        "llama_apply_adapter_cvec",
        "llama_kv_self_can_shift",
        "llama_kv_self_clear",
        "llama_kv_self_defrag",
        "llama_kv_self_n_tokens",
        "llama_kv_self_seq_add",
        "llama_kv_self_seq_cp",
        "llama_kv_self_seq_div",
        "llama_kv_self_seq_keep",
        "llama_kv_self_seq_pos_max",
        "llama_kv_self_seq_pos_min",
        "llama_kv_self_seq_rm",
        "llama_kv_self_update",
        "llama_kv_self_used_cells",
    ]
    # Note: llama_set_adapter_lora and llama_sampler_init_softmax are already overridden with real shims above
    
    for _sym in _MISSING_SYMBOLS:
        if _sym in globals():
            globals()[_sym] = llama_missing_symbol_dummy

    print("PKGBUILD: Successfully Applied LLAMA Shims (LoRA, Samplers, Dummies)", file=sys.stderr)
except Exception as e:
    print(f"PKGBUILD: Failed to apply shims: {e}", file=sys.stderr)

# ---------------------------------
