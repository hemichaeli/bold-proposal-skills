# Video Prompting Guide, Veo

## The short version

Veo respects specificity. It respects restraint. It punishes busy prompts. The best Veo prompts are paragraphs that describe one continuous moment in cinematic language, not lists of "epic, stunning, amazing" adjectives.

---

## The seven parameters that matter

Every good video prompt answers these seven questions, in roughly this order:

1. **What is the mood?** One sentence.
2. **What is in the frame?** Composition: wide/medium/close, what's in foreground, middle, background.
3. **How is it lit?** The single most important factor. Name the source, direction, and color of light.
4. **What materials and colors are present?** Not adjectives, real materials.
5. **What moves in the frame?** Name specific motions with specific subjects.
6. **How does the camera move?** Often: "static" or "slow drift". Rarely anything more.
7. **What should be avoided?** A short negative list.

Plus two technical parameters:
- Duration (5 to 15 seconds)
- Aspect ratio (16:9, 1:1, 9:16)

---

## Examples from weak to strong

### Weak (generic)
```
A luxury event, beautiful lighting, elegant atmosphere, cinematic.
```
This returns a TV-commercial average. Skip.

### Okay (some specifics)
```
A warm event space at night with candles on the tables and people in nice
clothes walking through, cinematic feel.
```
Still too abstract. The model has to invent too much.

### Strong (directed)
```
Mood: intimate, reverent, the first breath of an evening about to begin.

Composition: wide shot of a long dining hall, camera eye-level, centered,
parallel perspective. Low tables stretch toward a dim far wall. Each table
holds a single tall ivory candle. Ceiling out of frame.

Light: only the candles and one hidden warm uplight along the far wall.
Surrounding darkness is almost complete. Amber-warm color grade.

Materials: unpolished concrete floor, raw plaster walls, linen-covered tables,
ivory beeswax candles.

Motion: camera remains perfectly still. Candle flames flicker subtly. A single
silhouetted figure in a dark suit walks slowly from right to left across the
middle ground, passes through frame in about 4 seconds. Nothing else moves.

Duration: 9 seconds.
Aspect ratio: 16:9.

Avoid: camera movement, more than one person, music, any text, any artificial
light other than the candles and the uplight, cuts, transitions.
```

That is the right size and specificity for a Bold atmosphere video.

---

## Motion vocabulary that works

### Camera moves (use sparingly)

- **Static**, default choice, strongest for atmosphere pieces
- **Slow drift**, camera moves imperceptibly, 1-2 cm per second (implied)
- **Slow push in**, camera moves forward toward a focal element, 10-20cm over the duration
- **Slow pull back**, reverse of push, used for reveals of context
- **Slow pan left / right**, horizontal rotation, very slow
- **Slow tilt up / down**, vertical rotation
- **Gentle handheld**, implies slight movement, warmer/more human feel

Avoid: zoom, whip pan, crane shots, drone moves, dolly zoom, rack focus. Veo interprets these unreliably and they rarely serve atmosphere.

### In-frame motion (be specific)

- "Candle flame flickers"
- "Ivory linen drifts slightly in a still room"
- "One silhouetted figure walks from [side] to [side] over [seconds]"
- "Dust motes drift through a beam of warm light"
- "Steam rises from a cup on a low table"
- "Water surface ripples gently in a black basin"
- "Single droplet falls, slow-motion feel"
- "Curtain sways as if a door opened nearby"

Every in-frame motion should have a subject and a specific description. "People walking" is too vague; "one figure walking from right to left over 4 seconds" is directable.

---

## Light recipes

### Candle light
```
Only candlelight. Multiple small flames, warm 1800K color, flickering.
Deep falloff to blackness beyond 2m. Skin tones glow warm.
```

### Dawn / dusk exterior
```
Blue-hour exterior, the horizon still slightly luminous. Ambient soft blue
everywhere with a single warm practical source inside the visible window.
```

### Editorial interior (daylight)
```
Cool morning daylight diffused through sheer white curtains, even soft fill,
subtle shadows, clean editorial feel.
```

### Warm low lounge
```
Warm low-tungsten only, no overhead light. Three hidden ground-level fixtures
grazing a back wall. Deep warm shadows. Faces in silhouette or rim-lit.
```

### Stark stage
```
Single top light on the stage, hard cut, everything beyond the pool of light
falls to deep shadow. Theatrical, chiaroscuro.
```

### Gallery
```
Multiple small directional spot lights on individual objects, walls in neutral
shadow, the feeling of a museum at evening.
```

---

## Aspect-ratio-specific advice

