# Gamma Prompt Template

This is the skeleton of the prompt you paste into Gamma.app to produce the interactive presentation. Replace everything in `{{braces}}` with values drawn from the proposal artifacts.

**How to use:**
1. After stage 6 writes the final PDF and XLSX, copy this template.
2. Fill in the braces using stage 1-5 outputs. For mockups, reference the file path; Hemi will attach them manually in Gamma.
3. Save the completed prompt to `06-assembly/gamma-prompt.md`.
4. Deliver to Hemi with a one-line instruction: "פתח Gamma → Generate → הדבק את התוכן של gamma-prompt.md → בחר סגנון [השם מה-brand-system]."

---

## Template

```
Create a cinematic event-proposal presentation for the following event. The presentation should be polished, editorial, premium, not corporate or cluttered. ~15 slides. Use full-bleed visuals where possible. Minimal text per slide.

EVENT: {{event_name}}
CLIENT: {{client_name}}
DATE: {{event_date}}
GUEST COUNT: {{guest_count}}

## Visual direction
- Palette: {{palette_hex_list}}
- Primary color: {{primary_hex}} (backgrounds, accents)
- Accent color: {{accent_hex}} (CTAs, hero typography)
- Neutral: {{neutral_hex}}
- Typography feel: {{display_font_desc}} for titles, {{text_font_desc}} for body
- Mood keywords: {{mood_words_from_inspiration}}
- Avoid: {{forbidden_list_from_brand_system}}
- No stock photos of people smiling at camera. No corporate-handshake imagery. No generic event decor.

## Slide-by-slide

### Slide 1, Cover
Title: {{event_name}}
Subtitle: {{tagline}}
Visual: full-bleed hero image (I will attach: mockups/01-arrival.png)
No other text on this slide. The cover should breathe.

### Slide 2, The moment
A short paragraph (2-3 sentences) explaining the cultural or business moment this event arrives in. Pull from this source:
{{insight_from_challenges_md}}

### Slide 3, The concept
Large text: "{{concept_sentence}}"
A supporting paragraph (2-3 sentences) explaining what this means in practice.

### Slide 4, The name
Display: {{event_name}}
Under: {{tagline}}
One line of reasoning for the name underneath.

### Slide 5, The visual world
Short paragraph describing the visual motif: {{motif_description}}
Two-column layout:
  Left: palette strip (show the 4-6 hex colors as a horizontal bar with their roles)
  Right: typography sample (H1 in display font showing "{{event_name}}", body text sample in text font)

### Slide 6, Arrival
Full-bleed image (I will attach: mockups/01-arrival.png)
One line caption at the bottom: {{arrival_caption}}

### Slide 7, The hero moment
Full-bleed image (I will attach: mockups/02-hero.png)
One line caption: {{hero_caption}}

### Slide 8, Atmosphere
Embed video (I will attach: atmosphere-video.mp4) as full-bleed background if Gamma supports; otherwise, use a representative still frame.

### Slide 9, The experience (flow)
Five-block horizontal flow, left to right:
{{block_1_name}} → {{block_2_name}} → {{block_3_name}} → {{block_4_name}} → {{block_5_name}}
Each block with a 3-5 word label.

### Slide 10, Culinary
Short paragraph: {{culinary_narrative}}
If available, I will attach a mockup image of food presentation.

### Slide 11, Signature moments
Three short callouts, each with an icon or small visual:
1. {{moment_1}}
2. {{moment_2}}
3. {{moment_3}}

### Slide 12, Site and scale
Short paragraph on the venue and guest flow.
Include a simple diagram if Gamma can generate one, otherwise text-only.

### Slide 13, Investment
Title: "השקעה"
Body:
- סה"כ לפני מע"מ: ₪{{total_pre_vat}}
- סה"כ כולל מע"מ: ₪{{total_with_vat}}
- שורות מותנות (בהסכמה): ₪{{conditional_total}}
- תוקף: עד {{valid_until}}
Note under: "תקציב מפורט בקובץ ה-Excel המצורף"

### Slide 14, Timeline
Horizontal timeline from today to event day:
{{milestone_1_date}}: {{milestone_1_label}}
{{milestone_2_date}}: {{milestone_2_label}}
{{milestone_3_date}}: {{milestone_3_label}}
{{milestone_4_date}}: {{milestone_4_label}}
{{event_date}}: האירוע

### Slide 15, Next steps
Clean layout:
- החלטה עקרונית: עד {{decision_deadline}}
- אישור קונספט: {{concept_approval_date}}
- סגירת ספקים: {{vendor_lock_date}}
- חזרה גנרלית: {{rehearsal_date}}

Contact:
Bold Productions
Hemi Michaeli
hemi.michaeli@gmail.com

End with a quiet page. No "thank you". No exclamation marks.
```

