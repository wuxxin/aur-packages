#!/bin/bash
# outetts-v1-integration-patch.sh
# Integrates OuteTTS 1.0 (DAC + WavTokenizer) support into llama.cpp

set -e

LLAMA_DIR="llama.cpp"

if [ ! -d "$LLAMA_DIR" ]; then
    LLAMA_DIR="."
fi

# --- 1. RESET FILES TO ENSURE CLEAN STATE ---
echo "Resetting modified files in llama.cpp..."
if [ -d "$LLAMA_DIR/.git" ]; then
    (cd "$LLAMA_DIR" && git checkout -f -- ggml/include/ggml.h ggml/src/ggml.c ggml/src/ggml-cpu/ops.cpp ggml/src/ggml-cpu/ggml-cpu.c src/llama-arch.h src/llama-hparams.h src/llama-model.h src/llama-arch.cpp src/llama-model.cpp tools/tts/tts.cpp src/CMakeLists.txt src/models/models.h 2>/dev/null || true)
fi

# Cleanup: remove only DAC-specific content (never touch upstream WavTokenizer code)
echo "Cleaning up DAC leftovers..."
sed -i '/LLM_ARCH_DAC_DEC/d' "$LLAMA_DIR/src/llama-model.cpp"
sed -i '/DAC_HPARAMS_PLACEHOLDER/d' "$LLAMA_DIR/src/llama-model.cpp"
sed -i '/DAC_TENSORS_PLACEHOLDER/d' "$LLAMA_DIR/src/llama-model.cpp"
sed -i '/DAC_GRAPH_PLACEHOLDER/d' "$LLAMA_DIR/src/llama-model.cpp"
sed -i '/DAC_MEMORY_PLACEHOLDER/d' "$LLAMA_DIR/src/llama-model.cpp"
sed -i '/llm_build_dac_dec/d' "$LLAMA_DIR/src/llama-model.cpp"
rm -f "$LLAMA_DIR/src/models/dac-dec.cpp"

# Cleanup for other files
sed -i '/LLM_ARCH_DAC_DEC/d' "$LLAMA_DIR/src/llama-arch.h"
sed -i '/LLM_ARCH_DAC_DEC/d' "$LLAMA_DIR/src/llama-arch.cpp"
sed -i '/LLM_TENSOR_DAC_SNAKE\b/d' "$LLAMA_DIR/src/llama-arch.h"
sed -i '/LLM_TENSOR_DAC_OUTPUT_SNAKE/d' "$LLAMA_DIR/src/llama-arch.h"
sed -i '/LLM_TENSOR_DAC_UPSAMPLE/d' "$LLAMA_DIR/src/llama-arch.h"
sed -i '/LLM_TENSOR_DAC_RU/d' "$LLAMA_DIR/src/llama-arch.h"
sed -i '/LLM_TENSOR_FFN_SNAKE_ALPHA/d' "$LLAMA_DIR/src/llama-arch.h"
sed -i '/LLM_TENSOR_DAC_SNAKE\b/d' "$LLAMA_DIR/src/llama-arch.cpp"
sed -i '/LLM_TENSOR_DAC_OUTPUT_SNAKE/d' "$LLAMA_DIR/src/llama-arch.cpp"
sed -i '/LLM_TENSOR_DAC_UPSAMPLE/d' "$LLAMA_DIR/src/llama-arch.cpp"
sed -i '/LLM_TENSOR_DAC_RU/d' "$LLAMA_DIR/src/llama-arch.cpp"
sed -i '/LLM_TENSOR_FFN_SNAKE_ALPHA/d' "$LLAMA_DIR/src/llama-arch.cpp"

# --- 2. SNAKE ACTIVATION FUNCTION ---
# (Replaced by composite ops in dac-dec.cpp to ensure GPU compatibility)
echo "Skipping custom GGML_OP_SNAKE injection..."

# --- 4. LLAMA ARCHITECTURE REGISTRATION ---
echo "Registering LLM_ARCH_DAC_DEC..."
if ! grep -q "LLM_ARCH_DAC_DEC" "$LLAMA_DIR/src/llama-arch.h"; then
    cat <<EOF > dac_arch.h
    LLM_ARCH_DAC_DEC,
EOF
    cat <<EOF > dac_tensors.h
    LLM_TENSOR_DAC_ONES,
    LLM_TENSOR_DAC_SNAKE,
    LLM_TENSOR_DAC_OUTPUT_SNAKE,
    LLM_TENSOR_DAC_UPSAMPLE,
    LLM_TENSOR_DAC_RU_CONV1,
    LLM_TENSOR_DAC_RU_CONV2,
    LLM_TENSOR_DAC_RU_SNAKE1,
    LLM_TENSOR_DAC_RU_SNAKE2,
