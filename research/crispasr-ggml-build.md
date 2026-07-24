# CrispASR GGML Custom Operations Research

This document outlines the custom extensions that the CrispASR developers have added to their own fork of `ggml` (referenced under the `ggml` submodule in CrispASR). These extensions are required to run Conformer speech-to-text models (like Canary, FireRedASR, LFM2) and Whisper variants utilizing SiGLU activations.

---

## 1. Public Headers: `ggml.h` (`include/ggml.h`)

### 1.1 `enum ggml_op` Additions
* **Location**: Line 500
* **Details**: A new enum value is registered to identify the fused normalize + affine operation.
```c
        GGML_OP_NORM, // normalize
        GGML_OP_NORM_AFFINE, // fused normalize + affine (w*norm(x)+b)
        GGML_OP_RMS_NORM,
```

### 1.2 `enum ggml_glu_op` Additions
* **Location**: Line 624
* **Details**: Adds `SIGLU` activation function to the Gated Linear Unit operations list.
```c
        GGML_GLU_OP_GEGLU_QUICK,
        GGML_GLU_OP_SIGLU,

        GGML_GLU_OP_COUNT,
```

### 1.3 Function Declarations
* **SiGLU wrappers** (Line 1321–1327):
```c
    GGML_API struct ggml_tensor * ggml_siglu(
            struct ggml_context * ctx,
            struct ggml_tensor  * a);

    GGML_API struct ggml_tensor * ggml_siglu_swapped(
            struct ggml_context * ctx,
            struct ggml_tensor  * a);
```
* **Fused LayerNorm Affine wrapper** (Line 1386–1391):
```c
    // fused: w * norm(a, eps) + b   (LayerNorm affine in one kernel)
    GGML_API struct ggml_tensor * ggml_norm_affine(
            struct ggml_context * ctx,
            struct ggml_tensor  * a,
            struct ggml_tensor  * w,
            struct ggml_tensor  * b,
            float                 eps);
```

---

## 2. Core Implementation: `ggml.c` (`src/ggml.c`)

### 2.1 String & Symbol Registers
* **Location**: Lines 1002, 1117, 1241
* **Details**: Maps the new enums to text names and symbols for compute graphs.
```c
static const char * GGML_OP_NAME[GGML_OP_COUNT] = {
    // ...
    "NORM",
    "NORM_AFFINE",
    "RMS_NORM",
};

static const char * GGML_OP_SYMBOL[GGML_OP_COUNT] = {
    // ...
    "norm(x)",
    "w*norm(x)+b",
    "rms_norm(x)",
};

static const char * GGML_GLU_OP_NAME[GGML_GLU_OP_COUNT] = {
    // ...
    "GEGLU_QUICK",
    "SIGLU",
};
```

### 2.2 Function Core Definitions
* **`ggml_norm_affine`** (Line 3149):
```c
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
```
* **SiGLU wrappers** (Line 3090):
```c
struct ggml_tensor * ggml_siglu(
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
```

---

## 3. CPU Backend (`src/ggml-cpu`)

### 3.1 Dispatching in `ggml-cpu.c`
* **Location**: Lines 1807, 2291
```c
        case GGML_OP_NORM_AFFINE:
            {
                ggml_compute_forward_norm_affine(params, tensor);
            } break;

        // ... inside case GGML_OP_GLU ...
                case GGML_GLU_OP_SIGLU:
                    {
                        ggml_compute_forward_siglu(params, dst);
                    } break;
```

### 3.2 Fused Norm Affine Kernel (`ops.cpp`)
* **Location**: Line 3860–3930
* **Details**: Computes normalization dynamically and scales/shifts using weight `w` and bias `b` buffers.
```cpp
static void ggml_compute_forward_norm_affine_f32(
        const ggml_compute_params * params,
        ggml_tensor * dst) {

    const ggml_tensor * src0 = dst->src[0]; // input
    const ggml_tensor * src1 = dst->src[1]; // weight
    const ggml_tensor * src2 = dst->src[2]; // bias
    // ... shapes and threads assertion ...
    
    for (int64_t i03 = 0; i03 < ne03; i03++) {
        for (int64_t i02 = 0; i02 < ne02; i02++) {
            for (int64_t i01 = ith; i01 < ne01; i01 += nth) {
                const float * x = (float *) ((char *) src0->data + i01*nb01 + i02*nb02 + i03*nb03);
                float       * y = (float *) ((char *) dst->data  + i01*nb1  + i02*nb2  + i03*nb3);

                float sum = 0.0f;
                ggml_vec_sum_f32(ne00, &sum, x);
                const float mean = sum / ne00;
                float variance = ggml_vec_cvar_f32(ne00, y, x, mean);
                const float scale = 1.0f / sqrtf(variance + eps);

                // Fused operation: y[i] = (x[i] - mean) * scale * w[i] + b[i]
                for (int64_t i00 = 0; i00 < ne00; i00++) {
                    y[i00] = y[i00] * scale * w[i00] + b[i00];
                }
            }
        }
    }
}
```

---

## 4. GPU/HIP Backend (`src/ggml-cuda`)

### 4.1 Dispatching in `ggml-cuda.cu`
* **Locations**: Lines 2843, 5199
* **Details**: Registers compatibility and dispatches execution kernels.
```cpp
        // inside ggml_cuda_compute_forward
        case GGML_OP_NORM_AFFINE:
            ggml_cuda_op_norm_affine(ctx, dst);
            break;

        // inside ggml_cuda_supports_op
        case GGML_OP_NORM:
        case GGML_OP_NORM_AFFINE:
        case GGML_OP_RMS_NORM:
            return true;
```

### 4.2 Fused Norm Affine Kernel (`norm.cu`)
* **Location**: Lines 289–335 (Kernel), Lines 729–756 (Launcher)
```cpp
template <int block_size>
static __global__ void norm_affine_f32(
        const float * x, const float * w, const float * b, float * dst,
        const int ncols, const int64_t stride_row, const int64_t stride_channel,
        const int64_t stride_sample, const float eps) {
    // ... thread offsets ...
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
```

### 4.3 SiGLU GPU Kernel Launcher (`unary.cu`)
* **Location**: Line 354
* **Details**: Because standard GGML already templates its Gated Linear Unit kernel using a function argument, the SiGLU kernel implementation simply dispatches the existing template with `op_sigmoid` as the activation parameter. No new GPU shaders/kernels are needed.
```cpp
void ggml_cuda_op_siglu(ggml_backend_cuda_context & ctx, ggml_tensor * dst) {
    ggml_cuda_op_unary_gated<op_sigmoid>(ctx, dst);
}
```
