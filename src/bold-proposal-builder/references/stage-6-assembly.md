# Stage 6, Assembly Reference (v2.9)

## Purpose

Stage 6 is production, not thinking. The thinking happened in stages 1 to 5. Stage 6 takes the artifacts and builds the client-facing package:

1. **Canva deck** - live URL + PDF export. No PPTX from Canva.
2. **Gamma deck** - live URL only. No PPTX from Gamma.
3. **Native Bold PPTX** - built directly with python-pptx. This is the ONLY .pptx the client receives.
4. **`budget.xlsx`** - detailed Excel in Bold's canonical template, produced by `scripts/build_budget_xlsx.py`.
5. **`kpis-scorecard.md`** - standalone KPI measurement plan.
6. **`summary.md`** - 1-page executive summary.
7. **Trello debrief card** in the "Bold, Debriefs" board, due day after the event.

Order: XLSX first (numbers lock), then Canva (visual flagship), then Gamma (interactive), then native PPTX, then KPIs scorecard, then summary, then Trello card.

**v2.9 changes (current):**
- Native Bold PPTX added as standalone third surface, built with python-pptx. Not an export.
- PPTX export removed from Canva flow. PPTX export removed from Gamma flow.
- Client receives exactly one .pptx file.
- Closing slide: animated MP4 full-bleed, no footer. Black variant default, white variant when deck background is white. Drive IDs documented below.
- Real-images rule added and enforced at gate before Stage 4a and before PPTX build.

**v2.7/v2.8 changes (historical):** 4:3 dropped, 16:9 adopted, Canva made mandatory, dual-layer margin documented.

---

## CRITICAL: The real-images rule

**All mockups, atmosphere videos, and entertainer visuals in the proposal must use real photos and videos provided by Hemi - not AI-generated imagery.**

### Venue visuals
- Before Stage 4a begins, Hemi must provide real photos or video of the actual event venue.
- All mockups produced in Stage 4a (hero, full set, atmosphere video) use these real venue photos as the base layer.
- nano-banana and veo-video-creator receive the real venue images as reference media, not a text description of an imagined space.
- If no venue photos are provided, Claude MUST ask Hemi for them before proceeding. Stage 4a does not start without real venue media.

### Entertainer and artist visuals
- If the proposal includes named entertainers, bands, artists, or performers (from Stage 4b), the slides featuring them in the native PPTX must include real, high-quality photos of those performers.
- Claude searches for good press/official photos using web search or asks Hemi to provide them.
- AI-generated performer imagery is never used.
- If no good real photo can be found, the slide uses text-only layout for that performer.

### In the native PPTX specifically
- Every slide that shows a venue space uses a real venue photo as background or as a full-bleed image.
- Every entertainer slide includes at minimum one real photo.
- Gamma and Canva `imageOptions.source` should be set to use uploaded/provided media where the MCP supports it; if not, set to "none" and note that images will be added manually post-export.

---

## 1. Building the Excel budget (budget.xlsx)

Run `scripts/build_budget_xlsx.py` against `05-budget/budget.json`.

Input requirements:
- Every `main_line` MUST have a `category` field from the 6 canonicals: כללי / תקשור מקדים / מיתוג ושילוט / טכני / כח אדם ולוגיסטיקה / שונות.
- Non-canonical categories are not silently dropped; the script warns and rolls them into שונות.
- `conditional_lines` is optional; conditional items go flat under a single כללי marker in the options section.
- `production_fee_rate` defaults to 0.15.

Output: `06-assembly/budget.xlsx`, single sheet "טמפלט ריק", 13 columns RTL, main + options sections.

---

## 2. Building the Canva deck (live URL + PDF only)

Full flow in `references/canva-deck-path.md`. Produces two artifacts: live URL + PDF. No PPTX.

### Pre-conditions

- Canva MCP connected (`mcp.canva.com/mcp`).
- Real venue photos available (per real-images rule above).
- Bold Canva brand kit ID cached in `data/canva-config.json` (optional but preferred).

### High-level flow

1. Resolve brand kit (or run `Canva:list-brand-kits` first time and cache).
2. `Canva:request-outline-review` with the 16-card outline. Strip all punctuation from titles and descriptions (Canva-MCP requirement). Hemi reviews + approves in widget.
3. `Canva:generate-design-structured` with `design_type: "presentation"`. Returns design candidates.
4. Hemi picks a candidate.
5. `Canva:create-design-from-candidate` returns `design_id`.
6. `Canva:export-design` once (format `pdf` only).
7. Save outputs:
   - `proposals/<slug>/06-assembly/proposal-canva.pdf`
   - Canva URL: `https://canva.com/design/<design_id>`

### Aspect ratio

16:9. No resize.

### Voice rules

- Hebrew-first, all client-facing text in Hebrew.
- No em-dash, no en-dash.
- Max 5-7 words per on-slide bullet; depth in speaker notes.
- Specific numbers, not adjectives.
- Banned clichés: "בלתי נשכח", "מרגש", "חוגגים יחד", "unforgettable", "once in a lifetime".
- Bold credit only via the centered footer text "A Bold Presentation© [year]".