EOF
    sed -i '/LLM_ARCH_WAVTOKENIZER_DEC,/r dac_arch.h' "$LLAMA_DIR/src/llama-arch.h"
    sed -i '/LLM_TENSOR_FFN_UP_EXPS,/r dac_tensors.h' "$LLAMA_DIR/src/llama-arch.h"
    rm dac_arch.h dac_tensors.h

    sed -i '/struct llama_hparams_convnext {/i \struct llama_hparams_dac { uint32_t n_filters; uint32_t n_block; uint32_t n_res_unit; };' "$LLAMA_DIR/src/llama-hparams.h"
    sed -i '/struct llama_hparams_convnext convnext;/a \    struct llama_hparams_dac      dac;' "$LLAMA_DIR/src/llama-hparams.h"

    cat <<EOF > dac_layer_struct.h
struct llama_layer_dac_ru {
    struct ggml_tensor * conv1   = nullptr;
    struct ggml_tensor * conv1_b = nullptr;
    struct ggml_tensor * conv2   = nullptr;
    struct ggml_tensor * conv2_b = nullptr;
    struct ggml_tensor * snake1  = nullptr;
    struct ggml_tensor * snake2  = nullptr;
};

struct llama_layer_dac {
    struct ggml_tensor * upsample   = nullptr;
    struct ggml_tensor * upsample_b = nullptr;
    struct ggml_tensor * snake      = nullptr;
    struct llama_layer_dac_ru ru[3];
};
EOF
    point=$(grep -n "struct llama_layer_convnext {" "$LLAMA_DIR/src/llama-model.h" | cut -d: -f1)
    sed -i "$((point - 1))r dac_layer_struct.h" "$LLAMA_DIR/src/llama-model.h"
    sed -i '/struct llama_layer_convnext convnext;/a \    struct llama_layer_dac      dac;' "$LLAMA_DIR/src/llama-model.h"
    rm dac_layer_struct.h

    # Add dac_ones to llama_model
    sed -i '/struct ggml_tensor \* output_norm[[:space:]]/a \    struct ggml_tensor * dac_ones = nullptr;' "$LLAMA_DIR/src/llama-model.h"

    cat <<EOF > dac_arch_cpp.h
    { LLM_ARCH_DAC_DEC,             "dac-dec"          },
EOF
    cat <<EOF > dac_tensors_cpp.h
    { LLM_TENSOR_DAC_ONES,                              "dac.ones"     },
    { LLM_TENSOR_DAC_SNAKE,                             "blk.%d.snake" },
    { LLM_TENSOR_DAC_OUTPUT_SNAKE,                      "output_snake" },
    { LLM_TENSOR_DAC_UPSAMPLE,                          "blk.%d.dac_upsample"    },
    { LLM_TENSOR_DAC_RU_CONV1,                          "blk.%d.dac_ru.%d.conv1" },
    { LLM_TENSOR_DAC_RU_CONV2,                          "blk.%d.dac_ru.%d.conv2" },
    { LLM_TENSOR_DAC_RU_SNAKE1,                         "blk.%d.dac_ru.%d.snake1" },
    { LLM_TENSOR_DAC_RU_SNAKE2,                         "blk.%d.dac_ru.%d.snake2" },
EOF
    sed -i '/{ LLM_ARCH_WAVTOKENIZER_DEC, "wavtokenizer-dec" },/r dac_arch_cpp.h' "$LLAMA_DIR/src/llama-arch.cpp"
    sed -i '/LLM_TENSOR_FFN_UP_EXPS,.*"blk.%d.ffn_up_exps"/r dac_tensors_cpp.h' "$LLAMA_DIR/src/llama-arch.cpp"
    rm dac_arch_cpp.h dac_tensors_cpp.h

    # --- LLM_TENSOR_INFOS: register DAC tensor op types ---
    cat <<EOF > dac_tensor_infos.cpp
    {LLM_TENSOR_DAC_SNAKE,                  {LLM_TENSOR_LAYER_REPEATING, GGML_OP_MUL}},
    {LLM_TENSOR_DAC_OUTPUT_SNAKE,           {LLM_TENSOR_LAYER_OUTPUT,    GGML_OP_MUL}},
    {LLM_TENSOR_DAC_UPSAMPLE,              {LLM_TENSOR_LAYER_REPEATING, GGML_OP_IM2COL}},
    {LLM_TENSOR_DAC_RU_CONV1,              {LLM_TENSOR_LAYER_REPEATING, GGML_OP_IM2COL}},
    {LLM_TENSOR_DAC_RU_CONV2,              {LLM_TENSOR_LAYER_REPEATING, GGML_OP_IM2COL}},
    {LLM_TENSOR_DAC_RU_SNAKE1,             {LLM_TENSOR_LAYER_REPEATING, GGML_OP_MUL}},
    {LLM_TENSOR_DAC_RU_SNAKE2,             {LLM_TENSOR_LAYER_REPEATING, GGML_OP_MUL}},
