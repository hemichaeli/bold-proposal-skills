---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow, brief gathering, research, three-direction brand heart selection, three-direction visualization, content/operations/culinary specialists, budget, assembly, and post-event debrief. Use whenever Hemi Michaeli asks to build, draft, or prepare a proposal or event concept for a Bold client. Also triggers for "לבנות הצעה", "פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Mentions of Phoenix, Keren, Efrat clients also trigger. Produces a client-facing package in three default deck surfaces (live Canva deck + live Gamma deck + downloadable PowerPoint files from both), plus PDF export from Canva, plus strategy, brand system, mockups, atmosphere video, agenda, scripts, menu, operations, budget XLSX in Bold's canonical 6-category template format, KPIs scorecard, and Trello debrief reminder. Default aspect ratio is 16:9 (Canva and Gamma native). Requires nano-banana and veo-video-creator skills for Stage 4, the Gamma MCP server, and the Canva MCP server for Stage 6.
license: Proprietary
---

# Bold Proposal Builder (v2.7)

A 7-stage orchestrator for producing premium event proposals for Bold Productions. Each stage reads a reference file in `references/`, produces its artifacts, hands off. Skip stages and the final proposal fragments.

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

## The deck surfaces (Stage 6, v2.7)

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
- No clichés ("בלתי נשכח", "מרגש", "unforgettable", "חוגגים יחד", "once in a lifetime")
- Specific numbers, not adjectives
- Max 5-7 words per on-slide bullet
- Bold credit only via the centered footer text "A Bold Presentation© [year]"

Brand kit (Canva): if `data/canva-config.json` has a `brand_kit_id`, pass it. Brand consistency comes from there.
Theme (Gamma): pick best match from `gamma_list_themes` against brand-system.md keywords.

### Logo handling

Logos still live in `assets/logos/` (`bold-black-opening.jpg`, `bold-white-footer.jpg`). They are no longer auto-placed at fixed coordinates. Use cases:
- Canva: paste manually post-export if the Canva brand kit doesn't include them, or save once into the brand kit
- Gamma: same, manual paste post-export if needed
- Cover slide: the black logo can still be used as a reference for "what Bold's cover looks like"

## Voice rules (apply everywhere)

- Hebrew-first. Numbers Western. Dates DD.MM.YYYY.
- No em-dash or en-dash.
- No clichés.
- Specific numbers, not adjectives.
- Short paragraphs.
- Max 5-7 words per on-slide bullet; depth in speaker notes.

## Gates

- Gate 1→2: Brief fields 1, 3, 6, 14, 16 filled.
- Gate 2→3: 3 trends + 3 case studies + 5 inspirations.
- Gate 3→4: One direction picked from three-direction set; brand-system.md has 9 fields.
- Gate 4a→rest: One visual direction picked; full mockup set + video + mood-direction.md.
- Gate 4→5: All specialists reference brand system + visual.
- Gate 5→6: Every line maps to one of the 6 canonical categories; 70%+ lines reference vendor registry; no line without `source_deliverable`.
- Gate 6→done: Six core artifacts (Canva URL+PDF+PPTX, Gamma URL+PPTX, XLSX, scorecard, summary, Trello card). If a deck MCP is unavailable at runtime, that surface is skipped (not blocked) and summary.md notes the gap.
- Gate 7: Runs 24h after event from Trello card.

## Required sibling skills

| Skill | Used in | Role |
|---|---|---|
| `nano-banana` | Stage 3, 4a | Visual reference images, mockups |
| `veo-video-creator` | Stage 4a | Atmosphere video |
| `premium-deck-strategist` | Legacy fallback only | Used if both Canva and Gamma MCPs are unavailable |

## Required MCP servers

| MCP server | Used in | Role |
|---|---|---|
| Gamma (custom Bold-operated, `gamma-mcp-server-production-959b.up.railway.app/sse`) | Stage 6, Stage 7 | `gamma_generate` builds the live Gamma deck and the downloadable PPTX. `gamma_generate_from_template` remixes the prior deck for returning clients (Phoenix, Keren, Efrat) |
| Canva (`mcp.canva.com/mcp`) | Stage 6 | `request-outline-review` → `generate-design-structured` → `create-design-from-candidate` → `export-design` produces the Canva deck with PDF + PPTX exports |

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
| `assets/logos/bold-black-opening.jpg` | Black Bold logo (binary, packaged with .skill, not in Git) |
| `assets/logos/bold-white-footer.jpg` | White Bold logo (binary, packaged with .skill, not in Git) |
| `assets/logos/README.md` | Logo usage rules |
| `scripts/build_budget_xlsx.py` v3.0 | Produces budget.xlsx in Bold's canonical template format |

## Session start

1. Check for brief/transcript input.
2. Read client profile if known (includes `gammaId` of prior deck for remix, Canva `design_id` for reference).
3. Read `data/hemi-preferences.md`.
4. Verify vendor registry.
5. Verify required sibling skills (nano-banana, veo-video-creator).
6. Verify Gamma MCP is connected. If absent, note that the Gamma surface will be skipped.
7. Verify Canva MCP is connected. If absent, note that the Canva surface will be skipped.
8. If both Canva and Gamma MCPs are absent, verify `premium-deck-strategist` is installed for fallback.
9. Verify `data/canva-config.json` exists or run `Canva:list-brand-kits` first time and cache.
10. Begin Stage 1.

## Success

Final deliverable: a client who, 30 days after the event, can say "Bold helped me hit these specific numbers". Secondary: over 5-10 events, three-direction sets land more often. Tertiary: returning clients get increasingly well-tuned proposals because `gamma_generate_from_template` and the Bold Canva brand kit preserve what worked.
