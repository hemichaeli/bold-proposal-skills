# Stage 1, Intake & Brief Reference (v2)

## Purpose

Stage 1 is the gate. Nothing starts until the brief is complete enough to justify the work that follows. Bold's 2001-era brief form is the foundation; v2 adds explicit goal classification and KPIs because Bold always builds events to serve goals, and those goals must be measurable at Debrief (Stage 7).

The flow produces two artifacts:
- `01-intake/brief.md`, the filled-in brief itself.
- `01-intake/challenges.md`, Claude's strategic reading of the brief, setting up Stage 2.

---

## Inputs

In priority order:

1. **Fireflies transcript**, if the user pastes one or references a recent call, Claude reads it first and pre-fills every field it can extract. Extraction is conservative: if the transcript is ambiguous, leave the field blank and ask.

2. **Prior project files**, if the user grants Drive access, Claude pulls from prior proposals for the same client to pre-fill "mandatory constraints", "forbidden elements", and "preferred vendors".

3. **Interactive intake**, the user and Claude fill the remaining fields through structured questions. One question at a time. Specific, not open-ended ("how many guests" not "tell me about the event").

---

## The brief fields

The fields mirror Bold's original 2001 form (`assets/brief-form-original.md`) with three additions: goal classification (field 3), KPIs (field 16), and undisclosed constraints (field 18).

### Contact
- שם ממלא הבריף
- תפקיד
- טלפון
- דוא"ל

### 1. The reason why
Why this event, why now. One paragraph. The cause, not the excuse.

### 2. Event type (one or more checkboxes)
- כנס / קד"מ חוויתי / תערוכה / אירוע חברה / פסטיבל / מסיבת עיתונאים / השקה / מנהלים / מכירות / יח"צ

### 3. Event goals, classified
This is the spine of Stage 7. Every goal selected here becomes a KPI in field 16 and a measurement target at Debrief.

Goals fall into four categories. An event can serve one, several, or all four, but each one chosen requires a specific goal statement:

- שיווקית (Marketing), awareness, reach, engagement, brand memory. If selected, ask: "איזה מדד שיווקי תרצה שיזוז?"
- Fun (Experience), enjoyment, bonding, emotional resonance. If selected, ask: "איך נדע שהאורחים נהנו?"
- מכירתית (Sales), leads, conversions, closed deals. If selected, ask: "כמה עסקאות, באיזה סכום, באיזה פרק זמן?"
- תדמיתית (Reputation), perception shift, narrative control. If selected, ask: "איזו תפיסה תשתנה, בקרב איזה קהל?"

Each selected goal produces a short statement: "להגדיל את מספר ההרשמות מ-400 ל-600 תוך 30 יום אחרי האירוע". Goals without numbers are not goals; they are wishes. Reject them and ask again.

### 4. Date / optional dates
Up to four, in priority order. Day of week + time per date.

### 5. Hours of operation
Opening, peak, closing. Israeli events benefit from acknowledging that guests arrive late.

### 6. Primary audience
Segmentation, characterization, headcount. Headcount drives most downstream scale decisions.

### 7. Secondary audience
Everyone else in the room: press, influencers, end-customers, employees, partners, reluctant attendees.

### 8. Messages to embed
Up to three. One sentence each. More than three = none retained.

### 9. Known / desired content
Speakers already confirmed, films to be screened, planned presentations, booked performers.

### 10. Past events in this space
What this client (or competitors, or the industry) did before. What worked. What didn't. Feeds Stage 2 research.

### 11. Past performers
Performers who appeared at this client's prior events. Don't repeat.

### 12. Design / brand guidelines
Colors to preserve, materials to avoid, safety / accessibility / kashrut / halakha / personal preference notes.

### 13. Ancillary needs
Video / stills documentation, giveaways, recording for external distribution, live stream, simultaneous translation, heightened security, subsidized parking / valet, shuttles.

### 14. Budget
Range or exact. Without a number, no Stage 5.

### 15. Deadline for proposal delivery
When the client expects the proposal. Drives the pace of the remaining stages.

### 16. KPIs and success measures (NEW)
Derived from the goals in field 3. Each goal becomes at least one KPI. Each KPI has:
- Metric (what is being counted)
- Current baseline (if known)
- Target (specific number or percentage)
- Time window (when it will be measured, usually 24h / 7d / 30d after event)
- Data source (how we'll get the number at Debrief)

Example for a product launch with marketing + sales goals:
```
KPI 1 (marketing):
  Metric: Press mentions of the product in Israeli tech media
  Baseline: 0 (pre-launch)
  Target: 8 mentions in first-tier outlets
  Window: 7 days post-event
  Source: manual scan of Globes, Calcalist, TheMarker, Geektime

KPI 2 (sales):
  Metric: Qualified leads entered into CRM
  Baseline: 0
  Target: 25
  Window: 72 hours post-event
  Source: Zoho CRM lead source = "Launch Event 2026"
```

Minimum: one KPI per selected goal. More is fine. Fewer is rejected.

### 17. Competitive context (NEW)
Is Bold the only agency proposing, or one of several? Affects the depth of the proposal and the pitch.

### 18. Undisclosed constraints (NEW)
Things the client hasn't written because they assume they're obvious: CEO doesn't like music in Hebrew, founder won't speak publicly, a past event failure to avoid repeating. Ask directly: "What would make you reject a proposal even if everything else was perfect?"

---

## The gate

Before leaving Stage 1, these fields MUST be filled:

| # | Field | Why it blocks |
|---|---|---|
| 1 | Reason why | Without it, the event has no thesis |
| 3 | Goals (classified) | Stage 7 has nothing to measure |
| 6 | Primary audience + headcount | Every scale decision downstream breaks |
| 14 | Budget (even a range) | Stage 5 has no ceiling |
| 16 | KPIs | Debrief has nothing to check against |

If any of these five are missing, Claude does not move to Stage 2.

---

## challenges.md, strategic reading output

After the brief is filled, Claude writes a short strategic reading, 1 to 2 pages:

```markdown
# קריאה אסטרטגית, [שם אירוע]

## מה באמת נמכר כאן
[One paragraph on the underlying business or brand moment.]

## המתחים (tensions to preserve)
1. [Tension 1]
2. [Tension 2]
3. [Tension 3 if relevant]

## המטרות והמשמעויות
For each goal selected in field 3:
  - Goal: [...]
  - Implies: [...]
  - Rules out: [...]

## סיכונים וסיכויים
Three risks and three opportunities.

## הנחות שהנחתי
Assumptions made where non-gated fields were missing.
```

---

## Handling Fireflies input

1. Extract what's there, don't invent.
2. Flag contradictions between speakers.
3. Mark sentiment cues in field 18.
4. Never quote directly, paraphrase.

---

## Vendor registry preload

Before writing the brief, Claude checks for `data/vendor-registry.json`. If missing or stale (>90 days old), Claude prompts the user to populate it from Drive via interactive extraction.

---

## What "done" looks like

A brief.md that a stranger could execute from, a challenges.md that reads like a senior strategist spent an hour thinking about the brief, and no blocked gate fields.