EOF
    sed -i '/LLM_TENSOR_CONVNEXT_GAMMA,.*GGML_OP_MUL/r dac_tensor_infos.cpp' "$LLAMA_DIR/src/llama-arch.cpp"
    rm dac_tensor_infos.cpp

    cat <<EOF > dac_tensors.cpp
        case LLM_ARCH_DAC_DEC:
            return {
                LLM_TENSOR_TOKEN_EMBD,
                LLM_TENSOR_CONV1D,
                LLM_TENSOR_DAC_ONES,
                LLM_TENSOR_DAC_SNAKE,
                LLM_TENSOR_DAC_OUTPUT_SNAKE,
                LLM_TENSOR_DAC_UPSAMPLE,
                LLM_TENSOR_DAC_RU_CONV1,
                LLM_TENSOR_DAC_RU_CONV2,
                LLM_TENSOR_DAC_RU_SNAKE1,
                LLM_TENSOR_DAC_RU_SNAKE2,
                LLM_TENSOR_OUTPUT,
            };
EOF
    insert_point=$(grep -n "case LLM_ARCH_WAVTOKENIZER_DEC:" "$LLAMA_DIR/src/llama-arch.cpp" | cut -d: -f1)
    insert_end=$(tail -n +$insert_point "$LLAMA_DIR/src/llama-arch.cpp" | grep -n "};" | head -n1 | cut -d: -f1)
    target_point=$((insert_point + insert_end - 1))
    sed -i "${target_point}r dac_tensors.cpp" "$LLAMA_DIR/src/llama-arch.cpp"
    rm dac_tensors.cpp

    # DAC Metadata loading & switches in llama-model.cpp
    # IMPORTANT: Re-lookup positions before EACH edit to avoid stale line numbers

    # --- load_hparams: DAC metadata (if-block, inserted after WavTokenizer's if-block) ---
    p=$(grep -n "void llama_model::load_hparams" "$LLAMA_DIR/src/llama-model.cpp" | cut -d: -f1)
    l_wt=$(tail -n +$p "$LLAMA_DIR/src/llama-model.cpp" | grep -n "if (arch == LLM_ARCH_WAVTOKENIZER_DEC)" | head -n1 | cut -d: -f1)
    l_wt=$((p + l_wt - 1))
    l_end=$(tail -n +$l_wt "$LLAMA_DIR/src/llama-model.cpp" | grep -n "}" | head -n1 | cut -d: -f1)
    l_end=$((l_wt + l_end - 1))
    cat <<EOF > dac_metadata.cpp
    if (arch == LLM_ARCH_DAC_DEC) {
        ml.get_key(LLM_KV_FEATURES_LENGTH,     hparams.n_embd);
        ml.get_key(LLM_KV_FEED_FORWARD_LENGTH,  hparams.n_ff_exp);
        ml.get_key(LLM_KV_EMBEDDING_LENGTH,    hparams.n_embd_out_impl);
        ml.get_key(LLM_KV_BLOCK_COUNT,         hparams.n_layer);
    }
