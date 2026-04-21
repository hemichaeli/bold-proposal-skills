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
**This is the spine of Stage 7.** Every goal selected here becomes a KPI in field 16 and a measurement target at Debrief.

Goals fall into four categories. An event can serve one, several, or all four, but each one chosen requires a specific goal statement:

- [ ] **שיווקית (Marketing)**, awareness, reach, engagement, brand memory.
  *If selected, ask:* "איזה מדד שיווקי תרצה שיזוז? הרשמות, אזכורים בתקשורת, שיתופים ברשת, זיהוי מותג?"
  
- [ ] **Fun (Experience)**, enjoyment, bonding, emotional resonance.
  *If selected, ask:* "איך נדע שהאורחים נהנו? משוב איכותני, שיתוף תמונות ברשת, חזרות לעוד אירועים?"
  
- [ ] **מכירתית (Sales)**, leads, conversions, closed deals, pipeline movement.
  *If selected, ask:* "כמה עסקאות, באיזה סכום, באיזה פרק זמן אחרי האירוע?"
  
- [ ] **תדמיתית (Reputation / positioning)**, perception shift, narrative control, crisis response.
  *If selected, ask:* "איזו תפיסה אנחנו רוצים שתשתנה, בקרב איזה קהל, ועד מתי?"

Each selected goal produces a short statement: "להגדיל את מספר ההרשמות לרשימת תפוצה מ-400 ל-600 תוך 30 יום אחרי האירוע". Goals without numbers are not goals; they are wishes. Reject them and ask again.

### 4. Date / optional dates
Up to four, in priority order. Day of week + time per date.

### 5. Hours of operation
Opening, peak, closing. Israeli events in particular benefit from acknowledging that guests arrive late.

### 6. Primary audience
Segmentation (age, role, industry, gender if relevant), characterization, headcount. Headcount drives most downstream scale decisions.

### 7. Secondary audience
Everyone else in the room: press, influencers, end-customers, employees, partners, reluctant attendees.

### 8. Messages to embed
Up to three. One sentence each. More than three = none retained.

### 9. Known / desired content
Speakers already confirmed, films to be screened, planned presentations, booked performers. What already exists and doesn't need to be invented.

### 10. Past events in this space
What this client (or competitors, or the industry) did before. What worked. What didn't. Feeds Stage 2 research.

### 11. Past performers
Performers who appeared at this client's prior events. Don't repeat. Includes MCs, singers, bands, comedians, visual artists, TED-style speakers.

### 12. Design / brand guidelines
Colors that must be preserved, materials to avoid, safety / accessibility / kashrut / halakha / personal preference notes from leadership.

### 13. Ancillary needs
Video / stills documentation, giveaways, recording for external distribution, live stream, simultaneous translation, heightened security, subsidized parking / valet, shuttles.

### 14. Budget
Range or exact. Without a number, no Stage 5. If the client resists a number, press for upper and lower bounds.

### 15. Deadline for proposal delivery
When the client expects the proposal. Drives the pace of the remaining stages.

