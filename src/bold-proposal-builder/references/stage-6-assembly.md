# Stage 6, Assembly Reference (v2.4)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds six final deliverables:

1. **Premium proposal deck** (PDF), built via `premium-deck-strategist` skill, brand system from Stage 3 applied. The flagship, polished, committee-ready.
2. `budget.xlsx`, the detailed Excel in Bold's canonical template format
3. **Live Gamma deck + editable PPTX**, generated together via the custom Gamma MCP (`gamma_generate` with `exportAs: "pptx"`). One call returns both the live URL and a downloadable PowerPoint file.
4. `summary.md`, a 1-page executive summary for intro messages
5. `kpis-scorecard.md`, a standalone KPI measurement plan (also embedded in the deck)
6. Trello debrief card, created in the "Bold, Debriefs" board, due the day after the event

**v2.4 change:** Gamma now exports to PPTX instead of PDF. Rationale: the PDF surface is already covered by premium-deck-strategist at higher design quality; the Gamma PPTX is additive, gives the client an editable file they can open in PowerPoint or Google Slides and comment directly. Three complementary surfaces, not two redundant ones.

Order: XLSX first (numbers lock), then premium PDF (tells the story with numbers confirmed), then live Gamma deck + PPTX export (interactive + editable), then KPIs scorecard, then summary (links all three surfaces), then Trello card.

---

## 1. Building the Excel budget (budget.xlsx)

Unchanged from v2.2. Use `build_budget_xlsx.py` against `05-budget/budget.json`, outputs the Bold canonical template format.

---

## 2. Building the premium deck (proposal.pdf)

Unchanged from v2.2. Claude invokes `premium-deck-strategist` with the full brief (slide order, voice rules, brand override from `brand-system.md`). See v2.2 section for the exact invocation payload.

### Budget threshold fallback
For proposals under ₪25K, premium-deck-strategist is overkill. Fall back to a simpler 8-slide version. Claude makes this decision automatically based on budget.json subtotal.

---

## 3. Building the live Gamma deck + PPTX export [v2.4, MCP-native]

### Three surfaces, one call

`gamma_generate` with `exportAs: "pptx"` and `wait: true` returns a result object containing both `gammaUrl` (the live, shareable, commentable Gamma page) and `exportUrl` (a signed URL to the PPTX file, valid ~1 week). Single MCP call, two artifacts.

### Precondition

Before calling `gamma_generate`, verify the Gamma MCP is connected. If the `gamma_generate` tool is not available in the current session, fall back to the v2.2 flow (write `gamma-prompt.md` and instruct Hemi to paste it into Gamma manually; no PPTX in this path).

### Theme resolution

Claude first calls `gamma_list_themes` and picks a theme by matching `brand-system.md` keywords to the theme's `colorKeywords` + `toneKeywords`. If no standard theme matches the brand heart (happens on high-concept events like Phoenix art), fall back to a Bold-default theme and let Gamma's prompt-level styling carry the brand.

### Invocation pattern

```
gamma_generate(
  inputText: <structured slide-by-slide outline, see below>,
  format: "presentation",
  numCards: 16,
  themeId: <resolved from gamma_list_themes>,
  folderIds: [<Bold-Proposals folder id, from gamma_list_folders, cached>],
  cardOptions: { dimensions: "16x9" },
  textOptions: {
    language: "he",
    tone: <from brand-system.md §4, condensed to one adjective>,
    audience: <from brief.md field 6, one sentence>,
    amount: "medium"
  },
  imageOptions: {
    source: "aiGenerated",
    style: <from brand-system.md §8, e.g. "editorial photography, shallow depth, warm light">
  },
  additionalInstructions: "Hebrew-first. No em-dash. No clichés. Specific numbers not adjectives. No Bold credits.",
  exportAs: "pptx",
  wait: true,
  pollTimeoutMs: 900000
)
```

### After the call

Claude downloads the PPTX from `exportUrl` and saves it to `proposals/<slug>/06-assembly/proposal.pptx`. The `gammaUrl` is embedded in `summary.md`. Both are captured alongside the premium PDF, so the client receives all three surfaces.

### Structured inputText (16 cards)

Claude assembles `inputText` with explicit card breaks (`---`) so Gamma's autosplit cannot reorganize:

```
# [Event Name]
[tagline from brand-system.md §3]
---
# הרגע (The Moment)
[one-paragraph reason-why from brief field 1]
---
# קריאה אסטרטגית
[3 bullets from challenges.md]
---
# הקונספט
[concept sentence + 2 unpack sentences from brand-system.md §1-2]
---
# הגעה (arrival mockup caption)
[caption from mood-direction.md]
---
# הרגע המרכזי (hero mockup caption)
[caption]
---
# האולם
[wide-shot caption]
---
# הפרט
[detail-shot caption]
---
# הקולינרי
[paragraph from menu.md intro]
---
# החוויה
[3 anchor moments from agenda.md block view]
---
# התפעול
[one paragraph: venue, technical dimensions, headcount]
---
# השקעה
[budget summary + conditional lines]
---
# KPIs והצלחה
[N KPIs from brief field 16, one line each]
---
# לוח זמנים
[milestones from today to event date]
---
# הצעדים הבאים
[decision points + contact]
---
```

### Post-generation QA

On return from `gamma_generate`, Claude verifies:
- `status == "completed"`
- `gammaUrl` present
- `exportUrl` present and downloads successfully (non-empty PPTX)
- Credits deducted as expected (log for cost tracking)

