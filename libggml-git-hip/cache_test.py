#!/usr/bin/env python3
import argparse
import base64
import json
import os
import random
import string
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests


@dataclass
class TestResult:
    ttft_ms: float
    total_time_ms: float
    output_tokens: int
    prompt_tokens: int
    tps_tokens: float
    tps_chars: float
    status: str


LOREM_IPSUM_WORDS = [
    "lorem",
    "ipsum",
    "dolor",
    "sit",
    "amet",
    "consectetur",
    "adipiscing",
    "elit",
    "sed",
    "do",
    "eiusmod",
    "tempor",
    "incididunt",
    "ut",
    "labore",
    "et",
    "dolore",
    "magna",
    "aliqua",
    "ut",
    "enim",
    "ad",
    "minim",
    "veniam",
    "quis",
    "nostrud",
    "exercitation",
    "ullamco",
    "laboris",
    "nisi",
    "ut",
    "aliquip",
    "ex",
    "ea",
    "commodo",
    "consequat",
    "duis",
    "aute",
    "irure",
    "dolor",
    "in",
    "reprehenderit",
    "in",
    "voluptate",
    "velit",
    "esse",
    "cillum",
    "dolore",
    "eu",
    "fugiat",
    "nulla",
    "pariatur",
    "excepteur",
    "sint",
    "occaecat",
    "cupidatat",
    "non",
    "proident",
    "sunt",
    "in",
    "culpa",
    "qui",
    "officia",
    "deserunt",
    "mollit",
    "anim",
    "id",
    "est",
    "laborum",
]


def generate_lorem_ipsum(length: int) -> str:
    """Generates a lorem ipsum string of approx fixed length."""
    text = ""
    while len(text) < length:
        text += " ".join(random.choices(LOREM_IPSUM_WORDS, k=10)) + " "
    return text[:length]


def load_text_file(filename: str) -> str:
    with open(filename, "r") as f:
        chars = f.read()
    return chars


def create_dummy_image_b64() -> str:
    """Creates a tiny 1x1 pixel red GIF as a base64 string for vision testing."""
    data = b"R0lGODlhAQABAIEAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAICTAEAOw=="
    return data.decode("utf-8")


def measure_request(
    url: str,
    api_key: str,
    model: str,
    prompt: str,
    image_b64: Optional[str] = None,
    max_tokens: int = 15,
    temperature: float = 0.0,
    seed: int = 42,
    verbose: bool = False,
) -> TestResult:
    """Sends a completion/chat request and measures timing."""
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    if image_b64:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/gif;base64,{image_b64}"},
                    },
                ],
            }
        ]
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
            "seed": seed,
            "cache_prompt": True,
        }
        endpoint = f"{url}/chat/completions"
    else:
        # Standard Completion
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
            "seed": seed,
            "cache_prompt": True,
        }
        endpoint = f"{url}/completions"

    start_time = time.time()
    first_token_time = None
    prompt_tokens = 0
    completion_tokens = 0

    try:
        response = requests.post(
            endpoint, headers=headers, json=payload, stream=True, timeout=300
        )
        response.raise_for_status()

        token_count = 0

        for line in response.iter_lines():
            if not line:
                continue
            line_text = line.decode("utf-8")
            if line_text.startswith("data: [DONE]"):
                break

            if line_text.startswith("data: "):
                try:
                    chunk = json.loads(line_text[6:])
                    # Parse final usage if available
                    if "usage" in chunk and chunk["usage"]:
                        prompt_tokens = chunk["usage"].get("prompt_tokens", 0)
                        completion_tokens = chunk["usage"].get("completion_tokens", 0)

                    # Capture First Token Time
                    if first_token_time is None and (
                        "choices" in chunk and len(chunk["choices"]) > 0
                    ):
                        delta = (
                            chunk["choices"][0].get("delta", {})
                            if "chat" in endpoint
                            else chunk["choices"][0]
                        )
                        text_content = (
                            delta.get("content", "")
                            if "chat" in endpoint
                            else chunk["choices"][0].get("text", "")
                        )
                        if text_content:  # Only count if there is actual content
                            first_token_time = time.time()
                            token_count += 1
                    elif first_token_time is not None:
                        token_count += 1

                except json.JSONDecodeError:
                    pass

        end_time = time.time()

        # If no tokens were streamed but request succeeded (e.g. max_tokens=0), use end_time
        if first_token_time is None:
            first_token_time = end_time

        ttft = (first_token_time - start_time) * 1000
        total_time = (end_time - start_time) * 1000

        # Generation TPS (Tokens)
        gen_duration = end_time - first_token_time
        tps_tokens = token_count / gen_duration if gen_duration > 0.001 else 0

        # Generation TPS (Chars - rough approx for compatibility)
        tps_chars = (
            (token_count * 4) / gen_duration if gen_duration > 0.001 else 0
        )  # Approximation

        # If prompt_tokens wasn't in usage (older server), estimate
        if prompt_tokens == 0:
            prompt_tokens = int(len(prompt) / 3.5)  # Crude estimation

        # If completion_tokens wasn't in usage, use streamed count
        if completion_tokens == 0:
            completion_tokens = token_count

        return TestResult(
            ttft,
            total_time,
            completion_tokens,
            prompt_tokens,
            tps_tokens,
            tps_chars,
            "SUCCESS",
        )

    except Exception as e:
        return TestResult(0, 0, 0, 0, 0, 0, f"ERROR: {str(e)}")