### 16. KPIs and success measures (NEW)
Derived from the goals in field 3. Each goal becomes at least one KPI. Each KPI has:
- **Metric** (what is being counted)
- **Current baseline** (if known)
- **Target** (specific number or percentage)
- **Time window** (when it will be measured, usually 24h / 7d / 30d after event)
- **Data source** (how we'll get the number at Debrief)

Example for a product launch with marketing + sales goals:
```
KPI 1 (marketing):
  Metric: Press mentions of the product in Israeli tech media
  Baseline: 0 (pre-launch)
  Target: 8 mentions in first-tier outlets
  Window: 7 days post-event
  Source: manual scan of Globes, Calcalist, TheMarker, Geektime

KPI 2 (sales):
  Metric: Qualified leads entered into CRM by attending sales team
  Baseline: 0
  Target: 25
  Window: 72 hours post-event
  Source: Zoho CRM lead source = "Launch Event 2026"

KPI 3 (reputation):
  Metric: Positive / neutral / negative sentiment ratio in press coverage
  Baseline: prior sentiment from brand tracker
  Target: 80% positive or neutral
  Window: 14 days post-event
  Source: manual review + Talkwalker / Mentionlytics if available
```

Minimum: one KPI per selected goal. More is fine. Fewer is rejected.

### 17. Competitive context (NEW)
Is Bold the only agency proposing, or one of several? If competitive, how many, and what's the client's likely priority ranking (price / creative / execution reliability)? Affects the depth of the proposal and the pitch.

### 18. Undisclosed constraints (NEW)
Things the client hasn't written because they assume they're obvious to them: CEO doesn't like music in Hebrew, founder won't speak publicly, a specific past event failure they're avoiding. Extract from Fireflies if possible; otherwise ask directly: "What would make you reject a proposal even if everything else was perfect?"

---

## The gate

Before leaving Stage 1, these fields MUST be filled. All of them. Not most:

| # | Field | Why it blocks |
|---|---|---|
| 1 | Reason why | Without it, the event has no thesis |
| 3 | Goals (classified) | Stage 7 has nothing to measure |
| 6 | Primary audience + headcount | Every scale decision downstream breaks |
| 14 | Budget (even a range) | Stage 5 has no ceiling |
| 16 | KPIs | Debrief has nothing to check against |

If any of these five are missing, Claude does not move to Stage 2. It goes back and asks.

Fields 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 17, 18 are strongly preferred but not blocking. Where they're missing, Claude notes their absence in `challenges.md` as assumptions that will need client confirmation.

---

## `challenges.md`, strategic reading output

After the brief is filled, Claude writes a short strategic reading. 1 to 2 pages. Structure:

```markdown
# קריאה אסטרטגית, [שם אירוע]

## מה באמת נמכר כאן
[One paragraph. The business or brand moment this event is actually for,
underneath the stated reason-why. Often the stated reason and the real
reason diverge; name both.]

## המתחים (tensions to preserve)
1. [Tension 1]
2. [Tension 2]
3. [Tension 3 if relevant]

Tensions are what make the event alive. "Intimate but grand." "Professional
but not corporate." "Celebratory but restrained." Without tension, the event
flattens into a template.

## המטרות והמשמעויות
For each goal selected in field 3:
  - Goal: [...]
  - What this goal implies for the event: [1-2 sentences]
  - What this goal rules OUT: [1 sentence; this is as important]

## סיכונים וסיכויים (Risks and opportunities)
Three risks (what could kill the event's effect) and three opportunities
(what could elevate it beyond the brief).

## הנחות שהנחתי
If any non-gated field was missing from the brief, Claude lists the
assumption it's making and flags for client confirmation before Stage 6.
```

This document drives Stage 2 (research), Stage 3 (brand heart), and informs the strategic-reading pages of the Stage 6 PDF.

---

## Handling Fireflies input

When the user provides a transcript or a Fireflies link:

1. **Extract what's there**, don't invent. If the transcript mentions "the Phoenix Group event in June" without specifying a date, the date field remains empty; it does NOT become "June 2026".

2. **Flag contradictions**, if two speakers disagree on a fact (budget range, headcount), note both and ask the user which is correct.

3. **Mark sentiment cues**, if the client sounded hesitant about something or excited about something else, note it in field 18 (undisclosed constraints). These signals are gold.

4. **Never quote directly**, paraphrase. The transcript may contain off-the-record remarks not intended for a proposal.

---

## Vendor registry preload (NEW, v2)

Before writing the brief, if this is the first time the user is running this skill since v2, Claude checks for `data/vendor-registry.json`. If it doesn't exist or is stale (>90 days old), prompt the user to run `scripts/extract-vendor-data.py` to populate it from Drive.

The vendor registry doesn't directly affect Stage 1, but it must be current before Stage 5 runs.

---

## What "done" looks like

A `brief.md` that a stranger could read and execute from, a `challenges.md` that reads like a senior strategist spent an hour thinking about the brief, and no blocked gate fields.

If any of those are shaky, Stage 1 is not done. Going into Stage 2 with a weak brief is the single biggest cause of mediocre proposals; do not rush past this stage.
