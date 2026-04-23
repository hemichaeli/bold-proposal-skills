---
name: bold-proposal-builder
description: Build premium event proposals for Bold Productions, a Tel-Aviv event production company, through a 7-stage flow, brief gathering, research, three-direction brand heart selection, three-direction visualization, content/operations/culinary specialists, budget, assembly, and post-event debrief. Use whenever Hemi Michaeli asks to build, draft, or prepare a proposal or event concept for a Bold client. Also triggers for "לבנות הצעה", "פיץ' לאירוע", "הצעת מחיר לכנס", "קונספט לאירוע של". Mentions of Phoenix, Keren, Efrat clients also trigger. Produces a client-facing package, strategy, brand system, mockups, atmosphere video, agenda, scripts, menu, operations, budget XLSX, designed PDF, Gamma prompt, KPIs scorecard, Trello debrief reminder. Requires nano-banana, veo-video-creator, and premium-deck-strategist skills.
license: Proprietary
---

# Bold Proposal Builder (v2.2)

A 7-stage orchestrator for producing premium event proposals for Bold Productions. The skill does not improvise: each stage reads a reference file in `references/`, produces its artifacts, and hands off to the next. Skip stages and the final proposal fragments; the sequence is load-bearing.

## Required companion skills

This skill calls out to three other skills during the flow. All three must be installed:

| Skill | Used in | Purpose |
|---|---|---|
| **nano-banana** | Stage 3, Stage 4a | Generate visual references and hero mockups for three-direction selection |
| **veo-video-creator** | Stage 4a | Generate 10-15 second atmosphere video after visual direction is chosen |
| **premium-deck-strategist** | Stage 6 | Build the slide-by-slide deck spec for `proposal.pdf` (Rule of Three, max 5 words per bullet, Bold palette override) |

If any is missing, Claude warns Hemi at the start of the session and offers fallbacks where possible.

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
| 5 | Budget | `references/stage-5-budget.md` | `budget.json` (uses `data/vendor-registry.json`) |
| 6 | Assembly | `references/stage-6-assembly.md` | PDF (via premium-deck-strategist), XLSX, KPIs scorecard, Gamma prompt, summary, Trello card |
| 7 | Debrief | `references/stage-7-debrief.md` | `debrief-[event].md`, client profile, preferences update, skill PR |

## The four goal categories

1. שיווקית (Marketing)
2. Fun (Experience)
3. מכירתית (Sales)
4. תדמיתית (Reputation)

## The three-directions principle

Both Stage 3 and Stage 4a propose three distinct directions along a chosen axis. Each direction has a visual representation. Hemi picks one. If none land, Claude asks one clarifying question, picks a different axis, proposes three new. Max 3 rejection cycles per stage. Stretch policy: always one stretch direction per set.

### Learning Hemi over time
Every selection logged to `data/hemi-preferences.md`. Read at start of every Stage 3 and Stage 4a session.

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
- Gate 5→6: 70%+ lines reference vendor registry.
- Gate 6→done: Six Stage 6 artifacts + Trello debrief card.
- Gate 7: Runs 24h after event from Trello card.

## Session start

1. Check for brief/transcript input.
2. Read client profile if known.
3. Read hemi-preferences.md.
4. Verify vendor registry.
5. Verify companion skills present (nano-banana, veo-video-creator, premium-deck-strategist).
6. Begin Stage 1.

## Success

Final deliverable: a client who, 30 days after the event, can say "Bold helped me hit these specific numbers". Secondary: over 5-10 events, three-direction sets land more often, but Claude never stops offering stretch directions.
