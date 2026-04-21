# Stage 6 — Assembly Reference

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds the four final deliverables:
1. `proposal.pdf` the designed, client-facing PDF
2. `budget.xlsx` the detailed Excel budget with formulas
3. `gamma-prompt.md` the ready-to-paste prompt for Gamma.app
4. `summary.md` a 1-page executive summary for intro messages

Order matters: XLSX first (the numbers lock), then PDF (tells the story with numbers confirmed), then Gamma prompt (digital companion), then summary.

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

The script:
- Reads `budget.json`.
- Creates three sheets: `סיכום`, `פירוט תקציב`, `שורות מותנות`.
- Populates the detail sheet with all non-conditional items, grouped by category with subtotal rows.
- Populates the conditional sheet separately.
- Writes formulas (not hardcoded numbers) for subtotal, contingency, margin, VAT, and totals.
- Applies the brand palette to headers.
- Adds a "Valid until" note from `meta.valid_until`.
- Sets RTL for Hebrew content.

### If the script is unavailable
Fall back to the `xlsx` public skill. Open `/mnt/skills/public/xlsx/SKILL.md` and follow its guidance. The structure (3 sheets, categories with subtotals, formulas, RTL) stays the same.

### Post-build QA
- Open the xlsx and verify the total matches `summary.total_pre_vat` implied by the JSON.
- Check formulas: click a total cell and verify it sums the right range, not a hardcoded number.
- Verify conditional items are on their own sheet and do NOT appear in the main subtotal.

---

## 2. Building the PDF (`proposal.pdf`)

### Structure

A Bold proposal PDF follows this spine. Adjust depth per event; never change the order.

```
Cover (1 page)
  - Event name, client name, date, Bold logo, tagline
  - Visual: hero mockup from 4a OR canvas-design artwork tied to brand-system

About the event (1 page)
  - The concept in one sentence
  - 3-4 sentences of context ("the moment this event arrives in")

Strategic reading (1-2 pages)
  - The 1-2 key insights from challenges.md (rewritten for client eyes, not raw)
  - Why this direction now

The creative concept (2-3 pages)
  - Name, tagline, visual treatment
  - Color palette strip
  - Typography sample
  - Motif explanation with visual

Visualization (3-5 pages)
  - Mockup images, each on its own page or two per page
  - Brief captions tying each to a brand-system element
  - Atmosphere video QR code / link

The experience (2-3 pages)
  - Agenda block view (not minute-by-minute, that's internal)
  - Signature moments described in 1-2 sentences each
  - Culinary paragraph

Operations (1-2 pages)
  - Site plan description
  - Technical infrastructure summary
  - What makes this event safe, accessible, smooth

Investment (2-3 pages)
  - Budget summary table (categories + totals, not every line)
  - Conditional items clearly separated
  - Payment terms
  - Note: "Detailed budget in accompanying Excel file"

Timeline (1 page)
  - From today to event day: key milestones
  - Decision dates for the client
  - Production milestones

About Bold (1 page, optional)
  - Include only if new relationship. Existing clients skip.

Next steps (1 page)
  - Proposed decision points
  - Who owns what
  - Contact + signature block
```

Total: 14 to 22 pages. Shorter than that, the client feels underserved. Longer than that, they stop reading.

### Method

Two paths, depending on complexity:

**Path A: Markdown → PDF via `pdf` public skill**
For proposals where the visuals are simple and the client is technical / efficient.

1. Write all the page content in markdown in `06-assembly/proposal.md`.
2. Use the `pdf` skill (read `/mnt/skills/public/pdf/SKILL.md`) to convert with custom CSS styled to the brand palette.

**Path B: `canvas-design` cover + markdown body, assembled**
For proposals where design quality is the selling point.

1. Use `canvas-design` to create the cover page as a standalone PNG or PDF, using the brand system.
2. Generate the body pages from markdown as in Path A.
3. Stitch: insert the cover as page 1, the body follows.