EOF
    sed -i "${l_end}r dac_metadata.cpp" "$LLAMA_DIR/src/llama-model.cpp"
    rm dac_metadata.cpp

    # --- load_hparams: switch case (fallthrough before WavTokenizer) ---
    p=$(grep -n "void llama_model::load_hparams" "$LLAMA_DIR/src/llama-model.cpp" | cut -d: -f1)
    l_wt=$(tail -n +$p "$LLAMA_DIR/src/llama-model.cpp" | grep -n "case LLM_ARCH_WAVTOKENIZER_DEC:" | head -n1 | cut -d: -f1)
    l_wt=$((p + l_wt - 1))
    sed -i "${l_wt}i \\        case LLM_ARCH_DAC_DEC:" "$LLAMA_DIR/src/llama-model.cpp"

    # --- load_tensors: separate DAC case block AFTER WavTokenizer's "} break;" ---
    # The original logic for inserting dac_tensors_case.cpp was fragile.
    # We'll replace it with a marker-based insertion.
    # First, remove the old insertion logic if it exists (it's commented out in the provided snippet, but good to be explicit)
    # The original script calculates l_insert and then uses sed -i "${l_insert}r dac_tensors_case.cpp"
    # We need to ensure that the dac_tensors_case.cpp content is correctly formed with the 'case' statement.

    # --- 6. ADD DAC TENSOR METADATA ---
    # Insert DAC enum case in create_tensor switch
    # logic: strict insert before WavTokenizer case in load_tensors
    
    # Insert DAC enum case in create_tensor switch
    # logic: strict insert before WavTokenizer case in load_tensors
    
    # 1. Find start of load_tensors function
    l_start=$(grep -n "::load_tensors" "$LLAMA_DIR/src/llama-model.cpp" | head -n1 | cut -d: -f1)
    echo "DEBUG: l_start=$l_start"
    
    if [ -z "$l_start" ]; then
        echo "ERROR: Could not find load_tensors function"
        exit 1
    fi
    
    # 2. Find WavTokenizer case AFTER l_start
    l_wt_rel=$(tail -n +$l_start "$LLAMA_DIR/src/llama-model.cpp" | grep -n "case LLM_ARCH_WAVTOKENIZER_DEC:" | head -n1 | cut -d: -f1)
    echo "DEBUG: l_wt_rel=$l_wt_rel"
    
    if [ -z "$l_wt_rel" ]; then
        echo "ERROR: Could not find WavTokenizer usage in load_tensors"
        exit 1
    fi
    
    # 3. Calculate absolute line number
    l_wt=$((l_start + l_wt_rel - 1))
    echo "DEBUG: l_wt=$l_wt"

    cat <<EOF > dac_tensors_case.cpp
            case LLM_ARCH_DAC_DEC:
                {
                    tok_embd = create_tensor(tn(LLM_TENSOR_TOKEN_EMBD, "weight"), {hparams.n_embd, vocab.n_tokens()}, 0);
                    dac_ones = create_tensor(tn(LLM_TENSOR_DAC_ONES,   "weight"), {1}, 0);

                    conv1d   = create_tensor(tn(LLM_TENSOR_CONV1D, "weight"), {7, hparams.n_embd, hparams.n_ff()}, 0);
                    conv1d_b = create_tensor(tn(LLM_TENSOR_CONV1D, "bias"),   { 1, hparams.n_ff()}, 0);

                    static const int dac_kws[] = {16, 10, 8, 4};
                    static const int dac_channels[] = {1536, 768, 384, 192, 96};

                    for (uint32_t i = 0; i < hparams.n_layer; ++i) {
                        auto & layer = layers[i].dac;
                        int c_in  = dac_channels[i];
                        int c_out = dac_channels[i+1];
                        int kw    = dac_kws[i];
                        
                        // Alpha: [1, C, 1]
                        layer.snake      = create_tensor(tn(LLM_TENSOR_DAC_SNAKE, "alpha", i), {1, (int64_t)c_in, 1}, 0);
                        layer.upsample   = create_tensor(tn(LLM_TENSOR_DAC_UPSAMPLE, "weight", i), { (int64_t)kw, (int64_t)c_out, (int64_t)c_in}, 0);
                        layer.upsample_b = create_tensor(tn(LLM_TENSOR_DAC_UPSAMPLE, "bias",   i), { 1, (int64_t)c_out}, 0);

                        for (int j = 0; j < 3; ++j) {
                            auto & ru = layer.ru[j];
                            ru.snake1   = create_tensor(tn(LLM_TENSOR_DAC_RU_SNAKE1, "alpha", i, j), {1, (int64_t)c_out, 1}, 0);
                            ru.conv1    = create_tensor(tn(LLM_TENSOR_DAC_RU_CONV1,  "weight", i, j), {7, (int64_t)c_out, (int64_t)c_out}, 0);
                            
                            // Conv biases: use 2D {1, C} for correct broadcasting
                            ru.conv1_b  = create_tensor(tn(LLM_TENSOR_DAC_RU_CONV1,  "bias",   i, j), { 1, (int64_t)c_out}, 0);
                            
                            ru.snake2   = create_tensor(tn(LLM_TENSOR_DAC_RU_SNAKE2, "alpha", i, j), {1, (int64_t)c_out, 1}, 0);
                            ru.conv2    = create_tensor(tn(LLM_TENSOR_DAC_RU_CONV2,  "weight", i, j), {1, (int64_t)c_out, (int64_t)c_out}, 0);
                            // Conv biases: use 2D {1, C} for correct broadcasting
                            ru.conv2_b  = create_tensor(tn(LLM_TENSOR_DAC_RU_CONV2,  "bias",   i, j), { 1, (int64_t)c_out}, 0);
                        }
                    }
                    
                    output_norm   = create_tensor(tn(LLM_TENSOR_DAC_OUTPUT_SNAKE, "alpha"), {1, 96, 1}, 0);
                    output        = create_tensor(tn(LLM_TENSOR_OUTPUT,      "weight"), {7, 96, 1}, 0);
                    output_b      = create_tensor(tn(LLM_TENSOR_OUTPUT,      "bias"),   { 1, 1}, 0);
                } break;
