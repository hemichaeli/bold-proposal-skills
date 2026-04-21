# Stage 4a — Visualization Reference

## Purpose

Turn the brand heart into images the client can see. A written concept is abstract. Mockups and atmosphere video let the client walk into the event in their mind before writing a check. The consistency of these visuals (palette, motif, light, typography) is what separates a premium proposal from a Pinterest board.

Output:
- 4 to 8 still mockups in `04-specialists/visual/mockups/`
- 1 atmosphere video (5 to 15 seconds) in `04-specialists/visual/atmosphere-video.mp4`
- `mood-direction.md` explaining prompt choices and visual logic

Tools: the `nano-banana` skill (Gemini image generation) and the `veo-video-creator` skill (Google Veo). Read their SKILL.md files before starting this stage.

---

## The "style anchor" pattern

The single most important trick for consistency across mockups is building a **style anchor**, a reusable block of prompt language that describes the visual world in one paragraph. This anchor goes into every image prompt. Without it, mockup 3 will look like it's from a different event than mockup 1.

### How to build the style anchor

Pull directly from `brand-system.md`:
- Palette (hex codes → descriptive words: "#E8D5B7 warm sand")
- Motif (the repeating visual device)
- Typography style (only if signage appears)
- Sensory cues (light, texture)
- Forbidden list (as negative prompts)

### Template

```
STYLE ANCHOR [Hebrew internal name: עוגן סגנון]:

Visual world: [one sentence capturing the event's feel]
Palette: [3-5 colors described in words, with hex in parentheses]
Motif: [the one repeating visual device]
Light: [quality of light: warm low tungsten / cool morning / chiaroscuro / etc.]
Materials: [real-world materials: brushed brass + raw concrete / lacquered wood + linen / etc.]
Typography (when visible): [font style and weight]
Composition: [wide cinematic / intimate medium / architectural symmetry / candid]
Camera feel: [full-frame 35mm / medium format / phone-authentic / etc.]
Avoid: [forbidden elements, e.g.: no generic corporate decor, no stock-photo people, no flower centerpieces]
```

Every subsequent image prompt is structured as:
```
[STYLE ANCHOR]
[Specific scene: what this particular mockup shows]
Aspect ratio: [16:9 / 4:5 / 1:1 / 9:16]
```

This way, mockup 8 still looks like it belongs to mockup 1.

---

## The mockup shot list

A strong proposal shows the client the event from multiple vantage points. Default shot list (adjust per event type):

1. **Arrival / first impression**, what guests see when they walk in. Wide shot, establishing the space.
2. **Hero moment**, the central visual: the stage, the reveal, the anchor installation. This is the image the client will remember.
3. **Scale reference**, a shot that shows the full room with people in it, establishing size and flow.
4. **Detail / texture**, close-up of a signature element: table setting, signage, menu card, installation detail. Sells the craftsmanship.
5. **Food / beverage**, if applicable. Branded presentation.
6. **Atmosphere / ambient**, the space without people, or with people blurred. Captures mood.
7. **Signage / wayfinding**, the typography and motif applied to navigation.
8. **Exit / takeaway**, what guests leave with, if there is a takeaway element.

For smaller events, 4 to 5 of the above is enough. For proposals requiring persuasion of a committee, all 8.

### Negative examples to avoid in prompts

- "beautiful event", meaningless
- "luxury", lazy; describe what luxury looks like in this palette
- "vibrant" / "stunning", filler words
- "people smiling at camera", will return stock-photo output
- "modern", vague and trend-chasing

### Positive examples

Instead of "a beautiful entrance":
> "Guests approach through a narrow corridor lit only by warm ground-level lighting. Walls are clad in brushed brass panels that catch the light in soft horizontal streaks. At the corridor's end, a single wall of matte ivory stone displays the event name in thin 40-point serif type. Shot from guest's point of view, 35mm, slight vignetting."

Good prompts are paragraphs, not adjective soup.

---

## Consistency checklist (before saving mockups)

