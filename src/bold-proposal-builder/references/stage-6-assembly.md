# Stage 6 — Assembly Reference (v2)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds the six final deliverables:
1. `proposal.pdf`, the designed, client-facing PDF
2. `budget.xlsx`, the detailed Excel budget with formulas
3. `gamma-prompt.md`, the ready-to-paste prompt for Gamma.app
4. `summary.md`, a 1-page executive summary for intro messages
5. **`kpis-scorecard.md`**, a standalone KPI measurement plan (also embedded in the proposal) (NEW v2)
6. **Trello debrief card**, created in the "Bold, Debriefs" board, due the day after the event (NEW v2)

Order matters: XLSX first (the numbers lock), then PDF (tells the story with numbers confirmed), then Gamma prompt (digital companion), then KPIs scorecard, then summary, then Trello card.

---

## 1. Building the Excel budget (`budget.xlsx`)

### Inputs
- `05-budget/budget.json` (the source of truth)
- Bold brand palette from `brand-system.md` (for XLSX header styling)

### Method
Use the `build_budget_xlsx.py` script in `scripts/`. Command:

```bash
cd /home/claude
python3 /home/claude/skills/bold-proposal-builder/scripts/build_budget_xlsx.py \
  --input <path-to-budget.json> \
  --output <path-to-output>/budget.xlsx
```

The script creates three sheets: `סיכום`, `פירוט תקציב`, `שורות מותנות`. Reads `budget.json` as source of truth. Writes formulas (not hardcoded numbers). Applies brand palette. Sets RTL for Hebrew.

### If the script is unavailable
Fall back to the `xlsx` public skill. Open `/mnt/skills/public/xlsx/SKILL.md` and follow its guidance. The structure (3 sheets, categories with subtotals, formulas, RTL) stays the same.

### Post-build QA
- Open the xlsx and verify the total matches `summary.total_pre_vat` implied by the JSON.
- Check formulas: click a total cell and verify it sums the right range, not a hardcoded number.
- Verify conditional items are on their own sheet and do NOT appear in the main subtotal.

---

## 2. Building the PDF (`proposal.pdf`)

### Structure (v2, includes KPI page)

A Bold proposal PDF follows this spine. Adjust depth per event; never change the order.

```
Cover (1 page)
About the event (1 page)
Strategic reading (1-2 pages)
The creative concept (2-3 pages)
Visualization (3-5 pages)
The experience (2-3 pages)
Operations (1-2 pages)
Investment (2-3 pages)
**KPIs and success measurement (1 page)** (NEW v2)
Timeline (1 page)
About Bold (1 page, optional)
Next steps (1 page)
```

Total: 15 to 23 pages. The new KPI page sits between Investment and Timeline because the client is most receptive to "how we measure success" right after they see the price; it answers the unspoken "what do I get for this".

### The KPIs page (NEW v2)

A single page titled "איך נמדוד הצלחה". Shows the KPIs from Stage 1 field 16 in a structured table. Format:

| מטרה | מדד | יעד | מתי נמדוד | מקור נתונים |
|---|---|---|---|---|
| שיווקית | אזכורים בתקשורת טק ישראלית | 8 אזכורים | 7 ימים אחרי | סריקה ידנית: Globes, Calcalist, TheMarker, Geektime |
| מכירתית | לידים איכותיים ל-CRM | 25 | 72 שעות אחרי | Zoho CRM, source tag "Launch 2026" |
| תדמיתית | יחס סנטימנט בסיקור | 80% חיובי/ניטרלי | 14 ימים אחרי | סקירה ידנית + כלי האזנה אם זמין |

Below the table, one short paragraph:

> "לאחר האירוע, 24 שעות לאחר קיומו, נבצע סיכום משותף מול המדדים לעיל. תקבל דוח מסודר עם המספרים, ופגישה של 30 דקות לסיכום הלקחים אם תבקש."

This signals commitment and sets up Stage 7 naturally.

### Rest of PDF structure

[Unchanged from v1 spec. See existing stage-6-assembly.md for full page specs.]

### Method

Two paths:
- **Path A:** Markdown → PDF via `pdf` public skill, with custom CSS matching brand palette. For proposals ₪50K or below.
- **Path B:** `canvas-design` cover + markdown body, assembled. Default for proposals above ₪50K.

---

## 3. Building the Gamma prompt (`gamma-prompt.md`)

Gamma.app does not have a public API at the time of writing. Bold's Gamma presentations are created by pasting a well-structured prompt into Gamma's generate interface.

The v2 prompt template includes a new slide between Investment and Timeline:

```
### Slide 13b — KPIs (NEW v2)
Title: "איך נמדוד הצלחה"
Body: Table from the KPIs scorecard.
Closing line: "נבצע debrief 24 שעות אחרי האירוע."
```

See `assets/gamma-prompt-template.md` for the full template.

---

## 4. Building the KPIs scorecard (`kpis-scorecard.md`) (NEW v2)

This is a standalone artifact, separate from the PDF. It lives in `06-assembly/kpis-scorecard.md` and serves two audiences:

1. **The client**, receives a copy, uses it to track measurement post-event.
2. **Stage 7**, Claude reads this file directly when the debrief chat opens.

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
- **קטגוריה:** שיווקית / Fun / מכירתית / תדמיתית
- **מדד:** [what is being counted]
- **Baseline:** [pre-event number, if known]
- **יעד:** [target number or %]
- **חלון מדידה:** [e.g., 72 hours post-event]
- **מקור נתונים:** [how we'll get the number]
- **אחראי לאיסוף:** [name]

### KPI 2: ...

(One section per KPI)

## פגישת Debrief
- **מתי:** [date + 1 day, time TBD]
- **משך:** 30-45 דקות
- **משתתפים מצד Bold:** Hemi Michaeli
- **משתתפים מצד הלקוח:** [TBD]
- **פלט:** `debrief-[event-slug].md` (יישלח תוך 48 שעות מהפגישה)
```

---

## 5. Building the summary (`summary.md`)

A one-page executive summary Hemi pastes into WhatsApp or email to introduce the proposal.

### Template (v2, includes KPI callout)

```markdown
[Client first name] שלום,

הנה ההצעה שלנו ל-[Event Name].

**הקונספט בקצרה:**
[Concept sentence from brand-system.md]

**מה יחוו האורחים:**
[3-4 sentences pulling from agenda block view and culinary narrative.]

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
- מצגת אינטראקטיבית (Gamma - קישור יישלח)
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
  - הצעה: [link to PDF in Drive or GitHub]
  - בריף: [link to brief.md]
  - KPIs: [link to kpis-scorecard.md]
  - debrief folder: [link to 06-assembly/]
  
  ---
  פרומפט מוכן להדבקה בשיחה חדשה של Claude:
  
  הפק לקחים לאירוע [Event Name] של [Client] שהתקיים ב-[Event Date].
  הבריף וה-KPIs נמצאים ב-GitHub: hemichaeli/bold-proposal-skills 
  או ב-Drive.
  תעבור איתי מדד-מדד לפי מה שמופיע ב-kpis-scorecard.md.

Due date: [event date + 1 day], 10:00
Labels: "Debrief" (yellow), "[client]" (custom color)
```

After creating the card, store the card URL in the proposal's summary.md so Hemi has one place to find everything.

### If Trello MCP is unavailable

Write a plain markdown reminder file `DEBRIEF-REMINDER.md` in the proposal folder. Email Hemi (Gmail MCP) the day before the event with: "תזכורת: Debrief של [Event] מחר ב-10:00". Same effect, different channel.

---

## Final QA checklist before delivery

Before calling `present_files` on the final deliverables:

- [ ] PDF opens and renders correctly on both macOS Preview and Adobe Acrobat (Hebrew RTL often breaks in one or the other)
- [ ] PDF fonts are embedded (not missing)
- [ ] Excel totals match the PDF's summary table
- [ ] Excel has 3 sheets with correct tab names
- [ ] Gamma prompt has all ATTACH markers pointing to files that actually exist
- [ ] **KPIs scorecard matches brief.md field 16 exactly** (NEW v2)
- [ ] **KPI page in PDF matches scorecard** (NEW v2)
- [ ] Summary.md word count is under 250 words (slightly up from v1 due to KPI mention)
- [ ] Valid-until date is in the future and matches across PDF, Excel, summary, scorecard
- [ ] Event name spelled identically across all files
- [ ] Client name spelled identically
- [ ] Contact info correct
- [ ] **Trello card created and URL captured in summary.md** (NEW v2)

---

## Present-files call

At the end, call `present_files` with exactly these five, in this order:

```
[
  "proposals/<slug>/06-assembly/proposal.pdf",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/kpis-scorecard.md",
  "proposals/<slug>/06-assembly/gamma-prompt.md",
  "proposals/<slug>/06-assembly/summary.md"
]
```

Then output the one-line completion marker including the Trello card URL and stop. Don't narrate what was produced; the files speak.

Example completion marker:
```
✓ ההצעה מוכנה. Trello debrief card: [URL]
```