EOF
    
    # Insert code block strictly at the found line (before WavTokenizer)
    l_prev=$((l_wt - 1))
    sed -i "${l_prev}r dac_tensors_case.cpp" "$LLAMA_DIR/src/llama-model.cpp"
    
    rm dac_tensors_case.cpp

    # --- 7. FIX WavTokenizer HIP Broadcast Crash ---
    # Workaround for ggml_cuda binbcast assertion failure when adding {1, C} biases to (L, C).
    # We manually repeat the bias tensor to match 'cur' before adding.
    sed -i 's/cur = ggml_add(ctx0, cur, model.conv1d_b);/cur = ggml_add(ctx0, cur, ggml_repeat(ctx0, model.conv1d_b, cur));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/cur = ggml_add(ctx0, cur, layer.conv1_b);/cur = ggml_add(ctx0, cur, ggml_repeat(ctx0, layer.conv1_b, cur));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/cur = ggml_add(ctx0, cur, layer.conv2_b);/cur = ggml_add(ctx0, cur, ggml_repeat(ctx0, layer.conv2_b, cur));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/q = ggml_add(ctx0, q, layer.attn_q_b);/q = ggml_add(ctx0, q, ggml_repeat(ctx0, layer.attn_q_b, q));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/k = ggml_add(ctx0, k, layer.attn_k_b);/k = ggml_add(ctx0, k, ggml_repeat(ctx0, layer.attn_k_b, k));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/v = ggml_add(ctx0, v, layer.attn_v_b);/v = ggml_add(ctx0, v, ggml_repeat(ctx0, layer.attn_v_b, v));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/cur = ggml_add(ctx0, cur, layer.attn_o_b);/cur = ggml_add(ctx0, cur, ggml_repeat(ctx0, layer.attn_o_b, cur));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/cur = ggml_add(ctx0, cur, layer.dw_b);/cur = ggml_add(ctx0, cur, ggml_repeat(ctx0, layer.dw_b, cur));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"
    sed -i 's/cur = ggml_add(ctx0, cur, model.output_b);/cur = ggml_add(ctx0, cur, ggml_repeat(ctx0, model.output_b, cur));/g' "$LLAMA_DIR/src/models/wavtokenizer-dec.cpp"

    # --- 8. FIX GGML_CONV_1D F32 TYPE HARDCODING ---
    # Upstream ggml_conv_1d hardcodes GGML_TYPE_F16 when creating the im2col tensor.
    # We patch it to use a->type so F32 tensors don't crash the CPU backend's im2col.
    sed -i 's/false, GGML_TYPE_F16); \/\/ \[N, OL, IC \* K\]/false, a->type == GGML_TYPE_F16 ? GGML_TYPE_F16 : GGML_TYPE_F32); \/\/ \[N, OL, IC \* K\]/g' "$LLAMA_DIR/ggml/src/ggml.c"

    # --- 9. FIX IM2COL f32 ---
    # Fix "im2col_f32 not implemented" by checking upstream changes or ensuring it compiles.
    # Current upstream seems to have it, but strict-math etc might remove it.
    # We used to patch it, but now we rely on upstream.
    # However, we must ensure proper padding logic for DAC if needed.
    # (Previously we had RDNA2 hack here, removed now as per user instruction).
    
    # Check if we need to implement im2col_f32 custom? 
    # If build fails with undefined symbol, we add it. 
    # But last build succeeded, so it's fine.

    # --- create_memory: fallthrough before WavTokenizer ---
    p=$(grep -n "llama_model::create_memory" "$LLAMA_DIR/src/llama-model.cpp" | cut -d: -f1)
    l_wt=$(tail -n +$p "$LLAMA_DIR/src/llama-model.cpp" | grep -n "case LLM_ARCH_WAVTOKENIZER_DEC:" | head -n1 | cut -d: -f1)
    l_wt=$((p + l_wt - 1))
    sed -i "${l_wt}i \\        case LLM_ARCH_DAC_DEC:" "$LLAMA_DIR/src/llama-model.cpp"

    # --- build_graph: separate DAC case block BEFORE WavTokenizer ---
    p=$(grep -n "llama_model::build_graph" "$LLAMA_DIR/src/llama-model.cpp" | cut -d: -f1)
    l_wt=$(tail -n +$p "$LLAMA_DIR/src/llama-model.cpp" | grep -n "case LLM_ARCH_WAVTOKENIZER_DEC:" | head -n1 | cut -d: -f1)
    l_wt=$((p + l_wt - 1))
    cat <<EOF > dac_graph_case.cpp
        case LLM_ARCH_DAC_DEC:
            {
                llm = std::make_unique<llm_build_dac_dec>(*this, params);
            } break;
