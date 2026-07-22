#!/usr/bin/env python3
import sys
import os
import re

def patch_file(filepath, search, replace, is_regex=False):
    print(f"Patching {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist!")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if replace in content:
        print(f"Already patched: {filepath}")
        return
    if is_regex:
        if not re.search(search, content):
            print(f"Error: Regex pattern not found in {filepath}!")
            sys.exit(1)
        new_content = re.sub(search, replace, content)
    else:
        if search not in content:
            print(f"Error: Search anchor not found in {filepath}!")
            sys.exit(1)
        new_content = content.replace(search, replace)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully patched {filepath}")

def main():
    if len(sys.argv) < 2:
        print("Usage: patch-ggml.py <srcdir>")
        sys.exit(1)
        
    srcdir = sys.argv[1]
    ggml_h_path = os.path.join(srcdir, "llama.cpp/ggml/include/ggml.h")
    ggml_c_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml.c")
    ggml_cpu_c_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cpu/ggml-cpu.c")
    ops_h_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cpu/ops.h")
    ops_cpp_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cpu/ops.cpp")
    cuda_cu_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu")
    norm_cuh_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cuda/norm.cuh")
    norm_cu_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cuda/norm.cu")
    unary_cuh_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cuda/unary.cuh")
    unary_cu_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cuda/unary.cu")

    # 1. Patch ggml.h
    patch_file(ggml_h_path, 
               "        GGML_OP_NORM, // normalize",
               "        GGML_OP_NORM, // normalize\n        GGML_OP_NORM_AFFINE, // fused normalize + affine (w*norm(x)+b)")

    patch_file(ggml_h_path,
               "        GGML_OP_GLU,",
               "        GGML_OP_GLU,\n        GGML_OP_AA_SNAKE_BETA,")
               
    patch_file(ggml_h_path,
               "        GGML_GLU_OP_GEGLU_QUICK,",
               "        GGML_GLU_OP_GEGLU_QUICK,\n        GGML_GLU_OP_SIGLU,")

    patch_file(ggml_h_path,
               """    GGML_API struct ggml_tensor * ggml_norm_inplace(
            struct ggml_context * ctx,
            struct ggml_tensor  * a,
            float                 eps);""",
               """    GGML_API struct ggml_tensor * ggml_norm_inplace(
            struct ggml_context * ctx,
            struct ggml_tensor  * a,
            float                 eps);

    // fused: w * norm(a, eps) + b   (LayerNorm affine in one kernel)
    GGML_API struct ggml_tensor * ggml_norm_affine(
            struct ggml_context * ctx,
            struct ggml_tensor  * a,
            struct ggml_tensor  * w,
            struct ggml_tensor  * b,
            float                 eps);

    GGML_API struct ggml_tensor * ggml_aa_snake_beta(
            struct ggml_context * ctx,
            struct ggml_tensor  * x,
            struct ggml_tensor  * log_alpha,
            struct ggml_tensor  * log_beta,
            struct ggml_tensor  * us_filter,
            struct ggml_tensor  * ds_filter);""")

    patch_file(ggml_h_path,
               "    GGML_API struct ggml_tensor * ggml_swiglu_oai(",
               """    GGML_API struct ggml_tensor * ggml_siglu(
            struct ggml_context * ctx,
            struct ggml_tensor  * a);

    GGML_API struct ggml_tensor * ggml_siglu_swapped(
            struct ggml_context * ctx,
            struct ggml_tensor  * a);

    GGML_API struct ggml_tensor * ggml_siglu_split(
            struct ggml_context * ctx,
            struct ggml_tensor  * a,
            struct ggml_tensor  * b);

    GGML_API struct ggml_tensor * ggml_swiglu_oai(""")

    # 2. Patch ggml.c
    patch_file(ggml_c_path,
               '    "NORM",',
               '    "NORM",\n    "NORM_AFFINE",')

    patch_file(ggml_c_path,
               '    "norm(x)",',
               '    "norm(x)",\n    "w*norm(x)+b",')

    patch_file(ggml_c_path,
               '    "GLU",',
               '    "GLU",\n    "AA_SNAKE_BETA",')

    patch_file(ggml_c_path,
               '    "glu(x)",',
               '    "glu(x)",\n    "aa_snake_beta(x, log_a, log_b, usf, dsf)",')

    patch_file(ggml_c_path,
               '    "GEGLU_QUICK",',
               '    "GEGLU_QUICK",\n    "SIGLU",')

    # Fix static assertions in ggml.c dynamically supporting dirty trees
    patch_file(ggml_c_path,
               r'static_assert\(GGML_OP_COUNT\s*==\s*\d+,\s*"GGML_OP_COUNT\s*!=\s*\d+"\);',
               'static_assert(GGML_OP_COUNT == 103, "GGML_OP_COUNT != 103");',
               is_regex=True)

    patch_file(ggml_c_path,
               r'static_assert\(GGML_GLU_OP_COUNT\s*==\s*\d+,\s*"GGML_GLU_OP_COUNT\s*!=\s*\d+"\);',
               'static_assert(GGML_GLU_OP_COUNT == 7, "GGML_GLU_OP_COUNT != 7");',
               is_regex=True)

    patch_file(ggml_c_path,
               """struct ggml_tensor * ggml_norm_inplace(
        struct ggml_context * ctx,
        struct ggml_tensor  * a,
        float                 eps) {
    return ggml_norm_impl(ctx, a, eps, true);
}""",
               """struct ggml_tensor * ggml_norm_inplace(
        struct ggml_context * ctx,
        struct ggml_tensor  * a,
        float                 eps) {
    return ggml_norm_impl(ctx, a, eps, true);
}

// ggml_norm_affine

struct ggml_tensor * ggml_norm_affine(
        struct ggml_context * ctx,
        struct ggml_tensor  * a,
        struct ggml_tensor  * w,
        struct ggml_tensor  * b,
        float                 eps) {
    GGML_ASSERT(ggml_are_same_shape(a, w) || (w->ne[0] == a->ne[0] && ggml_nelements(w) == a->ne[0]));
    GGML_ASSERT(ggml_are_same_shape(a, b) || (b->ne[0] == a->ne[0] && ggml_nelements(b) == a->ne[0]));

    struct ggml_tensor * result = ggml_dup_tensor(ctx, a);

    ggml_set_op_params(result, &eps, sizeof(eps));

    result->op     = GGML_OP_NORM_AFFINE;
    result->src[0] = a;
    result->src[1] = w;
    result->src[2] = b;

    return result;
}

// ggml_aa_snake_beta

struct ggml_tensor * ggml_aa_snake_beta(
        struct ggml_context * ctx,
        struct ggml_tensor  * x,
        struct ggml_tensor  * log_alpha,
        struct ggml_tensor  * log_beta,
        struct ggml_tensor  * us_filter,
        struct ggml_tensor  * ds_filter) {
    GGML_ASSERT(ggml_is_matrix(x));                  // [T, C]
    GGML_ASSERT(log_alpha->ne[0] == x->ne[1]);       // C matches
    GGML_ASSERT(log_beta->ne[0]  == x->ne[1]);
    GGML_ASSERT(us_filter->ne[0] == 12);             // K fixed at 12 for now
    GGML_ASSERT(ds_filter->ne[0] == 12);
    GGML_ASSERT(x->type         == GGML_TYPE_F32);
    GGML_ASSERT(log_alpha->type == GGML_TYPE_F32);
    GGML_ASSERT(log_beta->type  == GGML_TYPE_F32);
    GGML_ASSERT(us_filter->type == GGML_TYPE_F32);
    GGML_ASSERT(ds_filter->type == GGML_TYPE_F32);

    struct ggml_tensor * result = ggml_dup_tensor(ctx, x);
    result->op     = GGML_OP_AA_SNAKE_BETA;
    result->src[0] = x;
    result->src[1] = log_alpha;
    result->src[2] = log_beta;
    result->src[3] = us_filter;
    result->src[4] = ds_filter;
    return result;
}""")

    patch_file(ggml_c_path,
               "struct ggml_tensor * ggml_swiglu_oai(",
               """struct ggml_tensor * ggml_siglu(
        struct ggml_context * ctx,
        struct ggml_tensor  * a) {
    return ggml_glu_impl(ctx, a, NULL, GGML_GLU_OP_SIGLU, false);
}

struct ggml_tensor * ggml_siglu_swapped(
        struct ggml_context * ctx,
        struct ggml_tensor  * a) {
    return ggml_glu_impl(ctx, a, NULL, GGML_GLU_OP_SIGLU, true);
}

struct ggml_tensor * ggml_siglu_split(
        struct ggml_context * ctx,
        struct ggml_tensor  * a,
        struct ggml_tensor  * b) {
    return ggml_glu_impl(ctx, a, b, GGML_GLU_OP_SIGLU, false);
}

struct ggml_tensor * ggml_swiglu_oai(""")

    # 3. Patch ggml-cpu.c
    patch_file(ggml_cpu_c_path,
               """        case GGML_OP_NORM:
            {
                ggml_compute_forward_norm(params, tensor);
            } break;""",
               """        case GGML_OP_NORM:
            {
                ggml_compute_forward_norm(params, tensor);
            } break;
        case GGML_OP_NORM_AFFINE:
            {
                ggml_compute_forward_norm_affine(params, tensor);
            } break;""")

    patch_file(ggml_cpu_c_path,
               """        case GGML_OP_COL2IM_1D:
            {
                ggml_compute_forward_col2im_1d(params, tensor);
            } break;""",
               """        case GGML_OP_COL2IM_1D:
            {
                ggml_compute_forward_col2im_1d(params, tensor);
            } break;
        case GGML_OP_AA_SNAKE_BETA:
            {
                ggml_compute_forward_aa_snake_beta(params, tensor);
            } break;""")

    patch_file(ggml_cpu_c_path,
               """        case GGML_OP_COL2IM_1D:
        case GGML_OP_CONV_TRANSPOSE_1D:
        case GGML_OP_CONV_TRANSPOSE_2D:""",
               """        case GGML_OP_COL2IM_1D:
        case GGML_OP_CONV_TRANSPOSE_1D:
        case GGML_OP_CONV_TRANSPOSE_2D:
        case GGML_OP_AA_SNAKE_BETA:""")

    patch_file(ggml_cpu_c_path,
               """                case GGML_GLU_OP_GEGLU_QUICK:
                    {
                        n_tasks = n_threads;
                    } break;""",
               """                case GGML_GLU_OP_GEGLU_QUICK:
                case GGML_GLU_OP_SIGLU:
                    {
                        n_tasks = n_threads;
                    } break;""")

    # 4. Patch ops.h
    patch_file(ops_h_path,
               "void ggml_compute_forward_norm(const struct ggml_compute_params * params, struct ggml_tensor * dst);",
               "void ggml_compute_forward_norm(const struct ggml_compute_params * params, struct ggml_tensor * dst);\nvoid ggml_compute_forward_norm_affine(const struct ggml_compute_params * params, struct ggml_tensor * dst);\nvoid ggml_compute_forward_aa_snake_beta(const struct ggml_compute_params * params, struct ggml_tensor * dst);")

    # 5. Patch ops.cpp
    patch_file(ops_cpp_path,
               """void ggml_compute_forward_norm(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];

    switch (src0->type) {
        case GGML_TYPE_F32:
            {
                ggml_compute_forward_norm_f32(params, dst);
            } break;
        default:
            {
                GGML_ABORT("fatal error");
            }
    }
}""",
               """void ggml_compute_forward_norm(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];

    switch (src0->type) {
        case GGML_TYPE_F32:
            {
                ggml_compute_forward_norm_f32(params, dst);
            } break;
        default:
            {
                GGML_ABORT("fatal error");
            }
    }
}

// ggml_compute_forward_norm_affine (CrispASR addition)

static void ggml_compute_forward_norm_affine_f32(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0]; // input
    const ggml_tensor * src1 = dst->src[1]; // weight (scale)
    const ggml_tensor * src2 = dst->src[2]; // bias

    GGML_ASSERT(ggml_are_same_shape(src0, dst));
    GGML_ASSERT(src0->nb[0] == sizeof(float));

    const int ith = params->ith;
    const int nth = params->nth;

    GGML_TENSOR_UNARY_OP_LOCALS

    float eps;
    memcpy(&eps, dst->op_params, sizeof(float));

    GGML_ASSERT(eps >= 0.0f);

    const float * w = (const float *) src1->data;
    const float * b = (const float *) src2->data;

    for (int64_t i03 = 0; i03 < ne03; i03++) {
        for (int64_t i02 = 0; i02 < ne02; i02++) {
            for (int64_t i01 = ith; i01 < ne01; i01 += nth) {
                const float * x = (float *) ((char *) src0->data + i01*nb01 + i02*nb02 + i03*nb03);
                float       * y = (float *) ((char *) dst->data  + i01*nb1  + i02*nb2  + i03*nb3);

                float sum = 0.0f;
                ggml_vec_sum_f32(ne00, &sum, x);
                const float mean = sum / ne00;

                float variance = 0.0f;
#ifdef GGML_USE_ACCELERATE
                float neg_mean = -mean;
                vDSP_vsadd(x, 1, &neg_mean, y, 1, ne00);
                vDSP_measqv(y, 1, &variance, ne00);
#else
                variance = ggml_vec_cvar_f32(ne00, y, x, mean);
#endif

                const float scale = 1.0f / sqrtf(variance + eps);

                // fused: y[i] = (x[i] - mean) * scale * w[i] + b[i]
                for (int64_t i00 = 0; i00 < ne00; i00++) {
                    y[i00] = y[i00] * scale * w[i00] + b[i00];
                }
            }
        }
    }
}

void ggml_compute_forward_norm_affine(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];

    switch (src0->type) {
        case GGML_TYPE_F32:
            {
                ggml_compute_forward_norm_affine_f32(params, dst);
            } break;
        default:
            {
                GGML_ABORT("fatal error");
            }
    }
}""")

    # Append ggml_compute_forward_aa_snake_beta to ops.cpp
    patch_file(ops_cpp_path,
               """void ggml_compute_forward_norm_affine(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];

    switch (src0->type) {
        case GGML_TYPE_F32:
            {
                ggml_compute_forward_norm_affine_f32(params, dst);
            } break;
        default:
            {
                GGML_ABORT("fatal error");
            }
    }
}""",
               """void ggml_compute_forward_norm_affine(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];

    switch (src0->type) {
        case GGML_TYPE_F32:
            {
                ggml_compute_forward_norm_affine_f32(params, dst);
            } break;
        default:
            {
                GGML_ABORT("fatal error");
            }
    }
}

// ggml_compute_forward_aa_snake_beta (CrispASR addition)

void ggml_compute_forward_aa_snake_beta(
        const ggml_compute_params * params,
              ggml_tensor * dst) {

    const ggml_tensor * src_x   = dst->src[0]; // x         [T, C]
    const ggml_tensor * src_la  = dst->src[1]; // log_alpha [C]
    const ggml_tensor * src_lb  = dst->src[2]; // log_beta  [C]
    const ggml_tensor * src_usf = dst->src[3]; // us_filter [K, 1, 1]
    const ggml_tensor * src_dsf = dst->src[4]; // ds_filter [K, 1, 1]

    GGML_ASSERT(src_x->type   == GGML_TYPE_F32);
    GGML_ASSERT(src_la->type  == GGML_TYPE_F32);
    GGML_ASSERT(src_lb->type  == GGML_TYPE_F32);
    GGML_ASSERT(src_usf->type == GGML_TYPE_F32);
    GGML_ASSERT(src_dsf->type == GGML_TYPE_F32);
    GGML_ASSERT(dst->type     == GGML_TYPE_F32);
    GGML_ASSERT(ggml_is_contiguous(src_x));
    GGML_ASSERT(ggml_is_contiguous(dst));
    GGML_ASSERT(ggml_are_same_shape(src_x, dst));

    const int T = (int) src_x->ne[0];
    const int C = (int) src_x->ne[1];
    const int K = (int) src_usf->ne[0];
    GGML_ASSERT(K == 12 && "aa_snake_beta currently requires K=12 taps");
    GGML_ASSERT((int) src_la->ne[0] == C);
    GGML_ASSERT((int) src_lb->ne[0] == C);
    GGML_ASSERT((int) src_dsf->ne[0] == K);

    const int up_pad        = K / 2 - 1;                  // 5
    const int up_pad_left   = up_pad * 2 + (K - 2) / 2;   // 15
    const int up_pad_right  = up_pad * 2 + (K - 2 + 1)/2; // 15
    const int ds_pad_left   = K / 2 - 1;                  // 5
    const int ds_pad_right  = K / 2;                      // 6

    const int T_padded   = T + 2 * up_pad;
    const int T_up       = (T_padded - 1) * 2 + K;
    const int T_cropped  = T_up - up_pad_left - up_pad_right;
    const int T_ds_pad   = T_cropped + ds_pad_left + ds_pad_right;
    const int T_out_ds   = (T_ds_pad - K) / 2 + 1;
    const int T_final    = T_out_ds < T ? T_out_ds : T;

    const float * x_in     = (const float *) src_x->data;
    float       * x_out    = (float *)       dst->data;
    const float * log_a    = (const float *) src_la->data;
    const float * log_b    = (const float *) src_lb->data;
    const float * us_f_raw = (const float *) src_usf->data;
    const float * ds_f     = (const float *) src_dsf->data;

    float us_f_x2[12];
    for (int k = 0; k < K; k++) {
        us_f_x2[k] = us_f_raw[k] * 2.0f;
    }

    thread_local std::vector<float> tl_padded;
    thread_local std::vector<float> tl_upsampled;
    thread_local std::vector<float> tl_ds_padded;
    thread_local std::vector<float> tl_snake;
    if ((int) tl_padded.size()    < T_padded)  tl_padded.resize(T_padded);
    if ((int) tl_upsampled.size() < T_up)      tl_upsampled.resize(T_up);
    if ((int) tl_ds_padded.size() < T_ds_pad)  tl_ds_padded.resize(T_ds_pad);
    if ((int) tl_snake.size()     < T_cropped) tl_snake.resize(T_cropped);

    float * padded     = tl_padded.data();
    float * upsampled  = tl_upsampled.data();
    float * ds_padded  = tl_ds_padded.data();

    const int ith = params->ith;
    const int nth = params->nth;
    const int c_start = (C * ith) / nth;
    const int c_end   = (C * (ith + 1)) / nth;

    for (int c = c_start; c < c_end; c++) {
        const float alpha_c  = expf(log_a[c]);
        const float beta_c   = expf(log_b[c]);
        const float inv_beta = 1.0f / beta_c;

        const float * x_in_c  = x_in  + (size_t) c * T;
        float       * x_out_c = x_out + (size_t) c * T;

        const float left_edge  = x_in_c[0];
        const float right_edge = x_in_c[T - 1];
        for (int t = 0; t < up_pad; t++) padded[t] = left_edge;
        memcpy(padded + up_pad, x_in_c, (size_t) T * sizeof(float));
        for (int t = 0; t < up_pad; t++) padded[up_pad + T + t] = right_edge;

        memset(upsampled, 0, (size_t) T_up * sizeof(float));
        for (int t = 0; t < T_padded; t++) {
            const float v = padded[t];
            float * dst_row = upsampled + t * 2;
            for (int k = 0; k < K; k++) {
                dst_row[k] += v * us_f_x2[k];
            }
        }

        float * cropped = upsampled + up_pad_left;
        for (int t = 0; t < T_cropped; t++) {
            const float v = cropped[t];
            const float s = sinf(alpha_c * v);
            cropped[t] = v + inv_beta * s * s;
        }

        const float c_left  = cropped[0];
        const float c_right = cropped[T_cropped - 1];
        for (int t = 0; t < ds_pad_left; t++) ds_padded[t] = c_left;
        memcpy(ds_padded + ds_pad_left, cropped, (size_t) T_cropped * sizeof(float));
        for (int t = 0; t < ds_pad_right; t++) ds_padded[ds_pad_left + T_cropped + t] = c_right;

        for (int t = 0; t < T_final; t++) {
            const float * row = ds_padded + t * 2;
            float sum = 0.0f;
            for (int k = 0; k < K; k++) sum += row[k] * ds_f[k];
            x_out_c[t] = sum;
        }
        for (int t = T_final; t < T; t++) x_out_c[t] = 0.0f;
    }
}""")

    # Inside ops.cpp, add case GGML_GLU_OP_SIGLU
    patch_file(ops_cpp_path,
               """        case GGML_GLU_OP_GEGLU_QUICK:
            {
                ggml_compute_forward_geglu_quick(params, dst);
            } break;""",
               """        case GGML_GLU_OP_GEGLU_QUICK:
            {
                ggml_compute_forward_geglu_quick(params, dst);
            } break;
        case GGML_GLU_OP_SIGLU:
            {
                ggml_compute_forward_siglu(params, dst);
            } break;""")

    patch_file(ops_cpp_path,
               """void ggml_compute_forward_glu(
        const ggml_compute_params * params,
        ggml_tensor * dst) {""",
               """// ggml_compute_forward_siglu (CrispASR addition)

static void ggml_compute_forward_siglu_f32(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];
    const ggml_tensor * src1 = dst->src[1];

    GGML_ASSERT(src0->nb[0] == sizeof(float));
    if (src1) {
        GGML_ASSERT(src1->nb[0] == sizeof(float));
    }
    GGML_ASSERT(dst->nb[0]  == sizeof(float));

    const int ith = params->ith;
    const int nth = params->nth;

    GGML_TENSOR_UNARY_OP_LOCALS

    const size_t nb11 = src1 ? src1->nb[1] : 0;
    const size_t nb12 = src1 ? src1->nb[2] : 0;
    const size_t nb13 = src1 ? src1->nb[3] : 0;

    const int64_t ne00_half = ne00/2;

    const bool swapped = ggml_get_op_params_i32(dst, 1);

    for (int64_t i03 = 0; i03 < ne03; i03++) {
        for (int64_t i02 = 0; i02 < ne02; i02++) {
            for (int64_t i01 = ith; i01 < ne01; i01 += nth) {
                const float * x0 = (float *) ((char *) src0->data + i01*nb01 + i02*nb02 + i03*nb03);
                const float * x1 = src1 ? (float *) ((char *) src1->data + i01*nb11 + i02*nb12 + i03*nb13) : x0 + ne00_half;
                float       * y  = (float *) ((char *) dst->data  + i01*nb1  + i02*nb2  + i03*nb3);

                const float * a = swapped ? x1 : x0;
                const float * b = swapped ? x0 : x1;

                for (int64_t i00 = 0; i00 < ne00_half; i00++) {
                    const float val_a = a[i00];
                    const float val_b = b[i00];
                    y[i00] = val_a * (1.0f / (1.0f + expf(-val_b)));
                }
            }
        }
    }
}

static void ggml_compute_forward_siglu_f16(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];
    const ggml_tensor * src1 = dst->src[1];

    GGML_ASSERT(src0->nb[0] == sizeof(ggml_fp16_t));
    if (src1) {
        GGML_ASSERT(src1->nb[0] == sizeof(ggml_fp16_t));
    }
    GGML_ASSERT(dst->nb[0]  == sizeof(ggml_fp16_t));

    const int ith = params->ith;
    const int nth = params->nth;

    GGML_TENSOR_UNARY_OP_LOCALS

    const size_t nb11 = src1 ? src1->nb[1] : 0;
    const size_t nb12 = src1 ? src1->nb[2] : 0;
    const size_t nb13 = src1 ? src1->nb[3] : 0;

    const int64_t ne00_half = ne00/2;

    const bool swapped = ggml_get_op_params_i32(dst, 1);

    for (int64_t i03 = 0; i03 < ne03; i03++) {
        for (int64_t i02 = 0; i02 < ne02; i02++) {
            for (int64_t i01 = ith; i01 < ne01; i01 += nth) {
                const ggml_fp16_t * x0 = (ggml_fp16_t *) ((char *) src0->data + i01*nb01 + i02*nb02 + i03*nb03);
                const ggml_fp16_t * x1 = src1 ? (ggml_fp16_t *) ((char *) src1->data + i01*nb11 + i02*nb12 + i03*nb13) : x0 + ne00_half;
                ggml_fp16_t       * y  = (ggml_fp16_t *) ((char *) dst->data  + i01*nb1  + i02*nb2  + i03*nb3);

                const ggml_fp16_t * a = swapped ? x1 : x0;
                const ggml_fp16_t * b = swapped ? x0 : x1;

                for (int64_t i00 = 0; i00 < ne00_half; i00++) {
                    const float val_a = ggml_fp16_to_fp32(a[i00]);
                    const float val_b = ggml_fp16_to_fp32(b[i00]);
                    y[i00] = ggml_fp32_to_fp16(val_a * (1.0f / (1.0f + expf(-val_b))));
                }
            }
        }
    }
}

static void ggml_compute_forward_siglu(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0];

    switch (src0->type) {
        case GGML_TYPE_F32:
            {
                ggml_compute_forward_siglu_f32(params, dst);
            } break;
        case GGML_TYPE_F16:
            {
                ggml_compute_forward_siglu_f16(params, dst);
            } break;
        default:
            {
                GGML_ABORT("fatal error");
            }
    }
}

void ggml_compute_forward_glu(
        const ggml_compute_params * params,
        ggml_tensor * dst) {""")

    # 6. Patch ggml-cuda/norm.cuh
    patch_file(norm_cuh_path,
               "void ggml_cuda_op_norm(ggml_backend_cuda_context & ctx, ggml_tensor * dst);",
               "void ggml_cuda_op_norm(ggml_backend_cuda_context & ctx, ggml_tensor * dst);\nvoid ggml_cuda_op_norm_affine(ggml_backend_cuda_context & ctx, ggml_tensor * dst);")

    # 7. Patch ggml-cuda/norm.cu
    with open(norm_cu_path, 'r', encoding='utf-8') as f:
        norm_cu_content = f.read()
    if "ggml_cuda_op_norm_affine" not in norm_cu_content:
        print(f"Appending norm_affine kernels to {norm_cu_path}...")
        custom_norm_kernels = """
// CrispASR patch — fused LayerNorm + affine (w * norm(x) + b)

template <int block_size>
static __global__ void norm_affine_f32(
        const float * x, const float * w, const float * b, float * dst,
        const int ncols, const int64_t stride_row, const int64_t stride_channel,
        const int64_t stride_sample, const float eps) {
    const int nrows     = gridDim.x;
    const int nchannels = gridDim.y;

    const int row       = blockIdx.x;
    const int channel   = blockIdx.y;
    const int sample    = blockIdx.z;
    const int tid       = threadIdx.x;

    x   += sample*stride_sample + channel*stride_channel + row*stride_row;
    dst += ((sample*nchannels + channel)*nrows + row)*ncols;

    float2 mean_var = make_float2(0.0f, 0.0f);

    for (int col = tid; col < ncols; col += block_size) {
        const float xi = x[col];
        mean_var.x += xi;
        mean_var.y += xi * xi;
    }

    extern __shared__ float2 s_sum2[];
    mean_var = block_reduce<block_reduce_method::SUM, block_size>(mean_var, s_sum2);

    const float mean = mean_var.x / ncols;
    const float var = mean_var.y / ncols - mean * mean;
    const float inv_std = rsqrtf(var + eps);

    for (int col = tid; col < ncols; col += block_size) {
        dst[col] = (x[col] - mean) * inv_std * w[col] + b[col];
    }
}

static void norm_affine_f32_cuda(
        const float * x, const float * w, const float * b, float * dst,
        const int ncols, const int nrows, const int nchannels, const int nsamples,
        const int64_t stride_row, const int64_t stride_channel, const int64_t stride_sample,
        const float eps, cudaStream_t stream) {
    const dim3 blocks_num(nrows, nchannels, nsamples);
    if (ncols < 1024) {
        const dim3 block_dims(WARP_SIZE, 1, 1);
        norm_affine_f32<WARP_SIZE><<<blocks_num, block_dims, 0, stream>>>(x, w, b, dst, ncols, stride_row, stride_channel, stride_sample, eps);
    } else {
        const dim3 block_dims(1024, 1, 1);
        norm_affine_f32<1024><<<blocks_num, block_dims, block_dims.x > WARP_SIZE ? 32 * sizeof(float2) : 0, stream>>>(x, w, b, dst, ncols, stride_row, stride_channel, stride_sample, eps);
    }
}

void ggml_cuda_op_norm_affine(ggml_backend_cuda_context & ctx, ggml_tensor * dst) {
    const ggml_tensor * src0 = dst->src[0];
    const ggml_tensor * src1 = dst->src[1]; // weight
    const ggml_tensor * src2 = dst->src[2]; // bias

    const float * src0_d = (const float *) src0->data;
    const float * src1_d = (const float *) src1->data;
    const float * src2_d = (const float *) src2->data;
    float * dst_d = (float *) dst->data;
    cudaStream_t stream = ctx.stream();

    GGML_ASSERT(src0->type == GGML_TYPE_F32);
    GGML_ASSERT( dst->type == GGML_TYPE_F32);

    GGML_TENSOR_UNARY_OP_LOCALS;

    float eps;
    memcpy(&eps, dst->op_params, sizeof(float));
    GGML_ASSERT(eps >= 0.0f);

    const size_t ts0 = ggml_type_size(src0->type);
    GGML_ASSERT(nb00 == ts0);
    const int64_t s01 = nb01 / ts0;
    const int64_t s02 = nb02 / ts0;
    const int64_t s03 = nb03 / ts0;

    norm_affine_f32_cuda(src0_d, src1_d, src2_d, dst_d, ne00, ne01, ne02, ne03, s01, s02, s03, eps, stream);
}
"""
        with open(norm_cu_path, 'a', encoding='utf-8') as f:
            f.write(custom_norm_kernels)
        print(f"Successfully appended norm_affine kernels to {norm_cu_path}")

    # 8. Patch ggml-cuda/unary.cuh
    patch_file(unary_cuh_path,
               "void ggml_cuda_op_swiglu(ggml_backend_cuda_context & ctx, ggml_tensor * dst);",
               "void ggml_cuda_op_swiglu(ggml_backend_cuda_context & ctx, ggml_tensor * dst);\nvoid ggml_cuda_op_siglu(ggml_backend_cuda_context & ctx, ggml_tensor * dst);")

    # 9. Patch ggml-cuda/unary.cu
    with open(unary_cu_path, 'r', encoding='utf-8') as f:
        unary_cu_content = f.read()
    if "ggml_cuda_op_siglu" not in unary_cu_content:
        print(f"Appending siglu kernel launcher to {unary_cu_path}...")
        custom_siglu_launcher = """
// CrispASR patch — SiGLU CUDA launcher
void ggml_cuda_op_siglu(ggml_backend_cuda_context & ctx, ggml_tensor * dst) {
    ggml_cuda_op_unary_gated<op_sigmoid>(ctx, dst);
}
"""
        with open(unary_cu_path, 'a', encoding='utf-8') as f:
            f.write(custom_siglu_launcher)
        print(f"Successfully appended siglu launcher to {unary_cu_path}")

    # 10. Patch ggml-cuda/ggml-cuda.cu
    patch_file(cuda_cu_path,
               "static constexpr std::array<ggml_glu_op, 3> valid_glu_ops = { GGML_GLU_OP_SWIGLU, GGML_GLU_OP_GEGLU, GGML_GLU_OP_SWIGLU_OAI };",
               "static constexpr std::array<ggml_glu_op, 4> valid_glu_ops = { GGML_GLU_OP_SWIGLU, GGML_GLU_OP_GEGLU, GGML_GLU_OP_SWIGLU_OAI, GGML_GLU_OP_SIGLU };")

    patch_file(cuda_cu_path,
               """                case GGML_GLU_OP_GEGLU_QUICK:
                    ggml_cuda_op_geglu_quick(ctx, dst);
                    break;""",
               """                case GGML_GLU_OP_GEGLU_QUICK:
                    ggml_cuda_op_geglu_quick(ctx, dst);
                    break;
                case GGML_GLU_OP_SIGLU:
                    ggml_cuda_op_siglu(ctx, dst);
                    break;""")

    patch_file(cuda_cu_path,
               """        case GGML_OP_NORM:
            ggml_cuda_op_norm(ctx, dst);
            break;""",
               """        case GGML_OP_NORM:
            ggml_cuda_op_norm(ctx, dst);
            break;
        case GGML_OP_NORM_AFFINE:
            ggml_cuda_op_norm_affine(ctx, dst);
            break;""")

    patch_file(cuda_cu_path,
               """                case GGML_GLU_OP_GEGLU_QUICK:
                    return ggml_is_contiguous_1(op->src[0]);""",
               """                case GGML_GLU_OP_GEGLU_QUICK:
                case GGML_GLU_OP_SIGLU:
                    return ggml_is_contiguous_1(op->src[0]);""")

    patch_file(cuda_cu_path,
               """        case GGML_OP_NORM:
        case GGML_OP_RMS_NORM:
        case GGML_OP_L2_NORM:
            return ggml_is_contiguous_rows(op->src[0]);""",
               """        case GGML_OP_NORM:
        case GGML_OP_NORM_AFFINE:
        case GGML_OP_RMS_NORM:
        case GGML_OP_L2_NORM:
            return ggml_is_contiguous_rows(op->src[0]);""")

    # 11. Patch ggml-cpu/ggml-cpu.cpp for additional proc address exports
    ggml_cpu_cpp_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-cpu/ggml-cpu.cpp")
    patch_file(ggml_cpu_cpp_path,
               """    if (strcmp(name, "ggml_backend_cpu_set_threadpool") == 0) {
        return (void *)ggml_backend_cpu_set_threadpool;
    }""",
               """    if (strcmp(name, "ggml_backend_cpu_set_threadpool") == 0) {
        return (void *)ggml_backend_cpu_set_threadpool;
    }
    if (strcmp(name, "ggml_graph_plan") == 0) {
        return (void *)ggml_graph_plan;
    }
    if (strcmp(name, "ggml_graph_compute") == 0) {
        return (void *)ggml_graph_compute;
    }
    if (strcmp(name, "ggml_graph_compute_with_ctx") == 0) {
        return (void *)ggml_graph_compute_with_ctx;
    }
    if (strcmp(name, "ggml_get_type_traits_cpu") == 0) {
        return (void *)ggml_get_type_traits_cpu;
    }
    if (strcmp(name, "ggml_cpu_has_sse3") == 0) return (void *)ggml_cpu_has_sse3;
    if (strcmp(name, "ggml_cpu_has_ssse3") == 0) return (void *)ggml_cpu_has_ssse3;
    if (strcmp(name, "ggml_cpu_has_avx") == 0) return (void *)ggml_cpu_has_avx;
    if (strcmp(name, "ggml_cpu_has_avx_vnni") == 0) return (void *)ggml_cpu_has_avx_vnni;
    if (strcmp(name, "ggml_cpu_has_avx2") == 0) return (void *)ggml_cpu_has_avx2;
    if (strcmp(name, "ggml_cpu_has_bmi2") == 0) return (void *)ggml_cpu_has_bmi2;
    if (strcmp(name, "ggml_cpu_has_f16c") == 0) return (void *)ggml_cpu_has_f16c;
    if (strcmp(name, "ggml_cpu_has_fma") == 0) return (void *)ggml_cpu_has_fma;
    if (strcmp(name, "ggml_cpu_has_avx512") == 0) return (void *)ggml_cpu_has_avx512;
    if (strcmp(name, "ggml_cpu_has_avx512_vbmi") == 0) return (void *)ggml_cpu_has_avx512_vbmi;
    if (strcmp(name, "ggml_cpu_has_avx512_vnni") == 0) return (void *)ggml_cpu_has_avx512_vnni;
    if (strcmp(name, "ggml_cpu_has_avx512_bf16") == 0) return (void *)ggml_cpu_has_avx512_bf16;
    if (strcmp(name, "ggml_cpu_has_amx_int8") == 0) return (void *)ggml_cpu_has_amx_int8;
    if (strcmp(name, "ggml_cpu_has_neon") == 0) return (void *)ggml_cpu_has_neon;
    if (strcmp(name, "ggml_cpu_has_arm_fma") == 0) return (void *)ggml_cpu_has_arm_fma;
    if (strcmp(name, "ggml_cpu_has_fp16_va") == 0) return (void *)ggml_cpu_has_fp16_va;
    if (strcmp(name, "ggml_cpu_has_dotprod") == 0) return (void *)ggml_cpu_has_dotprod;
    if (strcmp(name, "ggml_cpu_has_matmul_int8") == 0) return (void *)ggml_cpu_has_matmul_int8;
    if (strcmp(name, "ggml_cpu_has_sve") == 0) return (void *)ggml_cpu_has_sve;
    if (strcmp(name, "ggml_cpu_get_sve_cnt") == 0) return (void *)ggml_cpu_get_sve_cnt;
    if (strcmp(name, "ggml_cpu_has_sme") == 0) return (void *)ggml_cpu_has_sme;
    if (strcmp(name, "ggml_cpu_has_sme2") == 0) return (void *)ggml_cpu_has_sme2;
    if (strcmp(name, "ggml_cpu_has_riscv_v") == 0) return (void *)ggml_cpu_has_riscv_v;
    if (strcmp(name, "ggml_cpu_get_rvv_vlen") == 0) return (void *)ggml_cpu_get_rvv_vlen;
    if (strcmp(name, "ggml_cpu_has_vsx") == 0) return (void *)ggml_cpu_has_vsx;
    if (strcmp(name, "ggml_cpu_has_vxe") == 0) return (void *)ggml_cpu_has_vxe;
    if (strcmp(name, "ggml_cpu_has_wasm_simd") == 0) return (void *)ggml_cpu_has_wasm_simd;
    if (strcmp(name, "ggml_cpu_has_llamafile") == 0) return (void *)ggml_cpu_has_llamafile;""")

    # 12. Patch ggml-backend-reg.cpp for dynamic CPU backend symbols fallback
    backend_reg_cpp_path = os.path.join(srcdir, "llama.cpp/ggml/src/ggml-backend-reg.cpp")
    with open(backend_reg_cpp_path, 'r', encoding='utf-8') as f:
        backend_reg_content = f.read()
    if "get_cpu_proc_address" not in backend_reg_content:
        print(f"Appending CPU backend compatibility wrappers to {backend_reg_cpp_path}...")
        cpu_wrappers = """
#include "ggml-cpu.h"

#ifdef GGML_BACKEND_DL
extern "C" {

static void * get_cpu_proc_address(const char * name) {
    ggml_backend_dev_t dev = ggml_backend_dev_by_type(GGML_BACKEND_DEVICE_TYPE_CPU);
    if (!dev) {
        ggml_backend_load_all();
        dev = ggml_backend_dev_by_type(GGML_BACKEND_DEVICE_TYPE_CPU);
    }
    if (!dev) {
        return nullptr;
    }
    ggml_backend_reg_t reg = ggml_backend_dev_backend_reg(dev);
    if (!reg) {
        return nullptr;
    }
    return ggml_backend_reg_get_proc_address(reg, name);
}

GGML_BACKEND_API ggml_backend_t ggml_backend_cpu_init(void) {
    ggml_backend_dev_t dev = ggml_backend_dev_by_type(GGML_BACKEND_DEVICE_TYPE_CPU);
    if (!dev) {
        ggml_backend_load_all();
        dev = ggml_backend_dev_by_type(GGML_BACKEND_DEVICE_TYPE_CPU);
    }
    if (!dev) {
        return nullptr;
    }
    return ggml_backend_dev_init(dev, nullptr);
}

GGML_BACKEND_API bool ggml_backend_is_cpu(ggml_backend_t backend) {
    if (!backend) {
        return false;
    }
    ggml_backend_dev_t dev = ggml_backend_get_device(backend);
    if (!dev) {
        return false;
    }
    return ggml_backend_dev_type(dev) == GGML_BACKEND_DEVICE_TYPE_CPU;
}

GGML_BACKEND_API void ggml_backend_cpu_set_n_threads(ggml_backend_t backend_cpu, int n_threads) {
    if (!backend_cpu || !ggml_backend_is_cpu(backend_cpu)) {
        return;
    }
    ggml_backend_dev_t dev = ggml_backend_get_device(backend_cpu);
    ggml_backend_reg_t reg = ggml_backend_dev_backend_reg(dev);
    if (!reg) {
        return;
    }
    auto fct = (ggml_backend_set_n_threads_t) ggml_backend_reg_get_proc_address(reg, "ggml_backend_set_n_threads");
    if (fct) {
        fct(backend_cpu, n_threads);
    }
}

typedef void (*ggml_backend_cpu_set_threadpool_t)(ggml_backend_t backend_cpu, ggml_threadpool_t threadpool);
typedef void (*ggml_backend_cpu_set_abort_callback_t)(ggml_backend_t backend_cpu, ggml_abort_callback abort_callback, void * abort_callback_data);
typedef void (*ggml_backend_cpu_set_use_ref_t)(ggml_backend_t backend_cpu, bool use_ref);

GGML_BACKEND_API void ggml_backend_cpu_set_threadpool(ggml_backend_t backend_cpu, ggml_threadpool_t threadpool) {
    if (!backend_cpu || !ggml_backend_is_cpu(backend_cpu)) {
        return;
    }
    ggml_backend_dev_t dev = ggml_backend_get_device(backend_cpu);
    ggml_backend_reg_t reg = ggml_backend_dev_backend_reg(dev);
    if (!reg) {
        return;
    }
    auto fct = (ggml_backend_cpu_set_threadpool_t) ggml_backend_reg_get_proc_address(reg, "ggml_backend_cpu_set_threadpool");
    if (fct) {
        fct(backend_cpu, threadpool);
    }
}

GGML_BACKEND_API void ggml_backend_cpu_set_abort_callback(ggml_backend_t backend_cpu, ggml_abort_callback abort_callback, void * abort_callback_data) {
    if (!backend_cpu || !ggml_backend_is_cpu(backend_cpu)) {
        return;
    }
    ggml_backend_dev_t dev = ggml_backend_get_device(backend_cpu);
    ggml_backend_reg_t reg = ggml_backend_dev_backend_reg(dev);
    if (!reg) {
        return;
    }
    auto fct = (ggml_backend_cpu_set_abort_callback_t) ggml_backend_reg_get_proc_address(reg, "ggml_backend_set_abort_callback");
    if (fct) {
        fct(backend_cpu, abort_callback, abort_callback_data);
    }
}

GGML_BACKEND_API void ggml_backend_cpu_set_use_ref(ggml_backend_t backend_cpu, bool use_ref) {
    if (!backend_cpu || !ggml_backend_is_cpu(backend_cpu)) {
        return;
    }
    ggml_backend_dev_t dev = ggml_backend_get_device(backend_cpu);
    ggml_backend_reg_t reg = ggml_backend_dev_backend_reg(dev);
    if (!reg) {
        return;
    }
    auto fct = (ggml_backend_cpu_set_use_ref_t) ggml_backend_reg_get_proc_address(reg, "ggml_backend_cpu_set_use_ref");
    if (fct) {
        fct(backend_cpu, use_ref);
    }
}

GGML_BACKEND_API ggml_backend_reg_t ggml_backend_cpu_reg(void) {
    ggml_backend_dev_t dev = ggml_backend_dev_by_type(GGML_BACKEND_DEVICE_TYPE_CPU);
    if (!dev) {
        ggml_backend_load_all();
        dev = ggml_backend_dev_by_type(GGML_BACKEND_DEVICE_TYPE_CPU);
    }
    if (!dev) {
        return nullptr;
    }
    return ggml_backend_dev_backend_reg(dev);
}

GGML_BACKEND_API struct ggml_threadpool * ggml_threadpool_new(struct ggml_threadpool_params * params) {
    typedef struct ggml_threadpool * (*fn_t)(struct ggml_threadpool_params *);
    auto fn = (fn_t) get_cpu_proc_address("ggml_threadpool_new");
    return fn ? fn(params) : nullptr;
}

GGML_BACKEND_API void ggml_threadpool_free(struct ggml_threadpool * threadpool) {
    typedef void (*fn_t)(struct ggml_threadpool *);
    auto fn = (fn_t) get_cpu_proc_address("ggml_threadpool_free");
    if (fn) fn(threadpool);
}

GGML_BACKEND_API struct ggml_cplan ggml_graph_plan(const struct ggml_cgraph * cgraph, int n_threads, struct ggml_threadpool * threadpool) {
    typedef struct ggml_cplan (*fn_t)(const struct ggml_cgraph *, int, struct ggml_threadpool *);
    auto fn = (fn_t) get_cpu_proc_address("ggml_graph_plan");
    if (fn) return fn(cgraph, n_threads, threadpool);
    struct ggml_cplan empty = {};
    return empty;
}

GGML_BACKEND_API enum ggml_status ggml_graph_compute(struct ggml_cgraph * cgraph, struct ggml_cplan * cplan) {
    typedef enum ggml_status (*fn_t)(struct ggml_cgraph *, struct ggml_cplan *);
    auto fn = (fn_t) get_cpu_proc_address("ggml_graph_compute");
    return fn ? fn(cgraph, cplan) : GGML_STATUS_FAILED;
}

GGML_BACKEND_API enum ggml_status ggml_graph_compute_with_ctx(struct ggml_context * ctx, struct ggml_cgraph * cgraph, int n_threads) {
    typedef enum ggml_status (*fn_t)(struct ggml_context *, struct ggml_cgraph *, int);
    auto fn = (fn_t) get_cpu_proc_address("ggml_graph_compute_with_ctx");
    return fn ? fn(ctx, cgraph, n_threads) : GGML_STATUS_FAILED;
}

GGML_BACKEND_API const struct ggml_type_traits_cpu * ggml_get_type_traits_cpu(enum ggml_type type) {
    typedef const struct ggml_type_traits_cpu * (*fn_t)(enum ggml_type);
    auto fn = (fn_t) get_cpu_proc_address("ggml_get_type_traits_cpu");
    return fn ? fn(type) : nullptr;
}

#define DEFINE_GGML_CPU_HAS(fn_name) \
GGML_BACKEND_API int fn_name(void) { \
    typedef int (*fn_t)(void); \
    auto fn = (fn_t) get_cpu_proc_address(#fn_name); \
    return fn ? fn() : 0; \
}

DEFINE_GGML_CPU_HAS(ggml_cpu_has_sse3)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_ssse3)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_avx)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_avx_vnni)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_avx2)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_bmi2)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_f16c)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_fma)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_avx512)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_avx512_vbmi)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_avx512_vnni)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_avx512_bf16)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_amx_int8)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_neon)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_arm_fma)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_fp16_va)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_dotprod)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_matmul_int8)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_sve)
DEFINE_GGML_CPU_HAS(ggml_cpu_get_sve_cnt)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_sme)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_sme2)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_riscv_v)
DEFINE_GGML_CPU_HAS(ggml_cpu_get_rvv_vlen)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_vsx)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_vxe)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_wasm_simd)
DEFINE_GGML_CPU_HAS(ggml_cpu_has_llamafile)
#undef DEFINE_GGML_CPU_HAS

} // extern "C"
#endif
"""
        with open(backend_reg_cpp_path, 'a', encoding='utf-8') as f:
            f.write(cpu_wrappers)
        print(f"Successfully appended CPU backend compatibility wrappers to {backend_reg_cpp_path}")

    print("All system ggml patches applied successfully!")

if __name__ == '__main__':
    main()