---

## Field mapping, where each `{{placeholder}}` comes from

| Placeholder | Source |
|---|---|
| `{{event_name}}` | `03-brand-heart/brand-system.md` §2 |
| `{{client_name}}` | `01-intake/brief.md` §1 |
| `{{event_date}}` | `01-intake/brief.md` §2 |
| `{{guest_count}}` | `01-intake/brief.md` §2 |
| `{{palette_hex_list}}` | `03-brand-heart/brand-system.md` §5 |
| `{{primary_hex}}` | `03-brand-heart/brand-system.md` §5 row 1 |
| `{{accent_hex}}` | `03-brand-heart/brand-system.md` §5 accent row |
| `{{neutral_hex}}` | `03-brand-heart/brand-system.md` §5 neutral row |
| `{{display_font_desc}}` | `03-brand-heart/brand-system.md` §6 |
| `{{text_font_desc}}` | `03-brand-heart/brand-system.md` §6 |
| `{{mood_words_from_inspiration}}` | `02-research/inspiration.md` "Mood words" |
| `{{forbidden_list_from_brand_system}}` | `03-brand-heart/brand-system.md` §9 |
| `{{tagline}}` | `03-brand-heart/brand-system.md` §3 |
| `{{insight_from_challenges_md}}` | `01-intake/challenges.md` §1 (rewritten for client tone) |
| `{{concept_sentence}}` | `03-brand-heart/brand-system.md` §1 |
| `{{motif_description}}` | `03-brand-heart/brand-system.md` §7 |
| `{{arrival_caption}}` | synthesize from `04-specialists/visual/mood-direction.md` |
| `{{hero_caption}}` | synthesize from `04-specialists/visual/mood-direction.md` |
| `{{block_1_name}}` etc. | `04-specialists/content/agenda.md` View A |
| `{{culinary_narrative}}` | `04-specialists/culinary/menu.md` intro paragraph, abbreviated |
| `{{moment_1,2,3}}` | `04-specialists/content/agenda.md` peak moments |
| `{{total_pre_vat}}` etc. | `05-budget/budget.json` summary |
| `{{conditional_total}}` | sum of conditional items from `05-budget/budget.json` |
| `{{valid_until}}` | `05-budget/budget.json` meta.valid_until |
| `{{milestone_1_date}}` etc. | derive from event date working backwards |
| `{{decision_deadline}}` | usually 7-14 days from proposal send |
| `{{concept_approval_date}}` | ~2 weeks before event |
| `{{vendor_lock_date}}` | ~3 weeks before event |
| `{{rehearsal_date}}` | day before event |

---

## Presentation style hints for Gamma

When Gamma asks for a style preference after receiving the prompt, the mapping from brand heart adjectives to Gamma styles is approximately:

- Minimal, restrained, quiet → Gamma "Minimalist" or "Editorial"
- Warm, intimate, human → "Warm" or "Casual"
- Bold, loud, premium → "Bold" or "Brand"
- Avant-garde, art, gallery → "Editorial" with inverted colors

Use Gamma's custom style option when possible and paste the palette hex values directly.
