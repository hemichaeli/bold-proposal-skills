# Stage 6, Assembly Reference (v2)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds six final deliverables:
1. `proposal.pdf`, the designed, client-facing PDF
2. `budget.xlsx`, the detailed Excel budget with formulas
3. `gamma-prompt.md`, the ready-to-paste prompt for Gamma.app
4. `summary.md`, a 1-page executive summary for intro messages
5. `kpis-scorecard.md`, a standalone KPI measurement plan (also embedded in the proposal) (NEW v2)
6. Trello debrief card, created in the "Bold, Debriefs" board, due the day after the event (NEW v2)

Order: XLSX first (the numbers lock), then PDF, then Gamma prompt, then KPIs scorecard, then summary, then Trello card.

---

## 1. Building the Excel budget (budget.xlsx)

### Inputs
- `05-budget/budget.json` (the source of truth)
- Bold brand palette from `brand-system.md` (for XLSX header styling)

### Method
Use the `build_budget_xlsx.py` script in `scripts/`:

```bash
python3 /home/claude/skills/bold-proposal-builder/scripts/build_budget_xlsx.py \
  --input <path-to-budget.json> \
  --output <path-to-output>/budget.xlsx
```

Creates three sheets: `סיכום`, `פירוט תקציב`, `שורות מותנות`. Reads `budget.json` as source of truth. Writes formulas (not hardcoded numbers). Applies brand palette. Sets RTL for Hebrew.

---

## 2. Building the PDF (proposal.pdf)

### Structure (v2, includes KPI page)

```
Cover (1 page)
About the event (1 page)
Strategic reading (1-2 pages)
The creative concept (2-3 pages)
Visualization (3-5 pages)
The experience (2-3 pages)
Operations (1-2 pages)
Investment (2-3 pages)
KPIs and success measurement (1 page) (NEW v2)
Timeline (1 page)
About Bold (1 page, optional)
Next steps (1 page)
```

Total: 15 to 23 pages. The new KPI page sits between Investment and Timeline.

### The KPIs page (NEW v2)

A single page titled "איך נמדוד הצלחה". Shows the KPIs from Stage 1 field 16 in a structured table:

| מטרה | מדד | יעד | מתי נמדוד | מקור נתונים |
|---|---|---|---|---|
| שיווקית | אזכורים בתקשורת | 8 אזכורים | 7 ימים אחרי | סריקה ידנית |
| מכירתית | לידים איכותיים | 25 | 72 שעות אחרי | Zoho CRM |

Below the table, one short paragraph:

> "לאחר האירוע, 24 שעות לאחר קיומו, נבצע סיכום משותף מול המדדים לעיל. תקבל דוח מסודר עם המספרים, ופגישה של 30 דקות לסיכום הלקחים אם תבקש."

---

## 3. Building the Gamma prompt (gamma-prompt.md)

The v2 template includes a new slide between Investment and Timeline:

```
### Slide 13b, KPIs (NEW v2)
Title: "איך נמדוד הצלחה"
Body: Table from the KPIs scorecard.
Closing line: "נבצע debrief 24 שעות אחרי האירוע."
```

See `assets/gamma-prompt-template.md` for the full template.

---

## 4. Building the KPIs scorecard (kpis-scorecard.md) (NEW v2)

A standalone artifact in `06-assembly/kpis-scorecard.md` serving two audiences:
1. The client, receives a copy, uses it to track measurement post-event.
2. Stage 7, Claude reads this file directly when the debrief chat opens.

### Template

```markdown
# Scorecard, [Event Name]
**לקוח:** [name]
**תאריך האירוע:** [date]
**תאריך הפקת לקחים:** [date + 1 day]

## מטרות האירוע
[List the goals from brief field 3, classified by category]

## KPIs

### KPI 1: [metric name]
- קטגוריה: שיווקית / Fun / מכירתית / תדמיתית
- מדד: [what is being counted]
- Baseline: [pre-event number]
- יעד: [target]
- חלון מדידה: [when]
- מקור נתונים: [how]
- אחראי לאיסוף: [name]

(One section per KPI)

## פגישת Debrief
- מתי: [date + 1 day]
- משך: 30-45 דקות
- פלט: debrief-[event-slug].md
```

