---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow, brief gathering, research, three-direction brand heart selection, three-direction visualization, content/operations/culinary specialists, budget, assembly, and post-event debrief. Use whenever Hemi Michaeli asks to build, draft, or prepare a proposal or event concept for a Bold client. Also triggers for "לבנות הצעה", "פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Mentions of Phoenix, Keren, Efrat clients also trigger. Produces a client-facing package in three complementary surfaces (premium PDF + live Gamma URL + editable PPTX) matching Bold's canonical 4:3 template with Tahoma-based type system and fixed footer composition, plus strategy, brand system, mockups, atmosphere video, agenda, scripts, menu, operations, budget XLSX in Bold's canonical 6-category template format, KPIs scorecard, and Trello debrief reminder. Requires nano-banana and veo-video-creator skills for Stage 4, premium-deck-strategist for Stage 6 PDF, and the Gamma MCP server for Stage 6 live deck + PPTX.
license: Proprietary
---

# Bold Proposal Builder (v2.6)

A 7-stage orchestrator for producing premium event proposals for Bold Productions. The skill does not improvise: each stage reads a reference file in `references/`, produces its artifacts, and hands off to the next. Skip stages and the final proposal fragments; the sequence is load-bearing.

## The seven stages

| Stage | Name | Reference | Output |
|---|---|---|---|
| 1 | Intake & Brief | `references/stage-1-intake.md` | `brief.md`, `challenges.md`, KPIs |
| 2 | Research | `references/stage-2-research.md` | `trends.md`, `case-studies.md`, `inspiration.md` |
| 3 | Brand heart, 3 directions | `references/stage-3-brand-heart.md` | `directions.md` then `brand-system.md` |
| 4a | Visualization, 3 directions | `references/stage-4a-visualization.md` | hero mockups, full set, atmosphere video, `mood-direction.md` |
| 4b | Content & experience | `references/stage-4b-content-experience.md` | `agenda.md`, `scripts.md` |
| 4c | Operations | `references/stage-4c-operations.md` | `logistics.md` |
| 4d | Culinary | `references/stage-4d-culinary.md` | `menu.md` |
| 5 | Budget | `references/stage-5-budget.md` + `assets/budget-categories-reference.md` | `budget.json` (6-category canonical tree) |
| 6 | Assembly | `references/stage-6-assembly.md` + `assets/bold-presentation-template-spec.md` + `assets/logos/` | **Premium PDF** (premium-deck-strategist, 4:3 Bold template) + **live Gamma URL** + **editable PPTX** (Gamma MCP `exportAs: "pptx"`), plus XLSX (Bold canonical template via `scripts/build_budget_xlsx.py` v3.0), KPIs scorecard, summary, Trello card |
| 7 | Debrief | `references/stage-7-debrief.md` | `debrief-[event].md`, client profile (including `gammaId` for remix), preferences update, skill PR |

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

Underneath the six sit 30 sub-categories and ~140 typical line items. Full tree, including the sub-category to canonical mapping: `assets/budget-categories-reference.md` (sourced from "Copy of Copy of תבנית מתודולוגית לאירועים 4.xls" sheet 1, in use at Bold since 2004).

XLSX layout matches Bold's actual template "טמפלט תקציב 01" (in use since 2010): 13 columns RTL, single sheet "טמפלט ריק", main section + options section. Column map: vendor / invoice / actual spend / payment terms / unit cost / total cost / category / service / units / unit price / total charge / profitability / margin percent. Columns 1-6 and 12-13 are Bold-internal (vendor tracking + margin monitoring); columns 7-11 are client-facing.

Production fee: single "דמי ארגון והפקה" line at 15% after the six categories. This IS the margin. No separate "Bold רווח" category. Script: `scripts/build_budget_xlsx.py` v3.0.

Conditional items live in the options section with their own 15% fee and separate total "סה\"כ חשבונית". They sit flat under a single כללי marker.

## The presentation template (Bold's canonical 4:3 deck)

Bold has produced 4:3 presentations (14.22 x 10.66 inches) with the same type system since 2007. Stage 6 MUST match this template. Full spec in `assets/bold-presentation-template-spec.md`. Highlights:

- Aspect ratio: **4:3**, NOT 16:9
- Title font: **Tahoma bold 35pt** (Hebrew), Verdana bold 35pt (English), color `#000000`
- Body font: Tahoma / Verdana 18-22pt, `#000000` or `#333333`
- Footer text font: Verdana 14pt, gray `#808080`

### Footer composition (every body slide)

```
[White Bold logo bottom-left]     A Bold Presentation© [YYYY]     [Client logo bottom-right]
```

- White logo: `assets/logos/bold-white-footer.jpg`
- Center text: current year, populated at Stage 6 time
- Client logo: requested in brief (Stage 1), stored as `proposals/<slug>/01-intake/client-logo.ext`
- If client hasn't provided a logo, the bottom-right slot stays empty; Stage 6 flags to Hemi and continues

### Cover and closing (unique no-footer layouts)

