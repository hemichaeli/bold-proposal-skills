# Stage 6, Assembly Reference (v2.7)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds the client-facing package:

1. **Canva deck** (always) - live designed surface + PDF export + PPTX export, produced via Canva MCP. The flagship visual artifact, replacing the prior premium-deck-strategist PDF as the polished deliverable
2. **Gamma deck** (always) - live interactive surface + PPTX export, produced via `gamma_generate` with `exportAs: "pptx"`. The shareable / commentable surface
3. **`budget.xlsx`** - detailed Excel in Bold's canonical template format, produced by `scripts/build_budget_xlsx.py` from `budget.json`
4. **`kpis-scorecard.md`** - standalone KPI measurement plan
5. **`summary.md`** - 1-page executive summary
6. **Trello debrief card** in the "Bold, Debriefs" board, due day after the event

**v2.7 changes (current):**
- Aspect ratio constraint dropped. 4:3 is no longer enforced. Default surface aspect is 16:9 (Canva and Gamma natively). The historical `bold-presentation-template-spec.md` 4:3 spec stays in the repo as a legacy reference document, but Stage 6 no longer enforces it.
- Canva moves from optional to mandatory. Stage 6 always produces a Canva deck unless the Canva MCP is explicitly disconnected at runtime.
- Three-surface deck delivery is now Canva (URL + PDF + PPTX) + Gamma (URL + PPTX). Five deck artifacts total from two MCP calls. The standalone PDF via `premium-deck-strategist` becomes a legacy/fallback path, used only when both Canva and Gamma are unavailable.
- Footer composition rules retained as brand identity, but rendered in Canva via brand kit and `additionalInstructions`, then logos pasted manually post-export. No fixed inch coordinates anymore.

**v2.6 changes (historical):** Optional Canva surface added, when v2.7 promoted to mandatory.
**v2.5 changes (historical):** Gamma cardDimensions corrected to 4:3, XLSX bumped to v3.0, footer composition documented. v2.7 drops the 4:3 part.

Order: XLSX first (numbers lock), then Canva deck (visual flagship), then Gamma deck (interactive sibling), then KPIs scorecard, then summary, then Trello card.

---

## 1. Building the Excel budget (budget.xlsx)

**v3.0 canonical format.** Run `scripts/build_budget_xlsx.py` against `05-budget/budget.json`.

