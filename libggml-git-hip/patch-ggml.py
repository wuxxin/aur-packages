#!/usr/bin/env python3
import sys
import os

def patch_file(filepath, search, replace):
    print(f"Patching {filepath}...")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist!")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if replace in content:
        print(f"Already patched: {filepath}")
        return
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
            float                 eps);""")

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
               '    "GEGLU_QUICK",',
               '    "GEGLU_QUICK",\n    "SIGLU",')

    patch_file(ggml_c_path,
               'static_assert(GGML_OP_COUNT == 101, "GGML_OP_COUNT != 101");',
               'static_assert(GGML_OP_COUNT == 102, "GGML_OP_COUNT != 102");')

    patch_file(ggml_c_path,
               'static_assert(GGML_GLU_OP_COUNT == 6, "GGML_GLU_OP_COUNT != 6");',
               'static_assert(GGML_GLU_OP_COUNT == 7, "GGML_GLU_OP_COUNT != 7");')

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
               "void ggml_compute_forward_norm(const struct ggml_compute_params * params, struct ggml_tensor * dst);\nvoid ggml_compute_forward_norm_affine(const struct ggml_compute_params * params, struct ggml_tensor * dst);")

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

    print("All system ggml patches applied successfully!")

if __name__ == '__main__':
    main()
