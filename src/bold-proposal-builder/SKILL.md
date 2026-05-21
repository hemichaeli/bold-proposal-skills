---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow, brief gathering, research, three-direction brand heart selection, three-direction visualization, content/operations/culinary specialists, budget, assembly, and post-event debrief. Use whenever Hemi Michaeli asks to build, draft, or prepare a proposal or event concept for a Bold client. Also triggers for "לבנות הצעה", "פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Mentions of Phoenix, Keren, Efrat clients also trigger. Produces a client-facing package in default deck surfaces (live Canva deck + live Gamma deck + downloadable PowerPoint files from both, plus PDF export from Canva), plus strategy, brand system, mockups, atmosphere video, agenda, scripts, menu, operations, budget XLSX in Bold's canonical 13-column RTL template with dual-layer margin (15% per-line embedded plus 15% production fee), KPIs scorecard, and Trello debrief reminder. At Stage 5 the skill auto-syncs vendor quotes from two Drive folders into data/vendor-registry.json. Requires nano-banana and veo-video-creator skills for Stage 4, the Gamma MCP server, and the Canva MCP server for Stage 6.
license: Proprietary
---

# Bold Proposal Builder (v2.8)

A 7-stage orchestrator for producing premium event proposals for Bold Productions. Each stage reads a reference file in `references/`, produces its artifacts, hands off. Skip stages and the final proposal fragments.

## What changed in v2.8

The budget margin model is now correctly described as dual-layer:

1. **15% per-line embedded markup** (invisible to client). Built into the client unit price in the XLSX. Surfaces only in the gray profit columns L-M.
2. **15% production fee** ("דמי ארגון והפקה") visible at the bottom of each section.

Effective Bold margin: ~32% (1.15 * 1.15 = 1.3225). The v2.7 description ("production fee IS the margin, no other markup") was incorrect and has been removed.

Also new: vendor-quote monitoring at Stage 5 open. The skill scans two Drive folders for new supplier quotes since the last sync and updates `data/vendor-registry.json` automatically. See `references/vendor-quote-monitoring.md`. Build script bumped to `scripts/build_budget_xlsx.py` v4.0 to support the formula-driven dual-margin layout.

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
| 5 | Budget | `references/stage-5-budget.md` + `references/vendor-quote-monitoring.md` + `assets/budget-categories-reference.md` | `budget.json` (supplier costs only; script derives client prices) |
| 6 | Assembly | `references/stage-6-assembly.md` + `references/canva-deck-path.md` | Canva deck (URL + PDF + PPTX), Gamma deck (URL + PPTX), `budget.xlsx`, KPI scorecard, summary, Trello card |
| 7 | Debrief | `references/stage-7-debrief.md` | `debrief-[event].md`, client profile (with `gammaId` and Canva `design_id`), preferences update |

## The four goal categories

1. שיווקית (Marketing)
2. Fun (Experience)
3. מכירתית (Sales)
4. תדמיתית (Reputation)

## The three-directions principle

Stages 3 and 4a each propose three distinct directions along a chosen axis. Each direction has a visual representation. Hemi picks one. If none land, Claude asks one clarifying question, picks a different axis, proposes three new. Max 3 rejection cycles per stage. Stretch policy: always one stretch direction per set.

Every selection logged to `data/hemi-preferences.md`. Read at start of every Stage 3 and Stage 4a session.

## The budget spine (Bold's canonical 6-category tree)

Bold has used the same 6 top-level budget categories since 2010. Stage 5 does NOT invent categories.

1. כללי (General)
2. תקשור מקדים (Pre-event communications)
3. מיתוג ושילוט (Branding & signage)
4. טכני (Technical)
5. כח אדם ולוגיסטיקה (Staff & logistics)
6. שונות (Miscellaneous)

Full taxonomy (30 sub-categories, ~140 line items) in `assets/budget-categories-reference.md`.

## The budget XLSX layout (Bold's canonical 13-column RTL template)

Single sheet "טמפלט ריק", 13 columns, RTL.

Right side (columns A-F, visible on the right in RTL view): **supplier data**.
- A vendor name
- B invoice
- C actual spend (filled post-event)
- D payment terms
- E supplier unit cost
- F total cost = qty * unit cost

Middle (columns G-K): **client-facing**.
- G category
- H description
- I qty
- J client unit price = supplier unit cost * 1.15 (the per-line markup, never labeled)
- K total charge = qty * unit price

Left side (columns L-M, gray fill): **profit, Bold internal**.
- L profit = total charge - total cost
- M margin % = profit / total charge

After all line items in a section: subtotal row, then "דמי ארגון והפקה" row (15% of section subtotal), then "סה\"כ חשבונית" grand total.

Conditional items live in a separate "אופציות" section below the main, flat under a single כללי marker, with its own 15% production fee and grand total.

All cells use Excel formulas (not static values), so editing a supplier price in column E live-updates every downstream cell.

## Vendor quote auto-sync (v2.8)

At Stage 1 close-out or Stage 5 open (whichever comes first), the skill performs a vendor-quote delta check against the two Drive source folders:

- `https://drive.google.com/drive/folders/0B7TFmdvhXcItS1JxM2xIZG5YeUU`
- `https://drive.google.com/drive/folders/0B7TFmdvhXcItZnVaVllQZmZOS0U`