After nano-banana returns each image, check:
- [ ] Palette match: dominant colors in the image are in the brand palette (not adjacent tones).
- [ ] Motif visible: the repeating visual device appears in at least 3 of the mockups.
- [ ] Light consistent: same light quality across the set (all warm, or all cool, not mixed unless intentional).
- [ ] No forbidden elements: scan for anything on the brand system's forbidden list.
- [ ] Scale believable: a 1000-seat gala does not appear in a 20-seat room.
- [ ] Text legible (when present): if signage is in the shot, the typography matches the brand system; misspellings or gibberish are regenerated.

If any image fails, regenerate with a tighter prompt rather than accepting a near-miss. The proposal is only as strong as its weakest mockup.

---

## The atmosphere video

The video is not a highlight reel. It is a 5-to-15-second mood piece. No cuts if possible (Veo handles single-shot video best at short durations). No text overlay. No music added in-generation (add music later in post if needed, using ffmpeg).

### Video prompt anatomy

```
[STYLE ANCHOR, condensed]
Scene: [one continuous moment, e.g., "Camera drifts slowly left across the arrival lounge. Guests in silhouette, warm low light, the brass wall catches the eye. Dust motes in the air."]
Duration: [5-15 seconds]
Camera: [static / slow pan / dolly in / slow push]
Motion in frame: [subtle, crowd murmur, fabric movement, candle flicker]
Mood: [exact mood words from brand-system.md's sensory signatures]
Aspect ratio: [16:9 widescreen / 9:16 vertical for Instagram]
Avoid: [fast cuts, title cards, music, busy motion]
```

### Why slow and silent

Fast cuts are TV-commercial grammar and they cheapen the proposal. Slow atmosphere says "this event is assured and composed". Silence is the gift of space; add music only in the final Gamma presentation or PDF walkthrough, not in the raw video generated here.

### Typical mockup-to-video translation

Take the "Arrival / first impression" mockup and turn it into a video. That is usually the strongest candidate because arrivals have natural motion (people walking, fabric moving, light shifting). The hero moment is often too static for a video unless something specifically reveals or transforms.

---

## `mood-direction.md`, what goes in it

This file explains to the user (and to future Claude instances iterating on the proposal) *why* the visuals look the way they do. It is for internal reasoning and optional inclusion in the client PDF as a "creative direction" section.

Template:

```markdown
# Mood Direction, [שם אירוע]

## עוגן הסגנון (Style Anchor)
[The full style anchor paragraph]

## החלטות חזותיות מרכזיות

### 1. אור
[Why this light, not that]

### 2. חומרים
[Why these materials]

### 3. הרכב (composition)
[Why wide vs tight, symmetry vs candid]

### 4. אנשים במסגרת
[Why people are shown this way, silhouetted, blurred, absent, featured]

## שוטים ופרומפטים
### Mockup 1, [שם]
**מה מראה:** [...]
**פרומפט:** [the actual prompt, including the style anchor]
**למה זה חשוב:** [...]

### Mockup 2, ...
(לכל mockup)

## וידאו האווירה
**מה מראה:** [...]
**פרומפט:** [...]
**למה חד-שוט וללא מוזיקה:** [...]

## קישורי מקור לקבצים
- `mockups/01-arrival.png`
- `mockups/02-hero.png`
- ...
- `atmosphere-video.mp4`
```

---

## When nano-banana is not installed

If `nano-banana` is not available in this session:
1. Tell the user clearly.
2. Offer two fallbacks:
   - Use `canvas-design` to create placeholder stylized illustrations (works for abstract/graphic events, not for photorealistic event mockups).
   - Skip mockups, deliver a stronger `mood-direction.md` that describes each shot in such detail the client can picture it.
3. Note in `mood-direction.md` that mockups are pending and will be added when the skill is available.

Do not fake mockup files.

---

## When veo-video-creator is not installed

Same principle:
1. Tell the user.
2. Offer to proceed without a video, noting it in the assembly stage.
3. Do not generate a placeholder video.

---

## Final sanity check

Before marking stage 4a complete, open the mockups side by side. Ask: *"Does this look like one event, or like eight different events?"* If eight, the style anchor was not tight enough. Tighten it and regenerate the outliers.
