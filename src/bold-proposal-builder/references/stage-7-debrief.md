# Stage 7, Debrief & Learning Loop

## Purpose

Bold builds events to serve goals. Stage 7 asks, "did it?" 24 hours after the event, Claude runs a structured debrief against the KPIs captured in Stage 1 field 16, and turns the answers into two kinds of learning:

1. **Client-specific learning**, saved to that client's profile for the next proposal.
2. **Skill-level learning**, proposed as updates to the skill itself for future events.

Without Stage 7, the flow is a one-shot tool. With it, every event makes the skill stronger for the next event.

---

## Triggers

Stage 7 runs when the user opens a new chat from a Trello task link created at the end of Stage 6.

**At Stage 6 Assembly, Claude creates:**
- A Trello card in the user's "Bold, Debriefs" list (or creates the list if missing).
- Due date: the day after the event.
- Card contents: event name, client, date, link back to this conversation (or to a summary file), and a one-line CTA: "להתחיל הפקת לקחים".
- The Trello card includes a pre-written chat prompt the user can copy.

**The user clicks the card, copies the prompt, pastes into a new Claude chat.**

The prompt:
```
הפק לקחים לאירוע [שם אירוע] של [לקוח] שקרה ב-[תאריך].
ההצעה נשמרה ב-GitHub: hemichaeli/bold-proposal-skills או ב-Drive.
תשלוף את הבריף והקובץ KPIs ותעבור איתי עליהם מדד-מדד.
```

---

## The debrief flow

### Part 1: Event happened, basic facts
Claude asks:
- Did the event take place on the planned date?
- Actual attendance vs. planned?
- Any major deviations from the run-sheet?

Short answers. Three sentences total. This is context, not deep analysis.

### Part 2: KPI-by-KPI review
This is the heart of the debrief. Claude pulls the KPIs from `brief.md` field 16 and walks through each one:

```
KPI [n] ([קטגוריה]):
  מדד: [from brief]
  יעד: [from brief]
  חלון מדידה: [from brief]
  מקור נתונים: [from brief]

  בפועל: [ask user]
  פער: [compute]
  אחוז השגה: [compute, e.g. 87% of target]
  
  למה? (1-2 משפטים על הסיבה להישג או לפער)
```

Claude does NOT ask "what do you think?" or "how did it feel?" It asks for numbers. If the number is unknown and retrievable (e.g., Zoho CRM lead count), Claude offers to pull it. If unknown and unretrievable, it's marked "no data" and flagged as a gap for the KPI design next time.

### Part 3: Goal-level summary
After all KPIs, Claude summarizes per goal category:

- **שיווקית**: מטרה X, השגה Y%, הערכה: [מעל / לפי / מתחת ליעד]
- **Fun**: ...
- **מכירתית**: ...
- **תדמיתית**: ...

One line per goal. No adjectives. Just the number.

### Part 4: Root-cause analysis
For each goal that missed target by more than 20%, Claude asks one probing question:

- "מה מהאירוע תרם הכי פחות למטרה הזאת?"
- "אילו החלטות לקח שלקחנו בבריף היו יוצרות תוצאה אחרת?"
- "מי במהלך התכנון לא היה בחדר וחבל שלא היה?"

One question per missed goal. The user answers briefly. Claude does not editorialize.

### Part 5: Client-specific learning
Claude extracts patterns to save for the next Bold proposal to this client:
- What worked disproportionately well?
- What the client's audience specifically liked or ignored?
- What operational surprises we should plan for next time?

These are saved to `data/client-profiles/[client-slug].md`. If the file doesn't exist, Claude creates it.

Example entry:
```markdown
# Phoenix Group, Client Profile

## Events run with Bold
- 2026-06-12: Art Event, Rishon campus (proposal: proposals/phoenix-art-2026/)

## Learned
- Audience skews 50+, declined late-night music activation
- Value deep catering over broad catering; paid attention to wine list
- Marketing director wants press list ahead of event, not just after
- 18:00 start time too early; 19:30 worked for this crowd
```

Next time a Phoenix Group proposal begins, Stage 1 reads this file and seeds the brief with the known constraints.

