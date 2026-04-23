# Bold Presentation Template Spec

**Source of truth:** `BOLDpresentation - TEMPLATE.ppt` (original 2007, maintained through 2014+) plus Hemi's 2026 updates to the footer convention and closing video.

**Purpose:** The visual blueprint for every Bold proposal deck. When Stage 6 of `bold-proposal-builder` invokes `premium-deck-strategist` or `gamma_generate`, it must match this spec. This is not a suggestion; it is the look the client pays for.

## Dimensions & aspect ratio

- Slide size: 14.22 x 10.66 inches (1.33:1, classic 4:3)
- Bold's decks have always been 4:3 for print-friendly PDF output. Do NOT switch to 16:9 unless Hemi explicitly overrides.
- Gamma MCP invocation uses `cardDimensions: "4x3"` (not `"16x9"`, which was a prior mistake in Stage 6 v2.3).

## Type system

| Role | Font | Size | Weight | Color |
|---|---|---|---|---|
| Slide title (Hebrew) | Tahoma | 35pt | Bold | `#000000` |
| Slide title (English) | Verdana | 35pt | Bold | `#000000` |
| Body text | Tahoma (Hebrew) / Verdana (English) | 18-22pt | Regular | `#000000` or `#333333` |
| Footer text | Verdana | 14pt | Regular | `#808080` (gray) |
| Accent / numbers | Tahoma | size-of-context | Bold | `#000000` |

Tahoma for Hebrew is non-negotiable. It is the font Bold has rendered its decks in for two decades; switching breaks visual continuity with the client's mental library of prior Bold events.

## Footer convention (every slide except cover and closing)

Every slide carries a three-element footer at the bottom, centered vertically in a ~0.8-inch tall stripe:

```
[white-logo bottom-left]     A Bold Presentation© [YYYY]     [client-logo bottom-right]
```

**Positions (for a 14.22 x 10.66 inch slide):**
- White Bold logo: bottom-left corner, roughly 120-150px wide (~1.2 inches), positioned at `(0.3, 9.8)` inches on a white background swatch
- Center text: `A Bold Presentation© [YYYY]`, Verdana 14pt, gray `#808080`, centered horizontally around x=7.1 inches, at y=9.9 inches
- Client logo: bottom-right corner, same size as white Bold logo, positioned at `(12.7, 9.8)` inches
- The year `[YYYY]` is populated at Stage 6 time (the current year, not the event year)

**Files:**
- `assets/logos/bold-white-footer.jpg` (original: White_JPG-01.jpg)
- Client logo: requested in brief field (Stage 1), stored as `proposals/<slug>/01-intake/client-logo.ext`

**Missing client logo fallback:** If the client hasn't provided a logo by Stage 6, the bottom-right slot shows nothing (not a placeholder) and the footer stripe keeps its width. Stage 6 flags to Hemi that the logo is missing and continues.

## Cover slide (slide 1)

Unique layout, no footer:
- Full-bleed background: either a hero mockup from Stage 4a, OR solid black if no hero is ready
- Centered: `assets/logos/bold-black-opening.jpg` (original: Black Logo-01.jpg), roughly 40-60% of slide width
- NO Bold footer on the cover
- NO client logo on the cover
- Title of the event appears BELOW the Bold logo, Tahoma bold 40pt, color inverted against background

## Closing slide (slide N, last)

Unique layout, no footer:
- Full-bleed auto-play video: `bold-closing.mp4` (original: Black.mp4, 30MB, lives in Bold Drive, NOT in the skill package)
- NO text overlay
- NO footer
- At Stage 6, Claude must fetch `bold-closing.mp4` from Bold's Drive and embed it into the final PDF/PPTX/Gamma. For PDF export, the video will be replaced by its first frame with a small "▶" overlay; the client opens the Gamma URL for the actual video.

## Body slide layouts

The Bold template has used a single "Default" layout for years. Variety comes from content arrangement, not from layout switching. The typical arrangements used on the 28 reference slides in `BOLDpresentation - TEMPLATE.ppt`:

### Layout 1: Full-bleed image + corner text
- Background image spans entire slide
- Title sits in a corner (typically top-right for Hebrew RTL), small area, high contrast
- Used for: cover, section breaks, hero moments
- Example slides in template: 1 (cover), 18 (עיצוב ואווירה)

### Layout 2: Image right, text left (or vice versa for RTL)
- Image panel takes ~60% of slide
- Title + short body on the other 40%
- Used for: concept reveal, mockup presentations
- Example slides: 9 (הקונספט), 16 (חויית הכניסה)

