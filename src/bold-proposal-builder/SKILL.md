---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow, brief gathering, research, three-direction brand heart selection, three-direction visualization, content/operations/culinary specialists, budget, assembly, and post-event debrief. Use whenever Hemi Michaeli asks to build, draft, or prepare a proposal or event concept for a Bold client. Also triggers for "לבנות הצעה", "פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Mentions of Phoenix, Keren, Efrat clients also trigger. Produces a client-facing package in three complementary surfaces (premium PDF + live Gamma URL + editable PPTX) plus strategy, brand system, mockups, atmosphere video, agenda, scripts, menu, operations, budget XLSX in Bold's canonical 6-category format, KPIs scorecard, and Trello debrief reminder. Requires nano-banana and veo-video-creator skills for Stage 4, and the Gamma MCP server for Stage 6.
license: Proprietary
---

# Bold Proposal Builder (v2.5)

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
| 6 | Assembly | `references/stage-6-assembly.md` | **Premium PDF** (premium-deck-strategist) + **live Gamma URL** + **editable PPTX** (Gamma MCP `exportAs: "pptx"`), plus XLSX (Bold canonical template), KPIs scorecard, summary, Trello card |
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

Underneath the six, sub-categories (חניה, אבטחה, הגברה, במות, קייטרינג, etc.) organize ~140 possible line items. Full tree: `assets/budget-categories-reference.md`. XLSX layout matches Bold's actual template ("טמפלט תקציב 01") including vendor name, invoice number, actual spend columns for Bold-internal tracking, plus client-facing "מחיר יחידה / סה\"כ חיוב / רווחיות / %" columns.

Production fee: single "דמי ארגון והפקה" line at 15% after the six categories. This IS the margin. No separate "Bold rewach" category.

Conditional items live on sheet 2 ("אופציות") with their own 15% fee and separate total.

## The three-surface delivery (Stage 6)

Every Bold proposal ships in three complementary surfaces, all driven by the same source material:

| Surface | Produced by | Used for |
|---|---|---|
| `proposal.pdf` | `premium-deck-strategist` skill | Flagship, polished, committee-ready. The PDF the client prints or projects. |
| Live Gamma URL | `gamma_generate` MCP call | Interactive, shareable, commentable. The link the client forwards around. |
| `proposal.pptx` | Gamma `exportAs: "pptx"` export | Editable. The client opens it in PowerPoint or Google Slides to annotate or tweak. |

The three are not redundant: PDF is polish, Gamma is interactivity, PPTX is editability. All three sit under `proposals/<slug>/06-assembly/` (PPTX file) or in `summary.md` (Gamma URL).

## Voice rules

- Hebrew-first. Numbers Western. Dates DD.MM.YYYY.
- No em-dash or en-dash.
- No clichés ("בלתי נשכח", "מרגש", "unforgettable", "חוגגים יחד").
- Specific numbers, not adjectives.
- No Bold credits/logos.
- Short paragraphs.

## Gates

- Gate 1→2: Brief fields 1, 3, 6, 14, 16 filled.
- Gate 2→3: 3 trends + 3 case studies + 5 inspirations.
- Gate 3→4: One direction picked from three-direction set; brand-system.md has 9 fields.
- Gate 4a→rest: One visual direction picked; full mockup set + video + mood-direction.md.
- Gate 4→5: All specialists reference brand system + visual.
- Gate 5→6: Every line maps to one of the 6 canonical categories; 70%+ lines reference vendor registry; no line without `source_deliverable`.
- Gate 6→done: Six Stage 6 artifacts (PDF, PPTX, XLSX, scorecard, summary with Gamma URL, Trello card with `gammaId`).
- Gate 7: Runs 24h after event from Trello card.

## Required sibling skills

| Skill | Used in | Role |
|---|---|---|
| `nano-banana` | Stage 3, 4a | Visual reference images, mockups |
| `veo-video-creator` | Stage 4a | Atmosphere video |
| `premium-deck-strategist` | Stage 6 | Premium proposal deck (PDF) |

If any is missing at runtime, the Stage that depends on it cannot complete. Claude warns and prompts installation.

## Required MCP servers

Stage 6 relies on a live external service. Source: `https://github.com/hemichaeli/gamma-mcp-server`. Production endpoint: `https://gamma-mcp-server-production-959b.up.railway.app/sse`.

| MCP server | Used in | Role |
|---|---|---|
| Gamma (custom, Bold-operated) | Stage 6, Stage 7 | `gamma_generate` with `exportAs: "pptx"` builds both the live Gamma deck and the downloadable PPTX in one call; `gamma_generate_from_template` remixes the prior deck for returning clients (Phoenix, Keren, Efrat) |

If the Gamma MCP is not connected in the current session, Stage 6 falls back to the v2.2 flow: Claude writes `gamma-prompt.md` for Hemi to paste into Gamma.app manually. Not blocking, but the PPTX and live-URL delivery are lost; only the premium PDF ships.

## Session start

1. Check for brief/transcript input.
2. Read client profile if known (includes `gammaId` of prior deck for remix).
3. Read hemi-preferences.md.
4. Verify vendor registry.
5. Verify required sibling skills present.
6. Verify Gamma MCP is connected (check for `gamma_generate` tool). If absent, note fallback path for Stage 6.
7. Begin Stage 1.

## Success

Final deliverable: a client who, 30 days after the event, can say "Bold helped me hit these specific numbers". Secondary: over 5-10 events, three-direction sets land more often, but Claude never stops offering stretch directions. Tertiary: returning clients get increasingly well-tuned proposals because `gamma_generate_from_template` preserves what worked.
