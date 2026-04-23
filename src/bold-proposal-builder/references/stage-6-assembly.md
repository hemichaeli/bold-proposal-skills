# Stage 6, Assembly Reference (v2.2)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds six final deliverables:

1. `proposal.pdf`, the designed client-facing PDF (built via **premium-deck-strategist**, v2.2)
2. `budget.xlsx`, the detailed Excel budget with formulas
3. `gamma-prompt.md`, the ready-to-paste prompt for Gamma.app (interactive version)
4. `summary.md`, a 1-page executive summary for intro messages
5. `kpis-scorecard.md`, a standalone KPI measurement plan
6. Trello debrief card, created in the "Bold, Debriefs" board, due the day after the event

Order: XLSX first (numbers lock), PDF second (via premium-deck-strategist, uses locked numbers), then Gamma prompt, then KPIs scorecard, then summary, then Trello card.

---

## 1. Building the Excel budget (budget.xlsx)

### Inputs
- `05-budget/budget.json` (source of truth)
- Bold brand palette from Stage 3 `brand-system.md` (for XLSX header styling)

### Method

```bash
python3 /home/claude/skills/bold-proposal-builder/scripts/build_budget_xlsx.py \
  --input <path-to-budget.json> \
  --output <path-to-output>/budget.xlsx
```

Three sheets: `סיכום`, `פירוט תקציב`, `שורות מותנות`. Formulas, not hardcoded numbers. RTL for Hebrew.

### Post-build QA
- Total matches summary.total_pre_vat
- Formulas reference correct ranges
- Conditional items on their own sheet

---

## 2. Building the PDF via premium-deck-strategist (v2.2 change)

### Why premium-deck-strategist
Bold's proposals are design-sensitive. Writing raw HTML/CSS or markdown-to-PDF for every proposal produces inconsistent results. `premium-deck-strategist` is a skill designed precisely for premium presentation-style documents, with:

- Slide-by-slide breakdown, not prose blocks
- Rule of Three methodology
- Max 5 words per on-slide bullet (forces concision)
- Visual layout specs per slide
- Speaker notes separated from slide text
- Professional minimalist design language

This matches how Bold proposals should read, short, punchy, designed.

### How to invoke it

At Stage 6, Claude invokes `premium-deck-strategist` with these inputs assembled from prior stages:

```
PREMIUM-DECK-STRATEGIST INVOCATION

Topic: [event name] הצעה, [client name]
Audience: [from brief.md field 6, primary audience]
Goals: [from brief.md field 3, the four-category goal classification]
Length: 15-23 slides (see structure below)

BRAND OVERRIDE (v2.2, critical):
Override premium-deck-strategist's default Deep Blue palette with this event's palette from brand-system.md:
- Primary: [hex from brand-system.md field 4]
- Secondary: [hex]
- Accent: [hex]
- Neutral: [hex]

Typography: Use brand-system.md field 5 (Display + Body fonts).
Language: Hebrew-first, RTL. Numbers Western digits. Dates DD.MM.YYYY.
Voice: Apply voice rules from SKILL.md (no clichés, no em-dashes, specific numbers).

DECK STRUCTURE (required spine):

Slide 1: Cover
  Title: [event name]
  Subtitle: [client name + date]
  Visual: hero mockup from Stage 4a (direction-chosen-hero.png)

Slide 2: About the event
  Three bullets from brief field 1 (reason why)
  Speaker notes: 2-3 sentences from challenges.md strategic reading

Slide 3-4: Strategic reading (challenges.md)
  Slide 3: "מה באמת נמכר כאן" + tensions
  Slide 4: Goals served + risks/opportunities (Rule of Three)

Slide 5-7: The creative concept (brand-system.md)
  Slide 5: Concept name + manifesto
  Slide 6: Three keywords (Rule of Three applied literally)
  Slide 7: Tone + forbidden elements

Slide 8-12: Visualization (mockup set from Stage 4a)
  One slide per mockup, title = moment name, visual = mockup image
  Speaker notes: mood-direction.md excerpts

Slide 13-14: The experience
  Slide 13: Agenda overview (agenda.md)
  Slide 14: Culinary narrative (menu.md top-level)

Slide 15-16: Operations
  Slide 15: Venue + logistics (logistics.md key points)
  Slide 16: Team + timeline

Slide 17-18: Investment
  Slide 17: Total + per-guest breakdown (big numbers)
  Slide 18: What's included vs. conditional

Slide 19: KPIs and success measurement (NEW v2)
  Table from kpis-scorecard.md
  Closing line: "debrief 24 שעות אחרי האירוע"

Slide 20: Timeline
  Milestones from deadline through event day

Slide 21: Next steps
  Three actions (Rule of Three)
  Valid-until date
  Contact: Hemi Michaeli

OPTIONAL:
Slide 22: About Bold (only if client is new)
```

