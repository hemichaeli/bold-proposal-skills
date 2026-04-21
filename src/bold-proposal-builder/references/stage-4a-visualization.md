# Stage 4a, Visualization Reference (v2.1)

## Purpose

Stage 4a turns the brand heart (Stage 3 output) into visual direction: mockups of the event's key moments, an atmosphere video, and written mood direction. This is what lets the client **see** the event before it exists.

**v2.1 change:** Like Stage 3, Stage 4a delivers **three distinct visual directions**, each with a hero mockup. Hemi picks one. That pick gets developed into the full mockup set (4-6 images), atmosphere video, and mood direction document. If none of the three land, Claude generates three new directions.

Output (after selection): `04-specialists/visual/mockups/*.png` + `atmosphere-video.mp4` + `mood-direction.md`
Output (during selection): `04-specialists/visual/directions/` with three hero mockups + comparison doc

---

## The three-directions method, visual edition

### Why three directions at both Stage 3 and Stage 4a
Stage 3 decides the concept. Stage 4a decides how the concept looks. These are genuinely different decisions, and the same brand heart can be visualized in radically different ways. A concept like "quiet confidence" could be:

- Minimal white room with one strong object
- Dense warm library with layered textures
- Nighttime garden with low lamps

All three honor the brand heart. They feel completely different. Hemi picks which visual world matches his vision for this specific client.

### Distinguishing axes (visual edition)

Claude picks one axis from the list, most relevant to the event's constraints:

- **Density axis:** minimal / balanced / maximal
- **Light axis:** daylight-bright / warm-ambient / dramatic-shadow
- **Material axis:** natural-organic / engineered-clean / mixed-crafted
- **Era axis:** timeless / contemporary / period-specific
- **Space axis:** open-architectural / enclosed-intimate / outdoor-integrated

Pick one axis. Generate three directions along it. Same rules as Stage 3: if two look too similar, wrong axis, regenerate.

---

## Pre-requisites

Before Stage 4a runs, these must exist:
- `03-brand-heart/brand-system.md` (all 9 fields filled)
- `data/hemi-preferences.md` if it exists (read for visual preferences across past events)
- nano-banana skill installed and working

If any is missing, Stage 4a cannot produce the three directions.

---

## The directions document format

Saved to `04-specialists/visual/directions/directions.md`:

```markdown
# שלושה כיוונים ויזואליים, [Event Name]

## הציר הנבחר
**[Axis name]:** [one sentence on why this axis matches the brand heart]

## תקציר Brand Heart (מ-Stage 3)
- Concept: [from brand-system.md field 1]
- Keywords: [field 3]
- Forbidden elements: [field 9]

---

## כיוון ויזואלי 1, [שם קצר]

### תחושה חזותית
[2 sentences describing the feeling the space creates]

### הסצנה שתהיה Hero (רגע השיא)
[Which moment of the event this direction shows best, and why]

### הסביבה החומרית
- Light: [specific]
- Colors: [specific hex + mood]
- Materials: [3-4 with texture]
- Scale of elements: [human / monumental / intimate]

### מה זה לא
[1 sentence: what this direction explicitly rejects visually]

### Hero mockup
![כיוון 1](direction-1-hero.png)

### מה הייתי מפתח אם תבחר את זה
[List of 4-6 additional mockups to generate if this direction is chosen:
  1. Arrival
  2. Main space
  3. Hero moment
  4. Catering area
  5. Closing
  6. Details shot
]

---

## כיוון ויזואלי 2, [שם]
[Same structure, different hero mockup]

---

## כיוון ויזואלי 3, [שם]
[Same structure, different hero mockup]

---

## ההשוואה
| | כיוון 1 | כיוון 2 | כיוון 3 |
|---|---|---|---|
| תחושה חזותית | [words] | [words] | [words] |
| ההשקעה בבינוי | [low/med/high] | ... | ... |
| התאמה לקונספט | [short] | ... | ... |
| סיכון חזותי | [main risk] | ... | ... |

---

## ההמלצה שלי
[Claude picks one and explains why in 2-3 sentences, referencing the brand heart and hemi-preferences if applicable]

## מה עכשיו
בחר כיוון: "1", "2", "3"
או "אף אחד, תן לי שלושה חדשים" (Claude יגנרט 3 כיוונים בציר שונה)
או "תיקן ככה: [edit]" (Claude יאפס כיוון ספציפי)
```

---

## Hero mockup generation

For each of the three directions, Claude uses nano-banana to generate ONE hero mockup (not four, not six) before presenting directions.md. This keeps the selection phase fast.

### nano-banana prompt template for hero mockup
```
Event interior, [venue type inferred from brief], hero moment.
Atmosphere: [direction's keywords], [direction's light setting].
Materials: [direction's materials list].
Palette: [brand-system palette].
Scale: [direction's scale of elements].
People: blurred, suggestive, no faces in focus.
Style: photographic, editorial, shot on 35mm, shallow depth of field.
Aspect ratio: 16:9, resolution 1920x1080.
No text, no logos, no watermarks.
```

