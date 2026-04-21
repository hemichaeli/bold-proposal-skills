# API Reference — Nano Banana (Gemini image generation)

Current as of April 2026. Verify at https://ai.google.dev/gemini-api/docs/image-generation before quoting pricing to clients.

---

## Endpoint and SDK

**Preferred SDK:** `google-genai` (unified, v1+)
**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
**Auth:** API key via `GEMINI_API_KEY` env var, or Application Default Credentials on Google Cloud.

```bash
pip install google-genai --break-system-packages
```

---

## Model IDs

| Name | Model ID | Notes |
|---|---|---|
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | Default for iteration. Supports up to 2K. |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Best text rendering, 4K capable, batch API supported |
| Nano Banana (v1) | `gemini-2.5-flash-image` | Legacy. Avoid for new work. |

All three model IDs are case-sensitive. The `-preview` suffix is part of the ID — do not drop it.

---

## Minimum request

```python
from google import genai
from google.genai import types

client = genai.Client()  # reads GEMINI_API_KEY from env automatically

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="prompt text here",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)
```

`response_modalities=['TEXT', 'IMAGE']` is required. Without it, the model returns only text.

---

## Response structure

The response contains `candidates[0].content.parts`, which is a list of `Part` objects. Each part has either `text` or `inline_data`. **Always iterate** — position is not guaranteed.

```python
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        image_bytes = part.inline_data.data  # raw bytes (PNG/JPEG)
        mime = part.inline_data.mime_type    # e.g. "image/png"
        with open("out.png", "wb") as f:
            f.write(image_bytes)
    elif part.text is not None:
        print("Model text:", part.text)
```

The `inline_data.data` is **raw bytes**, not base64-encoded (the new SDK handles decoding). The older `google-generativeai` SDK returned base64 strings; if you see a base64 string, you are on the old SDK — upgrade.

---

## Config options

```python
config = types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE'],       # required for image output
    temperature=0.7,                              # 0.0 to 2.0; lower = more deterministic
    candidate_count=1,                            # usually 1; Pro supports up to 4
    safety_settings=[...],                        # optional; see below
    image_config=types.ImageConfig(
        aspect_ratio="16:9",                      # if supported by SDK version
        # image_size="1024x1024",                  # alternative to aspect_ratio
    ),
)
```

If `image_config` is not supported in your SDK version, append aspect ratio as the last line of the prompt text:

```
Aspect ratio: 16:9
```

---

## Supported aspect ratios

| Ratio | Approx. pixel output (1K mode) |
|---|---|
| 1:1 | 1024 x 1024 |
| 16:9 | 1408 x 768 |
| 9:16 | 768 x 1408 |
| 4:5 | 896 x 1152 |
| 5:4 | 1152 x 896 |
| 3:2 | 1248 x 832 |
| 2:3 | 832 x 1248 |
| 3:4 | 896 x 1152 |
| 4:3 | 1152 x 896 |
| 21:9 (Pro only, 4K) | 3840 x 1632 |

For 4K output (Nano Banana Pro only), request `image_size="4K"` or `2160x3840` etc. in `ImageConfig`.

---

## Input images (editing and multi-ref)

Pass PIL Images or bytes in the `contents` list alongside the text prompt:

```python
from PIL import Image

ref_image = Image.open("reference.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Keep the composition and light exactly. Replace the signage text to read 'Phoenix 2026'.",
        ref_image,
    ],
    config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
)
```

Up to ~8 input images per request. Pro handles multi-reference better than Flash.

---

## Pricing (verified late March 2026)

| Model | Resolution | Per-image price |
|---|---|---|
| Nano Banana | 1024px | $0.039 |
| Nano Banana 2 | 1024px | $0.045 |
| Nano Banana 2 | 1024px standard | $0.067 |
| Nano Banana 2 | 4K | $0.151 |
| Nano Banana Pro | 1024-2048px | $0.134 |
| Nano Banana Pro (batch) | 2K | $0.067 |

Free tier through Google AI Studio: approximately 500 images/day for Nano Banana; much lower for Pro. Rate limits are project-level, not key-level.

