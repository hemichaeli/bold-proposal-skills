# data/client-profiles/

One markdown file per Bold client. Populated at Stage 7 (Debrief) with learnings. Read at Stage 1 (Brief) for subsequent proposals to the same client.

## Naming convention
`[client-slug].md`, lowercase, hyphen-separated. Examples:
- `phoenix-group.md`
- `keren-biotech.md`
- `efrat-pharma.md`

## File structure

Each file has these sections:

```markdown
# [Client Name], Client Profile

## About
Short paragraph: who the client is, who the main contact is, what their business does.

## Events run with Bold
Chronological list of every past event, with link to the proposal folder:
- 2026-06-12: Art Event, Rishon campus (proposal: proposals/phoenix-art-2026/)
- 2025-11-04: Innovation Summit, Tel Aviv (proposal: proposals/phoenix-summit-2025/)

## Learned, audience
What we observed about this client's audience:
- Demographics, behaviors, preferences
- What keeps them in the room, what loses them
- Language, volume, cultural cues

## Learned, client preferences
What the client as an organization prefers:
- Communication style (short emails, phone, WhatsApp)
- Approval process (single decision-maker, committee, founder veto)
- Budget posture (firm ceiling, flexible, staged)
- Deliverable expectations (formal PDF, informal voice memo, full deck)

## Learned, constraints
Hard rules for this client:
- Forbidden vendors (past bad experience)
- Forbidden topics (political sensitivities)
- Mandatory vendors (family business, ownership relationship)
- Legal/regulatory constraints specific to them (pharmaceutical, financial, governmental)

## Learned, success drivers
What made past Bold events for this client work:
- Timing (evening vs. morning)
- Format (seated vs. standing, formal vs. casual)
- Content ratio (speeches vs. socializing vs. content)
- Culinary (preferred service style, dietary mix)

## Learned, avoid
What missed the mark in past events:
- Specific mistakes not to repeat
- Elements that didn't land

## Active relationships
People at the client organization to coordinate with:
- [Name], role, preferred contact method
- [Name], role, preferred contact method

## Key dates / cycles
Annual events, budget cycles, product launch cadences that affect timing.

## Notes
Anything else that doesn't fit above.
```

## When Claude reads these files

At Stage 1, if the new brief is for a client with an existing profile, Claude:
1. Opens the profile file.
2. Pre-seeds the brief with known constraints from "Learned, constraints".
3. Uses "Learned, success drivers" to inform Stage 2 and Stage 3.
4. Confirms with Hemi that the learned context still applies before moving on.

## When Claude writes to these files

At Stage 7, Claude proposes additions to the profile based on the debrief findings. Hemi approves each addition ("כן" / "לא" / "תיקן ככה") before Claude commits to the file (via GitHub branch + PR, same workflow as the skill-level learning described in stage-7-debrief.md).

## What never goes in a client profile

- Raw budget numbers (those are per-event, in the proposal folder)
- Client personal data that isn't relevant to future proposals (personal phone if work phone is known; family details)
- Speculation about the client's finances, health, or private life
- Negative opinions about specific people that could be embarrassing if leaked
