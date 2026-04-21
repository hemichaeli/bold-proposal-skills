# Stage 4b — Content & Experience Reference

## Purpose

Every event lives in time. A brilliant space with the wrong running order feels awkward. A perfectly run evening with generic words feels forgettable. Stage 4b authors the two artifacts that make the event feel directed and written, not just produced:

- `04-specialists/content/agenda.md` — the time-based architecture of the event.
- `04-specialists/content/scripts.md` — every piece of written or spoken text.

---

## The agenda

### Principles

**Time is the scarcest material.** A 3-hour event has 180 minutes. Every 5-minute segment is a decision: who owns this time, what is happening, what is the guest feeling.

**Peaks need space around them.** A reveal moment, a key speech, a performance — these need a quiet minute before and after. Stacking peaks kills them.

**Guests get tired.** After 90 minutes of standing, everyone wants to sit. After 45 minutes of content, everyone wants to move. Build the agenda knowing this.

**The opening and the closing carry disproportionate weight.** The first 10 minutes and the last 10 minutes are what guests remember. Design them with more care than the middle.

### Agenda format

Two views, both in the same file:

**View A — Block view** (for the brand heart translation):
```markdown
## מבנה האירוע — תמונת על

### 1. הגעה (arrival) — 30 דק'
**תחושה מבוקשת:** [...]
**מה קורה:** [...]
**עוגן חזותי:** [...]

### 2. פתיחה — 15 דק'
**תחושה מבוקשת:** [...]
**מה קורה:** [...]

### 3. גוף האירוע — [X דק']
...

### 4. שיא — [X דק']
...

### 5. סיום — [X דק']
...
```

**View B — Minute-by-minute run-sheet** (for the production):
```markdown
## לוח זמנים מפורט

| שעה | משך | פעולה | אחראי | הערות |
|---|---|---|---|---|
| 19:00 | 45' | פתיחת שערים, הגעה | עמדת כניסה | DJ רך, משקאות מקדימים |
| 19:45 | 5' | תזוזה לאולם הראשי | צוות אושרים | שינוי אור הדרגתי |
| 19:50 | 10' | דברי פתיחה, מנחה | יוסי (מנחה) | טקסט ב-scripts.md §1 |
| 20:00 | 20' | מצגת הלקוח | דובר הלקוח | מיקרופון על חסן פרופר |
| 20:20 | 10' | מעבר + משקה | מלצרים | תצוגה חדשה |
| 20:30 | 15' | רגע השיא / reveal | כל הצוות | אור מלא, סאונד קרשנדו |
| ... | ... | ... | ... | ... |
```

### Timing rules of thumb (Israeli events)

- Israeli guests arrive late. A 19:00 event fills around 19:30. Design arrival with this in mind, not as a failure mode.
- Content segments longer than 25 minutes lose attention. Break long segments with transitions.
- Meals shorten the event's feel. A 3-hour event that includes a seated dinner feels like 2 hours.
- Leave 20-minute buffers around major transitions. They get eaten every time.

---

## Scripts

This file is a library of every word guests see or hear, keyed by moment.

### Structure

```markdown
# Scripts — [שם אירוע]

## §1. הזמנה (Invitation copy)
**ערוץ:** WhatsApp / דיגיטלית מודפסת
**אורך:** [מילים]

[הטקסט המלא]

---

## §2. תזכורת שבוע לפני
**ערוץ:** WhatsApp broadcast
[הטקסט]

---

## §3. תזכורת יום לפני
[הטקסט]

---

## §4. שלט כניסה (wayfinding at arrival)
[הטקסט]

---

## §5. תפריט / רשימה (if printed)
[הטקסט]

---

## §6. דברי פתיחה — מנחה
**משך צפוי:** 3-4 דק'
**טון:** [הפנייה ל-brand-system.md §4]

[הטקסט המלא, כולל שתיקות מכוונות המסומנות "(שתיקה - 2 שניות)"]

---

## §7. מעבר לדובר הלקוח
[הטקסט המעבירי]

---

## §8. דברי דובר הלקוח
**סטטוס:** טיוטה לעריכת הלקוח
**טון:** [...]

[הטקסט המוצע]

**הערה:** ספר לדובר איזה טון מבוקש והשאיר לו חופש לכתיבה סופית. לא לאלץ מילים.

---

## §9. רגע השיא — סקריפט ותזמון
**מה נאמר + מה קורה חזותית בו-זמנית.**

[תיאור משולב]

---

## §10. דברי סיום
[הטקסט]

---

## §11. תודה לאחר האירוע
**ערוץ:** WhatsApp / מייל
**תזמון:** 24 שעות אחרי
[הטקסט]

---

## §12. תזכיר לצוות המפיק (talking points)
[דברים שצוות הפרודקשן צריך לדעת לומר אם נשאלים, על הקונספט, המסרים, האנשים החשובים]
```

### Writing principles

**Brevity is respect.** Guests did not come to listen to speeches. Cut ruthlessly. A great opening is 3 minutes, not 12.

**Specificity is warmth.** "Tonight we gather" is cold. "Tonight, in this room, are 47 people who made this possible" is warm.

**Read aloud.** Every line of spoken text must be read aloud in Hebrew. If it trips the tongue, rewrite. Written Hebrew and spoken Hebrew are different languages.

**Tie back to the concept.** The opening line should carry an echo of the concept from the brand heart. Guests never hear the concept, but they feel it when the words are aligned.

**Avoid clichés.** "חוגגים יחד", "ערב בלתי נשכח", "להוסיף נופך מיוחד" — banned. Anything the MC of any other event might say is by definition wrong for this one.

### Tone calibration against the brand system

Pull the three adjectives and the "we are / we are not" oppositions from `brand-system.md` §4. Before finalizing any spoken text, check each paragraph against them.

---

## Coordination with other stages

- **From stage 1:** mandatory messages and CTA must appear somewhere in scripts.
- **From stage 3:** concept, name, tagline, tone must be internalized; forbidden list must be respected.
- **To stage 4a:** the arrival moment and the hero moment need matching mockups; if scripts say "the first thing guests see is a single projected line of text", the mockup must show that.
- **To stage 5:** scripts with talent (MC, performer, musician) imply talent line items in budget.
- **To stage 6 / Gamma:** the "flow of the evening" slide in the final presentation is derived from the block view of the agenda.

---

## When the client has a preferred MC, speaker, or host

If the brief or transcript names a specific MC/speaker:
- Write to their known style if Hemi can describe it. Ask if needed.
- Mark the `§n` section as "draft for [name]; to be reviewed".
- Do not put words in a named public figure's mouth without flagging it for review.

---

## What "done" looks like

A run-sheet a production manager could hand to their team and execute without further questions, and a scripts file an MC could rehearse from the night before. If a reader asks "wait, what happens at 20:45?" and the agenda does not answer, it's not done.