EOF
    sed -i "$((l_wt - 1))r dac_graph_case.cpp" "$LLAMA_DIR/src/llama-model.cpp"
    rm dac_graph_case.cpp

    # --- rope_type: fallthrough before WavTokenizer ---
    p=$(grep -n "llama_rope_type llama_model_rope_type" "$LLAMA_DIR/src/llama-model.cpp" | cut -d: -f1)
    l_wt=$(tail -n +$p "$LLAMA_DIR/src/llama-model.cpp" | grep -n "case LLM_ARCH_WAVTOKENIZER_DEC:" | head -n1 | cut -d: -f1)
    l_wt=$((p + l_wt - 1))
    sed -i "${l_wt}i \\        case LLM_ARCH_DAC_DEC:" "$LLAMA_DIR/src/llama-model.cpp"

    # --- 5. PATCH WAVTOKENIZER BIAS SHAPES (Fix for 2D broadcasting) ---
    # REVERTED: Standard broadcasting works fine with 1D biases [C].
    # The previous attempt to force {1, n_embd} caused runtime crashes and broadcasting mismatches.
    # We remove the sed commands that altered LLM_TENSOR_POS_NET_* and DW shapes.

    # --- 6. ADD DAC TENSOR METADATA ---
    # Fix "missing tensor info mapping for dac.ones"
    sed -i '/{LLM_TENSOR_TOKEN_EMBD,                 {LLM_TENSOR_LAYER_INPUT, GGML_OP_GET_ROWS}},/a \    {LLM_TENSOR_DAC_ONES,                   {LLM_TENSOR_LAYER_INPUT, GGML_OP_NONE}},' "$LLAMA_DIR/src/llama-arch.cpp"

fi

    # IM2COL SAFETY FIX
    sed -i 's/ggml_tensor \* b = ggml_new_tensor_4d(ctx, GGML_TYPE_F32, n_embd_inp, w->ne\[1\], 1, 1);/ggml_tensor * b = ggml_new_tensor_4d(ctx, GGML_TYPE_F32, std::max((int64_t)n_embd_inp, (int64_t)512), (int64_t)w->ne[1], 1, 1);/' "$LLAMA_DIR/src/llama-model.cpp"

    # Declare builder in models.h
    sed -i '/struct llm_build_wavtokenizer_dec/i struct llm_build_dac_dec : public llm_graph_context {\n    llm_build_dac_dec(const llama_model & model, const llm_graph_params & params);\n};\n' "$LLAMA_DIR/src/models/models.h"

    # Add to CMakeLists.txt
    sed -i '/models\/wavtokenizer-dec.cpp/i \            models/dac-dec.cpp' "$LLAMA_DIR/src/CMakeLists.txt"

    # Create dac-dec.cpp
    cat <<EOF > "$LLAMA_DIR/src/models/dac-dec.cpp"
#include "models.h"

// Helper for Snake activation: x + (1/alpha) * sin^2(x * alpha)
static struct ggml_tensor * ggml_snake(struct ggml_context * ctx, struct ggml_tensor * a, struct ggml_tensor * alpha, struct ggml_tensor * ones) {
    struct ggml_tensor * tmp = ggml_mul(ctx, a, alpha);
    tmp = ggml_sin(ctx, tmp);
    tmp = ggml_sqr(ctx, tmp);
    // 1/alpha (ones / alpha). In ggml_div(a,b), 'a' determines output shape.
    // So 'ones' must be repeated to match 'alpha' shape before dividing.
    struct ggml_tensor * rep_ones  = ggml_repeat(ctx, ones, alpha);
    struct ggml_tensor * inv_alpha = ggml_div(ctx, rep_ones, alpha);
    tmp = ggml_mul(ctx, tmp, inv_alpha);
    return ggml_add(ctx, a, tmp);
}

