---
name: bold-proposal-builder
description: Build end-to-end premium event-production proposals for Bold Productions (חברת ההפקה "לי"). Use whenever the user wants to turn a client brief into a full proposal package including strategy, brand concept, visualizations, content, logistics, culinary, budget, and the three final deliverables (Gamma presentation, designed PDF, detailed Excel budget) plus an atmosphere video. Trigger even when the user says things like "יש לי לקוח חדש", "צריך להכין הצעה", "בוא נפצח בריף", "תכין לי הצעת מחיר לאירוע", "קבלתי בריף מ-X", or attaches a Fireflies transcript of an intake call. Also trigger when the user asks to work on a specific stage of an event proposal such as brief, trends, brand, visualizations, content, operations, culinary, budget, or assembly.
---

# Bold Proposal Builder

A six-stage orchestration skill for producing world-class event proposals. The skill is structured as a **pipeline of specialist agents**, each with its own reference file. You (Claude) play all six roles, in order, for a single client brief.

**Company voice**: Bold Productions produces premium live experiences. The tone is confident, strategic, crafted; never marketing clichés, never filler, never "we believe" language. Every sentence earns its place.

**Language**: All client-facing output is in Hebrew unless the brief explicitly calls for English. Internal planning can mix Hebrew and English.

---

## When to trigger, when not to

**Trigger:**
- User hands over a client brief (text, transcript, recording summary, email, or verbal description).
- User says they want to build / prepare / draft a proposal, הצעת מחיר, deck, or pitch for an event.
- User asks to iterate on a specific stage of an existing proposal.
- User uploads a Fireflies transcript of an intake call.

**Do NOT trigger:**
- User asks a single factual question about event production ("what's a typical ceiling drape budget?") — answer directly.
- User is working on a different company's proposal (QUANTUM, GenoMAX, PharMAX). Those have their own workflows.

---

## The six stages at a glance

```
STAGE 1: INTAKE            → brief.md + challenges.md
STAGE 2: RESEARCH          → trends.md + case-studies.md + inspiration.md
STAGE 3: BRAND HEART       → brand-system.md (concept, name, tone, palette, type)
STAGE 4: SPECIALISTS       → visual/ + content/ + operations/ + culinary/
STAGE 5: BUDGET            → budget.json
STAGE 6: ASSEMBLY          → Gamma prompt + PDF + XLSX + MP4
```

Each stage produces files in a **working directory** for the project. Never skip a stage. Never run stage 6 before stages 1-5 are complete. The reason: every downstream stage draws on upstream artifacts. If you skip stage 2, the brand heart has no cultural anchor. If you skip stage 3, the visualizations have no visual DNA to express. The pipeline is the product.

---

## Working directory convention

For every new proposal, create this structure. Use a slug derived from client + event (e.g., `phoenix-art-2026-summer`):

```
proposals/<slug>/
├── 01-intake/
│   ├── brief.md
│   ├── challenges.md
│   └── raw-input.txt        (transcript or notes)
├── 02-research/
│   ├── trends.md
│   ├── case-studies.md
│   └── inspiration.md
├── 03-brand-heart/
│   └── brand-system.md
├── 04-specialists/
│   ├── visual/
│   │   ├── mood-direction.md
│   │   ├── mockups/         (PNGs from nano-banana)
│   │   └── atmosphere-video.mp4   (from veo-video-creator)
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
    ├── gamma-prompt.md
    └── summary.md
```

---

## Stage 1 — Intake

**Role**: Extract the client's true need, not just their words.

Read `references/stage-1-intake.md` before starting this stage. It contains the full intake questionnaire, rules for parsing Fireflies transcripts vs. free-form descriptions, and the "challenge distillation" methodology (what the client actually needs to solve, often different from what they asked for).

**Inputs**: free-form conversation, phone call summary, Fireflies transcript, email thread, or any mix.
**Outputs**: `01-intake/brief.md` (structured brief) and `01-intake/challenges.md` (the brand/business challenges this event must address).

**Gate to stage 2**: all mandatory fields in `brief.md` are filled or explicitly marked "חסר — להשלים מול הלקוח". Never invent data.

---

## Stage 2 — Research, Trends & Strategy

**Role**: Find the cultural wind the proposal will sail on.

Read `references/stage-2-research.md`. It defines the trend-spotting methodology, the case-study sourcing process, and the inspiration synthesis.

**Inputs**: `brief.md`, `challenges.md`.
**Outputs**:
- `02-research/trends.md` — 3 to 5 global/local trends with direct relevance to this event's challenges. Each trend has a source, a year, and a "so what" clause.
- `02-research/case-studies.md` — 3 to 5 real events/activations (Israel + world) that solved adjacent challenges. Include what they did, the result, and what Bold will borrow/avoid.
- `02-research/inspiration.md` — a creative mood board in words: references, motifs, tensions worth holding onto.

