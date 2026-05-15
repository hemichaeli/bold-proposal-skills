---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow, brief gathering, research, three-direction brand heart selection, three-direction visualization, content/operations/culinary specialists, budget, assembly, and post-event debrief. Use whenever Hemi Michaeli asks to build, draft, or prepare a proposal or event concept for a Bold client. Also triggers for "לבנות הצעה", "פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Mentions of Phoenix, Keren, Efrat clients also trigger. Produces a client-facing package across three deck surfaces (live Canva deck, live Gamma deck, downloadable PPTX from both), PDF export, strategy, brand system, mockups, atmosphere video, agenda, scripts, menu, operations, budget XLSX in Bold's canonical 6-category format, KPIs scorecard, and Trello debrief reminder. Default 16:9. Requires nano-banana, veo-video-creator, plus Gamma and Canva MCP servers.
license: Proprietary
---

# Bold Proposal Builder (v2.8)

A 7-stage orchestrator for producing premium event proposals for Bold Productions. Each stage reads a reference file in `references/`, produces its artifacts, hands off. Skip stages and the final proposal fragments.

## Branding mode (ask first)

At session start, before Stage 1, ask Hemi:

> Apply the full Bold-branded layout (logos + footer), or produce a clean unbranded deck?

If **Bold-branded** (the default for any client-facing proposal): apply the per-slide-type spec described in the `Logo and footer handling` section below. Use the Bold Canva brand kit if available. Pick a Bold-aligned Gamma theme.