Input requirements:
- Every `main_line` MUST have a `category` field from the 6 canonicals in `assets/budget-categories-reference.md`: כללי / תקשור מקדים / מיתוג ושילוט / טכני / כח אדם ולוגיסטיקה / שונות.
- Non-canonical categories are not silently dropped; the script warns and rolls them into שונות.
- `conditional_lines` is optional; conditional items go flat under a single כללי marker in the options section.
- `production_fee_rate` defaults to 0.15 (Bold's standard 15% margin).

Output: `06-assembly/budget.xlsx`, single sheet "טמפלט ריק", 13 columns RTL, main + options sections.

---

## 2. Building the Canva deck (default flagship surface)

Full flow in `references/canva-deck-path.md`. Five MCP calls, three artifacts (live URL + PDF + PPTX).

### Pre-conditions

- Canva MCP connected (`mcp.canva.com/mcp`).
- (Optional) Bold Canva brand kit ID cached in `data/canva-config.json`.

### High-level flow

1. Resolve brand kit (or run `Canva:list-brand-kits` first time and cache).
2. `Canva:request-outline-review` with the 16-card outline. **Strip all punctuation** from titles and descriptions (Canva-MCP requirement for Claude). Hemi reviews + approves in widget.
3. `Canva:generate-design-structured` with `design_type: "presentation"`. Returns design candidates.
4. Hemi picks a candidate.
5. `Canva:create-design-from-candidate` returns `design_id`.
6. `Canva:export-design` twice (format `pdf`, format `pptx`).
7. Save outputs:
   - `proposals/<slug>/06-assembly/proposal-canva.pdf`
   - `proposals/<slug>/06-assembly/proposal-canva.pptx`
   - Canva URL: `https://canva.com/design/<design_id>`

### Aspect ratio

16:9 (Canva default). No resize, no workaround. v2.7 drops the 4:3 enforcement.

### Voice rules (still non-negotiable)

- Hebrew-first, all client-facing text in Hebrew
- No em-dash, no en-dash
- Max 5-7 words per on-slide bullet; depth in speaker notes
- Specific numbers, not adjectives
- Banned clichés: "בלתי נשכח", "מרגש", "חוגגים יחד", "unforgettable", "once in a lifetime"
- Bold credit only via the centered footer text "A Bold Presentation© [year]"

### Brand styling

- Pass `brand_kit_id` from `data/canva-config.json` if available
- `style` parameter: pick from "minimalist" | "elegant" | "modular" | "geometric" | custom string matching brand-system.md keywords
- `additionalInstructions`: Hebrew-first, banned clichés, footer text, palette hints from brand-system.md

### Fallback

If Canva MCP is not connected at runtime, log to summary.md and skip the Canva surface. Gamma + premium-deck-strategist PDF (legacy) become the deliverables instead.

### Slide outline (16 cards)

The same outline used for Gamma:

1. Cover, tagline from brand-system.md §3
2. The moment, reason-why from brief field 1
3. Strategic reading, 3 insights from challenges.md
4. Concept, brand-system.md §1-2
5. Arrival mockup
6. Hero moment mockup
7. Main space mockup
8. Detail mockup
9. Culinary
10. Experience flow, 3 anchors from agenda.md
11. Operations
12. Investment
13. KPIs
14. Timeline
15. Next steps
16. Closing

---

## 3. Building the Gamma deck (default interactive surface)

`gamma_generate` with `exportAs: "pptx"` and `wait: true` returns a result object containing `gammaUrl` (live, shareable, commentable) and `exportUrl` (signed URL to PPTX, valid ~1 week).

### Theme resolution

`gamma_list_themes`, pick a theme matching brand-system.md keywords. Fall back to a Bold-default theme if no clear match.

### Invocation

```
gamma_generate(
  inputText: <16-card outline, same as Canva but with punctuation kept>,
  format: "presentation",
  numCards: 16,
  themeId: <resolved>,
  folderIds: [<Bold-Proposals folder id, cached in data/gamma-config.json>],
  cardOptions: { dimensions: "16x9" },                 // v2.7: 16x9, was 4x3
  textOptions: {
    language: "he",
    tone: <one adjective from brand-system.md §4>,
    audience: <brief.md field 6 condensed>,
    amount: "medium"
  },
  imageOptions: {
    source: "aiGenerated",
    style: <from brand-system.md §8>
  },
  additionalInstructions: "Hebrew-first. No em-dash. No clichés. Specific numbers. Footer: 'A Bold Presentation© [current year]' centered in small gray text.",
  exportAs: "pptx",
  wait: true,
  pollTimeoutMs: 900000
)
```

### After the call

Download PPTX from `exportUrl` to `proposals/<slug>/06-assembly/proposal-gamma.pptx`. Embed `gammaUrl` in `summary.md`.

### Returning clients: `gamma_generate_from_template`

When the client profile has a prior `gammaId`, call `gamma_generate_from_template` instead. Same outline, same `exportAs: "pptx"`. Preserves layout from the winning prior deck.

### Fallback

If Gamma MCP not connected: write `gamma-prompt.md` from `assets/gamma-prompt-template.md`. Hemi pastes manually. PPTX skipped in fallback (Canva PPTX still ships).

---

## 4. Building the KPIs scorecard (kpis-scorecard.md)

Unchanged from v2.1.

---

## 5. Building the summary (summary.md)

### Template (v2.7)

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

**ההצעה בכמה גרסאות משלימות:**
- **מצגת ב-Canva:** [canvaUrl], לעריכה ושיתוף בסביבת Canva
- **מצגת ב-Gamma:** [gammaUrl], לצפייה אינטראקטיבית ותגובות
- **PowerPoint להורדה:** מצורף proposal-canva.pptx + proposal-gamma.pptx
- **PDF להדפסה / להפצה לוועדה:** מצורף proposal-canva.pdf

**מצורפים נוספים:**
- תקציב מפורט (Excel, פורמט "טמפלט תקציב 01" הקנוני של Bold)
- KPIs scorecard (Markdown)
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

If Canva MCP is unavailable, drop the Canva URL/PPTX/PDF bullets and add: "PDF הופק ב-premium-deck-strategist (fallback)."
If Gamma MCP is unavailable, drop the Gamma bullets and add: "מצגת Gamma תופק ידנית; קישור יישלח בנפרד."

---

## 6. Creating the Trello debrief card

Card goes into "Bold, Debriefs" board with due date = event date + 1. Description includes:
- `gammaId` (for `gamma_generate_from_template` next time)
- Canva `design_id` (for reference; no remix tool yet but useful for manual duplication)
- Link to all five deck artifacts

---

## Final QA checklist (v2.7)

### Canva surface
- [ ] Canva MCP connected
- [ ] `data/canva-config.json` present (or brand_kit_id intentionally omitted)
- [ ] Outline approved by Hemi via widget
- [ ] Candidate picked by Hemi
- [ ] `proposal-canva.pdf` downloaded and opens
- [ ] `proposal-canva.pptx` downloaded and opens in PowerPoint
- [ ] Canva URL captured for summary.md

### Gamma surface
- [ ] Gamma deck status=completed, gammaUrl present
- [ ] Gamma cardDimensions = "16x9"
- [ ] `proposal-gamma.pptx` downloaded from exportUrl, opens in PowerPoint
- [ ] gammaId captured for Trello card

### Voice and content
- [ ] All client-facing surfaces Hebrew-first
- [ ] No em-dash or en-dash anywhere
- [ ] No banned clichés
- [ ] No Bold credits outside the centered footer text
- [ ] Investment slide totals match budget.xlsx total across all surfaces
- [ ] KPI slides match scorecard

### Files and metadata
- [ ] Excel produced via `build_budget_xlsx.py` v3.0
- [ ] Excel uses Bold's canonical 6-category tree with single "דמי ארגון והפקה" line
- [ ] Summary.md word count under 280 words
- [ ] Summary.md lists all available surfaces (skips ones whose MCP was unavailable)
- [ ] Valid-until date consistent everywhere
- [ ] Event name + client name spelled identically across files
- [ ] Trello card created, URL in summary.md

---

## Present-files call

```
[
  "proposals/<slug>/06-assembly/proposal-canva.pdf",
  "proposals/<slug>/06-assembly/proposal-canva.pptx",
  "proposals/<slug>/06-assembly/proposal-gamma.pptx",
  "proposals/<slug>/06-assembly/budget.xlsx",
  "proposals/<slug>/06-assembly/kpis-scorecard.md",
  "proposals/<slug>/06-assembly/summary.md"
]
```

Then output:
```
✓ ההצעה מוכנה.
  Canva: [canvaUrl]
  Gamma: [gammaUrl]
  Trello debrief: [trelloUrl]
```

---

## Dependencies

### Required at runtime

- Bold Gamma MCP server: `gamma-mcp-server-production-959b.up.railway.app/sse`. Without it, Gamma surface skipped.
- Canva MCP: `mcp.canva.com/mcp`. Without it, Canva surface skipped.
- `scripts/build_budget_xlsx.py` v3.0
- `assets/budget-categories-reference.md` for category validation

### Optional

- `assets/logos/bold-black-opening.jpg` and `bold-white-footer.jpg` for manual post-export logo paste in Canva. Skill can ship without these but the deck will have only the centered footer text.
- Bold Canva brand kit ID (cached in `data/canva-config.json`). Without it, Canva styles from `style` parameter and prompt only.
- `premium-deck-strategist` skill, used as a legacy fallback only when both Canva and Gamma MCPs are unavailable.

### Legacy / historical

- `assets/bold-presentation-template-spec.md` documents Bold's 2007-2025 4:3 deck. v2.7 no longer enforces this spec but the file stays in the repo as historical reference and may inform Bold-style prompts (Tahoma type system, footer composition concept).

If Canva and Gamma are both unavailable, fall back to `premium-deck-strategist` PDF with a warning to Hemi. The skill never blocks; it ships whatever surfaces are reachable.
