# Stage 6, Assembly Reference (v2.2)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds six final deliverables:
1. `proposal.pdf`, the designed, client-facing PDF (v2.2: built via **premium-deck-strategist** skill)
2. `budget.xlsx`, the detailed Excel budget with formulas
3. `gamma-prompt.md`, the ready-to-paste prompt for Gamma.app
4. `summary.md`, a 1-page executive summary for intro messages
5. `kpis-scorecard.md`, a standalone KPI measurement plan (also embedded in the proposal)
6. Trello debrief card, created in the "Bold, Debriefs" board, due the day after the event

Order: XLSX first (the numbers lock), then PDF (via premium-deck-strategist), then Gamma prompt, then KPIs scorecard, then summary, then Trello card.

---

## 1. Building the Excel budget (budget.xlsx)

### Inputs
- `05-budget/budget.json` (the source of truth)
- Bold brand palette from `brand-system.md`

### Method
Use `build_budget_xlsx.py` in `scripts/`:

```bash
python3 /home/claude/skills/bold-proposal-builder/scripts/build_budget_xlsx.py \
  --input <path-to-budget.json> \
  --output <path-to-output>/budget.xlsx
```

Creates three sheets: `סיכום`, `פירוט תקציב`, `שורות מותנות`. Writes formulas (not hardcoded numbers). Applies brand palette. Sets RTL for Hebrew.

### Post-build QA
- Verify total matches summary.total_pre_vat.
- Check formulas sum the right ranges.
- Verify conditional items are on their own sheet.

---

## 2. Building the PDF (proposal.pdf) via premium-deck-strategist (NEW v2.2)

