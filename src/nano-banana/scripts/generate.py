#!/usr/bin/env python3
"""
generate.py

Single-image generation CLI for Nano Banana (Gemini image models).

Usage:
    python3 generate.py --prompt "..." --output out.png
    python3 generate.py --prompt-file prompt.txt --output out.png --model nano-banana-pro --aspect 16:9
    python3 generate.py --prompt "Change the sign to read 'Phoenix 2026'" --ref-image input.png --output out.png

Env:
    GEMINI_API_KEY — required
"""

import argparse
import os
import sys
import time
from pathlib import Path

MODEL_ALIASES = {
    "nano-banana-2": "gemini-3.1-flash-image-preview",
    "nano-banana-pro": "gemini-3-pro-image-preview",
    "nano-banana-v1": "gemini-2.5-flash-image",
    "flash": "gemini-3.1-flash-image-preview",
    "pro": "gemini-3-pro-image-preview",
}


def load_prompt(args) -> str:
    if args.prompt and args.prompt_file:
        print("ERROR: use either --prompt or --prompt-file, not both.", file=sys.stderr)
        sys.exit(2)
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if args.prompt:
        return args.prompt
    print("ERROR: must provide --prompt or --prompt-file.", file=sys.stderr)
    sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Generate an image with Nano Banana.")
    parser.add_argument("--prompt", help="Prompt text")
    parser.add_argument("--prompt-file", help="Path to text file with prompt")
    parser.add_argument("--output", required=True, help="Output path (PNG)")
    parser.add_argument(
        "--model",
        default="nano-banana-2",
        help="Model alias: nano-banana-2 (default), nano-banana-pro, nano-banana-v1, or raw model ID",
    )
    parser.add_argument(
        "--aspect",
        default=None,
        help="Aspect ratio: 16:9, 1:1, 9:16, 4:5, 3:2, etc. Appended to prompt.",
    )
    parser.add_argument(
        "--ref-image",
        action="append",
        default=[],
        help="Path to reference image for editing or multi-ref. Can be passed multiple times.",
    )
    parser.add_argument(
        "--retries", type=int, default=2, help="Retry on transient errors"
    )
    args = parser.parse_args()

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print(
            "ERROR: google-genai not installed. Install with: "
            "pip install google-genai --break-system-packages",
            file=sys.stderr,
        )
        sys.exit(2)

    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY is not set.", file=sys.stderr)
        sys.exit(2)

    prompt = load_prompt(args)
    if args.aspect:
        prompt = f"{prompt.rstrip()}\n\nAspect ratio: {args.aspect}"

    model_id = MODEL_ALIASES.get(args.model, args.model)

    contents = [prompt]
    if args.ref_image:
        from PIL import Image
        for ref_path in args.ref_image:
            contents.append(Image.open(ref_path))

    config = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])

    client = genai.Client()

    last_error = None
    for attempt in range(args.retries + 1):
        try:
            resp = client.models.generate_content(
                model=model_id, contents=contents, config=config
            )
            break
        except Exception as e:  # covers ResourceExhausted, InternalServerError, etc.
            last_error = e
            if attempt < args.retries:
                wait = 5 * (2 ** attempt)
                print(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"ERROR after {args.retries+1} attempts: {e}", file=sys.stderr)
                sys.exit(1)

    wrote = False
    for part in resp.candidates[0].content.parts:
        if getattr(part, "inline_data", None) is not None:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(part.inline_data.data)
            print(f"✓ Wrote {out} ({len(part.inline_data.data)} bytes, mime={part.inline_data.mime_type})")
            wrote = True
            break
        elif getattr(part, "text", None):
            print(f"[model text] {part.text}", file=sys.stderr)

    if not wrote:
        finish = getattr(resp.candidates[0], "finish_reason", None)
        print(f"ERROR: no image returned (finish_reason={finish}).", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
