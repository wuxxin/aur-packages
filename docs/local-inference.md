# Local Inference Management Guide

`local-inference.sh` manages a persistent `llama-server` instance optimized for AMD ROCm hardware (specifically tested on Radeon Pro W6800).

## Usage

| Command | Description |
|---|---|
| `install` | Sets up the service and generates a default configuration. |
| `uninstall` | Stops and removes the service. |
| `edit` | Edit model selection and server parameters. |
| `logs` | View the inference server output. |
| `exec` | Run `llama-server` in a transient unit with the same GPU access. |

## Implementation Considerations

### Hardware Optimization
The script is tuned for a 30 GiB VRAM footprint:
- **KV Cache**: Uses `q4_0` for both K and V caches to maximize context window.
- **Context Window**: Automatically calculates `n_ctx` based on available VRAM after model loading. Defaults to 262,144 tokens for Qwen 35B/27B models.
- **Throughput**: Uses `--parallel 2` for concurrent session handling and `-ub 1024` for optimized physical micro-batching.
- **Flash Attention**: Enabled via `-fa on`.

### ROCm / GPU Access
Because `llama-server` requires direct access to GPU device nodes:
- `PrivateDevices=no` is set in the systemd unit.
- Access to `/dev/dri` and `/dev/kfd` is required for the ROCm runtime.

### Data Access
- **Models**: Read-only access to `/data/public/machine-learning` is expected.
- **Sandboxing**: Uses `ProtectSystem=strict` but allows binding to `$HOME` for access to local files if needed during inference.

### Configuration
Model selection and specific flags (like `mmproj` for vision support) are managed in `~/.config/systemd/user/local-inference.env`.
- **MoE Support**: Optimized for `Qwen3.6-35B-A3B-APEX-I-Compact`.
- **Dense Support**: Supports `Qwen3.6-27B Q5_K_L`.
