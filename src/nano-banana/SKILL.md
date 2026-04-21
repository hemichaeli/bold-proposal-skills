---
name: nano-banana
description: Generate and edit photorealistic images using Google's Gemini image models (Nano Banana, Nano Banana 2, Nano Banana Pro). Use whenever the user asks to generate, create, produce, or edit images for events, mockups, product shots, atmosphere visuals, branded collateral, social posts, marketing imagery, infographics, or any photoreal or styled image. Trigger even when the user says "תכין לי תמונה", "הדמיה של", "visualize this", "show me what X would look like", "make me an image of", "generate a mockup", "generate hero image", or attaches a reference image and asks for variants. Also trigger when called from another skill (e.g., bold-proposal-builder's stage 4a). Requires a GEMINI_API_KEY environment variable.
---

# Nano Banana

Gemini's native image generation, via the Gemini API. Reliable multi-image consistency, excellent text rendering, real-world knowledge, 4K output on the Pro tier. Free tier: ~500 images/day via a standard `GEMINI_API_KEY`.

---

## The three models

| Name | Model ID | Best for | Cost (1K) |
|---|---|---|---|
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | Fast iteration, consistency across sets, default choice | $0.045/img |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Hero / cover shots, accurate text-in-image, up to 4K | $0.134/img |
| Nano Banana (v1) | `gemini-2.5-flash-image` | Legacy; prefer Nano Banana 2 | $0.039/img |

**Default rule:** use **Nano Banana 2** for all mockups and iterative work. Switch to **Nano Banana Pro** only for:
- The cover image of a proposal or campaign (one shot that has to be perfect)
- Any image with significant text (signage, posters, menus, magazine mockups)
- 4K output for print

Verify current pricing at `https://ai.google.dev/pricing` before quoting the client.

---

## When to use this skill

**Trigger when the user asks to:**
- Generate any image (photoreal, illustration, 3D, infographic, mockup, logo concept, atmosphere).
- Edit an existing image (replace backgrounds, change outfit/product, remove objects, style transfer, add elements).
- Create a consistent set (4+ images that share a visual DNA).
- Add accurate text to an image (posters, menus, signage with real spelled-out words).

**Don't use for:**
- Pure ideation where no image is needed (respond with description).
- Image-to-video — use the `veo-video-creator` skill.
- Abstract single-page art objects with heavy typography manipulation — `canvas-design` may serve better.

---

## Prerequisites

### API key
```bash
export GEMINI_API_KEY="your-key-here"
```

Get a free key at https://aistudio.google.com/apikey. Hemi already has accounts; check the connected secrets before prompting.

### Python packages
```bash
pip install google-genai pillow --break-system-packages -q
```

Use `google-genai` (the new SDK), not the older `google-generativeai`.

---

## Minimum working example

```python
from google import genai
from google.genai import types
import base64
from pathlib import Path

client = genai.Client()  # reads GEMINI_API_KEY from env

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="A wide cinematic shot of an empty arrival lounge at dusk. Brushed brass panels on the walls catching warm ground-level light. Ivory stone floor. A single thin line of serif type on the far wall reads 'Phoenix Art'. 35mm film feel, slight grain, warm color grading. No people in frame.",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        Path("output.png").write_bytes(part.inline_data.data)
        print("✓ Wrote output.png")
```

For quick work, use the helper script at `scripts/generate.py` (see below).

---

## The style-anchor pattern (consistency across a set)

When generating multiple images that should belong to the same world (event mockups, campaign assets, product shots with consistent lighting), structure every prompt as:

```
[STYLE ANCHOR - identical across all images in the set]
[SCENE - the one thing that changes per image]
[ASPECT RATIO]
[NEGATIVE - what to avoid, usually identical across the set]
```

**Example style anchor** (for an event mockup set):
```
Visual world: editorial, restrained, warm. Feels like an interiors magazine photograph, not an event ad.
Palette: #1E2B3A deep navy, #C9A961 brushed brass, #F5F1EA ivory, #3A3A3A charcoal.
Light: warm low-tungsten from ground level, soft shadows, single-source feel.
Materials: brushed brass, unpolished concrete, ivory linen, matte charcoal metal.
Camera: 35mm, medium-format feel, shallow-to-medium depth of field.
Composition: symmetry or strong horizontals, negative space respected, never busy.
Avoid: stock-photo smiling people, generic event decor, flower centerpieces, LED wall sponsor logos, crowded frames, neon, cliché lighting.
```