Save each mockup to `04-specialists/visual/directions/direction-[1|2|3]-hero.png`.

---

## Rejection path, visual edition

If Hemi says "אף אחד":
1. Claude asks ONE question. Options:
   - "איזה מהשלושה היה הכי רחוק, ולמה?"
   - "מה בכיוונים האלה הרגיש לא מתאים לקונספט?"
   - "חסר לך משהו שלא הצלחתי להראות? תן לי רמז."
2. Hemi answers briefly.
3. Claude picks a **different axis** (never the same one that failed).
4. Generates three new hero mockups along the new axis.
5. Max 3 rejection cycles per Stage 4a. After 3, Claude says: "אני לא מצליח להראות לך את מה שבראש שלך. בוא נדבר 5 דקות על רפרנס ויזואלי אחד שאתה אוהב, ונחזור לכאן עם כיוונים חדים יותר."

---

## Selection path, full visual development

Once Hemi picks ("1", "2", or "3"):
1. Claude confirms: "בחרת ב-[name]. אני מפתח עכשיו 4-6 מוקאפים נוספים + סרטון אווירה + mood direction."
2. Generate remaining mockups listed under "מה הייתי מפתח" in the chosen direction, via nano-banana.
3. Generate atmosphere video (10-15 seconds) via veo-video-creator using the hero mockup as reference.
4. Write `mood-direction.md`.

### The mockup set (4-6 images)

Standard event mockup sequence:
1. Arrival (what the guest sees walking in)
2. Main space (hero wide shot)
3. Peak moment (the event's climactic visual)
4. Catering / hospitality area
5. Closing moment (what the guest sees leaving)
6. Details (close-ups: materials, signage, florals, lighting fixtures, specific objects)

For smaller budgets (below ₪80K), 4 mockups are acceptable. For larger budgets, aim for 6.

### The atmosphere video
10-15 seconds. Pans or slow zooms across hero composition. No speech, no text overlay. Music optional; if included, matches brand-system sensory signature.

### mood-direction.md
```markdown
# Visual Mood Direction, [Event Name]

## The direction (from Hemi's pick)
[Name, and 1 paragraph summary]

## Color system
- Hex palette: [ordered by hierarchy]
- Where each color appears: [specific applications]

## Light system
- Daytime: [description if relevant]
- Primary lighting: [fixtures, intensity, color temperature]
- Accent: [specific features]
- Forbidden: [what not to do lighting-wise]

## Material palette
[Detailed notes per material, where used, supplier/category if known]

## Typography in space
[How signage, menus, program look]

## Reference images
[Links to each mockup in the full set + atmosphere video link]

## For vendors
[3-5 specific directives vendors must follow to stay on brand]
```

---

## Learning Hemi over time, Stage 4a loop

Same logging pattern as Stage 3, separate log file.

### What gets logged per event, in `data/hemi-preferences.md` under "Stage 4a"

```markdown
## Stage 4a choice log

### [Event name], [date]
- Axis used: [density / light / material / era / space]
- Options presented: [dir 1 desc, dir 2 desc, dir 3 desc]
- Chosen: dir [N]
- Client feedback on final visual (from Stage 7): [1-5 + notes]
- Bold's own assessment (Hemi's reflection): [1-5 + notes]
```

### What Claude infers from 3+ events

```markdown
# Hemi, Stage 4a Preferences (inferred)

## Axes Hemi responds to
- Light axis: picks "warm-ambient" in 4 of 5 events; never picked "daylight-bright"
- Material axis: picks "mixed-crafted" in 3 of 4 events; never picked "engineered-clean"

## Visual patterns Hemi consistently picks
- Shallow depth of field over wide deep focus
- Human-scale objects over monumental installations
- Single strong focal object over decorative accumulation

## Visual patterns Hemi consistently rejects
- Minimalism that feels "cold"
- Period-specific references (picks timeless or contemporary, never period)
- Symmetry-heavy compositions

## Client-specific visual patterns
- Phoenix Group: warmth + deep color saturation
- Keren portfolio: cooler palette + clean lines

## Implications for future Stage 4a runs
- Default one direction toward Hemi's strong preferences
- Always include one "stretch" direction (even if Hemi rejects 70% of stretches, the 30% land big)
- For Phoenix Group: bias warm. For Keren: bias cool.
```

Read at the start of every Stage 4a session.

**CRITICAL:** Same rule as Stage 3. Do NOT collapse to Hemi's preferences. Always include one stretch direction. The learning loop refines the other two, not all three.

---

## What "done" looks like for Stage 4a

- One hero mockup per direction presented (3 total)
- Hemi's explicit pick logged with the axis used
- Full mockup set (4-6 images) generated from chosen direction
- Atmosphere video rendered
- mood-direction.md complete with palette, light, materials, typography, vendor directives
- Selection logged to `data/hemi-preferences.md`

If Hemi didn't pick from three options, Stage 4a is not done. Go back.