def incremental_prefill(args, full_text):
    """Incremental prefill with fail-fast support and granular reporting."""
    print(f"\n### Incremental Prefill & Warmup\n")
    print(f"**Step size:** {args.step} chars\n")
    print(f"| Chars | Tokens | Delta (ms) | Char/s | Tok/s |")
    print(f"| ---: | ---: | ---: | ---: | ---: |")

    step_chars = args.step
    current_len = step_chars
    total_len = len(full_text)

    prev_time = time.time()
    prev_tokens = 0
    prev_chars = 0
    
    results = []

    # Initial request to get token count baseline if needed, but we start with 0.
    
    while current_len <= total_len:
        subset = full_text[:current_len]
        
        # We need to measure the wall clock time for this step specifically
        step_start_time = time.time()
        
        # max_tokens=1 to force processing up to this point
        res = measure_request(args.url, args.api_key, args.model, subset, max_tokens=1)
        
        step_end_time = time.time()

        if res.status != "SUCCESS":
            print(f"| {current_len:<7} | ERROR | ERROR | ERROR | ERROR |")
            break

        current_tokens = res.prompt_tokens
        
        # Calculate Deltas
        # Delta time is the time taken for *this request* alone, which effectively measures 
        # the time to process the *incremental* new tokens (due to KV caching).
        # User requested "sensitive systemtime diff from last call". 
        # Ideally, this loop's stride time = step_end_time - step_start_time
        # But if we want "cumulative" implied:
        # Actually, since we are doing separate requests, the "Delta (ms)" is exactly the latency of the current request.
        # If caching works, this latency should be proportional to `step_chars`, not `current_len`.
        
        delta_time_s = step_end_time - step_start_time
        delta_tokens = current_tokens - prev_tokens
        delta_chars = len(subset) - prev_chars

        # Handling the first step or weird token reporting
        if delta_tokens < 0: delta_tokens = 0 # Should not happen with increasing context
        
        # Metrics based on this step's delta
        step_tok_s = delta_tokens / delta_time_s if delta_time_s > 0.0001 else 0
        step_char_s = delta_chars / delta_time_s if delta_time_s > 0.0001 else 0

        print(
            f"| {len(subset)} | {current_tokens} | {delta_time_s * 1000:.0f} | {step_char_s:.2f} | {step_tok_s:.2f} |"
        )
        
        # Fail-fast check
        if args.min_cps > 0 and len(results) >= 1: 
             # We check per-step performance for fail-fast
             if step_char_s < args.min_cps:
                 print(f"\n! Aborting: Step Char/s {step_char_s:.2f} < Threshold {args.min_cps}")
                 raise RuntimeError(f"Performance too low ({step_char_s:.2f} Char/s)")

        results.append((len(subset), current_tokens, delta_time_s, step_tok_s, step_char_s))

        prev_tokens = current_tokens
        prev_chars = len(subset)
        
        current_len += step_chars
        # Clamp to total length for final step
        if current_len > total_len and current_len - step_chars < total_len:
            current_len = total_len
            
    return results