- **Cover (slide 1):** full-bleed background (hero mockup or black), `assets/logos/bold-black-opening.jpg` centered at 40-60% of slide width, event title below. NO footer.
- **Closing (last slide):** full-bleed `bold-closing.mp4` (30MB, lives in Bold's Drive at `K:\My Drive\macshare\Booper` or similar, fetched at Stage 6 time, NOT in the .skill package). NO footer, NO text overlay.

## The three-surface delivery (Stage 6)

Every Bold proposal ships in three complementary surfaces, all driven by the same source material:

| Surface | Produced by | Used for |
|---|---|---|
| `proposal.pdf` | `premium-deck-strategist` skill | Flagship, polished, committee-ready. The PDF the client prints or projects. |
| Live Gamma URL | `gamma_generate` MCP call | Interactive, shareable, commentable. The link the client forwards around. |
| `proposal.pptx` | Gamma `exportAs: "pptx"` export | Editable. The client opens it in PowerPoint or Google Slides to annotate or tweak. |

The three are not redundant: PDF is polish, Gamma is interactivity, PPTX is editability. All three use the same 4:3 aspect ratio, the same Tahoma/Verdana type system, and the same footer composition.

## Voice rules

- Hebrew-first. Numbers Western. Dates DD.MM.YYYY.
- No em-dash or en-dash.
- No clichés ("בלתי נשכח", "מרגש", "unforgettable", "חוגגים יחד", "once in a lifetime").
- Specific numbers, not adjectives.
- No Bold credits/logos outside the footer stripe.
- Short paragraphs.
- Max 5-7 words per on-slide bullet; depth goes in speaker notes.

## Gates

- Gate 1→2: Brief fields 1, 3, 6, 14, 16 filled.
- Gate 2→3: 3 trends + 3 case studies + 5 inspirations.
- Gate 3→4: One direction picked from three-direction set; brand-system.md has 9 fields.
- Gate 4a→rest: One visual direction picked; full mockup set + video + mood-direction.md.
- Gate 4→5: All specialists reference brand system + visual.
- Gate 5→6: Every line maps to one of the 6 canonical categories (per `assets/budget-categories-reference.md`); 70%+ lines reference vendor registry; no line without `source_deliverable`.
- Gate 6→done: Six Stage 6 artifacts (PDF, PPTX, XLSX, scorecard, summary with Gamma URL, Trello card with `gammaId`). Deck matches 4:3 template; footer composition correct on body slides; cover and closing are unique layouts.
- Gate 7: Runs 24h after event from Trello card.

## Required sibling skills

| Skill | Used in | Role |
|---|---|---|
| `nano-banana` | Stage 3, 4a | Visual reference images, mockups |
| `veo-video-creator` | Stage 4a | Atmosphere video |
| `premium-deck-strategist` | Stage 6 | Premium proposal deck (PDF), must be configured for 4:3 with Tahoma/Verdana per `bold-presentation-template-spec.md` |

If any is missing at runtime, the Stage that depends on it cannot complete. Claude warns and prompts installation.

## Required MCP servers

Stage 6 relies on a live external service. Source: `https://github.com/hemichaeli/gamma-mcp-server`. Production endpoint: `https://gamma-mcp-server-production-959b.up.railway.app/sse`.

| MCP server | Used in | Role |
|---|---|---|
| Gamma (custom, Bold-operated) | Stage 6, Stage 7 | `gamma_generate` with `cardDimensions: "4x3"` and `exportAs: "pptx"` builds both the live Gamma deck and the downloadable PPTX in one call; `gamma_generate_from_template` remixes the prior deck for returning clients (Phoenix, Keren, Efrat) |

If the Gamma MCP is not connected in the current session, Stage 6 falls back: Claude writes `gamma-prompt.md` for Hemi to paste into Gamma.app manually. Not blocking, but the PPTX and live-URL delivery are lost; only the premium PDF ships.

## Assets in the skill package

| Asset | Purpose |
|---|---|
| `assets/bold-brand-guidelines.md` | Bold's verbal brand rules |
| `assets/brief-form-original.md` | The original brief form Bold uses |
| `assets/gamma-prompt-template.md` | Fallback prompt template for Gamma when MCP is unavailable |
| `assets/proposal-pdf-structure.md` | PDF structure reference |
| `assets/budget-categories-reference.md` | The 6 canonical categories + 30 sub-categories + ~140 line items (sourced from "תבנית מתודולוגית לאירועים 4" sheet 1) |
| `assets/bold-presentation-template-spec.md` | 4:3 aspect, Tahoma 35pt, 28-slide canonical sequence, footer/cover/closing rules (sourced from "BOLDpresentation - TEMPLATE.ppt" plus 2026 footer updates) |
| `assets/logos/bold-black-opening.jpg` | Black Bold logo for cover slide (binary, packaged with .skill, not in Git) |
| `assets/logos/bold-white-footer.jpg` | White Bold logo for footer bottom-left (binary, packaged with .skill, not in Git) |
| `assets/logos/README.md` | Logo usage rules + reference to `bold-closing.mp4` on Drive |
| `scripts/build_budget_xlsx.py` v3.0 | Produces budget.xlsx in Bold's exact canonical template format |

## Session start

1. Check for brief/transcript input.
2. Read client profile if known (includes `gammaId` of prior deck for remix).
3. Read hemi-preferences.md.
4. Verify vendor registry.
5. Verify required sibling skills present (nano-banana, veo-video-creator, premium-deck-strategist).
6. Verify Gamma MCP is connected (check for `gamma_generate` tool). If absent, note fallback path for Stage 6.
7. Verify critical assets present: `budget-categories-reference.md`, `bold-presentation-template-spec.md`, `logos/bold-black-opening.jpg`, `logos/bold-white-footer.jpg`. If logo binaries missing (skill installed without the binaries), flag to Hemi; Stage 6 can still proceed but the PDF will be missing the Bold logo.
8. Begin Stage 1.

## Success

Final deliverable: a client who, 30 days after the event, can say "Bold helped me hit these specific numbers". Secondary: over 5-10 events, three-direction sets land more often, but Claude never stops offering stretch directions. Tertiary: returning clients get increasingly well-tuned proposals because `gamma_generate_from_template` preserves what worked.