If **clean / unbranded** (used for early internal drafts before client sign-off, white-label events Bold is producing under the client's own brand, or any deck that should not visibly read as "by Bold"): skip the entire logo and footer apparatus. No `bold-black-opening.jpg` on the opening slide, no `bold-white-footer.jpg` bottom-left, no centered footer text, no `bold-closing.mp4` on the closing slide. Voice rules and the seven-stage flow still apply; only the visible Bold branding is suppressed.

The answer is recorded in `proposals/<slug>/summary.md` as `branding_mode: bold-branded | clean`.

Default: ask, do not assume.

## The seven stages

| Stage | Name | Reference | Output |
|---|---|---|---|
| 1 | Intake & Brief | `references/stage-1-intake.md` | `brief.md`, `challenges.md`, KPIs |
| 2 | Research | `references/stage-2-research.md` | `trends.md`, `case-studies.md`, `inspiration.md` |
| 3 | Brand heart, 3 directions | `references/stage-3-brand-heart.md` | `directions.md`, `brand-system.md` |
| 4a | Visualization, 3 directions | `references/stage-4a-visualization.md` | hero mockups, full set, atmosphere video, `mood-direction.md` |
| 4b | Content & experience | `references/stage-4b-content-experience.md` | `agenda.md`, `scripts.md` |
| 4c | Operations | `references/stage-4c-operations.md` | `logistics.md` |
| 4d | Culinary | `references/stage-4d-culinary.md` | `menu.md` |
| 5 | Budget | `references/stage-5-budget.md` + `assets/budget-categories-reference.md` | `budget.json` (6-category canonical tree) |
| 6 | Assembly | `references/stage-6-assembly.md` + `references/canva-deck-path.md` | **Canva deck** (URL + PDF + PPTX) + **Gamma deck** (URL + PPTX) + budget XLSX + scorecard + summary + Trello card |
| 7 | Debrief | `references/stage-7-debrief.md` | `debrief-[event].md`, client profile (with `gammaId` and Canva `design_id`), preferences update |

## The four goal categories

1. שיווקית (Marketing)
2. Fun (Experience)
3. מכירתית (Sales)
4. תדמיתית (Reputation)

## Marketing moves - when to invoke marketing-council

At Stage 1 intake, identify whether the event has a **שיווקית (Marketing)** goal or requires marketing moves before, during, or after the event. Examples:

- Pre-event: awareness campaign, email invitations, social media, paid ads, press
- During event: live social content, UGC activation, influencer presence
- Post-event: media coverage, recap content, lead nurturing from attendees

If marketing moves are part of the proposal scope, **invoke `marketing-council`** after Stage 1 (or after Gate 3 once the brand heart is chosen) to build the marketing layer alongside the event plan.

`marketing-council` produces a MARKETING-PLAN.md that becomes an appendix to the Bold proposal package. The brand system and visual direction from Stage 3 are passed to marketing-council as the creative foundation - so the marketing assets are consistent with the event concept.

When to invoke:
- Client explicitly requests marketing deliverables as part of the proposal
- Goal category is primarily or partially שיווקית
- Event has a pre-event awareness or ticket-sales phase
- Client is a brand (not an internal corporate event) that needs content amplification
- Budget includes a line for "תקשור מקדים" beyond simple digital invitations

When NOT to invoke:
- Internal corporate event (no external audience)
- Event is fully closed / VIP with no amplification need
- Client explicitly said marketing is handled by their own team

## The three-directions principle

Both Stage 3 and Stage 4a propose three distinct directions along a chosen axis. Each direction has a visual representation. Hemi picks one. If none land, Claude asks one clarifying question, picks a different axis, proposes three new. Max 3 rejection cycles per stage. Stretch policy: always one stretch direction per set.

### Learning Hemi over time
Every selection logged to `data/hemi-preferences.md`. Read at start of every Stage 3 and Stage 4a session.

## The budget spine (Bold's canonical 6-category tree)

Bold has used the same 6 top-level budget categories since 2010. Stage 5 does NOT invent categories; it picks from this spine:

1. כללי (General)
2. תקשור מקדים (Pre-event communications)
3. מיתוג ושילוט (Branding & signage)
4. טכני (Technical)
5. כח אדם ולוגיסטיקה (Staff & logistics)
6. שונות (Miscellaneous)

Underneath the six sit 30 sub-categories and ~140 typical line items. Full tree in `assets/budget-categories-reference.md` (sourced from "Copy of Copy of תבנית מתודולוגית לאירועים 4.xls" sheet 1, in use at Bold since 2004).

XLSX layout matches Bold's actual template "טמפלט תקציב 01" (in use since 2010): 13 columns RTL, single sheet "טמפלט ריק", main + options sections. Production fee: single "דמי ארגון והפקה" line at 15% after the six categories. Conditional items live in the options section under a single כללי marker. Script: `scripts/build_budget_xlsx.py` v3.0.

## The deck surfaces (Stage 6, v2.8)

Every Bold proposal ships in two default deck surfaces, producing five artifacts from two MCP calls:

| Source | Live URL | PPTX | PDF |
|---|---|---|---|
| Canva (`generate-design-structured`) | yes | yes | yes |
| Gamma (`gamma_generate`) | yes | yes (via `exportAs`) | no |

The two are not redundant: Canva is the polished designed deck (visual flagship + printable PDF), Gamma is the interactive shareable deck (commentable, fast). Both are 16:9 (Canva and Gamma native).

The historical Bold 4:3 template (`assets/bold-presentation-template-spec.md`) is preserved as a legacy reference file but no longer enforced. v2.7 dropped the 4:3 constraint.

### Brand identity in the deck

Voice rules apply to all surfaces:
- Hebrew-first
- No em-dash, no en-dash
- No cliches ("בלתי נשכח", "מרגש", "unforgettable", "חוגגים יחד", "once in a lifetime")
- Specific numbers, not adjectives
- Max 5-7 words per on-slide bullet

Brand kit (Canva): if `data/canva-config.json` has a `brand_kit_id`, pass it. Brand consistency comes from there.
Theme (Gamma): pick best match from `gamma_list_themes` against brand-system.md keywords.

### Logo and footer handling

Bold's canonical per-slide-type logo and footer spec, in use since 2010. **Applied only when `branding_mode = bold-branded`.** When `branding_mode = clean`, the entire spec is suppressed.

| Slide type | Hero / main visual | Bottom-left | Bottom-right | Centered footer text |
|---|---|---|---|---|
| Opening | `bold-black-opening.jpg` (full bleed, centered on black background) | none | none | none |
| Body slides | content | `bold-white-footer.jpg` (small, ~120-150px wide) | client logo (small) | `A Bold Presentation© [year]` |
| Closing | `bold-closing.mp4` (full bleed, autoplay, animated) | none | none | none |

The `[year]` token is replaced with the event year (4 digits, Western numerals) at deck-assembly time. Footer text rendered Verdana 14pt, gray `#808080`, horizontally centered.

#### Asset locations and source of truth

| File | Repo location | Source of truth | Travel mechanism |
|---|---|---|---|
| `bold-black-opening.jpg` | `assets/logos/` | packaged with .skill | binary, not in Git, manual placement at build time |
| `bold-white-footer.jpg` | `assets/logos/` | packaged with .skill | binary, not in Git, manual placement at build time |
| `bold-closing.mp4` | `assets/logos/` (fallback only) | Bold's Google Drive | binary, not in Git. Stage 6 fetches from Drive at runtime; if fetch fails, falls back to the packaged copy |
| Client logo | `data/client-assets/<slug>/` | client-provided | requested in brief at Stage 1 |

#### Placement at build time

Canva: a properly configured brand kit handles bottom-left + footer text + bottom-right slot automatically. If the kit lacks any of them, paste manually post-export. Insert the closing MP4 as a video element on the last slide.

Gamma: paste the bottom-left, bottom-right, and footer text manually post-export if the chosen theme does not supply them. Insert the closing MP4 on the last slide.

In both surfaces: opening and closing slides do NOT carry the body-slide footer stripe. Their hero asset (black JPG / animated MP4) is the entire slide.

## Voice rules (apply everywhere)

- Hebrew-first. Numbers Western. Dates DD.MM.YYYY.
- No em-dash or en-dash.
- No cliches.
- Specific numbers, not adjectives.
- Short paragraphs.
- Max 5-7 words per on-slide bullet; depth in speaker notes.

## Gates

- Gate 0->1: Branding mode answered (bold-branded or clean).
- Gate 1->2: Brief fields 1, 3, 6, 14, 16 filled.
- Gate 2->3: 3 trends + 3 case studies + 5 inspirations.
- Gate 3->4: One direction picked from three-direction set; brand-system.md has 9 fields.
- Gate 4a->rest: One visual direction picked; full mockup set + video + mood-direction.md.
- Gate 4->5: All specialists reference brand system + visual.
- Gate 5->6: Every line maps to one of the 6 canonical categories; 70%+ lines reference vendor registry; no line without `source_deliverable`.
- Gate 6->done: Six core artifacts (Canva URL+PDF+PPTX, Gamma URL+PPTX, XLSX, scorecard, summary, Trello card). If a deck MCP is unavailable at runtime, that surface is skipped (not blocked) and summary.md notes the gap.
- Gate 7: Runs 24h after event from Trello card.

## Required sibling skills

| Skill | Used in | Role |
|---|---|---|
| `nano-banana` | Stage 3, 4a | Visual reference images, mockups |
| `veo-video-creator` | Stage 4a | Atmosphere video |
| `marketing-council` | Stage 1 (conditional) | Full marketing plan when proposal has marketing scope - see "Marketing moves" section above |
| `premium-deck-strategist` | Legacy fallback only | Used if both Canva and Gamma MCPs are unavailable |

## Required MCP servers

| MCP server | Used in | Role |
|---|---|---|
| Gamma (custom Bold-operated, `gamma-mcp-server-production-959b.up.railway.app/sse`) | Stage 6, Stage 7 | `gamma_generate` builds the live Gamma deck and the downloadable PPTX. `gamma_generate_from_template` remixes the prior deck for returning clients (Phoenix, Keren, Efrat) |
| Canva (`mcp.canva.com/mcp`) | Stage 6 | `request-outline-review` -> `generate-design-structured` -> `create-design-from-candidate` -> `export-design` produces the Canva deck with PDF + PPTX exports |

If either MCP is missing at runtime, that surface is skipped silently and summary.md flags it. If both are missing, Stage 6 falls back to `premium-deck-strategist` PDF.

## Assets in the skill package

| Asset | Purpose |
|---|---|
| `assets/bold-brand-guidelines.md` | Bold's verbal brand rules |
| `assets/brief-form-original.md` | Bold's original 2001-era brief form |
| `assets/gamma-prompt-template.md` | Fallback prompt template for Gamma when MCP is unavailable |
| `assets/proposal-pdf-structure.md` | PDF structure reference (legacy) |
| `assets/budget-categories-reference.md` | 6 canonical categories + 30 sub-categories + ~140 line items |
| `assets/bold-presentation-template-spec.md` | **Legacy 4:3 template spec** (2007-2025). Kept for historical reference; no longer enforced as of v2.7 |
| `assets/logos/bold-black-opening.jpg` | Black Bold logo for opening slide hero (binary, packaged with .skill, not in Git) |
| `assets/logos/bold-white-footer.jpg` | White Bold logo for body-slide bottom-left (binary, packaged with .skill, not in Git) |
| `assets/logos/bold-closing.mp4` | Animated closing-slide hero (binary, packaged as fallback only; Bold's Google Drive is source of truth) |
| `assets/logos/README.md` | Logo and footer placement rules |
| `scripts/build_budget_xlsx.py` v3.0 | Produces budget.xlsx in Bold's canonical template format |

## Session start

1. Ask the branding mode question (see `## Branding mode (ask first)` above). Record the answer in the proposal's `summary.md`.
2. Check for brief/transcript input.
3. Read client profile if known (includes `gammaId` of prior deck for remix, Canva `design_id` for reference).
4. Read `data/hemi-preferences.md`.
5. Verify vendor registry.
6. Verify required sibling skills (nano-banana, veo-video-creator).
7. Verify Gamma MCP is connected. If absent, note that the Gamma surface will be skipped.
8. Verify Canva MCP is connected. If absent, note that the Canva surface will be skipped.
9. If both Canva and Gamma MCPs are absent, verify `premium-deck-strategist` is installed for fallback.
10. Verify `data/canva-config.json` exists or run `Canva:list-brand-kits` first time and cache.
11. Begin Stage 1.

## Success

Final deliverable: a client who, 30 days after the event, can say "Bold helped me hit these specific numbers". Secondary: over 5-10 events, three-direction sets land more often. Tertiary: returning clients get increasingly well-tuned proposals because `gamma_generate_from_template` and the Bold Canva brand kit preserve what worked.

## Hebrew/RTL OOXML Authoring Rules

When the deck is in Hebrew (or any RTL language), follow these rules to prevent bidi/spell-check defects. Every rule was learned from a real defect in production decks.

### 1. `lang` attribute on every run
Every `<a:rPr>` must declare a language. Hebrew runs: `lang="he-IL"`. English/numeric/punctuation-only runs: `lang="en-US"`. **Missing `lang` causes red spell-check squiggles AND breaks the bidi engine's ordering.**

### 2. Never split a Hebrew word across runs
A single Hebrew word = a single `<a:r>`. Splitting across two runs lets the bidi engine treat the two halves as independent segments and any punctuation between them lands in the wrong visual position.

### 3. Punctuation belongs in the Hebrew run
Commas, periods, colons, semicolons, quotation marks adjacent to Hebrew text must live **inside the same `<a:r>` as the Hebrew text**, not in a separate `lang="en-US"` run.

### 4. Prefer one Hebrew run per phrase
Write the entire sentence as a single `<a:r lang="he-IL">` whenever possible. Per-word splitting is the #1 source of bidi defects.

### 5. Strip `err="1"`
Never write `err="1"` on `<a:rPr>`. It produces visible red wavy underlines. When editing existing text, remove it.

### 6. Mixed numeric + Hebrew titles

Bold's convention: Hebrew topic word at visual right, numeric prefix at visual left. Write logical text Hebrew-first in a single `lang="he-IL"` run:

```xml
<a:p><a:pPr algn="r" rtl="1">...</a:pPr>
  <a:r><a:rPr lang="he-IL" .../><a:t>הרגעים החיים / 06</a:t></a:r>
</a:p>
```

DO NOT write number-first logical order. It inverts the visual layout.

### 7. Hebrew paragraphs need `algn="r" rtl="1"` on `<a:pPr>`

### 8. Tables: `cell.text =` does NOT persist
Use `edit_slide_xml` to rewrite `<a:txBody>` inside `<a:tc>`.

### 9. ASCII punctuation only
- U+2014 em-dash -> `-`
- U+2013 en-dash -> `-`
- U+2019 curly apostrophe -> `'`
- U+201C, U+201D curly double quotes -> `"`

### 10. Don't add `<a:latin>` unless changing the font

### Final QA pass before delivery
1. Regex `/[\u2014\u2013\u2019\u201C\u201D\u00B7\u2022]/g` across all slide XML.
2. Sweep every `<a:rPr>` in Hebrew text: `lang="he-IL"`, no `err="1"`.
3. Every "{number} / {Hebrew topic}" title: confirm logical text is Hebrew-first.
4. Spot-check 2-3 dense paragraphs visually for misplaced punctuation.