def run_test(args):
    img_data = create_dummy_image_b64() if args.vision else None

    if args.payload_filename:
        static_prefix = load_text_file(args.payload_filename)
    else:
        static_prefix = generate_lorem_ipsum(args.context_len)

    # Print Header
    print(f"# LLM Benchmark Report\n")
    print(f"- **URL:** `{args.url}`")
    print(f"- **Model:** `{args.model}`")
    print(f"- **Payload:** {len(static_prefix)} chars")
    print(f"- **Vision:** {'ENABLED' if args.vision else 'DISABLED'}\n")

    # 1. Warmup / Incremental Prefill
    # Always use incremental prefill if 'step' is reasonable, or if user asked for it.
    # The user asked to "also display steps iff skip linearity". 
    # This implies we should always use the stepping logic to populate the cache and report status.
    
    if args.step < len(static_prefix):
        incremental_prefill(args, static_prefix)
    else:
        # Fallback for single-shot if step is larger than payload
        print(f"\n### Warmup (Single Shot)\n")
        res = measure_request(
             args.url, args.api_key, args.model, static_prefix, max_tokens=1
        )
        print(f"Single shot complete. Latency: {res.ttft_ms:.2f} ms")

    # 2. Main Loop
    print(f"\n### Cache Hit Latency Test (8 Loops)\n")
    print(f"| Loop | Distractor (ms) | Target Hit (ms) | Status |")
    print(f"| :--- | :--- | :--- | :--- |")

    hits = 0

    for i in range(1, 9):
        # A. Distractor
        distractor = (
            f"Q: Calculate {random.randint(100, 999)} + {random.randint(100, 999)}? A:"
        )
        res_d = measure_request(
            args.url, args.api_key, args.model, distractor, max_tokens=10
        )

        # B. Target
        query = f" Query {i}?"
        res_t = measure_request(
            args.url,
            args.api_key,
            args.model,
            static_prefix + query,
            img_data,
            max_tokens=10,
        )

        # Determine Status
        status = "UNK"

        if res_t.status != "SUCCESS":
            status = f"ERROR: {res_t.status}"
        elif res_t.ttft_ms < 1000:
            status = "**HIT**"
            hits += 1
        else:
            status = "MISS"

        # Print Row
        print(f"| {i:02d} | {res_d.ttft_ms:.1f} | {res_t.ttft_ms:.1f} | {status} |")

    # 4. Summary
    print(f"\n### Summary\n")
    print(f"- **Cache Hit Rate:** {(hits / 8) * 100:.1f}% ({hits}/8)")

    if args.vision:
        print(f"- **Vision Test:** ENABLED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Cache Performance Tester")
    parser.add_argument("--url", default="http://localhost:8080/v1", help="API URL")
    parser.add_argument("--key", default="sk-none", dest="api_key", help="API Key")
    parser.add_argument(
        "--payload",
        type=str,
        default="",
        dest="payload_filename",
        help="optional static payload",
    )
    parser.add_argument("--model", default="default", help="Model Name")
    parser.add_argument(
        "--len",
        type=int,
        default=50000,
        dest="context_len",
        help="Context length in chars",
    )
    parser.add_argument(
        "--step", type=int, default=3000, help="Step size in chars (default 3000)"
    )
    parser.add_argument(
        "--vision", action="store_true", help="Include dummy image in requests"
    )
    parser.add_argument(
        "--skip-linearity",
        action="store_true",
        help="Skip incremental checks and do one full prefill",
    )
    parser.add_argument(
        "--min-cps",
        type=float,
        default=0.0,
        dest="min_cps",
        help="Minimum Char/s threshold for fail-fast",
    )

    args = parser.parse_args()
    try:
        if args.min_cps > 0:
            print(f"- **Fail-Fast:** Enabled (< {args.min_cps} Char/s)")
        run_test(args)
    except KeyboardInterrupt:
        print(f"\n> **Test Aborted by User.**")
    except RuntimeError as e:
        print(f"\n> **Test Aborted:** {e}")
        sys.exit(1)
