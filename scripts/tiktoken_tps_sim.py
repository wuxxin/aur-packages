#!/usr/bin/env python3

"""
A Python script to simulate a token-per-second (TPS) output stream.
It reads text from a file or standard input, tokenizes it using OpenAI's
tiktoken library, and prints the decoded tokens to standard output at a
specified rate.

Dependencies:
  - tiktoken: Can be installed via pip: `pip install tiktoken`

Usage:
  - From file: tiktokenPerSecond.py --tps 20 --file your_document.txt
  - From stdin: echo "This is a test sentence." | python tiktokenest.py --tps 5
"""

import argparse
import sys
import time

import tiktoken


def simulate_tps_stream(text, tps):
    """
    Tokenizes the input text and prints it to stdout at a specified TPS rate.

    Args:
        text (str): The input string to process.
        tps (float): The target tokens per second.
    """
    # Using cl100k_base, the tokenizer for gpt-4, gpt-3.5-turbo, and text-embedding-ada-002
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception as e:
        sys.stderr.write(f"Error initializing tiktoken encoder: {e}\n")
        sys.stderr.write(
            "Please ensure 'tiktoken' is installed (`pip install tiktoken`).\n"
        )
        sys.exit(1)

    # Encode the entire text into a list of token integers
    tokens = encoding.encode(text)

    if not tokens:
        return  # Nothing to do if the input is empty

    # Calculate the delay required to achieve the target TPS
    # This is the time to wait between emitting each token.
    # delay_per_token = 1.0 / tps  # kept for reference but not used

    start_time = time.monotonic()
    tokens_emitted = 0

    print("--- Starting token stream simulation ---", file=sys.stderr)

    try:
        for token in tokens:
            # Decode the single token. Note: decoding token-by-token might not
            # perfectly reconstruct the original string for all tokenizers, but
            # it's effective for simulating a stream.
            # We wrap the token in a list as decode expects a list of tokens.
            decoded_token = encoding.decode([token])

            # Write the decoded token to standard output
            sys.stdout.write(decoded_token)
            sys.stdout.flush()  # Ensure the output is not buffered

            tokens_emitted += 1

            # --- Rate Limiting Logic ---
            # Calculate the expected time that should have elapsed for the
            # number of tokens emitted so far.
            expected_elapsed_time = tokens_emitted / tps

            # Calculate the actual time that has elapsed since the start.
            actual_elapsed_time = time.monotonic() - start_time

            # If the script is running ahead of schedule, sleep for the difference.
            # This self-correcting mechanism ensures the average TPS is maintained.
            if actual_elapsed_time < expected_elapsed_time:
                sleep_duration = expected_elapsed_time - actual_elapsed_time
                time.sleep(sleep_duration)

    except KeyboardInterrupt:
        # Allow the user to exit gracefully with Ctrl+C
        sys.stderr.write("\n--- Stream interrupted by user ---\n")
    finally:
        end_time = time.monotonic()
        total_duration = end_time - start_time
        if total_duration > 0:
            actual_tps = len(tokens) / total_duration
            print("\n--- Simulation complete ---", file=sys.stderr)
            print(f"Target TPS: {tps:.2f}", file=sys.stderr)
            print(f"Actual TPS: {actual_tps:.2f}", file=sys.stderr)
            print(f"Total Tokens: {len(tokens)}", file=sys.stderr)
            print(f"Total Duration: {total_duration:.2f}s", file=sys.stderr)


def main():
    """
    Main function to parse arguments and run the simulation.
    """
    parser = argparse.ArgumentParser(
        description="Simulate a token-per-second output stream to stdout.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--tps",
        type=float,
        required=True,
        help="Tokens per second rate for the output stream.",
    )

    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to the input text file. If not provided, reads from stdin.",
    )

    args = parser.parse_args()

    if args.tps <= 0:
        sys.stderr.write("Error: --tps must be a positive number.\n")
        sys.exit(1)

    input_text = ""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                input_text = f.read()
        except FileNotFoundError:
            sys.stderr.write(f"Error: File not found at '{args.file}'\n")
            sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Error reading file: {e}\n")
            sys.exit(1)
    else:
        # Read from standard input if no file is specified
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print(
                "Reading from stdin. Please provide input and press Ctrl+D (or Ctrl+Z on Windows) to end.",
                file=sys.stderr,
            )
            input_text = sys.stdin.read()

    simulate_tps_stream(input_text, args.tps)


if __name__ == "__main__":
    main()