### Layout 3: Full-text centered
- Title top, body centered below
- No image
- Used for: values, strategic insights, agenda summary
- Example slides: 2 (קהל היעד), 5 (ערכים שיועברו באירוע)

### Layout 4: Grid of images
- 2x2 or 3x3 grid of reference images or mockups
- Minimal or no text
- Used for: mood boards, atmosphere collections
- Example slides: 3-4 (אופי האירוע)

### Layout 5: Timeline / schedule
- Horizontal or vertical flow of time-marked entries
- Used for: run sheet, agenda breakdown
- Example slide: 15 (לו"ז האירוע)

## The canonical 28-slide reference sequence (from the original template)

This is what Bold has pitched with for ~20 years. Stage 6's `premium-deck-strategist` brief and the Gamma `inputText` should follow this order, though the spec trims to 16 cards for modern attention spans (see Stage 6 reference for the 16-card version).

| # | Slide title | Purpose |
|---|---|---|
| 1 | [Event name + cover visual] | Cover |
| 2 | קהל היעד | Target audience |
| 3 | אופי האירוע | Event character / mood |
| 4 | אופי האירוע (המשך) | Event character continued |
| 5 | ערכים שיועברו באירוע | Values the event conveys |
| 6 | פרטים כלליים | Core facts (date, venue, count) |
| 7 | אופציה א' | Option A (concept direction 1) |
| 8 | בדרך אל הקונספט | Approach to the concept |
| 9 | הקונספט | The concept |
| 10 | Save the date | Save-the-date design |
| 11 | הזמנות | Invitations |
| 12 | Follow up | Follow-up communications |
| 13 | מתחילים | Opening moment |
| 14 | בדרך לאירוע | En route, shuttle experience |
| 15 | לו"ז האירוע | Run sheet |
| 16 | חויית הכניסה | Arrival experience |
| 17 | קבלת הפנים | Reception |
| 18 | עיצוב ואווירה | Design & atmosphere |
| 19 | צלילים של התחלה חדשה | Opening ceremony |
| 20 | ארוחת ערב | Dinner |
| 21 | פעילות במה | Stage activity |
| 22 | הישיבה | Seating |
| 23 | תפיסת הבמה | Stage design |
| 24 | פעילות בימתית | Performance |
| 25 | מנחה | Host / MC |
| 26 | אייטם | Feature item |
| 27 | אייטם סיום | Closing item |
| 28 | חלוקת מתנות | Gift distribution |

The modern 16-card Stage 6 version compresses this to: cover, strategic reading, concept, 5 visualization, culinary, experience (3 anchors), operations, culinary, investment, KPIs, timeline, next steps.

## Design references from Bold's archive

Hemi maintains a visual archive on his Drive at `K:\My Drive\macshare\` with three key folders that exemplify current Bold design language:

| Folder | Type of event | Design takeaway |
|---|---|---|
| `events/` | Mixed corporate / launches | Broadest library; pull for general mood |
| `נהר היומיים/` | Multi-day river event | Outdoor, natural, large-scale production |
| `Booper/` | Creative / experiential | Bold, playful, medium-scale, unusual venues |

These Drive folders are not accessible to Claude in skill runtime. At Stage 4a, Hemi uploads hero references from these folders when needed; the skill does not autonomously browse his Drive.

## Voice & content rules (re-stated from SKILL.md for emphasis)

- Hebrew-first, always
- No em-dash, no en-dash
- Max 5-7 words per on-slide bullet; depth goes in speaker notes
- Specific numbers, not adjectives
- No banned clichés: "בלתי נשכח", "מרגש", "חוגגים יחד", "unforgettable", "once in a lifetime"
- No Bold credit text or Bold logo anywhere except the footer; no "proudly produced by Bold", no decorative Bold stamps on slides

## Palette

Bold has never prescribed a fixed palette. The palette comes from the brand system built at Stage 3. What stays constant:

- Title text black `#000000` (or white on dark backgrounds; never a third color)
- Footer gray `#808080`
- Body dark gray `#333333` or pure black `#000000`
- Any other color is brand-system driven, one per slide maximum

## QA checklist before Stage 6 closes

- [ ] Cover slide uses `bold-black-opening.jpg` or a hero mockup (no footer on cover)
- [ ] All body slides have the three-element footer
- [ ] Closing slide is `bold-closing.mp4` (or its first frame in PDF), no footer
- [ ] Title font is Tahoma (Hebrew) or Verdana (English)
- [ ] Client logo present bottom-right (or blank if not provided, logged to Hemi)
- [ ] Year in footer matches current year, not event year
- [ ] Aspect ratio 4:3
- [ ] No em-dash, no en-dash anywhere
- [ ] No banned clichés
- [ ] No Bold credits outside the footer stripe
