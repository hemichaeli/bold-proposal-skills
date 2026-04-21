# Prompting Guide — Nano Banana

## The core principle

The model has seen everything. The question is which part of everything you ask it to recall. A vague prompt averages across all the examples the model has seen and returns the statistical middle, which looks like stock photography. A specific prompt points to a narrow region of the training distribution and returns something specific.

Specificity is the entire game.

---

## The four layers of a good prompt

Every strong prompt has these four layers, in this order:

### 1. Composition, what is in the frame, from where

Examples:
- "Wide shot from the guest's point of view, looking down a narrow corridor toward a far wall."
- "Close-up at table height, eye level with the plate."
- "Top-down flatlay, even diffuse light."
- "Low angle, camera 30cm off the floor, looking up at the stage."

Without a composition cue, the model picks the statistical-average angle, which is "medium shot, straight on". Almost never what you want.

### 2. Light, the defining factor

Light is more important than color. Light is what separates "amateur event photo" from "editorial".

Vocabulary that works:
- "Warm low-tungsten from ground level, single-source"
- "Cool morning diffuse, window light only"
- "Chiaroscuro, one hard spot on the subject, deep shadows"
- "Dusk, fading ambient, warm artificial punching through"
- "Overhead softbox, studio-clean"
- "Candlelight, flickering, warm-orange fall-off"
- "Blue-hour exterior, the horizon still glowing"

Never just "well-lit" or "dramatic lighting". Those are non-words.

### 3. Materials and color

After you've set composition and light, specify what things are *made of*, not just what they *look like*.

"Brushed brass", "unpolished concrete", "ivory linen", "matte charcoal aluminum", "waxed oak", "frosted glass", "unglazed stoneware", "raw plaster". Each of these maps to a recognizable set of material references the model can pull from.

Color: give hex codes OR descriptive color names, not both. Hex codes are more precise but harder for the model to interpret when used alone; pair them with a word:
- "#1E2B3A deep navy"
- "#C9A961 brushed brass"
- "#F5F1EA ivory"

The model uses the color word and treats the hex as a refining hint.

### 4. Mood and camera

One short sentence to anchor feeling and production grammar:

- "Editorial, like an interiors magazine photograph"
- "Candid, phone-authentic, slightly overexposed"
- "Cinematic anamorphic, wide frame, shallow depth"
- "Studio-clean, catalogue"
- "Documentary, 35mm film, slight grain"

These are shorthand for whole bundles of decisions. "Editorial" implies composed, restrained, considered. "Candid" implies motion blur allowed, imperfect composition, natural light preferred.

---

## Negative prompts ("Avoid:")

The last line of every prompt names what the model should not default to. This is your defense against the training-set average.

For event mockups, always avoid:
- "stock-photo people smiling at camera"
- "generic corporate event decor"
- "flower arrangement centerpieces" (unless you want them)
- "LED wall sponsor logos"
- "laser lighting in fog" (unless it fits)
- "plastic chair and folding table looks"
- "neon signage" (unless intentional)
- "crowded frames"

Stack 3 to 5 avoids. More than 5 and the model starts fighting itself.

---

## The "reference verbs", how to describe style

Instead of adjectives, use analogies to known visual territories:

- "Like a Vincent Van Duysen interior" (calm modernist architecture)
- "Like a Wes Anderson frame" (symmetry, pastel, deadpan)
- "Like a David Lynch scene" (warm, unsettling, deep shadows)
- "Like a Kinfolk magazine photograph" (natural light, restrained, ceramic/linen textures)
- "Like a Deakins-shot film" (motivated light, controlled contrast)
- "Like an Apple product launch 2015" (clean, airy, white-gradient, single hero)
- "Like the Aesop store aesthetic" (apothecary, amber, wood, brass)
- "Like a Bauhaus poster" (geometric, primary colors, sans-serif)

These are loaded references. They carry a lot of meaning in few words.

Warning: **copying living artists' signature styles** may violate usage policies. Reference traditions and schools (modernism, minimalism, brutalism) more than specific copyrighted living artists where possible.

---

## Scene-specific recipes (for event mockups)

### Recipe: Arrival corridor
```
Wide shot from the guest's point of view. Guests approach down a narrow corridor.
Warm ground-level lighting only (no overhead light). Walls clad in [material].
At the corridor's end, a single wall of [material] bears the event name in
thin [display font] type, roughly 40cm tall.
Camera: 35mm film feel, slight grain, warm grade.
Avoid: generic corporate decor, overhead lighting, logos other than the event name.
Aspect ratio: 16:9
```