### Output file

premium-deck-strategist produces PPTX or PDF. Bold's proposal needs PDF for client delivery, so:
- If output is PPTX, convert via LibreOffice: `soffice --headless --convert-to pdf proposal.pptx`
- If output is already PDF, save directly

Save to: `06-assembly/proposal.pdf`

### Brand override enforcement

After premium-deck-strategist produces the file, Claude verifies:
- [ ] Primary brand color appears, not Deep Blue
- [ ] Font family matches brand-system.md
- [ ] Hebrew RTL renders correctly
- [ ] No "premium-deck-strategist" or Deep Blue branding visible

If any fail, regenerate with stronger brand override in the prompt.

### Fallback

If premium-deck-strategist is not available (shouldn't happen, it's a user skill), fall back to:
- Proposals ≤ ₪50K: markdown-to-PDF via `pdf` public skill
- Proposals > ₪50K: `canvas-design` cover + markdown body

---

## 3. Building the Gamma prompt (gamma-prompt.md)

Gamma is the interactive companion, separate from the PDF. Same content structure but optimized for web presentation.

The v2 template includes a KPIs slide between Investment and Timeline (slide 13b in Gamma numbering, matching the PDF spine).

See `assets/gamma-prompt-template.md` for the full template. Structure should mirror the 21-slide PDF spine above, since both communicate the same proposal.

---

## 4. Building the KPIs scorecard (kpis-scorecard.md)

Standalone artifact at `06-assembly/kpis-scorecard.md`. Two audiences:
1. The client, for post-event tracking
2. Stage 7, Claude reads this at debrief

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

(One section per KPI)

## פגישת Debrief
- מתי: [date + 1 day]
- משך: 30-45 דקות
- פלט: debrief-[event-slug].md
```

---

## 5. Building the summary (summary.md)

```markdown
[Client first name] שלום,

הנה ההצעה שלנו ל-[Event Name].

**הקונספט בקצרה:** [Concept sentence]

**מה יחוו האורחים:** [3-4 sentences]

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

Use the Trello MCP server. Check for "Bold, Debriefs" board; create if missing with list "ממתין להפקת לקחים".

Card:
```
Title: הפקת לקחים, [Event Name]
Description:
  לקוח: [client]
  תאריך האירוע: [event date]
  תאריך ההפקת לקחים: [event date + 1]
  
  קבצי המקור:
  - הצעה: [link]
  - בריף: [link]
  - KPIs: [link]
  
  ---
  פרומפט מוכן:
  הפק לקחים לאירוע [Event Name] של [Client] שהתקיים ב-[Event Date].
  תעבור איתי מדד-מדד לפי kpis-scorecard.md.

Due date: [event date + 1 day], 10:00
Labels: "Debrief" (yellow), "[client]"
```

Store card URL in summary.md.

Fallback if Trello MCP unavailable: `DEBRIEF-REMINDER.md` file + Gmail reminder day before.

---

## Final QA checklist

- [ ] PDF generated via premium-deck-strategist with event's brand palette, NOT Deep Blue
- [ ] PDF opens correctly on macOS Preview and Adobe Acrobat
- [ ] Hebrew RTL renders correctly
- [ ] 21-slide spine followed (with optional slide 22 for new clients)
- [ ] Excel totals match PDF summary slide
- [ ] Excel has 3 sheets with correct tab names
- [ ] Gamma prompt mirrors the PDF spine
- [ ] KPIs scorecard matches brief.md field 16 exactly
- [ ] KPI slide in PDF matches scorecard
- [ ] Summary.md word count under 250 words
- [ ] Valid-until date consistent everywhere
- [ ] Event name and client name spelled identically across all files
- [ ] Trello card created, URL in summary.md

---

## Present-files call

Final step:

```
present_files([
  "proposals/<slug>/06-assembly/proposal.pdf",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/kpis-scorecard.md",
  "proposals/<slug>/06-assembly/gamma-prompt.md",
  "proposals/<slug>/06-assembly/summary.md"
])
```

Then one-line completion:

```
✓ ההצעה מוכנה. Trello debrief card: [URL]
```
