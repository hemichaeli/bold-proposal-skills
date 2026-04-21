---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow that moves from brief gathering through research, three-direction brand heart selection, three-direction visualization selection, specialist design (content, operations, culinary), budget, assembly, and post-event debrief. Use this skill whenever Hemi Michaeli asks to build, draft, create, or prepare a proposal, pitch, or event concept for a Bold client. Also triggers for related phrases in Hebrew like "לבנות הצעה", "לכתוב פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Use also when the user mentions a specific Bold client (Phoenix, Keren, Efrat, etc.) and wants event work. The flow produces a full client-facing package including strategy, brand system, visual mockups, atmosphere video, agenda, scripts, menu, operations plan, budget Excel, designed PDF, Gamma prompt, KPIs scorecard, and a Trello debrief reminder. Requires nano-banana and veo-video-creator skills to be installed for Stage 4 (visualization).
license: Proprietary
---

# Bold Proposal Builder (v2.1)

A 7-stage orchestrator for producing premium event proposals for Bold Productions. The skill does not improvise: each stage reads a reference file in `references/`, produces its artifacts, and hands off to the next. Skip stages and the final proposal fragments; the sequence is load-bearing.

---

## The seven stages

| Stage | Name | Reference | Output |
|---|---|---|---|
| 1 | Intake & Brief | `references/stage-1-intake.md` | `brief.md`, `challenges.md`, KPIs |
| 2 | Research | `references/stage-2-research.md` | `trends.md`, `case-studies.md`, `inspiration.md` |
| 3 | Brand heart, **3 directions** | `references/stage-3-brand-heart.md` | `directions.md` then `brand-system.md` |
| 4a | Visualization, **3 directions** | `references/stage-4a-visualization.md` | hero mockups, full mockup set, atmosphere video, `mood-direction.md` |
| 4b | Content & experience | `references/stage-4b-content-experience.md` | `agenda.md`, `scripts.md` |
| 4c | Operations | `references/stage-4c-operations.md` | `logistics.md` |
| 4d | Culinary | `references/stage-4d-culinary.md` | `menu.md` |
| 5 | Budget | `references/stage-5-budget.md` | `budget.json` (sources from `data/vendor-registry.json`) |
| 6 | Assembly | `references/stage-6-assembly.md` | `proposal.pdf`, `budget.xlsx`, `kpis-scorecard.md`, `gamma-prompt.md`, `summary.md`, Trello card |
| 7 | Debrief | `references/stage-7-debrief.md` | `debrief-[event].md`, client profile update, preferences update, skill PR |

---

## The four goal categories

Bold builds events to serve goals. At Stage 1, the client's goals are classified into one or more of four categories. Every downstream decision is checked against these goals. At Stage 7, actual outcomes are measured against the KPIs derived from them.

1. **שיווקית (Marketing)**, awareness, reach, brand memory.
2. **Fun (Experience)**, enjoyment, bonding, emotional resonance.
3. **מכירתית (Sales)**, leads, conversions, closed deals.
4. **תדמיתית (Reputation)**, perception shift, positioning, narrative control.

A single event can serve any combination. Each selected goal produces at least one KPI.

---

## The three-directions principle (v2.1, applied at Stage 3 and Stage 4a)

Both Stage 3 and Stage 4a operate on the same principle:

- Claude proposes **three distinct directions** along a chosen axis (e.g., tone/energy/frame for concept; density/light/material for visual).
- Each direction has a **visual representation** (abstract reference for Stage 3, hero mockup for Stage 4a).
- Hemi picks one. That pick gets fully developed.
- If none land, Claude asks one clarifying question, picks a **different axis**, and proposes three new directions. Max 3 rejection cycles per stage.
- **Stretch policy:** Always one of the three directions is a deliberate stretch. Never collapse all three to safe, on-taste picks.

### Learning Hemi over time
Every selection is logged to `data/hemi-preferences.md`. After 3+ events, Claude uses the log to propose more calibrated three-direction sets. This file is read at the start of every Stage 3 and Stage 4a session.

Updates to hemi-preferences.md go through the same approval workflow as skill-level learnings (Stage 7, Part 6): Claude proposes, Hemi approves ("כן" / "לא" / "תיקן ככה"), Claude auto-commits to a branch + opens PR.

---

## Voice rules (non-negotiable across all stages)

### Hebrew-first
- All client deliverables in Hebrew unless the client is English-speaking.
- Internal artifacts (e.g., `challenges.md`) can be in Hebrew or English.
- Numbers in Western digits; dates in Israeli format (DD.MM.YYYY).

### No long dashes
- Never em-dash or en-dash.
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

- **Gate 1 to 2:** Brief must have fields 1, 3 (with at least one goal category selected), 6, 14, 16 filled.
- **Gate 2 to 3:** At least 3 trends + 3 case studies + 5 inspiration references sourced.
- **Gate 3 to 4:** Hemi picked one direction from a three-direction set; `brand-system.md` has all 9 fields filled based on that pick.
- **Gate 4a to 4b/c/d:** Hemi picked one visual direction; full mockup set + atmosphere video + `mood-direction.md` produced.
- **Gate 4 to 5:** All four specialist outputs exist and reference the chosen brand system and visual direction.
- **Gate 5 to 6:** Budget `summary.subtotal` is non-null; at least 70% of non-internal lines have `source_vendor_registry` populated.
- **Gate 6 to done:** All six Stage 6 artifacts produced; Trello debrief card created.
- **Gate 7:** Runs 24 hours after the event, triggered by Hemi from a Trello card.

---

## When things are missing

### Missing nano-banana or veo-video-creator
Stage 4a requires both. Without them, Stage 4a cannot run the three-directions method (the hero mockups require nano-banana) and cannot produce the atmosphere video. Claude tells Hemi to install them.

### Missing hemi-preferences.md
First-ever run. Claude creates the file from `data/hemi-preferences.md` template. Stage 3 and Stage 4a still run with three generic directions (no prior learning), and start populating the log from event one.

### Missing vendor registry
Stage 5 requires `data/vendor-registry.json`. If missing or stale (>90 days), Claude prompts Hemi to populate from Drive via interactive extraction using the Google Drive MCP. Meanwhile, Stage 5 can run with lines flagged "awaiting vendor quote".

### Missing Trello MCP
Stage 6 creates the debrief card via Trello MCP. If unavailable, falls back to `DEBRIEF-REMINDER.md` file + Gmail reminder.

### Missing client profile
Stage 7 writes to `data/client-profiles/[slug].md`. If first time with a client, Claude creates the file.

---

## How Claude should start each session

1. Check for pre-existing brief/transcript input (attached file, pasted text, Fireflies reference).
2. If the request mentions a known client, read `data/client-profiles/[slug].md` if it exists and seed Stage 1 with the known constraints.
3. Read `data/hemi-preferences.md` to calibrate future Stage 3 and Stage 4a direction sets.
4. Verify the vendor registry is present and fresh (warn if not).
5. Begin Stage 1 by presenting the brief fields to the user.

Do NOT start with research or with a creative pitch. The brief is the gate.

---

## Success

The final deliverable is not the PDF. The final deliverable is a client who, 30 days after the event, can point to specific numbers and say "Bold helped me hit these". Stage 7 closes the loop. The flow exists to serve that.

Secondary success: over 5-10 events, the skill proposes three-direction sets that land more often, because it has learned Hemi. But it never stops offering stretch directions. The day Claude only offers safe picks is the day the skill stops being useful.
