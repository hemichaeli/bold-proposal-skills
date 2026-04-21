---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow that moves from brief gathering through research, brand heart, specialist design (visualization, content, operations, culinary), budget, assembly, and post-event debrief. Use this skill whenever Hemi Michaeli asks to build, draft, create, or prepare a proposal, pitch, or event concept for a Bold client. Also triggers for related phrases in Hebrew like "לבנות הצעה", "לכתוב פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Use also when the user mentions a specific Bold client (Phoenix, Keren, Efrat, etc.) and wants event work. The flow produces a full client-facing package including strategy, brand system, visual mockups, atmosphere video, agenda, scripts, menu, operations plan, budget Excel, designed PDF, Gamma prompt, KPIs scorecard, and a Trello debrief reminder. Requires nano-banana and veo-video-creator skills to be installed for Stage 4 (visualization).
license: Proprietary
---

# Bold Proposal Builder

A 7-stage orchestrator for producing premium event proposals for Bold Productions. The skill does not improvise: each stage reads a reference file in `references/`, produces its artifacts, and hands off to the next. Skip stages and the final proposal fragments; the sequence is load-bearing.

---

## The seven stages

| Stage | Name | Reference | Output |
|---|---|---|---|
| 1 | Intake & Brief | `references/stage-1-intake.md` | `brief.md`, `challenges.md`, KPIs |
| 2 | Research | `references/stage-2-research.md` | `trends.md`, `case-studies.md`, `inspiration.md` |
| 3 | Brand heart | `references/stage-3-brand-heart.md` | `brand-system.md` |
| 4a | Visualization | `references/stage-4a-visualization.md` | mockups + atmosphere video + `mood-direction.md` |
| 4b | Content & experience | `references/stage-4b-content-experience.md` | `agenda.md`, `scripts.md` |
| 4c | Operations | `references/stage-4c-operations.md` | `logistics.md` |
| 4d | Culinary | `references/stage-4d-culinary.md` | `menu.md` |
| 5 | Budget | `references/stage-5-budget.md` | `budget.json` (sources from `data/vendor-registry.json`) |
| 6 | Assembly | `references/stage-6-assembly.md` | `proposal.pdf`, `budget.xlsx`, `kpis-scorecard.md`, `gamma-prompt.md`, `summary.md`, Trello card |
| 7 | Debrief | `references/stage-7-debrief.md` | `debrief-[event].md`, client profile update, skill PR |

---

## The four goal categories

Bold builds events to serve goals. At Stage 1, the client's goals are classified into one or more of four categories. Every downstream decision is checked against these goals. At Stage 7, actual outcomes are measured against the KPIs derived from them.

1. **שיווקית (Marketing)** — awareness, reach, brand memory.
2. **Fun (Experience)** — enjoyment, bonding, emotional resonance.
3. **מכירתית (Sales)** — leads, conversions, closed deals.
4. **תדמיתית (Reputation)** — perception shift, positioning, narrative control.

A single event can serve any combination. Each selected goal produces at least one KPI.

---

## Voice rules (non-negotiable across all stages)

These rules apply to every word of client-facing output. Claude enforces them without being reminded.

### Hebrew-first
- All client deliverables in Hebrew unless the client is English-speaking.
- Internal artifacts (e.g., `challenges.md`) can be in Hebrew or English.
- Numbers in Western digits; dates in Israeli format (DD.MM.YYYY).

### No long dashes
- Never em-dash (—) or en-dash (–).
- Use a comma, a period, or a colon instead.

### No clichés
Banned words and phrases:
- "בלתי נשכח", "מרגש", "חוויה ייחודית", "נופך מיוחד"
- "unforgettable", "tailored", "exceeding expectations", "elevated experience"
- "חוגגים יחד", "להוסיף נופך", "ערב של חיבורים"
- Anything that could appear at any other event's proposal is by definition wrong for this one.

### Specific numbers, not vague adjectives
- "210 אורחים" not "קהל גדול".
- "₪450 לסועד" not "השקעה נאותה".
- "45 דקות של הגעה" not "זמן הגעה נעים".

