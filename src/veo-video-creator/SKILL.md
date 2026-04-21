---
name: veo-video-creator
description: Generate short atmosphere videos using Google Veo through the connected Veo MCP server. Use whenever the user asks to create, generate, produce, or make a video, clip, reel, or atmosphere piece, especially for event proposals, product launches, brand moments, social content, or cinematic 5-15 second clips. Trigger even when the user says "תכין לי סרטון אווירה", "וידאו קצר ל...", "make me a 10 second video of", "generate a cinematic clip", "show me the space coming alive", or when called from bold-proposal-builder stage 4a. This skill is designed for single-shot cinematic pieces; for multi-cut edits use ffmpeg-editor after. Requires the Veo MCP server to be connected (veo-mcp-server in the user's MCP list).
---

# Veo Video Creator

A thin wrapper over the user's connected **Veo MCP server** at `veo-mcp-server-production.up.railway.app`. Focuses on the craft of making a good short atmosphere video, not on the mechanics of the API (the MCP handles those).

Google Veo is Google DeepMind's video generation model. Veo 3 (current as of early 2026) handles 5 to 15 second clips reliably, supports image-to-video with reference stills, and produces cinematic quality suitable for client proposals.

---

## When to use this skill

**Trigger:**
- User asks for any video, reel, clip, or moving image under ~20 seconds.
- User asks for an "atmosphere video", "mood video", "ambient clip", "loop", "cinemagraph".
- Called from `bold-proposal-builder` stage 4a.
- User has a still image and wants to bring it to motion.

**Don't use for:**
- Multi-shot edits with cuts, transitions, text overlays — use `ffmpeg-editor` after Veo produces the raw footage.
- Long-form video (30+ seconds) — Veo is not built for that.
- Voiceover/music generation — generate separately and layer with ffmpeg.

---

## Prerequisites

### MCP connection
The Veo MCP server must be listed in the user's active MCP servers. Verify by calling `tool_search` with the query `"veo video"`. If the server is not available or returns errors, report this to the user before proceeding — do not attempt to call the Veo REST API directly from this skill.

### Finding the right tool
The exact tool names on the Veo MCP may vary between versions. Before generating, search:

```
tool_search(query="veo video generate")
```

The canonical tool pattern is: a function that takes a prompt + optional reference image + duration + aspect ratio, and returns a video URL or file path.

---

## The craft of a good atmosphere video

A Bold-quality atmosphere video is **slow, silent, and single-shot**. It is not a commercial. It is not a highlight reel. It is a held moment.

### The three rules

1. **No cuts.** One continuous shot. Five seconds of a single drifting camera move beats fifteen seconds of quick cuts every time.

2. **No music in-generation.** Veo can produce audio, but the raw piece should be clean. Music added later is more flexible and less cheesy than auto-generated soundtrack.

3. **Subtle motion only.** The camera moves slowly or not at all. Things in frame move quietly: candle flicker, fabric drift, a guest's silhouette passing, dust motes in a beam of light. Nothing explosive.

### The two shapes that work

**Shape A — the slow push-in.** Camera drifts toward a single focal element. Duration 8-10s. Starts wide, ends at a detail. Used for reveals, hero moments.

**Shape B — the ambient hold.** Camera static or barely moving. Duration 6-8s. Captures a space with quiet life in it. Used for establishing atmosphere.

Most Bold atmosphere videos are Shape B. Shape A is for when there is a specific thing to reveal.

---

## Prompt anatomy

```
[Mood sentence]
[Composition — what's in the frame and how it's framed]
[Light — the defining factor]
[Materials & color — texture and palette]
[Motion — camera and in-frame motion, deliberately limited]
[Duration — 5 to 15 seconds]
[Aspect ratio — 16:9 cinematic / 9:16 Instagram story / 1:1 square]
[Negative — what to avoid]
```

### Worked example

```
Mood: quiet, expectant, the moment before guests arrive.

Composition: wide shot of an empty arrival lounge, camera static at eye level,
centered on a single brass wall at the far end.

Light: warm low-tungsten from ground-level fixtures only, no overhead light.

Materials: brushed brass, unpolished concrete floor, ivory linen.

Motion: camera does not move. In frame: candle flicker on a low bar, slow dust
motes drifting through the ground-light beams, one silhouetted figure passing
once from right to left at mid-ground.

Duration: 8 seconds.
Aspect ratio: 16:9.

Avoid: crowd movement, zoom, pan, cut, music, text overlay, neon, lens flare.
```

Note the specificity of motion. "One silhouetted figure passing once" is directable; "people walking around" is not.

---

## Image-to-video (the most reliable pattern)

For event proposals, the strongest workflow is:

1. Generate the still mockup with `nano-banana` first (stage 4a).
2. Pick the strongest still (usually arrival or hero).
3. Pass that still to Veo as a reference / start frame, along with a motion prompt.

This gives you:
- A still and a video that share the exact same composition and palette.
- Much more reliable results than pure text-to-video.
- Consistency with the rest of the proposal's visual language.

### Calling pattern

Use the Veo MCP's image-to-video tool (find via `tool_search`). Typical parameters:

```
- image: path or URL to the reference still
- prompt: motion description (what should move, how the camera moves)
- duration_seconds: 5 to 15
- aspect_ratio: "16:9" (should match the reference image)
```

The motion prompt for image-to-video is **only about motion**, not about the scene. The scene is already in the image. Focus on:
- What moves in frame (and what doesn't)
- Camera motion (static / slow pan left / slow dolly in)
- Duration and pacing (slow, not fast)

---

## Aspect ratios and durations

| Use | Aspect | Duration |
|---|---|---|
| Proposal cinematic | 16:9 | 8-12s |
| Instagram feed | 1:1 | 6-10s |
| Instagram story | 9:16 | 6-15s |
| Gamma slide background | 16:9 | 6-8s |

Longer than 15s: stitch two 8-second clips with ffmpeg crossfade.

---

## Operational flow

```
1. tool_search(query="veo video")
2. (Optional) Generate reference still with nano-banana
3. Call the Veo MCP tool with reference image + motion prompt + duration + aspect ratio
4. Wait for completion (30-120 seconds typical)
5. Download the resulting video to /mnt/user-data/outputs/
6. Call present_files on the video file
```

If the MCP returns a URL, download:

```python
import requests
from pathlib import Path
Path("atmosphere-video.mp4").write_bytes(requests.get(url).content)
```

---

## Error handling

**Tool not found:** MCP server disconnected or wrong tool name. Ask user to reconnect. Do not fall back silently.

**Generation timeouts:** simplify the prompt (too many simultaneous motions time out more often).

**Morph artifacts:** Veo is stronger with less motion. Halve the motion and regenerate.

**Unwanted audio:** strip with ffmpeg:
```bash
ffmpeg -i input.mp4 -c:v copy -an output.mp4
```

---

## Integration with bold-proposal-builder

When called from stage 4a:

1. Read the style anchor from `mood-direction.md` or `brand-system.md`.
2. Pick the reference mockup (usually `01-arrival.png` or `02-hero.png`).
3. Build a motion prompt preserving the still's mood (usually Shape B).
4. Generate one video (not multiple variants).
5. Save to `proposals/<slug>/04-specialists/visual/atmosphere-video.mp4`.
6. Strip audio if auto-generated.

---

## When Veo is unavailable

If the user does not have the Veo MCP connected:
1. Tell them the proposal will be delivered without the atmosphere video.
2. Offer a still photography sequence (3 stills as storyboard) or a later attachment.
3. Do not substitute another service without explicit consent.
