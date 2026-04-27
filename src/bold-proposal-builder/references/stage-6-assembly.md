# Stage 6, Assembly Reference (v2.6)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds six core deliverables plus one optional fourth client-facing deck surface (Canva):

1. **Premium proposal deck** (PDF), built via `premium-deck-strategist` skill, brand system from Stage 3 applied, Bold's canonical 28-slide structure (or 16-card compressed form), strict footer/cover/closing rules per `assets/bold-presentation-template-spec.md`
2. `budget.xlsx`, the detailed Excel in Bold's canonical template format, produced by `scripts/build_budget_xlsx.py` from `budget.json`, matches "טמפלט תקציב 01" byte-for-byte in layout terms
3. **Live Gamma deck + editable PPTX**, generated together via `gamma_generate` with `exportAs: "pptx"`. One call returns both the live URL and a downloadable PowerPoint file. Card dimensions 4x3 (matching Bold's longstanding 4:3 PPT template)
4. `summary.md`, a 1-page executive summary for intro messages
5. `kpis-scorecard.md`, a standalone KPI measurement plan (also embedded in the deck)
6. Trello debrief card in the "Bold, Debriefs" board, due the day after the event
7. **(Optional) Canva deck**, produced via the Canva MCP server when Hemi requests it or the client uses Canva natively. Detailed flow in `references/canva-deck-path.md`. Aspect ratio 16:9 by default (Canva limitation), see canva-deck-path.md for the resize workaround.

**v2.6 changes:**
- Optional Canva surface added as a fourth client-facing deck. Detailed in the new `canva-deck-path.md` reference. Triggered by Hemi's explicit request, presence of a Bold Canva brand kit, or returning client preference. Default behavior unchanged: PDF + Gamma + PPTX still ship by default.
- Canva integration currently lives inside bold-proposal-builder. When `premium-deck-strategist` is pushed to the repo, the Canva path moves there as a generic output mode and Stage 6 becomes a wrapper that picks `output_mode`.

**v2.5 changes:** 
- Gamma `cardDimensions` corrected from `"16x9"` to `"4x3"`. Bold has used 4:3 for two decades; 16:9 would break visual continuity with prior client work
- XLSX output now matches Bold's actual canonical template (see `scripts/build_budget_xlsx.py` v3.0 and `assets/budget-categories-reference.md`)
- Explicit references to `assets/bold-presentation-template-spec.md` for type system, layout, footer, cover, closing rules
- Explicit references to `assets/logos/` for the three official logo assets
- Mandatory footer composition: white Bold logo bottom-left + "A Bold Presentation© [current year]" center + client logo bottom-right

Order: XLSX first (numbers lock), then premium PDF (tells the story with numbers confirmed), then live Gamma deck + PPTX export (interactive + editable), then optionally Canva, then KPIs scorecard, then summary (links all surfaces), then Trello card.

---

## 1. Building the Excel budget (budget.xlsx)

**v3.0 canonical format.** Run `scripts/build_budget_xlsx.py` against `05-budget/budget.json`.

Input requirements:
- Every `main_line` MUST have a `category` field from the 6 canonicals in `assets/budget-categories-reference.md`: כללי / תקשור מקדים / מיתוג ושילוט / טכני / כח אדם ולוגיסטיקה / שונות.
- Non-canonical categories are not silently dropped; the script warns and rolls them into שונות. If a warning appears, Stage 5 should be revisited.
- `conditional_lines` is optional but all conditional items go flat under a single כללי marker in the options section.
- `production_fee_rate` defaults to 0.15 (Bold's standard 15% margin). Override only with Hemi's explicit approval.

Output: `06-assembly/budget.xlsx`, single sheet "טמפלט ריק", 13 columns RTL, main section + options section, matching Bold's template in use since 2010.

---

## 2. Building the premium deck (proposal.pdf)

Claude invokes `premium-deck-strategist` with a full brief. The brief must include:

### Slide structure

Either the 16-card compressed form (modern attention spans) OR the canonical 28-slide sequence from `assets/bold-presentation-template-spec.md` (for larger clients expecting the full Bold treatment). Hemi picks; default is 16-card.

### Required slide order (16-card compressed)

1. Cover (`bold-black-opening.jpg` or hero mockup, no footer)
2. About this event (one-line reason-why from brief field 1)
3. Strategic reading (3 key insights from challenges.md)
4. The creative concept (brand-system.md fields 1-3, hero mockup)
5-9. Visualization (5 mockups: arrival, main space, hero moment, catering, details)
10. The experience (agenda highlights, 3 anchor moments)
11. Operations (run-sheet outline, 1 slide)
12. Culinary (menu narrative, 1 slide)
13. Investment (budget summary, clear price + conditional lines)
14. KPIs and success measurement (table from brief field 16, closing line about 24h debrief)
15. Timeline (delivery dates + decision points)
16. Closing (`bold-closing.mp4` first frame + "▶" overlay in PDF; no footer)

### Design directive

- Aspect ratio 4:3 (14.22 x 10.66 inches), NEVER 16:9
- Title font Tahoma bold 35pt Hebrew, Verdana bold 35pt English
- Body text Tahoma/Verdana 18-22pt, black or #333333
- Palette sourced from `brand-system.md` Stage 3 output; no default Deep Blue
- Footer stripe on slides 2-15: white Bold logo (`assets/logos/bold-white-footer.jpg`) bottom-left at (0.3, 9.8) inches, `A Bold Presentation© [current year]` center Verdana 14pt gray #808080 at y=9.9, client logo bottom-right at (12.7, 9.8)
- Cover slide (1) and closing slide (16): no footer, no Bold logo credit, unique layouts per `bold-presentation-template-spec.md`

### Voice rules (non-negotiable)

- Hebrew-first, all client-facing slides in Hebrew
- No em-dash, no en-dash
- Max 5-7 words per on-slide bullet; depth in speaker notes
- Specific numbers, not adjectives
- Banned clichés: "בלתי נשכח", "מרגש", "חוגגים יחד", "unforgettable", "once in a lifetime"
- No Bold credits outside the footer stripe

### Output

`proposals/<slug>/06-assembly/proposal.pdf`

### Budget threshold fallback

For proposals under ₪25K, premium-deck-strategist is overkill. Fall back to a simpler 8-slide version (cover, concept, visualization x2, experience, investment, KPIs, closing). Claude makes this decision automatically based on budget.json subtotal. Footer and cover/closing rules still apply.

### Post-generation QA

- Slide count matches spec (16 or 8 for low-budget, or 28 if Hemi chose long form)
- Palette matches brand-system.md exactly
- Footer present on all body slides, absent on cover and closing
- White Bold logo, center text, and client logo correctly positioned
- Hebrew RTL rendering correct
- Investment slide total matches budget.xlsx total
- Aspect ratio 4:3

If any check fails, Claude asks premium-deck-strategist to regenerate the specific slide, not the whole deck.

---

## 3. Building the live Gamma deck + PPTX export

### Three surfaces, one call

`gamma_generate` with `exportAs: "pptx"` and `wait: true` returns a result object containing both `gammaUrl` (the live, shareable, commentable Gamma page) and `exportUrl` (a signed URL to the PPTX file, valid ~1 week). Single MCP call, two artifacts.

### Precondition

Before calling `gamma_generate`, verify the Gamma MCP is connected. If the `gamma_generate` tool is not available in the current session, fall back to the v2.2 prompt-paste flow (write `gamma-prompt.md`; no PPTX in this path).

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
  cardOptions: { dimensions: "4x3" },                 // <<< 4x3, not 16x9
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
  additionalInstructions: "Hebrew-first. No em-dash. No clichés. Specific numbers not adjectives. No Bold credits on body slides. Footer: 'A Bold Presentation© [current year]' centered in small gray text.",
  exportAs: "pptx",
  wait: true,
  pollTimeoutMs: 900000
)
```

Note: Gamma does not support embedding custom logos in the footer programmatically via API. The "A Bold Presentation© [year]" text can be placed via `additionalInstructions`. The white/client logo assets are added by hand after export if the client wants the PPTX polished to match the PDF; for the live Gamma URL, the centered text alone is sufficient.

### After the call

Claude downloads the PPTX from `exportUrl` and saves it to `proposals/<slug>/06-assembly/proposal.pptx`. The `gammaUrl` is embedded in `summary.md`. Both are captured alongside the premium PDF, so the client receives all three surfaces.

### Structured inputText (16 cards)

Claude assembles `inputText` with explicit card breaks (`---`) so Gamma's autosplit cannot reorganize. See the existing v2.5 structured outline (unchanged in v2.6).

### Post-generation QA

On return from `gamma_generate`, Claude verifies:
- `status == "completed"`
- `gammaUrl` present
- `exportUrl` present and downloads successfully (non-empty PPTX)
- Credits deducted as expected (log for cost tracking)

If `status == "failed"`, Claude reads `error.message`, fixes the obvious issue (invalid themeId, numCards over cap, etc.), and retries once. If the second attempt fails, fall back to the prompt-paste path and continue (PPTX will not be available in the fallback).

### For returning clients: `gamma_generate_from_template`

When the event is for a returning client (Phoenix, Keren, Efrat, etc.) AND a prior successful deck exists in the client profile:

1. Stage 1 or Stage 3 reads the `gammaId` of the prior deck from `data/client-profiles/[client-slug].md`.
2. At Stage 6, Claude calls `gamma_generate_from_template` instead of `gamma_generate`, same `exportAs: "pptx"`.

This preserves the layout, visual system, and scale of the winning deck while swapping content, and still delivers both the live URL and the PPTX export.

### Fallback: prompt-paste path

If the Gamma MCP is not connected at runtime:
1. Claude writes `gamma-prompt.md` using the template in `assets/gamma-prompt-template.md`.
2. `summary.md` references the prompt file instead of a live URL, notes that PPTX is not produced in the fallback.
3. Hemi pastes into Gamma manually, exports PPTX from the Gamma UI if desired.

---

## 4. Building the KPIs scorecard (kpis-scorecard.md)

Unchanged from v2.1.

---

## 5. Building the summary (summary.md)

### Template (v2.6)

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

[IF Canva surface NOT enabled, default 3-surface block:]
**הצעה בשלוש גרסאות משלימות:**
- **הצעה מעוצבת מלאה (PDF)**, נבנתה ב-premium-deck-strategist, מיועדת לקריאה ולהפצה בוועדה
- **מצגת אינטראקטיבית ב-Gamma:** [gammaUrl from gamma_generate result], לצפייה ותגובות
- **גרסת PowerPoint (PPTX):** מצורפת, לעריכה חופשית בצד הלקוח

[IF Canva surface IS enabled, 4-surface block:]
**הצעה בארבע גרסאות משלימות:**
- **הצעה מעוצבת מלאה (PDF)**, נבנתה ב-premium-deck-strategist, מיועדת לקריאה ולהפצה בוועדה
- **מצגת אינטראקטיבית ב-Gamma:** [gammaUrl from gamma_generate result], לצפייה ותגובות
- **גרסת PowerPoint (PPTX):** מצורפת, לעריכה חופשית בצד הלקוח
- **גרסת Canva:** [canvaUrl from create-design-from-candidate], לעריכה ושיתוף בסביבת Canva של הלקוח

**מצורפים נוספים:**
- תקציב מפורט (Excel, פורמט "טמפלט תקציב 01" הקנוני של Bold)
- KPIs scorecard (Markdown)
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

If the Gamma fallback path was used, replace the Gamma + PPTX bullets with "מצגת Gamma: קישור יישלח אחרי בנייה; גרסת PowerPoint תופק ידנית מה-Gamma."

---

## 6. Creating the Trello debrief card

Unchanged from v2.1. Card goes into "Bold, Debriefs" board with due date = event date + 1. Include the `gammaId` of the generated deck in the card description so Stage 7 can pass it to `gamma_generate_from_template` when the next proposal for this client begins. If a Canva surface was produced, also include the Canva `design_id` in the card description (no remix tool yet, but useful for manual reference).

---

## 7. Building the Canva deck (optional fourth surface)

When Hemi requests a Canva surface, or when the client uses Canva natively, Stage 6 produces a fourth deliverable in addition to the three default surfaces. Full flow in `references/canva-deck-path.md`.

### Trigger conditions

Canva surface activates when ANY of:
- Hemi explicitly requests it: "תפיק גם גרסת קנבה", "בנה את ההצעה ב-Canva", "want this in Canva too"
- Brief field 12 (design / brand guidelines) mentions Canva as the client's primary tool
- The client profile in `data/client-profiles/[client-slug].md` has `prefers_canva: true`
- Returning client whose prior deck was on Canva

### High-level flow

1. Resolve Bold brand kit ID from `data/canva-config.json` (or `Canva:list-brand-kits` if first run)
2. `Canva:request-outline-review` with the 16-card outline (mandatory gateway, punctuation stripped)
3. Wait for Hemi to approve in widget
4. `Canva:generate-design-structured` returns design candidates
5. Hemi picks one
6. `Canva:create-design-from-candidate` returns `design_id`
7. `Canva:export-design` twice: format `pdf` and format `pptx`
8. Save outputs as `proposal-canva.pdf`, `proposal-canva.pptx`; capture Canva URL for `summary.md`

### Aspect ratio note

Canva default is 16:9. Bold canonical is 4:3. See `canva-deck-path.md` for the `resize-design` experimental workaround if 4:3 is required for the Canva surface.

### Footer note

Canva MCP cannot programmatically place custom logo footers. Center text "A Bold Presentation© [year]" gets injected via `additionalInstructions`; logos placed manually after export if needed.

### Fallback

If the Canva MCP is not connected at runtime, skill notes the limitation in `summary.md` and proceeds without the Canva surface. Not blocking.

---

## Final QA checklist (v2.6)

- [ ] Premium deck PDF opens and renders on macOS Preview and Adobe Acrobat
- [ ] Deck has exactly 16 slides (or 8 for sub-₪25K fallback, or 28 for long form)
- [ ] Deck aspect ratio 4:3 (14.22 x 10.66 inches)
- [ ] Title font Tahoma Hebrew / Verdana English, bold 35pt
- [ ] Cover slide (1) uses `bold-black-opening.jpg` or hero mockup, NO footer
- [ ] Closing slide (last) uses `bold-closing.mp4` first frame with ▶ overlay in PDF, NO footer
- [ ] All body slides carry the three-element footer: white Bold logo bottom-left, `A Bold Presentation© [current year]` center, client logo bottom-right
- [ ] Client logo present (or blank bottom-right slot + flag to Hemi if missing)
- [ ] Year in footer matches current year, NOT event year
- [ ] Deck palette matches brand-system.md (not default)
- [ ] PDF fonts embedded
- [ ] Excel produced via `build_budget_xlsx.py` v3.0
- [ ] Excel uses Bold's canonical 6-category tree with single "דמי ארגון והפקה" line
- [ ] Excel totals match the deck's investment slide
- [ ] Gamma deck generated successfully (status=completed, gammaUrl present)
- [ ] Gamma cardDimensions = "4x3" (not 16x9)
- [ ] Gamma PPTX downloaded successfully from exportUrl, opens in PowerPoint
- [ ] Gamma deck's investment slide total matches budget.xlsx total
- [ ] Gamma deck's KPI slide matches scorecard
- [ ] (IF Canva surface enabled) Canva outline approved by Hemi via widget
- [ ] (IF Canva surface enabled) Canva candidate picked by Hemi
- [ ] (IF Canva surface enabled) Canva PDF + PPTX exports both downloaded
- [ ] (IF Canva surface enabled) Canva URL captured in summary.md
- [ ] (IF Canva surface enabled) Aspect ratio status flagged (16:9 default or 4:3 if resized)
- [ ] (IF Canva surface enabled) Footer status flagged (incomplete/partial/manually completed)
- [ ] Summary.md word count under 280 words (slightly higher cap when Canva surface adds a bullet)
- [ ] Summary.md lists all enabled client-facing surfaces
- [ ] Valid-until date consistent across all files
- [ ] Event name spelled identically across all files
- [ ] Client name spelled identically
- [ ] Contact info correct
- [ ] Trello card created, URL captured in summary.md, `gammaId` and (if applicable) Canva `design_id` captured in card description
- [ ] All client-facing surfaces are Hebrew-first
- [ ] No em-dash or en-dash anywhere
- [ ] No banned clichés
- [ ] No Bold credits outside the footer stripe

---

## Present-files call

At the end, call `present_files` with these files in this order:

```
[
  "proposals/<slug>/06-assembly/proposal.pdf",
  "proposals/<slug>/06-assembly/proposal.pptx",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/kpis-scorecard.md",
  "proposals/<slug>/06-assembly/summary.md"
]
```

If Canva surface was produced, append:

```
  "proposals/<slug>/06-assembly/proposal-canva.pdf",
  "proposals/<slug>/06-assembly/proposal-canva.pptx"
```

Then output one-line completion marker including Trello card URL, Gamma URL, Canva URL (if any), and stop:

```
✓ ההצעה מוכנה.
  Gamma: [gammaUrl]
  Canva: [canvaUrl]   (if surface enabled)
  Trello debrief: [trelloUrl]
```

---

## What changed from v2.5

- Added optional fourth client-facing deck surface: Canva. Detailed flow in new `references/canva-deck-path.md`. Default 3-surface delivery unchanged.
- New section 7 in this file describes trigger conditions and high-level Canva flow
- QA checklist gains conditional Canva items
- Summary template gains a 4-surface variant
- Trello card stores Canva `design_id` when applicable
- Future: when `premium-deck-strategist` is pushed to the repo, the Canva path migrates there as a generic output mode and Stage 6 becomes a wrapper

## What changed from v2.4

- Gamma cardDimensions corrected from 16x9 to 4x3 (Bold's longstanding template is 4:3)
- XLSX script bumped to v3.0, now matches Bold's canonical template byte-for-byte
- Explicit references to the new assets: `budget-categories-reference.md`, `bold-presentation-template-spec.md`, `logos/` folder
- Footer composition rules spelled out: white logo bottom-left, A Bold Presentation© center, client logo bottom-right
- Cover and closing treated as unique no-footer layouts (per Bold template)
- QA checklist expanded with aspect ratio, font, footer composition, cover/closing rules

## Dependencies

This stage requires:
- `premium-deck-strategist` skill, for the flagship PDF
- Bold Gamma MCP server connected at `gamma-mcp-server-production-959b.up.railway.app/sse`, for the live Gamma deck and PPTX export
- `scripts/build_budget_xlsx.py` v3.0 in the skill package
- `assets/budget-categories-reference.md` for Stage 5 category validation
- `assets/bold-presentation-template-spec.md` for the type system and layout rules
- `assets/logos/bold-black-opening.jpg` and `bold-white-footer.jpg` in the .skill package (binaries not in Git)
- Access to `bold-closing.mp4` on Bold's Drive (30MB, fetched at Stage 6 time)

Optional dependency:
- **Canva MCP** (`mcp.canva.com/mcp`), required only if the Canva surface is enabled. Without it, Stage 6 ships the default three surfaces and skips Canva silently.

If `premium-deck-strategist` or the Gamma MCP is missing, Claude warns, falls back (standard `pdf` skill for the deck; prompt-paste flow for Gamma with PPTX produced manually), and continues without blocking. Same for Canva: missing MCP means Canva surface is skipped, not blocked.
