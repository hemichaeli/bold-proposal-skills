# Stage 4a, Visualization Reference (v2.1)

## Purpose

Stage 4a turns the brand heart into visual direction. **v2.1 change:** like Stage 3, Stage 4a delivers three distinct visual directions (each with a hero mockup). Hemi picks one. That pick gets developed into full mockup set + atmosphere video + mood direction.

Output during selection: `04-specialists/visual/directions/` with 3 hero mockups + directions.md
Output after selection: `04-specialists/visual/mockups/*.png` + `atmosphere-video.mp4` + `mood-direction.md`

## Why three directions at both Stage 3 and Stage 4a
Stage 3 decides the concept. Stage 4a decides how the concept looks. The same brand heart can be visualized in radically different ways. "Quiet confidence" could be minimal white room, dense warm library, OR nighttime garden. Different visual worlds, same heart.

## Distinguishing axes (visual)

Pick one per session:

- Density axis: minimal / balanced / maximal
- Light axis: daylight-bright / warm-ambient / dramatic-shadow
- Material axis: natural-organic / engineered-clean / mixed-crafted
- Era axis: timeless / contemporary / period-specific
- Space axis: open-architectural / enclosed-intimate / outdoor-integrated

## Pre-requisites

- `03-brand-heart/brand-system.md` complete
- `data/hemi-preferences.md` read (for visual pattern learning)
- nano-banana installed

## The directions document format

```markdown
# שלושה כיוונים ויזואליים, [Event Name]

## הציר הנבחר
[Axis]: [why this axis matches the brand heart]

## תקציר Brand Heart
- Concept: [from brand-system]
- Keywords: [from brand-system]
- Forbidden elements: [from brand-system]

---

## כיוון ויזואלי 1, [שם]

### תחושה חזותית
[2 sentences]

### Hero moment
[Which event moment this direction shows best]

### הסביבה החומרית
- Light: [specific]
- Colors: [hex + mood]
- Materials: [3-4 with texture]
- Scale: [human / monumental / intimate]

### מה זה לא
[1 sentence]

### Hero mockup
![כיוון 1](direction-1-hero.png)

### מה הייתי מפתח אם תבחר את זה
1. Arrival
2. Main space
3. Hero moment
4. Catering area
5. Closing
6. Details

---

## כיוון ויזואלי 2
[Same structure, different hero]

---

## כיוון ויזואלי 3
[Same structure, different hero]

---

## ההשוואה
| | כיוון 1 | כיוון 2 | כיוון 3 |
|---|---|---|---|
| תחושה | [words] | [words] | [words] |
| השקעה בבינוי | low/med/high | ... | ... |
| התאמה לקונספט | [short] | ... | ... |
| סיכון | [risk] | ... | ... |

## ההמלצה שלי
[Claude picks one, 2-3 sentences]

## מה עכשיו
בחר: "1", "2", "3"
או "אף אחד, תן לי שלושה חדשים"
או "תיקן ככה: [edit]"
```

## Hero mockup generation

For each direction, one hero mockup via nano-banana BEFORE presenting directions.md.

Prompt template:
```
Event interior, [venue type], hero moment.
Atmosphere: [keywords], [light setting].
Materials: [direction's material list].
Palette: [brand-system palette].
Scale: [element scale].
People: blurred, suggestive, no faces in focus.
Style: photographic, editorial, shot on 35mm, shallow depth of field.
Aspect ratio: 16:9, resolution 1920x1080.
No text, no logos.
```

Save to `04-specialists/visual/directions/direction-[1|2|3]-hero.png`.

## Rejection path

If Hemi says "אף אחד":
1. ONE question: "איזה מהשלושה היה הכי רחוק, ולמה?"
2. Claude picks different axis, generates 3 new heroes.
3. Max 3 rejection cycles. After 3: "בוא נדבר 5 דקות על רפרנס ויזואלי אחד שאתה אוהב."

## Selection path

When Hemi picks:
1. Confirm: "בחרת ב-[name]. אני מפתח 4-6 mockups + atmosphere video + mood direction."
2. Generate remaining mockups via nano-banana.
3. Generate 10-15 second atmosphere video via veo-video-creator using hero mockup as reference.
4. Write `mood-direction.md`.

### mood-direction.md structure

```markdown
# Visual Mood Direction, [Event Name]

## The direction
[Name, 1 paragraph summary]

## Color system
- Hex palette (ordered by hierarchy)
- Where each color appears

## Light system
- Daytime (if relevant)
- Primary lighting (fixtures, intensity, color temperature)
- Accent
- Forbidden

## Material palette
[Per material: where used, supplier category]

## Typography in space
[Signage, menus, program]

## Reference images
[Links to each mockup + atmosphere video]

## For vendors
[3-5 specific directives]
```

## Learning Hemi over time

After every selection, log to `data/hemi-preferences.md` under Stage 4a section:

```markdown
### [Event name], [date], [client]
- Axis used: [axis]
- Heroes presented: [dir 1 desc] | [dir 2 desc] | [dir 3 desc]
- Chosen: [1/2/3], [name]
- Rejected axes: [list or "none"]
- Stage 7 verdict, client: [1-5 + line]
- Stage 7 verdict, Hemi: [1-5 + line]
```

After 3+ events, build inferred-patterns sections.

**Stretch policy:** Same as Stage 3. Always include one stretch direction. Rejection rate target: 15-35%.

## What "done" looks like

- 3 hero mockups generated
- directions.md presented
- Hemi's explicit pick logged
- Full mockup set (4-6 images) from chosen direction
- Atmosphere video rendered
- mood-direction.md complete
- hemi-preferences.md updated

If Hemi didn't pick from three options, Stage 4a is not done.
