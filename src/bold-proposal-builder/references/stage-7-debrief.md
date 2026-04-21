# Stage 7, Debrief & Learning Loop

## Purpose

Bold builds events to serve goals. Stage 7 asks, "did it?" 24 hours after the event, Claude runs a structured debrief against the KPIs captured in Stage 1 field 16, and turns the answers into two kinds of learning:

1. **Client-specific learning**, saved to that client's profile for the next proposal.
2. **Skill-level learning**, proposed to Hemi for approval, then committed automatically to the repo.

Without Stage 7, the flow is a one-shot tool. With it, every event makes the skill stronger for the next event.

---

## Triggers

Stage 7 runs when Hemi opens a new chat from a Trello task link created at the end of Stage 6.

**At Stage 6 Assembly, Claude creates:**
- A Trello card in the "Bold, Debriefs" board (or creates the board if missing).
- Due date: the day after the event.
- Card title: "הפקת לקחים, [Event Name]"
- Card description: event name, client, date, link to the proposal folder, and a pre-written chat prompt Hemi can copy.
- Card URL is embedded in the proposal's summary.md so Hemi can find it easily.

**The ready-to-paste prompt inside the Trello card:**
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

Short answers. Three sentences total. This is context, not deep analysis.

### Part 2: KPI-by-KPI review
This is the heart of the debrief. Claude pulls the KPIs from `brief.md` field 16 and walks through each one:

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
- "אילו החלטות שלקחנו בבריף היו יוצרות תוצאה אחרת?"
- "מי במהלך התכנון לא היה בחדר וחבל שלא היה?"

One question per missed goal. Hemi answers briefly. Claude does not editorialize.

### Part 5: Client-specific learning
Claude drafts patterns to save for the next Bold proposal to this client:
- What worked disproportionately well?
- What the client's audience specifically liked or ignored?
- What operational surprises we should plan for next time?

These go to `data/client-profiles/[client-slug].md`.

Example entry:
```markdown
# Phoenix Group, Client Profile

## Events run with Bold
- 2026-06-12: Art Event, Rishon campus (proposal: proposals/phoenix-art-2026/)

## Learned
- Audience skews 50+, declined late-night music activation
- Values deep catering over broad catering; paid attention to wine list
- Marketing director wants press list ahead of event, not just after
- 18:00 start time too early; 19:30 worked for this crowd
```

Next time a Phoenix Group proposal begins, Stage 1 reads this file and seeds the brief with the known constraints.

### Part 6: Skill-level learning, propose + approve + commit
This is the **most important** part of the debrief. It's how the skill evolves.

Some patterns aren't client-specific; they're about the flow itself:

- "שדה 6 בבריף (קהל יעד ראשי) החמיץ את העובדה שחצי מהמנהלים הם דוברי ספרדית. הוספתי שדה 'שפות במפגש'."
- "המחיר לסועד לקייטרינג עלה 15% מול ה-proposal של 2024. מעדכן את ה-vendor-registry."
- "שלב 4a ייצר mockup שהלקוח ביקש להחליף. הפרומפט התבסס על motif שלא חזר כמו שצריך. מוסיף בדיקת consistency."

**The approval workflow:**

Claude presents each proposed change in this format:

```markdown
## הצעת שינוי [n]

**קובץ:** src/bold-proposal-builder/references/stage-1-intake.md
**סעיף:** שדה 6 (קהל יעד ראשי)

**מה היה:**
> "פילוח, אפיון, כמות"

**מה אני מציע:**
> "פילוח, אפיון, כמות, שפות דיבור במפגש (חשוב לאירועים בינלאומיים או לחברות עם צוות מעורב)"

**למה:** באירוע Phoenix, חצי מהמנהלים דיברו ספרדית. לא הייתה לזה התייחסות בבריף, ובפועל זה יצר פער באיכות הקליטה של המסרים שהעברנו.

**אושר? (כן / לא / תיקן ככה)**
```

Hemi responds to each proposed change with one of three:
- **"כן"**, Claude commits the change to the repo under a branch named `debrief/[event-slug]`, and opens a PR into `main`.
- **"לא"**, the proposal is dropped. Claude doesn't argue, doesn't retry. Saves the reasoning to Hemi's scratchpad ("proposed but rejected, [date]") so the same suggestion doesn't recur in future debriefs.
- **"תיקן ככה: [edit]"**, Claude adjusts the change per Hemi's instruction, re-presents it. Once Hemi says "כן", commits as described.

**The automated commit:**

When Hemi approves, Claude performs (no further confirmation needed):

1. Creates branch `debrief/[event-slug]` from `main` if it doesn't already exist.
2. Commits the approved change to that branch with a message: "Debrief learning from [event]: [one-line description]".
3. After all approved changes are committed, opens a single PR into `main` titled "Debrief learnings from [event name]" with a body that lists all changes and links back to the debrief document.
4. Hemi can merge the PR from GitHub whenever. Typically: immediately, if changes are small; after a cooling period, if changes are structural.

**What Claude must NEVER do:**
- Commit a change without an explicit "כן" from Hemi.
- Batch-approve changes as "all yes" without going one by one.
- Apply a change directly to `main` (always through a branch + PR).
- Re-propose a change that was rejected in a prior debrief unless Hemi raises it again.

### Part 7: Close
Claude produces a short summary document: `debrief-[event-slug].md`, saved to the proposal's folder and linked from the Trello card.

The debrief document has a section that's internal-only (root causes, skill-level learnings) and a section that's client-facing (the KPI numbers and the "what we learned together" section) if the client is the kind who appreciates a report back.

---

## Data sources for KPI pulls

Wherever possible, Claude pulls KPI data automatically rather than asking Hemi to provide it manually. Available integrations:

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
- **Editorializing Hemi's answers.** If Hemi says "attendance was 60% of target because the weather was bad", Claude doesn't second-guess. It records and moves on.
- **Creating a Trello reminder for the next event's debrief before the current debrief is closed.** One thing at a time.
- **Auto-committing without approval.** Ever. Even tiny changes. Even obvious fixes.

---

## Output format, `debrief-[event-slug].md`

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

Every KPI has a number against it, a percentage achievement, and a one-line explanation. At least one client-specific learning captured. At least one skill-level learning proposed (even if Hemi ultimately rejects it). The client-profile file updated or created. The debrief document saved alongside the proposal. A GitHub PR opened with all approved skill changes. The next Trello follow-up tasks created.

If a debrief closes without proposing ANY skill-level learning across three events in a row, something is off: either the flow is perfect (unlikely), or the debrief is going too shallow. Raise the bar.
