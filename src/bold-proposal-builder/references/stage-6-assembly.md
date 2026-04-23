# Stage 6, Assembly Reference (v2.3)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds six final deliverables:

1. `proposal.pdf`, exported from Gamma after the Gamma deck is built and reviewed
2. `budget.xlsx`, the detailed Excel budget with formulas
3. Gamma deck URL (live, interactive, shareable)
4. `summary.md`, a 1-page executive summary for intro messages
5. `kpis-scorecard.md`, a standalone KPI measurement plan
6. Trello debrief card, due the day after the event

**Key change in v2.3:** The designed proposal PDF comes from Gamma's PDF export, not from a hand-built PDF. Gamma is the single source of truth for the designed deck. This gives Bold and the client both: a live interactive link AND a PDF attachment, both visually identical.

---

## Pipeline order (v2.3)

```
Stage 5 budget.json finalized
          ↓
Build XLSX budget (local)
          ↓
Call premium-deck-strategist with all Stage 1-5 artifacts
          ↓ (returns structured slide-by-slide spec)
Convert spec to Gamma prompt
          ↓
Create Gamma deck via Canva MCP or Gamma MCP (read-only) / manual paste
          ↓ (Hemi reviews deck in Gamma, optionally tweaks)
Export deck from Gamma to PDF
          ↓
Attach exported PDF to Bold's outputs
          ↓
Build summary.md with Gamma link + PDF attached
          ↓
Build kpis-scorecard.md
          ↓
Create Trello debrief card
          ↓
Present files to Hemi
```

---

## 1. Building the Excel budget (budget.xlsx)

Unchanged from v2.2. See:

```bash
python3 scripts/build_budget_xlsx.py --input 05-budget/budget.json --output 06-assembly/budget.xlsx
```

Three sheets: `סיכום`, `פירוט תקציב`, `שורות מותנות`. Formulas, not hardcoded. Bold palette. RTL.

---

## 2. Calling premium-deck-strategist to design the deck structure

`premium-deck-strategist` produces the slide-by-slide spec. It does NOT create the PDF itself; it produces a structured specification that Claude then converts to a Gamma prompt.

### The prompt Claude constructs for premium-deck-strategist

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

מבנה הדק (18-21 slides, סדר קשיח):

1. Cover (client name, event name, date, hero mockup as background)
2. About the event (type, reason-why, 3 keywords)
3-4. Strategic reading (from challenges.md)
5-7. The creative concept (name, manifesto, 3 keywords with anchors)
8-12. Visualization (one mockup per slide, full-bleed)
13. The experience (agenda highlights)
14. Operations (venue, flow, key vendors)
15-17. Investment (category table, conditional items, total)
18. KPIs and success measurement
19. Timeline (milestones now to event day)
20. About Bold (optional)
21. Next steps (decision date, contact)

עבור כל slide:
- Max 5 words per bullet
- Max 3 bullets per slide
- Speaker notes: 2-4 sentences

פלט רצוי: structured output, לכל slide:
- Slide number and title
- Layout type (full-bleed image, left-image-right-text, centered title, table)
- On-slide text (title + bullets, max 5 words each)
- Speaker notes
- Image reference (path to mockup if applicable)
- Specific color/typography notes if non-default
```

### After premium-deck-strategist returns

Claude saves the spec to `06-assembly/deck-spec.md` as an internal artifact (not shared with client). This is the source of truth for the Gamma prompt.

---

## 3. Creating the Gamma deck

Gamma's web interface is the target. Two paths:

### Path A (default): automated via Canva MCP
If the Canva MCP supports Gamma-like structured deck creation, use `Canva:request-outline-review` to preview the outline, then `Canva:generate-design-structured` with design_type="presentation". This gives an editable presentation that Hemi can refine before exporting.

NOTE: Canva is not Gamma. If Hemi specifically requires Gamma (for the card-based layout, interactive embeds, or responsive web view), use Path B.

### Path B (preferred when Gamma is required): structured prompt for manual paste
Claude converts the deck spec into a Gamma-formatted prompt and saves it to `06-assembly/gamma-prompt.md`. Hemi opens Gamma, starts a new presentation, pastes the prompt, and Gamma generates the deck.

The gamma-prompt.md format:

```
Create a 21-card presentation in Hebrew (RTL) for Bold Productions event proposal.

Theme settings:
- Primary color: [hex]
- Accent: [hex]
- Font: [display font], [body font]
- Layout mode: Presentation (not document)

Card 1: Cover
- Title: [Event Name]
- Subtitle: [Client Name] | [Date]
- Background image: [path/URL to hero mockup]
- Layout: full-bleed image with title bottom-left

