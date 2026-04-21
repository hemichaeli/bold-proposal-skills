# Stage 1 — Intake Reference

## Purpose of this stage

The brief the client hands you is never the real brief. Clients describe what they want; the intake agent's job is to surface what they *need*. A gala opening they described as "celebratory" may be quietly trying to reposition a brand that has gone stale. A product launch framed as "introducing X" may actually be a defensive move against a rising competitor. Stage 1 output feeds everything downstream; if it is thin, the whole proposal is thin.

Two things happen in this stage:
1. **Structured brief capture** — all the logistical facts.
2. **Challenge distillation** — the strategic tensions the event must resolve.

---

## Inputs you might receive

### A. Free-form conversation or phone call summary
Hemi will paraphrase what the client said. You may get 2 to 4 paragraphs. Ask clarifying questions only if a mandatory field is missing.

### B. Fireflies transcript
A full transcript of an intake call. Possibly 10-40 minutes. Parse it end-to-end. Attribute statements to speakers. Note emotional cues ("I'm just tired of the same thing every year") because they reveal unstated priorities.

### C. Email thread
Usually short, often missing budget and date. Flag gaps immediately.

### D. Hybrid
A voice note + a doc + three WhatsApp screenshots. Common. Merge them.

---

## The mandatory brief schema

Fill every field in `01-intake/brief.md`. If truly unknown, write `חסר — להשלים מול הלקוח`. Never guess.

```markdown
# בריף — [שם לקוח / אירוע]

## 1. לקוח
- שם הארגון:
- איש קשר (שם + תפקיד):
- טלפון + מייל:
- מי מאשר את ההצעה:

## 2. האירוע
- סוג אירוע: (השקת מוצר / גאלה / חנוכת בית / כנס / השקה פנים-ארגונית / יום הולדת / אחר)
- תאריך מועדף + תאריך גיבוי:
- שעת התחלה + משך:
- עיר + מקום (אם כבר סגור):
- מספר מוזמנים:
- פרופיל הקהל: (גיל, רקע, תפקידים, שפה)

## 3. מטרות עסקיות
- מטרה ראשית: (מה הלקוח מודד הצלחה לפיו אחרי 3 חודשים)
- מטרות משניות:
- KPIs (אם הוזכרו):

## 4. מסרים
- מסר מרכזי שחייב לעבור:
- מה אסור שייאמר:
- קריאה לפעולה (Call to action) אחרי האירוע:

## 5. תקציב וציפיות מסחריות
- טווח תקציב:
- גמישות:
- מה כלול / לא כלול בטווח:

## 6. שותפים, ספקים ואילוצים קיימים
- ספקי חובה (מי שהלקוח חייב להשתמש בו):
- ספקים חסומים (מי שאי אפשר לעבוד איתו):
- מותג-אב אם זה אירוע תחת מותג קיים:

## 7. היסטוריה
- אירועים קודמים של הלקוח (מה עבד, מה לא):
- מתחרים/Benchmarks שהלקוח מעריך או מפחד מהם:

## 8. חומרים שקיבלנו
- נכסי מותג (לוגו, מדריך מותג, פונטים):
- תמונות מאירועים קודמים:
- מצגות רקע:

## 9. תאריך יעד להצעה
- מתי הלקוח צריך לראות את ההצעה:
- מתי התשובה:
```

---

## Challenge distillation — how to find the real problem

After you have filled the brief, write `01-intake/challenges.md`. This is **not** a repetition of the brief. It is the strategic lens.

### The method

Ask these four questions against the brief and answer each in 2 to 4 sentences, with evidence from the brief:

1. **What tension is this event secretly solving?**
   - Brand vs. category? Internal (employees) vs. external (market)? Generational? Legacy vs. future?
   - Example: a law firm's 40-year anniversary. Stated: "celebrate our history". Real tension: the next generation of partners wants to signal modernity without insulting the founders.

