# Bold Proposal Skills

Claude skills for Bold Productions (חברת ההפקה "שלי"). Three of them work together as a pipeline that produces end-to-end, premium event-production proposals; a fourth, `rtl-hebrew-docs`, is a standalone utility for generating professional right-to-left Hebrew documents (PDF / DOCX / PPTX).

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    bold-proposal-builder                        │
│                   (6-stage orchestrator)                        │
│                                                                 │
│  Stage 1  Intake          → brief + challenges                  │
│  Stage 2  Research        → trends + case studies + inspo       │
│  Stage 3  Brand Heart     → concept, palette, motif, tone       │
│  Stage 4  Specialists     → visual, content, ops, culinary      │
│                                   │                             │
│                          ┌────────┴────────┐                    │
│                          ▼                 ▼                    │
│                    nano-banana      veo-video-creator           │
│                  (Gemini image gen)  (Veo video via MCP)        │
│                                                                 │
│  Stage 5  Budget          → structured JSON                     │
│  Stage 6  Assembly        → PDF + XLSX + Gamma prompt + MP4     │
└─────────────────────────────────────────────────────────────────┘
```

The orchestrator owns the pipeline. The two specialist skills handle the heavy visual work and are called in stage 4.

## The skills

### `bold-proposal-builder`

Main orchestrator. Six stages, each with its own reference file. Works from a free-form description, a phone call summary, a Fireflies transcript, or an email thread. Produces a working directory with structured artifacts at every stage, then assembles four final deliverables:

1. **`proposal.pdf`** the designed proposal PDF (14-22 pages)
2. **`budget.xlsx`** detailed Excel with formulas, RTL, conditional line items (built by the bundled `build_budget_xlsx.py` script using `openpyxl`)
3. **`gamma-prompt.md`** ready-to-paste prompt for Gamma.app
4. **`summary.md`** 1-page executive summary for WhatsApp/email intro

Voice rules enforced across all outputs: no clichés, no em-dashes, no "unforgettable experience" language, specific numbers not vague adjectives, Hebrew-first.

### `nano-banana`

Wraps Google's Gemini image generation API (the model family known as Nano Banana). Three models available:

| Model | Model ID | Use |
|---|---|---|
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | Default for iteration |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Hero shots, text-in-image, 4K |
| Nano Banana v1 | `gemini-2.5-flash-image` | Legacy |

Includes a "style anchor" pattern that keeps a set of 4-8 event mockups visually consistent. Two helper scripts:
- `scripts/generate.py` single image CLI
- `scripts/batch_generate.py` set generation with shared anchor

Requires `GEMINI_API_KEY` environment variable. Free tier ~500 images/day.

### `veo-video-creator`

Thin wrapper over the user's connected Veo MCP server (`veo-mcp-server-production.up.railway.app`). Focused on 5-15 second single-shot atmosphere videos. Two canonical shapes: *slow push-in* (reveal) and *ambient hold* (atmosphere). Image-to-video is the preferred workflow: generate the still with `nano-banana` first, then animate.

### `rtl-hebrew-docs`

Standalone skill for generating professional right-to-left Hebrew documents (PDF, DOCX, PPTX) with correct bidi layout and Hebrew typography. The default and most reliable path is HTML with `dir="rtl"` rendered to PDF via headless Chrome, the only path that renders identically across every viewer. DOCX (`python-docx`, three-level RTL) is reserved for files the recipient must edit in Microsoft Word; PPTX uses `pptxgenjs` with `rtlMode`. Covers safe commercial/administrative templates (הצעת מחיר, חוזה, פרוטוקול, מכתב רשמי, תעודה, דוח) and explicitly excludes regulated tax invoices/receipts (חשבונית מס / קבלה). Three helper scripts:
- `scripts/html_to_pdf.py` HTML → PDF via headless Chrome, plus `proposal`/`certificate` JSON templates
- `scripts/make_docx.py` editable Word with section + paragraph + run RTL
- `scripts/make_pptx.js` Hebrew slides with deck-wide and per-block RTL

On Linux, install a Hebrew font once (`fonts-noto-hebrew`); macOS and Windows ship one.

## Installation

For each `.skill` file in the `dist/` folder:

1. Open Claude in browser or app
2. Settings → Skills → Upload Skill
3. Select the `.skill` file
4. Start a new chat; the skill will be available

Recommended install order: `nano-banana` first, then `veo-video-creator`, then `bold-proposal-builder` (the orchestrator depends on the other two existing).

## Usage examples

### Starting a proposal from a phone call summary

```
Hemi: "קיבלתי עכשיו שיחה מחברת הפניקס. הם מתכננים אירוע השקה לקונספט אמנות חדש,
180 מוזמנים, ביוני, בקמפוס בראשון לציון. התקציב בסביבות 400 אלף. רוצים
שזה ירגיש יותר גלריה ופחות אירוע תאגידי."