### Why premium-deck-strategist
Bold's proposal PDFs need to feel like a designed deck, not a Word document exported to PDF. The `premium-deck-strategist` skill produces:
- Minimalist Deep Blue design language (overridden with Bold's palette from brand-system.md)
- Rule of Three methodology (three ideas per slide maximum)
- Max 5 words per on-slide bullet
- Speaker notes per slide for internal reference and Gamma conversion
- Structured slide-by-slide output (not free-form prose)

This gives Stage 6 a consistent visual grammar across every proposal.

### How to invoke premium-deck-strategist

Claude calls the skill with a structured prompt built from Stage 1-5 artifacts. The call happens AFTER budget.json is finalized (Stage 5) and AFTER brand-system.md + mood-direction.md are complete (Stage 3 + 4a).

**The prompt Claude constructs for premium-deck-strategist:**

```
בנה לי premium deck להצעת אירוע של Bold Productions ללקוח [Client Name].

הקונטקסט:
- שם האירוע: [Event Name]
- תאריך: [Date]
- כמות אורחים: [N]
- השקעה: ₪[Subtotal] + מע"מ
- תוקף ההצעה: עד [Valid Until]

עקרונות סגנון:
- Hebrew RTL throughout
- Deep Blue language, OVERRIDE palette with Bold's brand-system palette:
  - Primary: [hex from brand-system.md field 4]
  - Secondary: [hex]
  - Accent: [hex]
  - Neutral: [hex]
- Typography: [Display + Body from brand-system.md field 5]
- No Bold logos or credits
- No em-dashes or en-dashes
- Rule of Three per slide

מבנה הדק (15-23 slides, סדר קשיח):

1. Cover
   - Client name, event name, date
   - Hero mockup from 04-specialists/visual/mockups/02-hero.png as background

2. About the event
   - Event type, reason-why (from brief field 1)
   - 3 keywords from brand-system.md

3-4. Strategic reading
   - From 01-intake/challenges.md
   - "מה באמת נמכר כאן" + "המתחים" + "המטרות והמשמעויות"

5-7. The creative concept
   - Concept name from brand-system.md
   - Manifesto sentence
   - 3 keywords with visual anchor per keyword

8-12. Visualization
   - One slide per mockup from 04-specialists/visual/mockups/
   - Mockup image full-bleed, one caption per slide

13. The experience
   - Agenda summary from 04b/agenda.md
   - Key beats, timing

14. Operations
   - From 04c/logistics.md
   - Venue, flow, key vendors

15-17. Investment
   - Summary table from budget.json (categories + subtotals)
   - Conditional items separate slide
   - Total pre-VAT, VAT, total

18. KPIs and success measurement (NEW)
   - Table: goal, metric, target, measurement window, data source
   - Closing line: "debrief 24 שעות אחרי האירוע"

19. Timeline
   - From brief field 15 (deadline) + operations
   - Milestones from now to event day

20. About Bold (optional, skip if already known to client)
   - 2-3 past events relevant to this brief

21. Next steps
   - Decision required by [date]
   - Contact details

עבור כל slide:
- Max 5 words per bullet
- Max 3 bullets per slide
- Speaker notes: 2-4 sentences explaining WHY this slide, not just WHAT

פלטים רצויים:
- מבנה slide-by-slide מלא עם title, bullets, notes
- הפניות לתמונות שיוטמעו
- visual layout spec לכל slide (left-image-right-text / full-bleed / centered)

סיים בטבלה מסכמת: slide number, title, visual layout, key bullets, speaker notes length.
```

### After premium-deck-strategist returns

Claude gets back a structured deck specification. Claude then converts it to PDF using one of two paths:

**Path A (default, below ₪50K proposals):** Convert the premium-deck-strategist output to Markdown + CSS, then render with `pdf` public skill. Brand palette in CSS variables.

**Path B (above ₪50K proposals or when extra polish is needed):** Use `canvas-design` skill for the cover and section transitions, then assemble the slide bodies as Markdown-to-PDF. This gives an editorial-feel opener.

**Both paths import the mockup images** from `04-specialists/visual/mockups/` and place them per the layout spec from premium-deck-strategist.

### The KPIs page (NEW v2)

A single page titled "איך נמדוד הצלחה". Premium-deck-strategist builds this as slide 18 from the kpis-scorecard.md data. Structured table:

| מטרה | מדד | יעד | מתי נמדוד | מקור נתונים |
|---|---|---|---|---|

Closing line below table:
> "לאחר האירוע, 24 שעות לאחר קיומו, נבצע סיכום משותף מול המדדים לעיל. תקבל דוח מסודר עם המספרים."

---

## 3. Building the Gamma prompt (gamma-prompt.md)

The Gamma prompt MIRRORS the premium-deck-strategist structure 1:1, so the Gamma version and the PDF version are visually consistent.

Claude writes the Gamma prompt by taking the premium-deck-strategist slide-by-slide spec and reformatting it into Gamma's input format:

```
Slide 1: Cover
  Title: [Event Name]
  Subtitle: [Client Name], [Date]
  Layout: hero image full bleed, title bottom-left
  Background: ATTACH [path to hero mockup]

Slide 2: About the event
  ...
```

See `assets/gamma-prompt-template.md` for the full scaffolding.

---

## 4. Building the KPIs scorecard (kpis-scorecard.md)

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
[Goals from brief field 3, classified by category]

## KPIs
### KPI 1: [metric name]
- קטגוריה: שיווקית / Fun / מכירתית / תדמיתית
- מדד: [what is being counted]
- Baseline: [pre-event number]
- יעד: [target]
- חלון מדידה: [when]
- מקור נתונים: [how]
- אחראי לאיסוף: [name]

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
[Concept sentence from brand-system.md manifesto]

**מה יחוו האורחים:**
[3-4 sentences]

**מספרים מרכזיים:**
- מוזמנים: [X]
- תאריך מוצע: [Y]
- השקעה: ₪[Z] + מע"מ | שורות מותנות בנפרד
- תוקף ההצעה: עד [YYYY-MM-DD]

**איך נמדוד הצלחה:**
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

## 6. Creating the Trello debrief card

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

### If Trello MCP is unavailable
Write `DEBRIEF-REMINDER.md` in the proposal folder. Email Hemi via Gmail MCP the day before: "תזכורת: Debrief של [Event] מחר ב-10:00".

---

## Dependencies required for Stage 6 (v2.2)

| Dependency | Purpose | Fallback if missing |
|---|---|---|
| premium-deck-strategist skill | PDF slide structure | Use markdown + pdf skill with generic structure (lower polish) |
| pdf skill (public) | Rendering markdown to PDF | None, PDF cannot be produced |
| canvas-design skill (public) | Cover + section transitions (Path B only) | Path A only |
| Trello MCP server | Debrief card creation | DEBRIEF-REMINDER.md + Gmail reminder |

If premium-deck-strategist is not installed, Claude warns Hemi and asks whether to proceed with the fallback path (generic markdown-to-PDF with brand colors but no Rule of Three or Deep Blue methodology).

---

## Final QA checklist

- [ ] PDF opens and renders correctly on macOS Preview and Adobe Acrobat
- [ ] PDF fonts embedded
- [ ] Deck follows Rule of Three (max 3 bullets per slide)
- [ ] Max 5 words per bullet
- [ ] Bold palette applied (not Deep Blue default)
- [ ] Excel totals match PDF summary table
- [ ] Excel has 3 sheets with correct tab names
- [ ] Gamma prompt structure mirrors PDF 1:1
- [ ] KPIs scorecard matches brief.md field 16 exactly
- [ ] KPI slide in PDF matches scorecard
- [ ] Summary.md word count under 250 words
- [ ] Valid-until date consistent across all files
- [ ] Event name spelled identically
- [ ] Client name spelled identically
- [ ] Contact info correct
- [ ] Trello card created and URL captured in summary.md

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

Then output the one-line completion marker including the Trello card URL and stop:

```
✓ ההצעה מוכנה. Trello debrief card: [URL]
```