New quotes since `data/vendor-registry.json` `_meta.last_scan_utc` are parsed and ingested. Stage 5 then queries the registry by category + keyword to populate `unit_cost` for each line. Full protocol in `references/vendor-quote-monitoring.md`. The 15% per-line markup is applied by the script at XLSX render time, NEVER stored in `vendor-registry.json` or `budget.json`.

## The deck surfaces (Stage 6)

Two default deck surfaces, five artifacts from two MCP calls:

| Source | Live URL | PPTX | PDF |
|---|---|---|---|
| Canva (`generate-design-structured`) | yes | yes | yes |
| Gamma (`gamma_generate`) | yes | yes (via `exportAs`) | no |

Both 16:9 (Canva and Gamma native). The historical Bold 4:3 template (`assets/bold-presentation-template-spec.md`) is preserved as a legacy reference only.

## Voice rules

- Hebrew-first. Numbers Western. Dates DD.MM.YYYY.
- No em-dash or en-dash.
- No clichés ("בלתי נשכח", "מרגש", "חוגגים יחד", "unforgettable", "once in a lifetime").
- Specific numbers, not adjectives.
- Short paragraphs.
- Max 5-7 words per on-slide bullet; depth in speaker notes.
- **Budget**: never mention the 15% per-line markup. Anywhere. Not in client decks, not in summary.md, not in PDF, not in conversation with the client. The production fee at the bottom is the only 15% the client ever sees.

## Gates

- Gate 1→2: Brief fields 1, 3, 6, 14, 16 filled.
- Gate 2→3: 3 trends + 3 case studies + 5 inspirations.
- Gate 3→4: One direction picked from three-direction set; brand-system.md has 9 fields.
- Gate 4a→rest: One visual direction picked; full mockup set + video + mood-direction.md.
- Gate 4→5: All specialists reference brand system + visual.
- Gate 4→5 additional: vendor-quote delta check has run successfully; `vendor-registry.json` `_meta.last_scan_utc` is from this session.
- Gate 5→6: Every line maps to one of the 6 canonical categories; 70%+ lines reference `source_vendor_registry`; no line has a manual `unit_price` field; no line description contains "דמי ארגון" or "production fee" (the script adds that row automatically).
- Gate 6→done: Six core artifacts. If a deck MCP is unavailable, that surface is skipped and summary.md notes the gap.
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
| Gamma (custom Bold-operated, `gamma-mcp-server-production-959b.up.railway.app/sse`) | Stage 6, Stage 7 | Live Gamma deck + PPTX export, `gamma_generate_from_template` for returning clients |
| Canva (`mcp.canva.com/mcp`) | Stage 6 | Canva deck + PDF + PPTX exports |
| Google Drive (built-in) | Stage 5 vendor sync | Listing and fetching files from the two Drive source folders |

## Assets in the skill package

| Asset | Purpose |
|---|---|
| `assets/bold-brand-guidelines.md` | Bold's verbal brand rules |
| `assets/brief-form-original.md` | Bold's original 2001-era brief form |
| `assets/gamma-prompt-template.md` | Fallback prompt template for Gamma when MCP is unavailable |
| `assets/proposal-pdf-structure.md` | PDF structure reference (legacy) |
| `assets/budget-categories-reference.md` | 6 canonical categories + 30 sub-categories + ~140 line items |
| `assets/bold-presentation-template-spec.md` | Legacy 4:3 template (2007-2025), kept for historical reference only |
| `assets/logos/bold-black-opening.jpg` | Black Bold logo (binary, not in Git) |
| `assets/logos/bold-white-footer.jpg` | White Bold logo (binary, not in Git) |
| `assets/logos/README.md` | Logo usage rules |
| `scripts/build_budget_xlsx.py` v4.0 | Produces budget.xlsx with dual-layer margin, formula-driven |
| `data/vendor-registry.json` | Working memory of supplier quotes, auto-updated at Stage 5 open |

## Session start

1. Check for brief/transcript input.
2. Read client profile if known (includes `gammaId` and Canva `design_id` for remix).
3. Read `data/hemi-preferences.md`.
4. **Run vendor-quote delta sync** against the two Drive folders. Report new quotes count to Hemi. (See `references/vendor-quote-monitoring.md`.)
5. Verify required sibling skills (nano-banana, veo-video-creator).
6. Verify Gamma MCP connected. If absent, note that the Gamma surface will be skipped.
7. Verify Canva MCP connected. If absent, note that the Canva surface will be skipped.
8. If both Canva and Gamma MCPs absent, verify `premium-deck-strategist` for fallback.
9. Verify `data/canva-config.json` or run `Canva:list-brand-kits` first time and cache.
10. Begin Stage 1.

## Success

Final deliverable: a client who, 30 days after the event, can say "Bold helped me hit these specific numbers". Secondary: over 5-10 events, three-direction sets land more often. Tertiary: returning clients get increasingly well-tuned proposals because `gamma_generate_from_template` and the Bold Canva brand kit preserve what worked. Quaternary: Bold's effective ~32% margin is preserved end-to-end with zero client-facing mention of the per-line 15%.