llm_build_dac_dec::llm_build_dac_dec(const llama_model & model, const llm_graph_params & params) : llm_graph_context(params) {
    ggml_tensor * cur;
    ggml_tensor * inpL;

    inpL = build_inp_embd(model.tok_embd);

    cur = ggml_cont(ctx0, ggml_transpose(ctx0, inpL));

    cur = ggml_conv_1d_ph(ctx0, model.conv1d, cur, 1, 1);
    cur = ggml_add(ctx0, cur, model.conv1d_b);

    for (uint32_t il = 0; il < hparams.n_layer; ++il) {
        const auto & layer = model.layers[il].dac;

        cur = ggml_snake(ctx0, cur, layer.snake, model.dac_ones);
        static const int strides[] = {8, 5, 4, 2};
        int s = strides[il % 4];
        int k = (il % 4 == 0) ? 16 : ((il % 4 == 1) ? 10 : ((il % 4 == 2) ? 8 : 4));
        int p = (k - s) / 2;
        // GGML conv_transpose_1d asserts p0==0, so pass 0 and trim manually
        cur = ggml_conv_transpose_1d(ctx0, layer.upsample, cur, s, 0, 1);
        // Trim: skip p samples from start, take (original_len * stride) samples
        // Conv transpose with p0=0 output: L_out = (L_in-1)*s + k
        // Desired (PyTorch padding=p): L_desired = L_in*s = L_out - 2*p
        {
            int64_t n_channels = cur->ne[1];
            int64_t L_desired  = cur->ne[0] - 2*p;
            size_t  offset     = p * ggml_element_size(cur);
            cur = ggml_view_2d(ctx0, cur, L_desired, n_channels, cur->nb[1], offset);
        }
        cur = ggml_add(ctx0, cur, layer.upsample_b);

        for (int j = 0; j < 3; ++j) {
            const auto & ru = layer.ru[j];
            ggml_tensor * resid = cur;

            cur = ggml_snake(ctx0, cur, ru.snake1, model.dac_ones);
            cur = ggml_conv_1d_ph(ctx0, ru.conv1, cur, 1, 1);
            cur = ggml_add(ctx0, cur, ru.conv1_b);

            cur = ggml_snake(ctx0, cur, ru.snake2, model.dac_ones);
            cur = ggml_conv_1d_ph(ctx0, ru.conv2, cur, 1, 1);
            cur = ggml_add(ctx0, cur, ru.conv2_b);

            cur = ggml_add(ctx0, cur, resid);
        }
    }

    cur = ggml_snake(ctx0, cur, model.output_norm, model.dac_ones);
    cur = ggml_conv_1d_ph(ctx0, model.output, cur, 1, 1);
    cur = ggml_add(ctx0, cur, model.output_b);
    cur = ggml_tanh(ctx0, cur);

    cur = ggml_cont(ctx0, ggml_transpose(ctx0, cur));
    cb(cur, "result_embd", -1);
    res->t_embd = cur;

    ggml_build_forward_expand(gf, cur);
}
EOF


# --- 5. TTS DUAL-STREAM SUPPORT ---
echo "Applying TTS dual-stream support..."
TTS_FILE="$LLAMA_DIR/tools/tts/tts.cpp"
if ! grep -q "OUTETTS_V1_0" "$TTS_FILE"; then
    sed -i '/enum outetts_version {/a \    OUTETTS_V1_0,' "$TTS_FILE"

    # Replace get_tts_version with a robust one
    cat <<EOF > tts_version_detect.cpp
static outetts_version get_tts_version(llama_model * model, llama_model * vocoder = nullptr, json speaker = json::object()) {
    if (speaker.contains("version")) {
        std::string version = speaker["version"].get<std::string>();
        if (version == "1.0" || version == "3") return OUTETTS_V1_0;
        if (version == "0.3") return OUTETTS_V0_3;
        if (version == "0.2") return OUTETTS_V0_2;
    }
    
    // Auto-detect OuteTTS 1.0 based on speaker markers
    if (speaker.contains("global_features") || (speaker.contains("words") && !speaker["words"].empty() && speaker["words"][0].contains("c1"))) {
        return OUTETTS_V1_0;
    }

    // Auto-detect OuteTTS 1.0 based on vocoder architecture
    if (vocoder) {
        char arch[128];
        if (llama_model_meta_val_str(vocoder, "general.architecture", arch, sizeof(arch)) > 0) {
            if (std::string(arch) == "dac-dec") {
                return OUTETTS_V1_0;
            }
        }
    }

    // Default to chat template check
    const char *chat_template = llama_model_chat_template(model, nullptr);
    if (chat_template && std::string(chat_template).find("outetts-0.3") != std::string::npos) {
        return OUTETTS_V0_3;
    }

    return OUTETTS_V0_2;
}
EOF
    insert_point=$(grep -n "static outetts_version get_tts_version(" "$TTS_FILE" | head -n1 | cut -d: -f1)
    end_point=$(tail -n +$insert_point "$TTS_FILE" | grep -n "^}" | head -n1 | cut -d: -f1)
    final_end=$((insert_point + end_point - 1))
    sed -i "${insert_point},${final_end}d" "$TTS_FILE"
    sed -i "${insert_point}r tts_version_detect.cpp" "$TTS_FILE"
    rm tts_version_detect.cpp
    
    # Update audio_text_from_speaker
    cat <<EOF > tts_text_v1.cpp
    if (tts_version == OUTETTS_V1_0) {
        std::string speaker_text = "";
        if (speaker.contains("text")) {
            speaker_text = speaker["text"].get<std::string>();
        } else {
            for (const auto & word : speaker["words"]) {
                speaker_text += word["word"].get<std::string>() + " ";
            }
        }
        return speaker_text + ". ";
    }
