#!/usr/bin/env python3
"""
batch_generate.py

Generate a set of consistent images sharing a style anchor.

Reads a JSON spec like:

{
  "model": "nano-banana-2",
  "style_anchor": "Visual world: editorial, restrained... [full anchor]",
  "output_dir": "mockups",
  "default_aspect": "16:9",
  "scenes": [
    {"slug": "01-arrival", "scene": "Empty arrival corridor...", "aspect": "16:9"},
    {"slug": "02-hero",    "scene": "Wide stage moment..."}
  ]
}

Usage:
    python3 batch_generate.py --spec mockup_set.json
"""

import argparse
import json
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


def main():
    parser = argparse.ArgumentParser(description="Batch-generate a consistent set of images.")
    parser.add_argument("--spec", required=True, help="Path to JSON spec file")
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--sleep-between", type=float, default=2.0, help="Seconds between requests")
    args = parser.parse_args()

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("ERROR: google-genai not installed.", file=sys.stderr)
        sys.exit(2)

    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY is not set.", file=sys.stderr)
        sys.exit(2)

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    model_id = MODEL_ALIASES.get(spec.get("model", "nano-banana-2"), spec.get("model"))
    anchor = spec["style_anchor"]
    default_aspect = spec.get("default_aspect", "16:9")
    out_dir = Path(spec.get("output_dir", "mockups"))
    out_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client()
    config = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])

    summary = []
    for i, scene_spec in enumerate(spec["scenes"]):
        slug = scene_spec["slug"]
        scene_text = scene_spec["scene"]
        aspect = scene_spec.get("aspect", default_aspect)
        out_path = out_dir / f"{slug}.png"

        prompt = f"{anchor}\n\nScene: {scene_text}\n\nAspect ratio: {aspect}"

        last_error = None
        wrote = False
        for attempt in range(args.retries + 1):
            try:
                resp = client.models.generate_content(
                    model=model_id, contents=prompt, config=config
                )
            except Exception as e:
                last_error = e
                if attempt < args.retries:
                    wait = 5 * (2 ** attempt)
                    print(f"[{slug}] attempt {attempt+1} failed: {e}. Waiting {wait}s.", file=sys.stderr)
                    time.sleep(wait)
                    continue
                break

            for part in resp.candidates[0].content.parts:
                if getattr(part, "inline_data", None) is not None:
                    out_path.write_bytes(part.inline_data.data)
                    print(f"✓ {slug}.png ({len(part.inline_data.data)} bytes)")
                    summary.append({"slug": slug, "ok": True, "path": str(out_path)})
                    wrote = True
                    break
            if wrote:
                break
            else:
                finish = getattr(resp.candidates[0], "finish_reason", None)
                print(f"[{slug}] no image returned (finish_reason={finish}). attempt {attempt+1}.", file=sys.stderr)

        if not wrote:
            summary.append({"slug": slug, "ok": False, "error": str(last_error)})

        # Small delay between requests to stay under rate limits
        if i < len(spec["scenes"]) - 1:
            time.sleep(args.sleep_between)

    # Write a summary log
    (out_dir / "_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    success = sum(1 for s in summary if s["ok"])
    print(f"\nDone. {success}/{len(summary)} images generated successfully.")
    print(f"Summary: {out_dir / '_summary.json'}")


if __name__ == "__main__":
    main()