Use `web_search` and `web_fetch` aggressively in this stage. Favor original sources (event production case-study pages, agency portfolios, campaign recap decks on Behance/AdsOfTheWorld, industry publications like Event Marketer / Bizzabo / Campaign / Bold's own Drive archive if referenced).

**Gate to stage 3**: no fewer than 3 trends, 3 case studies, and 5 inspiration anchors, each with sourcing.

---

## Stage 3 — Brand Heart

**Role**: Build the coherent creative DNA of this specific event.

Read `references/stage-3-brand-heart.md`. This is the methodology for turning strategy into a brand system that can be expressed visually.

**Inputs**: stage 1 + stage 2 outputs.
**Output**: `03-brand-heart/brand-system.md` containing:
- **Concept** — the one-sentence creative thesis of the event.
- **Name** — a proposed event name (with 2 alternates).
- **Tagline** — short, memorable, Hebrew.
- **Tone of voice** — 3 adjectives + 2 "we are / we are not" pairs.
- **Color palette** — 4 to 6 colors with hex codes and a role for each (primary, secondary, accent, neutral, highlight).
- **Typography** — 1 display font + 1 text font, with fallback rationale. Prefer fonts available in Google Fonts or already in Bold's stack.
- **Visual motif** — the repeating visual device (a shape, pattern, material, light treatment).
- **Sensory signatures** — sound, scent, texture, temperature cues (even if rough).

**Gate to stage 4**: every field is filled. The palette uses actual hex codes. The concept is one sentence. The motif is describable in a prompt.

---

## Stage 4 — Specialists (parallel)

**Role**: Turn the brand system into concrete experience components. Four parallel sub-agents; run them in order but keep outputs independent so later edits don't cascade.

### 4a. Visualization

Read `references/stage-4a-visualization.md`. This file instructs how to use the `nano-banana` skill for still imagery and the `veo-video-creator` skill for the atmosphere video.

**Deliverables**:
- 4 to 8 mockup stills (venue dressing, stage, signage, food presentation, guest arrival) in `04-specialists/visual/mockups/`.
- One atmosphere video of 5 to 15 seconds in `04-specialists/visual/atmosphere-video.mp4`.
- `mood-direction.md` — the prompts used + rationale, so the client sees intent, not just output.

**Consistency rule**: all mockups must carry the brand system (palette + motif + typography). Reuse a "style anchor" prompt across all image generations for consistency. The `nano-banana` skill explains how.

### 4b. Content & Experience

Read `references/stage-4b-content-experience.md`.

**Deliverables**:
- `content/agenda.md` — minute-by-minute or block-by-block running order (Hebrew).
- `content/scripts.md` — MC scripts, opening/closing words, key moments, guest-facing copy (invitations, signage wording, WhatsApp reminders, post-event thank-you).

### 4c. Operations & Planning

Read `references/stage-4c-operations.md`.

**Deliverables**:
- `operations/logistics.md` — guest flow diagram (in words + optional Mermaid), build-out plan, infrastructure list (power, water, sound, light, restrooms, parking, accessibility, security), vendor list (roles only — actual vendors priced in stage 5), permits required, risk register.

### 4d. Culinary

Read `references/stage-4d-culinary.md`.

**Deliverables**:
- `culinary/menu.md` — branded menu including dietary coverage (הערה: פסקטריאני/טבעוני/כשר/ללא גלוטן), service style (seated / stations / passed / family-style), presentation notes tied to the brand motif, suggested beverage pairing.

**Gate to stage 5**: all four sub-outputs present. Visualizations passed a brand-consistency check (palette match ≥ 80%, motif visible in ≥ 3 of the stills).

---

## Stage 5 — Budget

**Role**: Turn the experience into a defensible number.

Read `references/stage-5-budget.md`. It defines the full cost-category tree Bold uses, the vendor-assignment rules, and the conditional line-item handling (the 6,000 ₪ scenography supplier is a conditional line Bold has flagged).

**Inputs**: everything from stages 1 to 4.
**Output**: `05-budget/budget.json` — a structured JSON tree of all line items with:
```json
{
  "categories": [
    {
      "name": "תפאורה ובמה",
      "items": [
        {
          "name": "קיר LED 3x2 מ'",
          "qty": 1,
          "unit": "יח'",
          "unit_cost": 4500,
          "vendor": "ProStage",
          "conditional": false,
          "notes": "כולל הקמה ופירוק"
        }
      ]
    }
  ],
  "margin_pct": 22,
  "currency": "ILS",
  "valid_until": "YYYY-MM-DD"
}
```

**Conditional items** (like the 6,000 ₪ scenography supplier) get `"conditional": true` and a `"trigger_condition"` field describing when they activate.

**Gate to stage 6**: every stage-4 deliverable has at least one matching budget line; no "phantom" budget lines without a deliverable.

---

## Stage 6 — Assembly

**Role**: Build the three (or four) final artifacts the client actually sees.

Read `references/stage-6-assembly.md`.

**Inputs**: everything from stages 1 to 5.
**Outputs** in `06-assembly/`:

1. **`proposal.pdf`** — designed proposal PDF. Use `canvas-design` for hero/cover pages and the existing Bold design language in `assets/bold-brand-guidelines.md`. PDF structure is defined in `assets/proposal-pdf-structure.md`.

2. **`budget.xlsx`** — detailed budget Excel with formulas, categories, totals, margin calculation, and a summary tab. Build with the `build_budget_xlsx.py` script from `scripts/`, which reads `budget.json` and emits a fully formatted XLSX. Use the `xlsx` skill for guidance on formulas and formatting.

3. **`gamma-prompt.md`** — a ready-to-paste prompt for Gamma.app that will produce the interactive presentation. The prompt bundles the brand system, the mockup URLs, the atmosphere video URL, and the content. The user pastes this into Gamma; Claude does not call Gamma's API (there is no MCP for Gamma at time of writing). Template in `assets/gamma-prompt-template.md`.

4. **`summary.md`** — 1-page executive summary for WhatsApp / email introduction of the proposal.

**Gate to delivery**: visual QA — open the PDF, spot-check the XLSX totals against the JSON, verify the Gamma prompt renders the right mockups.

---

## Skill dependencies

This skill calls out to these other skills; make sure they are installed and read their SKILL.md when the relevant stage begins:

| Stage | Skill needed | Why |
|---|---|---|
| 4a | `nano-banana` | Still image generation for mockups |
| 4a | `veo-video-creator` | Atmosphere video generation |
| 6  | `canvas-design` | Hero/cover pages for the PDF |
| 6  | `pdf` | PDF assembly |
| 6  | `xlsx` | Excel formatting and formulas |

If any of these are missing, tell the user before starting the stage.

---

## Running the skill

### Starting fresh

When the user gives you an initial brief:
1. Create the working directory `proposals/<slug>/` with all subfolders.
2. Save the raw input to `01-intake/raw-input.txt`.
3. Begin Stage 1. Announce the stage to the user in one short line.
4. Proceed through stages 2 to 6. After each stage, print a one-line summary of what was produced + gate status (PASS / BLOCKED + reason).
5. At the end, run `present_files` on the four final artifacts.

### Resuming mid-flow

If the user says "we did the brief, now do the research" — read the existing files under `proposals/<slug>/` to load context, then jump to the requested stage. Do not re-run earlier stages unless asked.

### Iterating on one stage

The user will often want to redo one stage (e.g., "change the concept, try a more minimal direction"). Re-run only that stage and every stage downstream of it. Keep the old version in `proposals/<slug>/archive/<timestamp>/` for comparison.

---

## Source material from Bold's history

Bold has thousands of past proposals in Google Drive. When the user grants access or points to specific examples, use the `Google Drive` or `Google drive MCP Server` tools to:
- Pull 3 to 5 relevant past proposals for the current brief.
- Extract their budget structure and vendor choices as a seed for stage 5.
- Cite them as internal precedent in stage 2 (case studies can be "internal" as well as external).

Do this only when the user authorizes it; do not auto-scrape the Drive.

---

## Voice rules (non-negotiable)

- No clichés. Never write "unforgettable experience", "tailored to your needs", "exceeding expectations".
- No em-dashes. Use regular hyphens or commas.
- No "we believe / we know / we are committed" openings.
- Numbers are concrete. "₪42,000" not "a competitive budget". "210 guests" not "an intimate gathering".
- Hebrew output uses nikud only when a word is genuinely ambiguous.
- Credits are omitted unless the user explicitly asks.

---

## Error handling

- **Missing data**: if a required field is empty, write `חסר — להשלים מול הלקוח` and continue. Never invent.
- **Skill unavailable**: if `nano-banana` or `veo-video-creator` is not installed, say so and ask whether to proceed with placeholder stills/video.
- **Conflicting instructions between stages**: surface the conflict to the user and ask. Do not silently pick one.

---

## One-line stage-completion format

After each stage, output exactly one line to the user:

```
✓ Stage <N> (<n>) complete. <files created>. Next: Stage <N+1>.
```

or

```
⚠ Stage <N> (<n>) BLOCKED. Reason: <why>. Needed: <what you need>.
```