### Recipe: Hero moment
```
Wide central shot of the stage area. Single focal element:
[describe the hero element, installation, reveal, platform].
Light tightly focused on the hero, room dim around it. Audience in silhouette.
Camera: medium format, centered composition, symmetric.
Mood: reverent, composed.
Avoid: LED screen background, stock-audience reaction shots, laser lights.
Aspect ratio: 16:9
```

### Recipe: Scale shot
```
Wide room shot at peak evening, guest count visible but individuals blurred.
Motion blur on people, tack-sharp environment. The event's visual motif
clearly visible in the background.
Camera: 35mm, slower shutter (~1/30), fixed tripod.
Mood: lived-in, social, warm.
Avoid: posed groups, camera flash look.
Aspect ratio: 16:9
```

### Recipe: Detail / table
```
Close-up at table height. A single place setting on [material] linen:
[describe plates, cutlery, glassware, any cards or typography].
Shallow depth of field, the setting sharp, the background falling off to warm blur.
Camera: 85mm equivalent, natural window light supplemented by candle.
Avoid: overhead flat lay (that's recipe 5, not this one).
Aspect ratio: 4:5
```

### Recipe: Food overhead
```
Overhead flat lay, even diffuse light, no shadow on the dish itself.
Three [dish description] on [serving piece] with [garnish].
Surface: [material].
Camera: direct overhead, 50mm equivalent.
Mood: restrained, editorial.
Avoid: busy styling, too many props, brightly colored garnishes that don't fit the palette.
Aspect ratio: 1:1
```

### Recipe: Signage / wayfinding
```
[Material] sign, roughly A3 size, mounted at eye level.
Type reads [exact text in quotes]. Typography is thin, [serif/sans], subtle.
Warm ground light grazes across the sign's surface.
Camera: 35mm, slight angle (not fully frontal).
Mood: confident, quiet.
Avoid: all-caps unless specified, decorative elements, other signage in frame.
Aspect ratio: 3:2
```

---

## Iterating when the first result is off

**If the image looks like stock:** your prompt is too generic. Add composition, light, materials, and a negative clause.

**If the image is too busy:** delete half your descriptive words. Usually you're over-specifying.

**If the image is weird/distorted:** specify camera and focal length ("35mm", "50mm equivalent"). The model calms down when it has camera parameters.

**If the color is wrong:** pair hex codes with color words. Repeat the main color twice in the prompt.

**If the material feels fake:** name *two* materials in contrast. "Brushed brass against unpolished concrete" gives the model a grounding comparison.

**If the people look uncanny:** either (a) remove people and show the space empty, (b) put people in silhouette or motion blur, or (c) ask for "backs of heads" explicitly. Faces are hard; avoid them when you can.

**If text in the image is gibberish:** switch to Nano Banana Pro. If you're already on Pro, shorten the text to 2-3 words and specify the typeface.

---

## Consistency across a set, the non-obvious rules

- **The style anchor must be *identical*, byte-for-byte, across all images.** Not paraphrased. Copy-paste.
- **Same aspect ratio per set** (mostly). Mixing 16:9 and 4:5 in the same set fractures the world.
- **Same time of day** within a set. Don't mix morning and evening shots.
- **Same camera vocabulary.** "35mm film" all the way through, not "35mm film" in image 1 and "cinematic anamorphic" in image 3.
- **Regenerate outliers, don't edit them.** If mockup 5 is off-world, regenerate with the same anchor rather than asking the model to "fix" it.

---

## Hebrew text specifics

Hebrew rendering works but is less reliable than English:

- Use Nano Banana Pro for any visible Hebrew text.
- Keep Hebrew strings short (1 to 5 words). Longer strings increase the chance of letter errors.
- Specify the typeface as "thin", "sans-serif", "serif", the model works better with font descriptors than font names it may not know.
- For any critical Hebrew signage, accept that you may need to overlay the real text in post (using PIL, Figma, or canvas-design).
- RTL considerations: Hebrew reads right-to-left. If specifying placement, say "right-aligned" for start-of-line.

Example:
```
Thin sans-serif Hebrew type reading "אולם ראשי" in white, right-aligned,
mounted on matte charcoal wall.
```

---

## The final check

Before committing to an image, ask:
1. Can I tell what time of day it is?
2. Can I tell what materials are in the frame?
3. Does the light have a *source* (not ambient everywhere)?
4. Does the image carry the brand motif?
5. If I showed this to the client, would they ask "is this a real photo of what we're building?", or would they assume it's a stock image?

If any answer is weak, iterate before moving on. One strong image beats three mediocre ones.
