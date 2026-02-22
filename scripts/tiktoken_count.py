#!/usr/bin/env python3

import sys
import argparse
from typing import Optional

import tiktoken


def count_tokens_in_string(
    content: str, model_encoding: str = "cl100k_base"
) -> Optional[int]:
    """
    Count tokens in a string using a specific tokenizer encoding.

    The tokenizer encoding. "cl100k_base" is used by gpt-4, gpt-3.5-turbo and text-embedding-ada-002.
    """

    try:
        # Load the tokenizer for the specified encoding.
        encoding = tiktoken.get_encoding(model_encoding)

        # Encode the text content into a list of token IDs.
        tokens = encoding.encode(content)

        # The token count is the length of this list.
        token_count = len(tokens)
        return token_count

    except Exception as e:
        print(f"An error occurred while counting tokens: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Count Token of input data.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--encoding",
        type=str,
        required=False,
        default="cl100k_base",
        help="Encoding of the Tokenizers. defaults to 'cl100k_base' which is used by gpt-4, gpt-3.5-turbo and text-embedding-ada-002",
    )

    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to the input text file. If not provided, reads from stdin.",
    )

    args = parser.parse_args()

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

        # Call the function and output the result.
    num_tokens = count_tokens_in_string(input_text, args.encoding)

    if num_tokens is not None:
        print(f"Text contains approximately {num_tokens} tokens.")


if __name__ == "__main__":
    main()