For this stage, **default to Path B for all Bold proposals above ₪50,000.** Bold's identity is premium; a markdown-rendered PDF cover cheapens it. Below ₪50,000 (small events, quick turnarounds), Path A is acceptable.

### Typography and palette
- Use the exact fonts from `brand-system.md`.
- Headers in the primary color, body in the neutral dark.
- White space is not empty; it's breathing room. Do not fill.

### Images
- Every mockup at its native resolution, not stretched.
- Captions under, not over.
- Atmosphere video: embed a frame + QR code + link. PDFs with embedded video are unreliable across readers.

### Cover page
The cover is a single visual statement. It carries:
- Event name (large, display font)
- Tagline (smaller, under name)
- Client name + date (small, lower third)
- Bold logo (small, lower corner or footer)

No "הצעת מחיר" label on the cover. That's obvious and diminishes.

### Back / last page
End with a quiet page. The contact, signature lines, next steps. Do not end with a "thank you" exclamation. The last impression is calm confidence, not gratitude.

---

## 3. Building the Gamma prompt (`gamma-prompt.md`)

### Why a prompt, not a call

Gamma.app does not have a public API at the time of writing (verified periodically; if this changes, update this section). Bold's Gamma presentations are created by pasting a well-structured prompt into Gamma's generate interface. This stage produces that prompt.

### Template structure

See `assets/gamma-prompt-template.md` for the full template with all placeholder fields. In summary, the prompt always contains:
- Context paragraph from challenges.md
- Creative direction (concept, name, tagline)
- Visual style block (palette hex, typography feel, mood keywords)
- 15 slide specifications with ATTACH markers for mockups and video
- Budget summary for the Investment slide

The prompt is long. That is the point. Gamma produces much better output when given structure instead of "make me a beautiful deck about X". Treat the prompt as a spec, not a nudge.

---

## 4. Building the summary (`summary.md`)

A one-page executive summary that Hemi pastes into WhatsApp or an email to introduce the proposal. The full proposal is attached; this is the hook.

### Template

```markdown
[Client first name] שלום,

הנה ההצעה שלנו ל-[Event Name].

**הקונספט בקצרה:**
[Concept sentence from brand-system.md]

**מה יחוו האורחים:**
[3-4 sentences pulling from agenda block view and culinary narrative. No buzzwords.]

**מספרים מרכזיים:**
- מוזמנים: [X]
- תאריך מוצע: [Y]
- השקעה: ₪[Z] + מע"מ | שורות מותנות בנפרד
- תוקף ההצעה: עד [YYYY-MM-DD]

**מצורפים:**
- הצעה מעוצבת מלאה (PDF)
- תקציב מפורט (Excel)
- מצגת אינטראקטיבית (Gamma, קישור יישלח)
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

Short. Direct. Specific. No salesmanship.

---

## Final QA checklist before delivery

Before calling `present_files` on the four outputs:

- [ ] PDF opens and renders correctly on both macOS Preview and Adobe Acrobat (Hebrew RTL often breaks in one or the other)
- [ ] PDF fonts are embedded (not missing)
- [ ] Excel totals match the PDF's summary table
- [ ] Excel has 3 sheets with correct tab names
- [ ] Gamma prompt has all ATTACH markers pointing to files that actually exist
- [ ] Summary.md word count is under 200 words
- [ ] Valid-until date is in the future and matches across PDF, Excel, summary
- [ ] Event name is spelled identically across all four files (common bug: typo in one)
- [ ] Client name is spelled identically
- [ ] Contact info is correct

---

## Present-files call

At the end, call `present_files` with exactly these four, in this order:

```
[
  "proposals/<slug>/06-assembly/proposal.pdf",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/gamma-prompt.md",
  "proposals/<slug>/06-assembly/summary.md"
]
```

Then output the one-line completion marker and stop. Don't narrate what was produced; the files speak.