### Part 6: Skill-level learning
Some patterns aren't client-specific; they're about the flow itself. Claude proposes updates:

- "שדה 6 בבריף (קהל יעד ראשי) החמיץ את העובדה שחצי מהמנהלים הם דוברי ספרדית. שווה להוסיף שדה 'שפות במפגש'?"
- "המחיר לסועד לקייטרינג עלה 15% מהמחיר ב-proposal של 2024. כדאי לעדכן את ה-vendor-registry?"
- "שלב 4a ייצר mockup שהלקוח ביקש להחליף. הפרומפט התבסס על motif שלא חזר כמו שצריך. שווה להוסיף בדיקת consistency ידנית?"

Each proposal is formulated as a concrete change to a specific file in the skill. Claude does NOT apply the changes automatically. Instead:

1. Claude drafts the proposed changes.
2. Claude asks the user to review.
3. On approval, Claude creates a GitHub branch named `debrief/[event-slug]-learning`, commits the changes, and opens a PR.
4. The user reviews the PR in GitHub and merges when ready.

This way, the skill evolves, but every evolution is deliberate.

### Part 7: Close
Claude produces a short summary document: `debrief-[event-slug].md`, saved to the proposal's folder and linked from the Trello card.

The debrief document is shareable with the client if the client is the kind of client who appreciates a report back. It has a section that's internal-only (the root causes, the skill-level learnings) and a section that's client-facing (the KPI numbers and the "what we learned together" section).

---

## Data sources for KPI pulls

Wherever possible, Claude pulls KPI data automatically rather than asking the user to provide it manually. Available integrations:

| Source | Tool |
|---|---|
| CRM leads / deals | Zoho MCP server |
| Email engagement | Gmail MCP |
| Calendar activity post-event | Google Calendar MCP |
| Press mentions | web_search on client + event name |
| Social engagement | web_search + manual review |
| Internal metrics / dashboards | user-provided |

If a KPI designed in Stage 1 turns out to be impossible to measure at Debrief, Claude flags this as a Skill-level learning (Part 6): "KPI type X was not measurable; consider removing or restructuring in future briefs."

---

## Anti-patterns Claude avoids

- **"How did it feel?"** The debrief is about numbers, not vibes. Feelings are captured in Part 4 only as follow-ups to missed KPIs.
- **"That was a great event!"** No adjectives from Claude. The numbers speak.
- **"We learned so much!"** Learnings are concrete file diffs. No platitudes.
- **Editorializing the client's answers.** If the client says "attendance was 60% of target because the weather was bad", Claude doesn't second-guess. It records and moves on.
- **Creating a Trello reminder for the next event's debrief before the current debrief is closed.** One thing at a time.

---

## Output format, `debrief-[event-slug].md`

```markdown
# Debrief, [Event Name]
**לקוח:** [name]
**תאריך האירוע:** [date]
**תאריך ההפקת לקחים:** [date]
**משתתפים בהפקת הלקחים:** [name(s)]

## תמצית מנהלים
[3-4 lines. What was achieved vs. targeted, the one clearest success and the one clearest miss.]

## מדד-מדד
[KPI table with: metric, target, actual, achievement %, explanation]

## מטרות
[Per-goal summary, 1 line each]

## מה למדנו על הלקוח
[Bullet points that will go into the client profile]

## מה למדנו על ה-flow
[Bullet points that may become skill-level PRs]

## המשך
[Trello tasks created for follow-up items. E.g., "לעדכן את vendor-registry.json",
"לכתוב post-event press release", "לקבוע שיחת המשך עם הלקוח בעוד שבועיים"]
```

---

## What "done" looks like

Every KPI has a number against it, a percentage achievement, and a one-line explanation. At least one client-specific learning captured. At least one skill-level learning proposed (even if it's "no changes needed, flow worked"). The client-profile file updated or created. The debrief document saved alongside the proposal. The next Trello follow-up tasks created.

If a debrief closes without proposing ANY skill-level learning across three events in a row, something is off: either the flow is perfect (unlikely), or the debrief is going too shallow. Raise the bar.