Claude: [invokes bold-proposal-builder → creates proposals/phoenix-art-2026/
         → runs stage 1 intake → stage 2 research → ... → delivers 4 files]
```

### Generating mockups for an existing proposal

```
Hemi: "ההצעה לפניקס מוכנה עד שלב 3. עכשיו תייצר את הדימוייים."

Claude: [invokes bold-proposal-builder stage 4a → calls nano-banana with 
         style anchor from brand-system.md → generates 6 mockups → 
         calls veo-video-creator for atmosphere video]
```

### Generating a standalone image

```
Hemi: "תכין לי תמונה של תצוגה בגלריה עם תאורה חמה מהרצפה וקיר נחושת מוברשת."

Claude: [invokes nano-banana → single generate]
```

## File structure

```
bold-proposal-skills/
├── README.md                                (this file)
├── dist/
│   ├── bold-proposal-builder.skill
│   ├── nano-banana.skill
│   └── veo-video-creator.skill
└── src/
    ├── bold-proposal-builder/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── stage-1-intake.md
    │   │   ├── stage-2-research.md
    │   │   ├── stage-3-brand-heart.md
    │   │   ├── stage-4a-visualization.md
    │   │   ├── stage-4b-content-experience.md
    │   │   ├── stage-4c-operations.md
    │   │   ├── stage-4d-culinary.md
    │   │   ├── stage-5-budget.md
    │   │   └── stage-6-assembly.md
    │   ├── assets/
    │   │   ├── proposal-pdf-structure.md
    │   │   ├── gamma-prompt-template.md
    │   │   └── bold-brand-guidelines.md
    │   └── scripts/
    │       └── build_budget_xlsx.py
    ├── nano-banana/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── prompting-guide.md
    │   │   └── api-reference.md
    │   └── scripts/
    │       ├── generate.py
    │       └── batch_generate.py
    ├── veo-video-creator/
    │   ├── SKILL.md
    │   └── references/
    │       └── video-prompting.md
    └── rtl-hebrew-docs/
        ├── SKILL.md
        ├── references/
        │   ├── rtl-rendering.md
        │   ├── hebrew-fonts.md
        │   └── document-templates.md
        ├── assets/
        │   └── fonts/
        │       └── README.md
        └── scripts/
            ├── html_to_pdf.py
            ├── make_docx.py
            └── make_pptx.js
```

## Dependencies

- **Skills (required before install):** `pptx`, `xlsx`, `pdf`, `canvas-design` (all public), and optionally `ffmpeg-editor` (for video post-processing)
- **MCP servers:** Veo MCP (already connected by user)
- **API keys:** `GEMINI_API_KEY` for `nano-banana`
- **Python packages (installed automatically when scripts run):** `openpyxl`, `google-genai`, `pillow`

## Development

To modify a skill:

1. Edit files under `src/<skill-name>/`
2. Re-package with Claude's skill-creator:
   ```bash
   python3 -m scripts.package_skill src/<skill-name> dist/
   ```
3. Re-upload the `.skill` file via Claude Settings

## Credits

Designed and built with Claude for Bold Productions. Orchestration pattern inspired by multi-agent event production workflows.