If `status == "failed"`, Claude reads `error.message`, fixes the obvious issue (invalid themeId, numCards over cap, etc.), and retries once. If the second attempt fails, fall back to the v2.2 prompt-paste path and continue (PPTX will not be available in the fallback).

### For returning clients: `gamma_generate_from_template`

When the event is for a returning client (Phoenix, Keren, Efrat, etc.) AND a prior successful deck exists in the client profile:

1. Stage 1 or Stage 3 reads the `gammaId` of the prior deck from `data/client-profiles/[client-slug].md`.
2. At Stage 6, Claude calls `gamma_generate_from_template` instead of `gamma_generate`, same `exportAs: "pptx"`:

```
gamma_generate_from_template(
  gammaId: <prior deck's ID>,
  prompt: <the same structured inputText as above>,
  themeId: <same or new>,
  wait: true,
  exportAs: "pptx"
)
```

This preserves the layout, visual system, and scale of the winning deck while swapping content, and still delivers both the live URL and the PPTX export.

### Fallback: v2.2 prompt-paste path

If the Gamma MCP is not connected at runtime:
1. Claude writes `gamma-prompt.md` using the template in `assets/gamma-prompt-template.md`.
2. `summary.md` references the prompt file instead of a live URL, notes that PPTX is not produced in the fallback.
3. Hemi pastes into Gamma manually, exports PPTX from the Gamma UI if desired.

---

## 4. Building the KPIs scorecard (kpis-scorecard.md)

Unchanged from v2.1.

---

## 5. Building the summary (summary.md)

### Template (v2.4)

```markdown
[Client first name] שלום,

הנה ההצעה שלנו ל-[Event Name].

**הקונספט בקצרה:**
[Concept sentence from brand-system.md]

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

**הצעה בשלוש גרסאות משלימות:**
- **הצעה מעוצבת מלאה (PDF)**, נבנתה ב-premium-deck-strategist, מיועדת לקריאה ולהפצה בוועדה
- **מצגת אינטראקטיבית ב-Gamma:** [gammaUrl from gamma_generate result], לצפייה וויד ותגובות
- **גרסת PowerPoint (PPTX):** מצורפת, לעריכה חופשית בצד הלקוח

**מצורפים נוספים:**
- תקציב מפורט (Excel)
- KPIs scorecard (Markdown)
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

If the fallback path was used, replace the three-surfaces block with "מצגת Gamma: קישור יישלח אחרי בנייה; גרסת PowerPoint תופק ידנית מה-Gamma."

---

## 6. Creating the Trello debrief card

Unchanged from v2.1. Card goes into "Bold, Debriefs" board with due date = event date + 1. Include the `gammaId` of the generated deck in the card description so Stage 7 can pass it to `gamma_generate_from_template` when the next proposal for this client begins.

---

## Final QA checklist (v2.4)

- [ ] Premium deck PDF opens and renders on macOS Preview and Adobe Acrobat
- [ ] Deck has exactly 16 slides (or 8 for sub-₪25K fallback)
- [ ] Deck palette matches brand-system.md (not default)
- [ ] PDF fonts embedded
- [ ] Excel totals match the deck's investment slide
- [ ] Excel uses Bold's canonical 6-category tree with single "דמי ארגון והפקה" line
- [ ] Gamma deck generated successfully (status=completed, gammaUrl present)
- [ ] Gamma PPTX downloaded successfully from exportUrl, opens in PowerPoint
- [ ] Gamma deck's investment slide total matches budget.xlsx total
- [ ] Gamma deck's KPI slide matches scorecard
- [ ] Summary.md word count under 250 words
- [ ] Summary.md lists all three client-facing surfaces (PDF, Gamma URL, PPTX)
- [ ] Valid-until date consistent across all files
- [ ] Event name spelled identically across all files
- [ ] Client name spelled identically
- [ ] Contact info correct
- [ ] Trello card created, URL captured in summary.md, `gammaId` captured in card description
- [ ] All client-facing surfaces are Hebrew-first
- [ ] No em-dash or en-dash anywhere
- [ ] No banned clichés
- [ ] No Bold credits on client-facing surfaces

---

## Present-files call

At the end, call `present_files` with these five files in this order (the Gamma live URL is in summary.md, not a file):

```
[
  "proposals/<slug>/06-assembly/proposal.pdf",
  "proposals/<slug>/06-assembly/proposal.pptx",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/kpis-scorecard.md",
  "proposals/<slug>/06-assembly/summary.md"
]
```

Then output one-line completion marker including Trello card URL, Gamma URL, and stop:

```
✓ ההצעה מוכנה.
  Gamma: [gammaUrl]
  Trello debrief: [trelloUrl]
```

---

## What changed from v2.3

- Gamma now exports to PPTX (not PDF); client receives three complementary surfaces instead of two redundant PDFs
- `proposal.pptx` added to the present-files list
- Summary template restructured to highlight the three surfaces
- QA checklist adds PPTX download verification

## Dependencies

This stage requires:
- `premium-deck-strategist` skill, for the flagship PDF
- Bold Gamma MCP server connected at `gamma-mcp-server-production-959b.up.railway.app/sse`, for the live Gamma deck and PPTX export

If either is missing, Claude warns, falls back (standard `pdf` skill for the deck; prompt-paste flow for Gamma with PPTX produced manually by Hemi), and continues without blocking.
