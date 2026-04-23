# Stage 6, Assembly Reference (v2.4)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds seven final deliverables:

1. **Premium proposal deck** (PDF), built via `premium-deck-strategist` skill, brand system from Stage 3 applied
2. `budget.xlsx`, the detailed Excel in Bold's canonical template format
3. **Live Gamma deck** (URL), generated via `gamma_generate` MCP tool, client-viewable and commentable
4. **`proposal.pptx`**, downloadable PowerPoint file, same source as the Gamma deck (single MCP call produces both)
5. `summary.md`, a 1-page executive summary for intro messages
6. `kpis-scorecard.md`, a standalone KPI measurement plan (also embedded in the deck)
7. Trello debrief card, created in the "Bold, Debriefs" board, due the day after the event

**v2.4 change:** The Gamma generation now requests `exportAs: "pptx"` instead of `"pdf"`. A single `gamma_generate` call returns **both** the live `gammaUrl` and a PPTX `exportUrl` to download. Client gets two interactive formats to choose from: live Gamma for commenting, PPTX for offline editing. The polished PDF continues to come from `premium-deck-strategist`, unchanged.

Order: XLSX first (numbers lock), then premium deck PDF (tells the story with numbers confirmed), then Gamma+PPTX in one call (interactive + offline companion), then KPIs scorecard, then summary, then Trello card.

---

## 1. Building the Excel budget (budget.xlsx)

Unchanged from v2.2. Use `build_budget_xlsx.py` against `05-budget/budget.json`, outputs the Bold canonical template format.

---

## 2. Building the premium deck (proposal.pdf)

Unchanged from v2.2. Claude invokes `premium-deck-strategist` with the full brief (slide order, voice rules, brand override from `brand-system.md`). See v2.2 section for the exact invocation payload.

### Budget threshold fallback
For proposals under ₪25K, premium-deck-strategist is overkill. Fall back to a simpler 8-slide version. Claude makes this decision automatically based on budget.json subtotal.

---

## 3. Building the Gamma deck and PPTX [v2.4, dual-format single call]

### Why both formats from one call

The client receives the proposal in three forms:
- **PDF** (premium-deck-strategist), the polished read-only pitch
- **Live Gamma URL**, for interactive viewing and comments in the browser
- **PPTX file**, for offline editing, insertion into the client's own deck, or email attachment

Gamma's API returns both the live URL (`gammaUrl`) and the PPTX download URL (`exportUrl`) in a single response when `exportAs: "pptx"` is set. One generation, two deliverables, one credit charge.

If the client ever requests PDF-from-Gamma specifically (rare, the premium PDF is usually what they want), Claude can make a second `gamma_generate` call with `exportAs: "pdf"`. Not the default flow.

### Precondition

