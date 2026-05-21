# Local Speech-to-Text Management Guide

`local-speech-to-text.sh` manages a persistent `whisper-server` instance for speech-to-text (STT) transcription. It serves an OpenAI-compatible audio transcription endpoint, enabling local, private, and high-performance voice processing. Optimized for AMD ROCm hardware (specifically tested on Radeon Pro W6800).

- **Source Code**: [GitHub - ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp)

## Usage

| Command | Description |
|---|---|
| `install` | Sets up the service, generates default configuration env file. |
| `uninstall` | Stops and removes the service. |
| `edit` | Edit model selection and server parameters. |
| `logs` | View the transcription server output. |
| `exec` | Run `whisper-server` in a transient unit with the same GPU access. |
| `shell` | Spawn an interactive shell in the speech sandbox (useful for manual testing). |

## Architecture

The service runs `whisper-server` which loads a GGML Whisper model and exposes a REST API. By default, it runs with Flash Attention and audio transcoding enabled.

### Endpoints (all on port 50090)

| Endpoint | Purpose |
|---|---|
| `/v1/audio/transcriptions` | OpenAI-compatible audio transcription API (POST multipart/form-data) |
| `/health` | Server health check endpoint |

### Configuration Files

| File | Purpose |
|---|---|
| `~/.config/systemd/user/local-speech-to-text.env` | Model path, port, host, and thread configuration |
| `~/.config/systemd/user/local-speech-to-text.service` | Auto-generated systemd unit |

## VRAM Budget

Hardware: AMD Radeon Pro W6800 — **30,704 MiB** usable VRAM.

### Model Weights & Runtime Memory Footprint

| Component | File Size | GPU VRAM |
|---|---|---|
| [GGML Whisper Large v3 Turbo (Q5_0)](https://huggingface.co/ggerganov/whisper.cpp/blob/main/ggml-large-v3-turbo-q5_0.bin) | 573.45 MB | ~573.45 MiB |
| KV Caches | — | ~49.81 MiB |
| Compute Buffers | — | ~202.35 MiB |
| HIP Context Runtime Overhead | — | ~600.00 MiB |
| **Combined VRAM Footprint** | — | **~1,425.61 MiB (~1.4 GiB)** |

The service requires approximately **1.4 GiB** of VRAM when loaded. It runs entirely on the GPU, ensuring sub-second transcription response times for short speech snippets.

## Implementation Considerations

### ROCm / GPU Access
Because `whisper-server` requires direct access to GPU device nodes:
- `PrivateDevices=no` is set in the systemd unit.
- Access to `/dev/dri` and `/dev/kfd` is mandatory.
- The user must be in the `render` and `video` groups.

### Filesystem and Data Access
- **Models**: Read-write access to `/data/public/machine-learning` is configured (required to read the GGML model).
- **Sandboxing**: Uses `ProtectSystem=strict`.
- **Audio Conversion**: The server automatically transcodes input audio files (e.g. MP3, AAC, FLAC) to the required format (16kHz WAV) using `ffmpeg`. Therefore, the script configures `BindPaths=%h` to allow the server to write transient temporary transcoded files in the home directory sandbox.
- **Isolation**: The home directory `%h` is bind-mounted, and system paths are kept read-only.

### Configuration & Ports
- **Default Port**: `50090`
- **Configuration File**: Environment parameters are stored in `~/.config/systemd/user/local-speech-to-text.env`.
