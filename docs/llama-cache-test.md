# llama-cache-test

`llama-cache-test.py` is a robust Python utility designed to measure the Key-Value (KV) cache performance, time-to-first-token (TTFT), and context processing speeds of a running `llama.cpp` server (or any OpenAI-compatible `/v1/completions` API).

It evaluates both incremental prefill performance and cache hit rates in standard and multimodal (vision) contexts.

## Features

- **Incremental Prefill & Warmup:** Measures the processing latency across a growing context window to assess prompt evaluation scaling.
- **Cache Hit Latency Test:** Queries the model with a distractor followed by a target payload to verify if the server's KV cache effectively retained the context.
- **Vision Support:** Automatically tests multimodal cache retention by generating a dummy 1x1 base64 PNG image and attaching it to requests.
- **Fail-Fast Mechanism:** Aborts the test early if incremental evaluation speeds fall below a configured threshold.

## Usage

Ensure you have a `llama-server` or an OpenAI-compatible API running locally or remotely.

```bash
# Basic run with default settings
python3 scripts/llama-cache-test.py --url http://localhost:8080/v1 --model default

# Run with a specific text file payload and test vision caching
python3 scripts/llama-cache-test.py \
    --url http://127.0.0.1:8088/v1 \
    --model Qwen3.6-35B \
    --payload big-skill-context.md \
    --vision
```

## Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--url` | String | `http://localhost:8080/v1` | The base URL of the OpenAI-compatible API. |
| `--key` | String | `sk-none` | API key if authentication is required. |
| `--payload` | String | `""` | Path to a text file containing the context to load. If empty, the script will generate a synthetic "lorem ipsum" payload. |
| `--model` | String | `default` | The identifier of the model to use. |
| `--len` | Integer | `50000` | Target context length in characters. Ignored if `--payload` is provided. |
| `--step` | Integer | `3000` | Step size in characters during the incremental prefill warmup phase. |
| `--vision` | Flag | `False` | Includes a dummy base64 1x1 PNG image in the requests to evaluate multimodal cache behavior. |
| `--skip-linearity` | Flag | `False` | Skips incremental checks and executes a single full prefill of the entire context. |
| `--min-cps` | Float | `0.0` | Minimum Characters/second threshold during prefilling. If performance drops below this rate, the script aborts immediately. |
| `--hit-threshold` | Float | `1500.0` | Maximum Time-To-First-Token (TTFT) in milliseconds to classify a request as a Cache `**HIT**`. For massive models, you may need to increase this if inference latency itself exceeds 1.5s. |

## Understanding the Output

1. **Incremental Prefill:** Reports the delta time and character processing speed for each chunk added to the context. A healthy server should maintain or slightly decrease its `Char/s` as the context grows.
2. **Cache Hit Test:** Alternates between a random math distractor query and a target payload query. A `**HIT**` indicates the TTFT was beneath `--hit-threshold` (default 1500ms), proving the cache survived the distractor query. A `MISS` indicates a full or partial context recalculation was required.