---

## 5. Building the summary (summary.md)

### Template (v2, includes KPI callout)

```markdown
[Client first name] שלום,

הנה ההצעה שלנו ל-[Event Name].

**הקונספט בקצרה:**
[Concept sentence]

**מה יחוו האורחים:**
[3-4 sentences]

**מספרים מרכזיים:**
- מוזמנים: [X]
- תאריך מוצע: [Y]
- השקעה: ₪[Z] + מע"מ | שורות מותנות בנפרד
- תוקף ההצעה: עד [YYYY-MM-DD]

**איך נמדוד הצלחה:** (NEW v2)
הגדרנו [N] מדדי הצלחה בהתאם למטרות שהעלית. פירוט ב-kpis-scorecard.md המצורף.
24 שעות אחרי האירוע, נעשה debrief מסודר ותקבל דוח מול המדדים.

**מצורפים:**
- הצעה מעוצבת מלאה (PDF)
- תקציב מפורט (Excel)
- KPIs scorecard (Markdown)
- מצגת אינטראקטיבית (Gamma, קישור יישלח)
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

---

## 6. Creating the Trello debrief card (NEW v2)

The final automated action of Stage 6. Creates a reminder that becomes the entry point for Stage 7.

### Method

Use the Trello MCP server. Check for a board called "Bold, Debriefs". If it doesn't exist, create it with a single list "ממתין להפקת לקחים".

Card creation:

```
Board: Bold, Debriefs
List: ממתין להפקת לקחים
Title: הפקת לקחים, [Event Name]
Description:
  לקוח: [client]
  תאריך האירוע: [event date]
  תאריך ההפקת לקחים: [event date + 1]
  
  קבצי המקור:
  - הצעה: [link]
  - בריף: [link to brief.md]
  - KPIs: [link to kpis-scorecard.md]
  
  ---
  פרומפט מוכן להדבקה בשיחה חדשה של Claude:
  
  הפק לקחים לאירוע [Event Name] של [Client] שהתקיים ב-[Event Date].
  תעבור איתי מדד-מדד לפי מה שמופיע ב-kpis-scorecard.md.

Due date: [event date + 1 day], 10:00
Labels: "Debrief" (yellow), "[client]" (custom color)
```

After creating the card, store the card URL in the proposal's summary.md.

### If Trello MCP is unavailable

Write a plain markdown reminder file `DEBRIEF-REMINDER.md` in the proposal folder. Email Hemi via Gmail MCP the day before: "תזכורת: Debrief של [Event] מחר ב-10:00".

---

## Final QA checklist

- [ ] PDF opens and renders correctly on macOS Preview and Adobe Acrobat
- [ ] PDF fonts embedded
- [ ] Excel totals match PDF summary table
- [ ] Excel has 3 sheets with correct tab names
- [ ] Gamma prompt has all ATTACH markers pointing to existing files
- [ ] KPIs scorecard matches brief.md field 16 exactly (NEW v2)
- [ ] KPI page in PDF matches scorecard (NEW v2)
- [ ] Summary.md word count under 250 words
- [ ] Valid-until date consistent across all files
- [ ] Event name spelled identically
- [ ] Client name spelled identically
- [ ] Contact info correct
- [ ] Trello card created and URL captured in summary.md (NEW v2)

---

## Present-files call

At the end, call `present_files` with these five, in this order:

```
[
  "proposals/<slug>/06-assembly/proposal.pdf",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/kpis-scorecard.md",
  "proposals/<slug>/06-assembly/gamma-prompt.md",
  "proposals/<slug>/06-assembly/summary.md"
]
```

Then output one-line completion marker including Trello card URL and stop:

```
✓ ההצעה מוכנה. Trello debrief card: [URL]
```