Before calling `gamma_generate`, verify the Gamma MCP is connected. If the `gamma_generate` tool is not available in the current session, fall back to the v2.2 flow (write `gamma-prompt.md` and instruct Hemi to paste into Gamma manually; PPTX then comes from Gamma's UI Export button).

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
    stylePreset: <photorealistic | illustration | abstract | 3D | lineArt | custom>,
    style: <from brand-system.md §8, e.g. "editorial photography, shallow depth, warm light">,
    model: <optional, e.g. "gemini-3-pro-image" for photo-real, "flux-2-pro" for illustrative>
  },
  additionalInstructions: "Hebrew-first. No em-dash. No clichés. Specific numbers not adjectives. No Bold credits.",
  exportAs: "pptx",
  wait: true,
  pollTimeoutMs: 900000
)
```

### Saving the PPTX to disk

After `gamma_generate` returns with `status: "completed"`:

1. Extract `exportUrl` from the response (this is the PPTX download URL, expires in ~1 week).
2. Download the binary file: `curl -L -o proposals/<slug>/06-assembly/proposal.pptx "<exportUrl>"` or equivalent.
3. Verify the file: check `file proposal.pptx` shows "Microsoft PowerPoint 2007+" and size is non-trivial (typically 2-15 MB for 16 slides with images).
4. The `gammaUrl` goes straight into `summary.md` (no download needed, it's a live link).

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
- `gammaUrl` present (live Gamma deck)
- `exportUrl` present (PPTX download link from `exportAs: "pptx"`)
- `gammaId` captured for future `gamma_generate_from_template` remix
- Credits deducted as expected (log for cost tracking)

After downloading the PPTX file, Claude verifies:
- File exists at `proposals/<slug>/06-assembly/proposal.pptx`
- File size > 500 KB (smaller typically means broken export)
- MIME type is `application/vnd.openxmlformats-officedocument.presentationml.presentation`

If `status == "failed"`, Claude reads `error.message`, fixes the obvious issue (invalid themeId, numCards over cap, etc.), and retries once. If the second attempt fails, fall back to the v2.2 prompt-paste path and continue.

### For returning clients: `gamma_generate_from_template`

When the event is for a returning client (Phoenix, Keren, Efrat, etc.) AND a prior successful deck exists in the client profile:

1. Stage 1 or Stage 3 reads the `gammaId` of the prior deck from `data/client-profiles/[client-slug].md`.
2. At Stage 6, Claude calls `gamma_generate_from_template` instead of `gamma_generate`:

```
gamma_generate_from_template(
  gammaId: <prior deck's ID>,
  prompt: <the same structured inputText as above>,
  themeId: <same or new>,
  wait: true,
  exportAs: "pptx"
)
```

This preserves the layout, visual system, and scale of the winning deck while swapping content. Still returns both `gammaUrl` and PPTX `exportUrl` in one call. Hemi's note: this single capability is why we run a custom MCP instead of Gamma's official connector.

### Fallback: v2.2 prompt-paste path

If the Gamma MCP is not connected at runtime:

1. Claude writes `gamma-prompt.md` using the template in `assets/gamma-prompt-template.md`.
2. `summary.md` references the prompt file instead of a live URL and notes "PPTX יישלח לאחר בנייה ידנית ב-Gamma".
3. Hemi pastes into Gamma manually, then exports PPTX via the Gamma UI (Share → Export → PowerPoint).

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

**מצורפים:**
- הצעה מעוצבת מלאה (PDF), נבנתה ב-premium-deck-strategist
- **מצגת PowerPoint (PPTX)** לעריכה מקומית, מצורפת
- **מצגת אינטראקטיבית ב-Gamma:** [gammaUrl from gamma_generate result]
- תקציב מפורט (Excel)
- KPIs scorecard (Markdown)
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

If the fallback path was used, replace the Gamma URL bullet with "מצגת Gamma: קישור יישלח אחרי בנייה" and the PPTX bullet with "PowerPoint יישלח לאחר ייצוא מ-Gamma".

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
- [ ] PPTX file downloaded to `proposals/<slug>/06-assembly/proposal.pptx`
- [ ] PPTX opens in PowerPoint/Keynote without errors
- [ ] PPTX file size above 500 KB
- [ ] Gamma deck's investment slide total matches budget.xlsx total
- [ ] Gamma deck's KPI slide matches scorecard
- [ ] Summary.md word count under 250 words
- [ ] Summary.md includes live Gamma URL AND references attached PPTX (or fallback notes)
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

At the end, call `present_files` with these five files in this order. The Gamma URL is live, not a file, so it appears only in summary.md:

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
  Gamma (live): [gammaUrl]
  PowerPoint: proposal.pptx (attached)
  Trello debrief: [trelloUrl]
```

---

## What changed from v2.3

- `exportAs: "pptx"` replaces `"pdf"` in the `gamma_generate` call, so the same call produces both the live Gamma URL and a PPTX file
- Claude downloads the PPTX from `exportUrl` and saves to `proposals/<slug>/06-assembly/proposal.pptx`
- `summary.md` now references the PPTX as an attachment alongside the Gamma URL
- `present_files` list expanded from 4 to 5 files (adds `proposal.pptx`)
- Completion marker surfaces both the live Gamma URL and a note that PPTX is attached
- Premium PDF path via `premium-deck-strategist` unchanged; it remains the polished client-facing document

## Dependencies

This stage requires:
- `premium-deck-strategist` skill, for the PDF
- Bold Gamma MCP server connected at `gamma-mcp-server-production-959b.up.railway.app/sse`, for the live Gamma deck AND the PPTX export
- `curl` or equivalent HTTP client on the runtime, to download the PPTX from `exportUrl`

If the Gamma MCP is missing, Claude warns, falls back to the v2.2 prompt-paste flow, and the PPTX must be exported manually from Gamma's UI.
