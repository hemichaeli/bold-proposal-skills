# Stage 7, Debrief & Learning Loop

## Purpose

Bold builds events to serve goals. Stage 7 asks, "did it?" 24 hours after the event, Claude runs a structured debrief against the KPIs captured in Stage 1 field 16, and turns the answers into two kinds of learning:

1. Client-specific learning, saved to that client's profile for the next proposal.
2. Skill-level learning, proposed to Hemi for approval, then committed automatically to the repo.

Without Stage 7, the flow is a one-shot tool. With it, every event makes the skill stronger for the next event.

---

## Triggers

Stage 7 runs when Hemi opens a new chat from a Trello task link created at the end of Stage 6.

### At Stage 6 Assembly, Claude creates:
- A Trello card in the "Bold, Debriefs" board
- Due date: the day after the event
- Card title: "הפקת לקחים, [Event Name]"
- Card description: event name, client, date, links, and a pre-written chat prompt Hemi can copy
- Card URL embedded in the proposal's summary.md

### Ready-to-paste prompt inside the Trello card:
```
הפק לקחים לאירוע [שם אירוע] של [לקוח] שהתקיים ב-[תאריך].
ההצעה והבריף נשמרים ב-GitHub: hemichaeli/bold-proposal-skills 
תחת proposals/[slug]/ או ב-Drive.
תשלוף את הבריף ואת ה-KPIs ותעבור איתי עליהם מדד-מדד.
```

---

## The debrief flow

### Part 1: Event happened, basic facts
Claude asks:
- Did the event take place on the planned date?
- Actual attendance vs. planned?
- Any major deviations from the run-sheet?

Short answers. Three sentences total.

### Part 2: KPI-by-KPI review
This is the heart of the debrief. Claude pulls the KPIs from brief.md field 16 and walks through each one:

```
KPI [n] ([קטגוריה]):
  מדד: [from brief]
  יעד: [from brief]
  חלון מדידה: [from brief]
  מקור נתונים: [from brief]

  בפועל: [ask Hemi]
  פער: [compute]
  אחוז השגה: [compute, e.g. 87% of target]
  
  למה? (1-2 משפטים על הסיבה להישג או לפער)
```

Claude asks for numbers, not feelings. If a number is retrievable (e.g., Zoho CRM lead count), Claude offers to pull it.

### Part 3: Goal-level summary
After all KPIs, summarize per goal category:

- שיווקית: מטרה X, השגה Y%, הערכה: [מעל / לפי / מתחת ליעד]
- Fun: ...
- מכירתית: ...
- תדמיתית: ...

One line per goal. No adjectives. Just the number.

### Part 4: Root-cause analysis
For each goal that missed target by more than 20%, one probing question:

- "מה מהאירוע תרם הכי פחות למטרה הזאת?"
- "אילו החלטות שלקחנו בבריף היו יוצרות תוצאה אחרת?"
- "מי במהלך התכנון לא היה בחדר וחבל שלא היה?"

Hemi answers briefly. Claude does not editorialize.

### Part 5: Client-specific learning
Claude drafts patterns to save for the next proposal to this client:
- What worked disproportionately well?
- What the client's audience specifically liked or ignored?
- What operational surprises to plan for next time?

These go to `data/client-profiles/[client-slug].md`. Next time a proposal for this client begins, Stage 1 reads this file.

### Part 6: Skill-level learning, propose + approve + commit

This is the most important part. It's how the skill evolves.

Claude presents each proposed change in this format:

```markdown
## הצעת שינוי [n]

**קובץ:** src/bold-proposal-builder/references/stage-1-intake.md
**סעיף:** שדה 6 (קהל יעד ראשי)

**מה היה:**
> "פילוח, אפיון, כמות"

**מה אני מציע:**
> "פילוח, אפיון, כמות, שפות דיבור במפגש"

**למה:** באירוע Phoenix, חצי מהמנהלים דיברו ספרדית. לא הייתה לזה התייחסות בבריף.

**אושר? (כן / לא / תיקן ככה)**
```

Hemi responds with one of three:
- "כן", Claude commits the change to a branch named `debrief/[event-slug]`, opens a PR into main
- "לא", the proposal is dropped. Saved to Hemi's scratchpad so the same suggestion doesn't recur
- "תיקן ככה: [edit]", Claude adjusts per Hemi's instruction, re-presents

When Hemi approves, Claude performs (no further confirmation):
1. Creates branch `debrief/[event-slug]` from main if it doesn't exist
2. Commits the approved change with message "Debrief learning from [event]: [one-line description]"
3. After all approved changes are committed, opens a single PR titled "Debrief learnings from [event name]"
4. Hemi merges the PR from GitHub whenever

What Claude must NEVER do:
- Commit a change without an explicit "כן" from Hemi
- Batch-approve changes as "all yes" without going one by one
- Apply a change directly to main (always through a branch + PR)
- Re-propose a change rejected in a prior debrief unless Hemi raises it again

### Part 7: Close
Claude produces a short summary document: `debrief-[event-slug].md`, saved to the proposal's folder and linked from the Trello card.

---

## Data sources for KPI pulls

Wherever possible, Claude pulls KPI data automatically:

| Source | Tool |
|---|---|
| CRM leads / deals | Zoho MCP server |
| Email engagement | Gmail MCP |
| Calendar activity post-event | Google Calendar MCP |
| Press mentions | web_search on client + event name |
| Social engagement | web_search + manual review |
| Internal metrics | user-provided |

If a KPI designed in Stage 1 turns out to be impossible to measure at Debrief, Claude flags this as a skill-level learning.

---

## Anti-patterns Claude avoids

- "How did it feel?", the debrief is about numbers, not vibes.
- "That was a great event!", no adjectives from Claude.
- "We learned so much!", learnings are concrete file diffs.
- Editorializing Hemi's answers.
- Creating the next event's debrief reminder before this debrief is closed.
- Auto-committing without approval. Ever. Even tiny changes.

---

## Output format

```markdown
# Debrief, [Event Name]
**לקוח:** [name]
**תאריך האירוע:** [date]
**תאריך הפקת הלקחים:** [date]
**משתתפים:** [names]

## תמצית מנהלים
[3-4 lines. What was achieved vs. targeted, the one clearest success and the one clearest miss.]

## מדד-מדד
[KPI table with: metric, target, actual, achievement %, explanation]

## מטרות
[Per-goal summary, 1 line each]

## מה למדנו על הלקוח
[Bullet points, saved to client profile]

## מה למדנו על ה-flow
[Bullet points for skill-level PR; marks which were approved/rejected]

## PR
Link to the opened PR with all approved changes.

## המשך
[Trello tasks created for follow-up items.]
```

---

## What "done" looks like

Every KPI has a number, a percentage achievement, and a one-line explanation. At least one client-specific learning captured. At least one skill-level learning proposed (even if rejected). Client-profile file updated or created. Debrief document saved. GitHub PR opened with approved changes. Next Trello follow-up tasks created.

If a debrief closes without proposing ANY skill-level learning across three events in a row, something is off. Raise the bar.