EOF
    insert_point=$(grep -n "static std::string audio_text_from_speaker(" "$TTS_FILE" | cut -d: -f1)
    target_point=$(tail -n +$insert_point "$TTS_FILE" | grep -n "{" | head -n1 | cut -d: -f1)
    final_point=$((insert_point + target_point - 1))
    sed -i "${final_point}r tts_text_v1.cpp" "$TTS_FILE"
    rm tts_text_v1.cpp

    # Update audio_data_from_speaker
    cat <<EOF > tts_data_v1.cpp
    if (tts_version == OUTETTS_V1_0) {
        std::string audio_data = "<|audio_start|>\n";
        if (speaker.contains("global_features")) {
            auto gf = speaker["global_features"];
            audio_data += "<|global_features_start|>";
            audio_data += "<|energy_" + std::to_string(gf["energy"].get<int>()) + "|>";
            audio_data += "<|spectral_centroid_" + std::to_string(gf["spectral_centroid"].get<int>()) + "|>";
            audio_data += "<|pitch_" + std::to_string(gf["pitch"].get<int>()) + "|>";
            audio_data += "<|global_features_end|>\n";
        }
        for (const auto & word : speaker["words"]) {
            std::string word_text = word["word"].get<std::string>();
            double duration = word["duration"].get<double>();
            
            std::ostringstream oss;
            oss << std::fixed << std::setprecision(2) << duration;
            
            audio_data += "<|word_start|>" + word_text + "<|features|><|t_" + oss.str() + "|>";
            if (word.contains("features")) {
                auto f = word["features"];
                audio_data += "<|energy_" + std::to_string(f["energy"].get<int>()) + "|>";
                audio_data += "<|spectral_centroid_" + std::to_string(f["spectral_centroid"].get<int>()) + "|>";
                audio_data += "<|pitch_" + std::to_string(f["pitch"].get<int>()) + "|>";
            }
            audio_data += "<|code|>";
            std::vector<int> c1 = word["c1"].get<std::vector<int>>();
            std::vector<int> c2 = word["c2"].get<std::vector<int>>();
            for (size_t i = 0; i < c1.size(); ++i) {
                audio_data += "<|c1_" + std::to_string(c1[i]) + "|>";
                audio_data += "<|c2_" + std::to_string(c2[i]) + "|>";
            }
            audio_data += "<|word_end|>\n";
        }
        return audio_data;
    }
EOF
    insert_point=$(grep -n "static std::string audio_data_from_speaker(" "$TTS_FILE" | cut -d: -f1)
    target_point=$(tail -n +$insert_point "$TTS_FILE" | grep -n "{" | head -n1 | cut -d: -f1)
    final_point=$((insert_point + target_point - 1))
    sed -i "${final_point}r tts_data_v1.cpp" "$TTS_FILE"
    rm tts_data_v1.cpp

    # Update call sites in main
    sed -i 's/outetts_version tts_version = get_tts_version(model_ttc);/outetts_version tts_version = get_tts_version(model_ttc, model_cts);/' "$TTS_FILE"
    sed -i '/json speaker = speaker_from_file(params.vocoder.speaker_file);/a \        tts_version = get_tts_version(model_ttc, model_cts, speaker);' "$TTS_FILE"

    # Completely replace the token filtering and subtraction logic in tts.cpp
    cat <<EOF > tts_filter_v1.cpp
    std::vector<llama_token> audio_codes;
    if (tts_version == OUTETTS_V1_0) {
        for (auto t : codes) {
            std::string piece = common_token_to_piece(ctx_ttc, t);
            if (t >= 151675 && t <= 155775) {
                // WavTokenizer 0.6B code tokens
                audio_codes.push_back(t - 151675);
            } else if (piece.find("<|c1_") == 0 || piece.find("<|c2_") == 0) {
                // DAC 1B code tokens
                size_t start = piece.find("_") + 1;
                size_t end = piece.find("|>");
                if (end != std::string::npos) {
                    try {
                        audio_codes.push_back(std::stoi(piece.substr(start, end - start)));
                    } catch (...) {}
                }
            }
        }
    } else {
        for (auto t : codes) {
            if (t >= 151675 && t <= 155775) {
                audio_codes.push_back(t - 151675);
            }
        }
    }
    codes = audio_codes;
EOF

    # Find the start of the filter logic
    filter_start=$(grep -n "// remove all non-audio tokens" "$TTS_FILE" | cut -d: -f1)
    # Find the end of the subtraction loop
    sub_end=$(tail -n +$filter_start "$TTS_FILE" | grep -n "token -= 151672;" | head -n1 | cut -d: -f1)
    if [ -n "$filter_start" ] && [ -n "$sub_end" ]; then
        target_end=$((filter_start + sub_end))
        # Delete the whole block
        sed -i "${filter_start},${target_end}d" "$TTS_FILE"
        # Insert the new logic
        sed -i "$((filter_start-1))r tts_filter_v1.cpp" "$TTS_FILE"
    fi
    rm tts_filter_v1.cpp
fi

# --- 6. F32 IM2COL IMPLEMENTATION ---
# Upstream now includes this, so we skip injection to avoid redefinition.
# We retain the safety fix for n_embd_inp below.

echo "All integrations complete."