Every scene prompt begins with this anchor. Keep the anchor *exact* across all images (copy-paste; don't rephrase).

---

## Image editing (change something, keep the rest)

Gemini's image models accept input images along with text instructions:

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()
input_image = Image.open("input.png")

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[
        "Keep the composition, lighting, and all architectural details exactly the same. Change the wall signage text to read 'Phoenix 2026' in the same serif typeface. Do not alter anything else.",
        input_image,
    ],
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)
```

**Tips for edits:**
- Start instructions with "Keep X, Y, Z exactly the same" to pin down what must not change.
- Describe the edit in one sentence.
- For text edits, specify the new text in quotes and say "same typeface".
- If the edit is not working after 2 tries, switch to Nano Banana Pro — it reasons about layout better.

---

## Multi-image input (style transfer, blending)

Pass 2+ reference images:

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Using the color and material palette of image A and the composition of image B, create a new event mockup showing a bar setup.",
        Image.open("palette_ref.png"),
        Image.open("composition_ref.png"),
    ],
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)
```

---

## Prompting that actually works

See `references/prompting-guide.md` for the full methodology. Short version:

**Good prompts are paragraphs, not adjective lists.** "A beautiful luxury event" is useless. "A wide shot of an empty lounge at 20:45, warm tungsten light from six hidden ground fixtures, brushed brass wall catching the light in soft horizontal streaks, ivory linen draped over low seating, 35mm film feel" is the right size.

**Lead with composition and light.** The first sentence of a prompt should describe what's in the frame and how it's lit. The second adds materials and color. The third adds mood.

**Specify camera and film.** "35mm", "medium format", "iPhone-authentic", "cinematic anamorphic", "studio softbox" — each maps to a recognizable look.

**Name what to avoid.** A short "Avoid:" clause at the end pins down what the model should not default to.

**Hebrew text in images:** Pro only. Even Pro gets Hebrew less reliably than English. For critical Hebrew signage, generate with placeholder English and overlay the real text in post (PIL, canvas-design, or a design tool).

---

## Aspect ratios

Nano Banana 2 supports these aspect ratios natively; specify in the config or prompt:

| Use case | Ratio | Pixels (1K) |
|---|---|---|
| Hero / wide | 16:9 | 1408 x 768 |
| Social square | 1:1 | 1024 x 1024 |
| Portrait / IG story | 9:16 | 768 x 1408 |
| Editorial print | 4:5 | 896 x 1152 |
| Landscape photo | 3:2 | 1248 x 832 |

Pass via config:
```python
config=types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE'],
    image_config=types.ImageConfig(aspect_ratio="16:9")
)
```

If `ImageConfig` is not available in your SDK version, include the aspect ratio as the last line of the prompt text: `Aspect ratio: 16:9`.

---

## The helper script

For common flows, use `scripts/generate.py`:

```bash
python3 scripts/generate.py \
  --prompt "prompt text here" \
  --output output.png \
  --model nano-banana-2 \
  --aspect 16:9
```

Flags:
- `--prompt` or `--prompt-file` (path to a text file for long prompts)
- `--output` (required)
- `--model` one of: `nano-banana-2` (default), `nano-banana-pro`, `nano-banana-v1`
- `--aspect` one of: `16:9`, `1:1`, `9:16`, `4:5`, `3:2`
- `--ref-image` (optional, can be passed multiple times for editing/blending)
- `--seed` (for reproducibility; not always honored but worth trying)

---

## Batch generation for mockup sets

See `scripts/batch_generate.py` and the worked example in `references/prompting-guide.md`.

---

## Error handling

Common failures:

| Error | Meaning | Fix |
|---|---|---|
| `PERMISSION_DENIED 403` | API key invalid or wrong model access | Check `GEMINI_API_KEY`; verify the model ID exactly matches (including `-preview` suffix) |
| `RESOURCE_EXHAUSTED 429` | Rate or quota limit | Wait, or switch to batch API for Pro |
| Response has no `inline_data` | Model returned only text | Your prompt may have triggered safety filters. Rephrase. |
| Generated image looks like stock photo | Prompt too generic | Rewrite prompt per the prompting guide |
| Text in image is gibberish | You used Nano Banana 2 for complex text | Switch to Nano Banana Pro |

Wrap every call in try/except and retry once on `RESOURCE_EXHAUSTED` after 5 seconds.

---

## Cost management

Typical session budget:
- Stage 4a of a Bold proposal: ~8 mockups × $0.045 = **$0.36**
- Cover image on Pro: 1 × $0.134 = **$0.13**
- Iteration (usually 2 to 3 tries per image): multiply by ~2.5
- Full proposal: **$1.00 to $2.50** typically

Free tier usually covers 2 to 3 full proposals per day.

---

## SynthID watermark

All images generated by Gemini include an invisible SynthID watermark. For client deliverables this is fine. The client retains commercial usage rights for images generated with a paid API key. Verify current terms at https://ai.google.dev/terms.

---

## Files

- `references/prompting-guide.md` — the full prompting methodology
- `references/api-reference.md` — model IDs, config options, error codes
- `scripts/generate.py` — single-image helper
- `scripts/batch_generate.py` — set generation with shared anchor