### Fallback

If Canva MCP is not connected at runtime, log to summary.md and skip the Canva surface.

---

## 3. Building the Gamma deck (live URL only)

`gamma_generate` with `wait: true` returns a result object containing `gammaUrl`. No `exportAs` call.

### Invocation

```
gamma_generate(
  inputText: <16-card outline, same structure as Canva but with punctuation kept>,
  format: "presentation",
  numCards: 16,
  themeId: <resolved from gamma_list_themes, matching brand-system.md keywords>,
  folderIds: [<Bold-Proposals folder id, cached in data/gamma-config.json>],
  cardOptions: { dimensions: "16x9" },
  textOptions: {
    language: "he",
    tone: <one adjective from brand-system.md section 4>,
    audience: <brief.md field 6 condensed>,
    amount: "medium"
  },
  imageOptions: {
    source: "none"
  },
  additionalInstructions: "Hebrew-first. No em-dash. No clichés. Specific numbers. Footer: 'A Bold Presentation© [current year]' centered in small gray text.",
  wait: true,
  pollTimeoutMs: 900000
)
```

Note: `imageOptions.source` is set to "none" because real images will be in the native PPTX. Gamma serves as the interactive/commentable surface, not the visual flagship.

### After the call

Embed `gammaUrl` in `summary.md`. Capture `gammaId` for Trello card.

### Returning clients

When the client profile has a prior `gammaId`, call `gamma_generate_from_template` instead. Same outline. Preserves layout from the winning prior deck.

### Fallback

If Gamma MCP not connected: write `gamma-prompt.md` from `assets/gamma-prompt-template.md`. Hemi pastes manually.

---

## 4. Building the native Bold PPTX

This is the only .pptx the client receives. Built with python-pptx in `scripts/build_budget_xlsx.py` or a dedicated `scripts/build_pptx.py` (whichever the session implements). All 16:9 (33.867 cm x 19.05 cm = 13.333 in x 7.5 in).

### Slide structure

**Cover slide (slide 1):**
- Full-bleed real venue photo or hero mockup from Stage 4a. Image fills 100% of slide.
- No footer.
- Client event name and tagline (from brand-system.md section 3) overlaid in white text, bottom-left area, with a semi-transparent backing if needed for legibility.

**Body slides (slides 2 to N-1):**
- Content per the 16-card outline.
- Slides that reference a venue space: use a real venue photo as background or as a prominent image block.
- Slides that reference an entertainer or artist: include a real photo of that performer (see real-images rule above).
- Footer on every body slide:
  - Bottom-left: white Bold logo (`assets/logos/bold-white-footer.jpg`). Height: ~1 cm. Positioned 0.5 cm from left and 0.4 cm from bottom.
  - Bottom-center: "A Bold Presentation© [year]" in Verdana 14pt, color #808080. Vertically aligned with logo.
  - Bottom-right: client logo (provided by Hemi or fetched from brief). Same height as Bold logo. Positioned 0.5 cm from right and 0.4 cm from bottom.
- No other Bold branding anywhere on the slide.

**Closing slide (last slide):**
- Full-bleed animated MP4 embedded as a movie shape, covering 100% of slide area.
- No footer, no text overlay.
- Variant selection:
  - If the deck's primary slide background color is white or near-white (#FFFFFF to #F0F0F0): use `White.mp4` (Drive ID: `1reQG6f2nd2F4W0nkxI5XPubM2SjkFGwD`).
  - All other cases (default): use `Black.mp4` (Drive ID: `1rd4HYz2O54ipI71jzER_4NwCyj-_GA2J`).
- The MP4 files are cached locally at `assets/closing/`. If not present, fetch from Drive via Google Drive MCP before building.

### python-pptx implementation notes

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

# Slide dimensions: 16:9
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Footer constants
FOOTER_BOLD_LOGO = "assets/logos/bold-white-footer.jpg"
FOOTER_TEXT = f"A Bold Presentation\u00A9 {year}"
FOOTER_FONT = "Verdana"
FOOTER_SIZE = Pt(14)
FOOTER_COLOR = RGBColor(0x80, 0x80, 0x80)
FOOTER_HEIGHT = Inches(0.4)
FOOTER_BOTTOM_MARGIN = Inches(0.16)