### 16:9 (cinematic widescreen)
The default for event atmosphere pieces. Gives room for wide composition. Use when the final destination is the proposal PDF, a Gamma slide background, or a web embed.

### 1:1 (square)
Good for Instagram feed posts. Compress the prompt, square frames don't handle extreme wide shots well. Favor medium and close compositions.

### 9:16 (vertical)
For Instagram stories, TikTok, Reels. Think vertical: stacked compositions (overhead + ground-level element), walking figures shot tall, vertical architectural elements. Landscape scenes look awkward cropped to vertical; use stills designed for the format.

---

## Duration and pacing

- **5s**, shortest useful. Enough for one small motion. Use when only one thing needs to happen.
- **6-8s**, sweet spot for ambient atmosphere holds. Long enough to breathe, short enough to loop.
- **9-12s**, for slow push-ins with a reveal. The first 4s establish, the next 5-6s advance, the last 1-2s rest at the destination.
- **13-15s**, maximum useful for Veo. Rare. Only when there's a genuine narrative arc (setup → reveal → breath).

Longer videos fragment in Veo's output: morph artifacts, coherence drift. Don't push past 15s.

---

## Image-to-video prompting (when you have a reference still)

When passing a reference image, the prompt is *only about motion and pacing*. The scene is already locked by the image. Don't re-describe the scene.

**Good image-to-video prompt:**
```
Camera remains static. In frame: candle flames flicker naturally, the linen on 
the far table sways as if disturbed by passing air, one silhouetted figure
crosses the middle ground from right to left over 4 seconds.
Duration: 9 seconds.
```

**Bad image-to-video prompt (redundant with the image):**
```
A warm event space with candles and elegant atmosphere. Ivory linens, warm
tones, guests in the background. Camera slowly drifts and people move around.
```

The model already sees the space from your image. Telling it again competes with the visual and confuses it.

---

## Handling of people

People are the hardest element in any generated video. Hands, faces, walks, all are failure-prone.

**Safe approaches:**
- **Silhouettes**, figures in full shadow against a lit background.
- **Backs of heads**, camera behind the subject.
- **Blurred movement**, figures passing fast enough to blur (motion + longer implied shutter).
- **Partial in frame**, a hand reaching in, a figure half-visible at the frame's edge.
- **Distant crowds**, people at a distance where individual features don't render.

**Risky:**
- Close-ups of faces (likely to look uncanny)
- Detailed hands holding objects
- Specific named people
- Groups in rapid motion

If the event requires people to be present in the shot, prefer silhouettes or motion blur. A proposal's atmosphere video is rarely the place for character-driven portraiture.

---

## Negative list templates

For event atmosphere:
```
Avoid: camera movement beyond what's specified, cuts, transitions, music,
text overlays, fast motion, crowds, drone shots, lens flare effects, 
artificial vignette, neon lighting, confetti, fireworks.
```

For product hero:
```
Avoid: people, busy backgrounds, zoom, rack focus, multiple product shots,
commercial-feel motion, text overlays, watermarks.
```

For quiet space:
```
Avoid: any motion other than what's specified, rain, wind, weather effects,
music, voiceover, text, cinematic flares.
```

---

## Post-generation steps

1. **Watch the first second carefully.** Veo morphs are most common in the first frame; if the first 15 frames look shaky or the subject warps, regenerate.
2. **Watch the last second.** Same issue, opposite end. The "landing" is where Veo sometimes drifts.
3. **Check audio.** If auto-generated audio is present and you want silent, strip with ffmpeg.
4. **Downsample only if needed.** Veo output is typically 1080p. For web embedding, 720p is plenty and saves file size.

```bash
# strip audio
ffmpeg -i input.mp4 -c:v copy -an output-silent.mp4

# downsample to 720p
ffmpeg -i input.mp4 -vf scale=-2:720 -c:v libx264 -crf 23 -preset slow -an output-720p.mp4

# loop-friendly (crossfade first and last frames)
# requires ffmpeg-editor skill for more complex looping
```

---

## When Veo gets it wrong

**Motion too fast:** the model amplifies whatever you describe. Halve the implied speed.

**Too much is happening:** trim the prompt. One or two motions, not five.

**Uncanny faces or hands appear:** regenerate without people, or specify silhouette/blur.

**Camera jitters:** explicitly say "camera is perfectly static" and remove any camera motion language.

**Color drifts from what the reference shows:** re-emphasize the palette in the prompt, and include hex codes paired with color words.

**The video looks like a stock clip:** your prompt was too generic. Go back to the seven parameters and be more specific on composition and light.