### No credits
Do not include Bold logos, credits, photo credits, or "produced by" lines in any client deliverable unless the client explicitly requests.

### Restraint
- Short paragraphs.
- Fewer words than you think.
- Silence is confidence.

---

## Gates between stages

Claude does not move between stages without verifying the gate:

- **Gate 1 → 2:** Brief must have fields 1, 3 (with at least one goal category selected), 6, 14, 16 filled. See `references/stage-1-intake.md` for details.
- **Gate 2 → 3:** At least 3 trends + 3 case studies + 5 inspiration references must be sourced.
- **Gate 3 → 4:** Brand system must have all 9 fields filled.
- **Gate 4 → 5:** All four specialist outputs exist and reference the brand system.
- **Gate 5 → 6:** Budget `summary.subtotal` is non-null; at least 70% of non-internal lines have `source_vendor_registry` populated.
- **Gate 6 → done:** All six Stage 6 artifacts produced; Trello debrief card created.
- **Gate 7:** Runs 24 hours after the event, triggered by Hemi from a Trello card.

---

## When things are missing

### Missing nano-banana or veo-video-creator
Stage 4a requires both. If either is unavailable, Claude tells Hemi and offers one of two fallbacks:
1. Proceed with textual mood direction only, mockups pending.
2. Use `canvas-design` for abstract/graphic event types (not photorealistic).

### Missing vendor registry
Stage 5 requires `data/vendor-registry.json`. If missing or stale (>90 days), Claude prompts Hemi to run `scripts/extract-vendor-data.py` to populate from Drive.

### Missing Trello MCP
Stage 6 creates the debrief card via Trello MCP. If unavailable, Claude falls back to a `DEBRIEF-REMINDER.md` file in the proposal folder + a Gmail reminder the day before the event.

### Missing client profile
Stage 7 writes to `data/client-profiles/[slug].md`. If first time with a client, Claude creates the file.

---

## Directory structure per proposal

```
proposals/<client-slug>-<event-slug>/
├── 01-intake/
│   ├── brief.md
│   └── challenges.md
├── 02-research/
│   ├── trends.md
│   ├── case-studies.md
│   └── inspiration.md
├── 03-brand-heart/
│   └── brand-system.md
├── 04-specialists/
│   ├── visual/
│   │   ├── mockups/01-arrival.png, 02-hero.png, ...
│   │   ├── atmosphere-video.mp4
│   │   └── mood-direction.md
│   ├── content/
│   │   ├── agenda.md
│   │   └── scripts.md
│   ├── operations/
│   │   └── logistics.md
│   └── culinary/
│       └── menu.md
├── 05-budget/
│   └── budget.json
└── 06-assembly/
    ├── proposal.pdf
    ├── budget.xlsx
    ├── kpis-scorecard.md
    ├── gamma-prompt.md
    ├── summary.md
    └── debrief-[event-slug].md     # written at Stage 7
```

---

## Repository-level data (shared across proposals)

```
data/
├── vendor-registry.json           # populated by scripts/extract-vendor-data.py
├── proposal-patterns.md           # populated by scripts/extract-proposal-patterns.py
├── cpi-israel.json                # CPI table for price adjustments
└── client-profiles/
    ├── phoenix-group.md
    ├── [other clients].md
    └── README.md
```

---

## How Claude should start each session

1. Check for pre-existing brief/transcript input (attached file, pasted text, Fireflies reference).
2. If the request mentions a known client, read `data/client-profiles/[slug].md` if it exists and seed Stage 1 with the known constraints.
3. Verify the vendor registry is present and fresh.
4. Begin Stage 1 by presenting the brief fields to the user.

Do NOT start with research or with a creative pitch. The brief is the gate.

---

## Success

The final deliverable is not the PDF. The final deliverable is a client who, 30 days after the event, can point to specific numbers and say "Bold helped me hit these". Stage 7 closes the loop. The flow exists to serve that.