# Closing slide: embed MP4
# python-pptx adds video via add_movie (requires pptx >= 0.6.21)
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
movie = slide.shapes.add_movie(
    mp4_path,
    left=0, top=0,
    width=prs.slide_width, height=prs.slide_height,
    poster_frame_image=poster_path,  # first frame or black frame
    mime_type="video/mp4"
)
```

### Slide count

16 slides matching the outline in section 2. If a section has no content (e.g., no entertainer), that card is skipped and slide count adjusts.

### Output

`proposals/<slug>/06-assembly/proposal-bold.pptx`

---

## 5. Building the KPIs scorecard (kpis-scorecard.md)

Unchanged from v2.1.

---

## 6. Building the summary (summary.md)

### Template (v2.9)

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
- השקעה: [Z] + מע"מ | שורות מותנות בנפרד
- תוקף ההצעה: עד [YYYY-MM-DD]

**איך נמדוד הצלחה:**
הגדרנו [N] מדדי הצלחה בהתאם למטרות שהעלית. פירוט ב-kpis-scorecard.md המצורף.
24 שעות אחרי האירוע, נעשה debrief מסודר ותקבל דוח מול המדדים.

**ההצעה בכמה גרסאות משלימות:**
- **מצגת ב-Canva:** [canvaUrl], לעריכה ושיתוף בסביבת Canva
- **מצגת ב-Gamma:** [gammaUrl], לצפייה אינטראקטיבית ותגובות
- **PowerPoint להורדה:** מצורף proposal-bold.pptx
- **PDF להדפסה / להפצה לוועדה:** מצורף proposal-canva.pdf

**מצורפים נוספים:**
- תקציב מפורט (Excel)
- KPIs scorecard
- סרטון האווירה (MP4)

שמח לדבר מתי שיתאים.

[Signature]
```

If Canva MCP is unavailable: drop Canva URL + PDF bullets, add "PDF יופק ידנית."
If Gamma MCP is unavailable: drop Gamma bullet, add "מצגת Gamma תופק ידנית; קישור יישלח בנפרד."
Native PPTX is always produced regardless of MCP availability.

---

## 7. Creating the Trello debrief card

Card goes into "Bold, Debriefs" board with due date = event date + 1. Description includes:
- `gammaId` (for `gamma_generate_from_template` next time)
- Canva `design_id`
- Link to `proposal-bold.pptx`, `proposal-canva.pdf`, `budget.xlsx`

---

## Final QA checklist (v2.9)

### Real images gate (before Stage 4a AND before PPTX build)
- [ ] Real venue photos received from Hemi
- [ ] Photos used as base in Stage 4a mockups and atmosphere video
- [ ] Named entertainers / artists identified in proposal
- [ ] Real photos sourced for each named entertainer (web search or provided by Hemi)

### Canva surface
- [ ] Canva MCP connected
- [ ] Outline approved by Hemi via widget
- [ ] Candidate picked by Hemi
- [ ] `proposal-canva.pdf` downloaded and opens
- [ ] Canva URL captured for summary.md
- [ ] No PPTX exported from Canva

### Gamma surface
- [ ] Gamma deck status=completed, gammaUrl present
- [ ] Gamma cardDimensions = "16x9"
- [ ] No PPTX exported from Gamma
- [ ] gammaId captured for Trello card

### Native Bold PPTX
- [ ] `assets/closing/Black.mp4` or `White.mp4` present (fetched from Drive if needed)
- [ ] Closing MP4 variant matches deck background color
- [ ] Cover slide: full-bleed real image, no footer
- [ ] All body slides: footer present (Bold logo BL + centered text + client logo BR)
- [ ] Entertainer slides: real photos included
- [ ] Venue slides: real photos used
- [ ] Closing slide: MP4 full-bleed, no footer
- [ ] `proposal-bold.pptx` opens in PowerPoint and closing MP4 plays

### Voice and content
- [ ] All client-facing surfaces Hebrew-first
- [ ] No em-dash or en-dash anywhere
- [ ] No banned clichés
- [ ] No Bold credits outside the centered footer text
- [ ] Investment slide totals match budget.xlsx across all surfaces
- [ ] KPI slides match scorecard

### Files and metadata
- [ ] Excel produced via `build_budget_xlsx.py` v4.0
- [ ] Summary.md lists all available surfaces
- [ ] Valid-until date consistent everywhere
- [ ] Event name + client name spelled identically across files
- [ ] Trello card created, URL in summary.md

---

## Present-files call

```
[
  "proposals/<slug>/06-assembly/proposal-bold.pptx",
  "proposals/<slug>/06-assembly/proposal-canva.pdf",
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
- `scripts/build_budget_xlsx.py` v4.0
- `assets/budget-categories-reference.md` for category validation
- `assets/logos/bold-white-footer.jpg` for PPTX footer. Required for native PPTX.
- `assets/closing/Black.mp4` or `White.mp4` - fetched from Drive at build time if not cached.
- Real venue photos from Hemi - required before Stage 4a and before PPTX build.

### Optional

- Bold Canva brand kit ID (cached in `data/canva-config.json`).
- `premium-deck-strategist` skill - legacy fallback only if both Canva and Gamma MCPs are unavailable.

### Legacy / historical

- `assets/bold-presentation-template-spec.md` documents Bold's 2007-2025 4:3 deck. No longer enforced.
- `proposal-canva.pptx` and `proposal-gamma.pptx` no longer produced as of v2.9.