2. **Who is the audience really performing for?**
   - The audience at an event usually plays two roles: the people in the room, and the people they'll show photos to tomorrow. Which audience is this event truly designed for?
   - A VC's portfolio day is officially for LPs in the room; it is really a status signal to future founders watching on Twitter.

3. **What is the one thing that cannot fail?**
   - Identify the single element where failure = the whole event fails. For a product launch, it may be the reveal moment. For a gala, it may be the host speech. For a family event, it may be the food. Everything else is secondary.

4. **What is the client embarrassed to ask for but clearly wants?**
   - The unspoken wish. Often luxury, often status, often "I want it to look like X which I can't afford". Name it.

### Output format

```markdown
# אתגרי מותג ואסטרטגיה — [שם אירוע]

## 1. המתח הסמוי
[2-4 משפטים. איזה מתח אסטרטגי האירוע באמת פותר?]
**ראיות מהבריף:** [ציטוטים או הפניות]

## 2. הקהל האמיתי
בחדר: [תיאור]
מחוץ לחדר (מי רואה את התמונות אחרי): [תיאור]
**העיקר:** [מי מהשניים קובע את העיצוב?]

## 3. הדבר שלא יכול להיכשל
**[אירוע הקריטי]**. אם זה עובד והכל סביב נופל בינוני, ההצעה עדיין הצליחה. אם זה נכשל, שום דבר אחר לא מציל.
**השלכות תקציב:** [איפה להשקיע כבד]

## 4. המשאלה הלא-מדוברת
[השאיפה הלא-מוצהרת של הלקוח]
**איך לענות לה בלי להלבין אותה:** [רעיון או כיוון]

## 5. שלוש שאלות פתוחות לסבב שני עם הלקוח
- [שאלה 1]
- [שאלה 2]
- [שאלה 3]
```

---

## Parsing a Fireflies transcript

When the input is a transcript:

1. **Skim once** for the overall flow. Don't get lost in minute 30 before you know what minute 2 was about.
2. **Extract** all concrete facts into the brief schema. Mark them with the timestamp when possible: `תאריך: 14/06/2026 [12:34]`.
3. **Quote** the exact client language for the mission/mandatory-message fields. Do not paraphrase the client's own words about their goals — those wordings carry information.
4. **Flag** contradictions between speakers on the client side. Two co-founders may disagree about the audience. Surface this explicitly:
   ```
   ⚠ סתירה: יואב אמר "אירוע לעובדים בלבד" [18:22], טל אמרה "אולי נזמין גם לקוחות VIP" [23:05]. נדרש הכרעה.
   ```
5. **Record** what was *not* said. If nobody mentioned budget in a 45-minute call, that is itself information (usually: budget is embarrassingly tight or embarrassingly big).

---

## Parsing a free-form description

When Hemi describes the brief in his own words:

1. Start from what he told you; treat it as the source of truth.
2. Re-read and check against the schema. List the missing fields.
3. Ask **one consolidated question** covering the top 3 missing items. Never pepper him with 8 small questions.
4. If he answers partially, proceed with `חסר` markers on the rest and move to stage 2. Don't stall.

---

## What "good" looks like

A strong stage-1 output reads like a senior strategist prepared it, not a form filler. When Hemi reads `challenges.md`, he should nod and say "yes, that's actually what's going on" — not "I already knew all that". If your challenges.md just restates the brief, you failed the stage.

---

## Common intake traps

- **Accepting "just make it beautiful" as a brief.** That is a symptom of a client who hasn't decided what the event is for. Probe.
- **Over-indexing on the date.** Dates move. Concepts don't.
- **Treating budget as a hard constraint too early.** In stage 1, capture the number but don't let it shape the concept. Stage 5 is where reality bites.
- **Ignoring the room.** A beautiful concept in a fluorescent-lit convention hall dies. Always ask about the physical venue, even if "not yet decided".
