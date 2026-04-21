# Stage 3, Brand Heart Reference (v2.1)

## Purpose

Stage 3 produces the brand heart of the event. **v2.1 change:** deliver three distinct directions (with visual references), let Hemi pick one, then develop that pick into the full brand system. If none land, generate three new directions.

Output during selection: `03-brand-heart/directions.md` with 3 options + 3 reference images
Output after selection: `03-brand-heart/brand-system.md` (9 fields)

## The three-directions method

### Why three
A single concept is a bet on taste. Three directions turn the creative choice into a conversation and teach the skill what Hemi picks.

### What makes directions distinct
They must differ on a fundamental axis, not surface details. Claude picks one axis per session:

- Tone axis: celebratory / contemplative / provocative
- Energy axis: high-intensity / steady / intimate
- Frame axis: narrative-driven / sensory-driven / symbolic-driven
- Time axis: looking back / in the moment / looking forward
- Scale axis: grand / human / subversive

Pick the axis most relevant to the event's goals (Stage 1 field 3). If two directions feel similar, wrong axis, regenerate.

## The directions.md format

```markdown
# שלושה כיוונים קונספטואליים, [Event Name]

## הציר הנבחר
[Axis name]: [one-sentence explanation]

---

## כיוון 1, [שם קצר 2-4 מילים]

### המשפט המרכזי
[One sentence that captures the idea]

### התזה
[2-3 sentences]

### 3 מילות מפתח
[Keyword 1, Keyword 2, Keyword 3]

### איך זה מרגיש
[1-2 sentences of sensory description]

### מה זה לא
[1 sentence naming what this direction rejects]

### משרת אילו מטרות מהבריף
[Per goal in brief field 3, one line]

### visual המחשה
![כיוון 1](mockups/direction-1.png)

---

## כיוון 2, [שם]
[Same structure]

---

## כיוון 3, [שם]
[Same structure]

---

## ההשוואה
| | כיוון 1 | כיוון 2 | כיוון 3 |
|---|---|---|---|
| תחושה | [1-2 words] | [1-2 words] | [1-2 words] |
| סיכון | [Main risk] | [Main risk] | [Main risk] |
| עדיפות לפי הבריף | [High/Med/Low] | ... | ... |

## ההמלצה שלי
[Claude picks one, explains in 2-3 sentences]

## מה עכשיו
בחר כיוון: "1", "2", "3"
או "אף אחד, תן לי שלושה חדשים"
או "תיקן ככה: [edit]"
```

## Visual generation

For each direction, Claude uses nano-banana to generate one abstract reference image BEFORE presenting directions.md.

Prompt template:
```
Atmosphere reference, [event type] in [city], feeling: [direction's keywords in English],
sensory: [light, materials, textures], mood: [1-2 adjectives].
Photographic style, no text, no logos, no people's faces in focus.
Resolution: 1536x1024.
```

Save to `04-specialists/visual/mockups/direction-[1|2|3].png`.

## Rejection path

If Hemi says "אף אחד":
1. Ask ONE clarifying question.
2. Hemi answers briefly.
3. Claude picks a different axis (never the same one that just failed).
4. Generate three new directions along the new axis.
5. Max 3 rejection cycles. After 3: "אני מפספס משהו בבריף. בוא נחזור ל-Stage 1 ונחדד."

## Selection path, building the brand heart

When Hemi picks:
1. Confirm: "בחרת ב-[name]. אני מפתח אותו ל-brand-system מלא."
2. Expand the chosen direction into `brand-system.md`:

```markdown
# Brand System, [Event Name]

## 1. Concept name
## 2. One-sentence manifesto
## 3. Three keywords
## 4. Palette (Primary/Secondary/Accent/Neutral, hex + name)
## 5. Typography (Display, Body, Hebrew-first notes)
## 6. Materials palette (3-5 materials with texture notes)
## 7. Sensory signature (Sound, Scent, Temperature, Pace)
## 8. Tone of voice
## 9. Forbidden elements (3-5 items)
```

## Learning Hemi over time

After every selection, log to `data/hemi-preferences.md`:

```markdown
### [Event name], [date], [client]
- Axis used: [axis]
- Options: [dir 1 name] | [dir 2 name] | [dir 3 name]
- Chosen: [1/2/3], [name]
- Rejected axes in this session: [list or "none"]
- Stage 7 verdict: [1-5 + 1 line] (filled at Stage 7)
```

After 3+ events, Claude builds inferred-patterns sections in the same file. At start of every Stage 3 session, read this file to calibrate.

**Stretch policy:** ALWAYS include one direction that is a deliberate stretch. The learning loop tunes the other two, not all three. Rejection rate target: 15-35%.

## What "done" looks like

- `directions.md` with three distinct directions + three visual references
- Hemi's explicit pick logged
- `brand-system.md` with all 9 fields
- `data/hemi-preferences.md` updated

If Hemi didn't pick from three options, Stage 3 is not done.