Always check `https://ai.google.dev/pricing` before committing numbers to a client.

---

## Rate limits (free tier, approximate)

- Requests per minute (RPM): 10
- Tokens per minute (TPM): 250,000
- Requests per day: shared across models at ~500 image-generating calls

Daily quota resets at 00:00 Pacific time (10:00 Israel in winter, 09:00 in summer).

---

## Safety filters

The model can refuse to generate certain content. Common triggers:

- Real named public figures (especially when the prompt implies controversy)
- Explicit violence, sexual content, weapons in use
- Copyrighted characters (Disney, Marvel, etc.)
- Medical/legal/financial advice in image form
- Minors in sensitive contexts

When refused, the response will have `finish_reason: SAFETY` and no `inline_data` in the parts. Rephrase the prompt — remove the trigger — and try again.

Relaxing safety (only at your own risk, and only for legitimate business use):

```python
from google.genai.types import SafetySetting, HarmCategory, HarmBlockThreshold

config = types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE'],
    safety_settings=[
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
        ),
        # ...
    ],
)
```

Do not use this to bypass legitimate safety concerns. Use it when the default is blocking legitimate professional content (e.g., an event photo mistaken for a controversial scene).

---

## SynthID

All Gemini-generated images embed an invisible SynthID watermark. This is mandatory and cannot be disabled. It does not visibly affect the image. It can be detected programmatically by Google's SynthID detector (web interface or API). Clients retain commercial usage rights with a paid API key; verify terms at https://ai.google.dev/terms.

---

## Error codes

| Code | Meaning | Response |
|---|---|---|
| `400 INVALID_ARGUMENT` | Malformed request — usually wrong modality config or bad model ID | Verify config and model ID spelling |
| `403 PERMISSION_DENIED` | API key invalid, wrong account, or model not enabled for this project | Regenerate key; verify you're using the right Google account |
| `404 NOT_FOUND` | Model ID does not exist (common typo: `gemini-3-pro-image` without `-preview`) | Check exact ID |
| `429 RESOURCE_EXHAUSTED` | Rate or quota limit hit | Wait, back off exponentially, or switch to batch API on Pro |
| `500 INTERNAL` | Transient server issue | Retry with exponential backoff |
| `503 UNAVAILABLE` | Service overloaded | Retry after 10-30s |

### Retry pattern

```python
import time
from google import genai
from google.genai import errors

def generate_with_retry(client, model, contents, config, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return client.models.generate_content(
                model=model, contents=contents, config=config
            )
        except errors.ResourceExhausted:
            wait = 2 ** attempt * 5
            print(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
        except errors.InternalServerError:
            time.sleep(10)
    raise RuntimeError(f"Failed after {max_attempts} attempts")
```

---

## Cost-aware patterns

- **Use Nano Banana 2 for all drafts.** Switch to Pro only for the 1-2 hero shots.
- **Batch API** (Pro only): halves per-image cost. Appropriate when a full mockup set can wait minutes rather than seconds.
- **Cache style-anchor results.** If you generated a reference image whose style you want to apply repeatedly, pass it as a ref rather than regenerating a new base each time.
- **Never regenerate "just to see another version" casually.** Each call is real money at scale.

---

## Platform access matrix

| Surface | Use case |
|---|---|
| **Gemini API (`google-genai` SDK)** | Programmatic integration from skills, scripts, servers |
| **Google AI Studio (web)** | Interactive testing of prompts before wiring into code |
| **Vertex AI** | Enterprise deployments with SLAs; different auth model (service account) |
| **Flow (Google AI film tool)** | Nano Banana 2 is the default image model; creative workflows |
| **Gemini app** | Consumer access; not for programmatic use |

This skill uses only the **Gemini API** path. The others are reference for context.

---

## Versioning policy

Google rotates preview model IDs periodically. When a new preview model launches, the previous one often remains available for 6 to 12 months with price adjustments. If a model ID starts returning 404:

1. Visit https://ai.google.dev/gemini-api/docs/models
2. Find the current image-generation model IDs
3. Update this reference and the `nano-banana/SKILL.md`

Do not silently swap models — notify the user when the default changes.