Card 2: About the event
- Title: [reason-why one-liner]
- 3 bullets: [keyword 1], [keyword 2], [keyword 3]
- Layout: centered title, bullets below

Card 3-4: Strategic reading
...

[continues for all 21 cards, each with layout spec, title, bullets, image references]

Export as PDF when done. Use Share > Export > PDF.
```

### Page setup for PDF export
Before exporting, Gamma's page setup must be configured. Set Format > Document > Letter (8.5x11) and enable "Scale content to fit" to avoid cards getting cut off on export. Alternatively use Presentation format (16:9) for a landscape PDF that matches the slide feel.

---

## 4. Exporting Gamma to PDF

Hemi does this step directly in Gamma:
1. Open the generated deck in Gamma
2. Click Share in the top-right
3. Click Export
4. Choose PDF
5. Download the file

Claude instructs Hemi with this exact sequence when presenting the Gamma link.

### If Bold has Gamma Plus or Pro
The exported PDF has no "Made with Gamma" watermark. Attach directly to outputs as `proposal.pdf`.

### If Bold is on Gamma Free
The PDF will have a "Made with Gamma" watermark on each card. For a Bold client proposal, this looks unprofessional. Recommend Plus or Pro subscription (~$10/month) before sending out proposals. If budget-constrained, use Path A (Canva) instead.

### After Hemi exports
Hemi places the PDF at `06-assembly/proposal.pdf`. Claude detects the file and continues with step 5 (summary).

Alternative: Claude can instruct Hemi to share the Gamma deck URL, and Claude uses `web_fetch` on the URL to confirm the deck exists, then proceeds with summary assuming Hemi will handle the PDF export and send to the client.

---

## 5. Building the summary (summary.md)

Template (v2.3, includes both Gamma link and PDF reference):

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

**להצעה המלאה:**
- גרסה אינטראקטיבית (מומלץ לצפייה): [Gamma link]
- PDF להדפסה / צירוף למיילים: מצורף

**קבצים נוספים מצורפים:**
- תקציב מפורט (Excel)
- KPIs scorecard
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

---

## 6. Building KPIs scorecard (kpis-scorecard.md)

Unchanged from v2.2. Template in brief.md field 16 format.

---

## 7. Creating the Trello debrief card

Unchanged from v2.2. Board: "Bold, Debriefs". Due date: event date + 1 day.

---

## Dependencies required for Stage 6 (v2.3)

| Dependency | Purpose | Fallback if missing |
|---|---|---|
| premium-deck-strategist skill | Slide-by-slide spec | Claude builds spec generically (lower polish) |
| Gamma account (Plus or Pro) | Deck creation + PDF export without watermark | Gamma Free with watermark, or Canva Path A |
| Canva MCP | Alternative deck creation if Gamma unavailable | Markdown to PDF via `pdf` skill |
| Trello MCP | Debrief card | DEBRIEF-REMINDER.md + Gmail reminder |

If Gamma is unavailable (no account, no access), fall back to Canva (Path A). If Canva is also unavailable, build a generic markdown-to-PDF with the brand palette as a last resort, and flag to Hemi that the output is not designed-deck quality.

---

## Final QA checklist

- [ ] Excel totals match deck's investment slides
- [ ] Excel has 3 sheets with correct tab names
- [ ] Gamma deck structure mirrors premium-deck-strategist spec
- [ ] Bold palette applied in Gamma (not Deep Blue default)
- [ ] Gamma deck tested in Present mode (no card overflows)
- [ ] PDF exported from Gamma without watermark (Plus/Pro only)
- [ ] PDF opens correctly on macOS Preview and Adobe Acrobat
- [ ] KPIs scorecard matches brief.md field 16 exactly
- [ ] KPI slide in deck matches scorecard
- [ ] Summary.md word count under 250 words
- [ ] Summary.md includes both Gamma link and PDF reference
- [ ] Valid-until date consistent across all files
- [ ] Event name and client name spelled identically across files
- [ ] Trello card created with URL captured in summary.md

---

## Present-files call

At the end, call `present_files` with:

```
[
  "proposals/<slug>/06-assembly/proposal.pdf",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/kpis-scorecard.md",
  "proposals/<slug>/06-assembly/summary.md"
]
```

`gamma-prompt.md` is not presented (internal artifact). Instead, the Gamma deck URL is embedded in summary.md.

Then output completion marker:

```
✓ ההצעה מוכנה.
   Gamma deck: [URL]
   Trello debrief card: [URL]
```
