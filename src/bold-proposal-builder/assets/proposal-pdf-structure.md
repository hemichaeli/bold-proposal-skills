# Proposal PDF Structure

The canonical spine for a Bold Productions client-facing proposal PDF. This file is read in stage 6 (Assembly) before writing the PDF. Page counts are targets, not quotas. Ship shorter when the content is lean; don't inflate.

---

## Page-by-page spec

### Page 1, Cover (always exactly 1 page)

**Layout:** full-bleed visual + restrained text.

**Elements:**
- Event name (display font, primary color, centered or lower-left depending on image composition)
- Tagline (1 line, smaller, text font, under the name)
- Client name + proposed date (small, lower third)
- Bold logo (small, bottom corner)

**No:** no "הצעת מחיר" label. No exclamation marks. No border framing.

**Source image:** highest-impact mockup from `04-specialists/visual/mockups/`, usually `02-hero.png` or `01-arrival.png`, OR a canvas-design output generated specifically for this cover.

### Page 2, The moment (1 page)

One short paragraph (3-5 sentences) setting the strategic context: why this event, why now, what it answers. Drawn from `01-intake/challenges.md` §1, rewritten for client tone (remove internal jargon, remove "tension" language).

**Visual element:** a thin horizontal line in accent color. Nothing else.

### Pages 3-4, Strategic reading (1-2 pages)

The one or two insights from `challenges.md` that justify the entire creative direction. Written as observation, not analysis. No bullet points. Prose.

Structure:
- Opening sentence: a single observation about the client's world.
- 2-3 sentences unpacking it.
- Closing sentence: what this means for the event.

If there is a second strategic insight, give it its own page. If only one, a single page is enough.

### Pages 5-6, The creative concept (2 pages)

**Page 5:** The concept sentence, large, with a 2-3 sentence unpacking beneath. The event name presented as a hero, display font, large type, breathing space around it.

**Page 6:** The tagline and the visual motif described in one paragraph. This is where the reader starts to *see* the event in their head, not just understand it.

### Page 7, Palette & typography (1 page)

Visual, not written.

**Top half:** horizontal strip showing the 4-6 palette colors. Each color a column. Below each: role name (ראשי / אקסנט / וכד').

**Bottom half:** typography sample. Display font showing the event name, H1, H2. Text font showing a full paragraph of body copy.

Keep legends minimal. No hex codes on the client PDF (keep those for internal use).

### Pages 8-12, Visualization (3-5 pages)

One page per key mockup. Full-bleed image, single-line caption at bottom in text font. 

Recommended order:
1. Arrival
2. Hero moment
3. Scale (wide shot)
4. Detail
5. Food / culinary (if applicable)

On page 12 (last visualization page), add a small footer: "סרטון האווירה זמין בקישור: [QR code + URL]". Do not embed the video in the PDF, it breaks across readers.

### Pages 13-14, The experience (2 pages)

**Page 13 (Flow):** The block view from `agenda.md` rendered as a horizontal 5-stage flow diagram. Each block a short label and a one-line description. No minute-by-minute. The reader should grasp the arc in 15 seconds.

**Page 14 (Signature moments):** 3 signature moments pulled from the agenda, each written as a short paragraph describing what guests experience. These are the moments the client will talk about internally, design them deliberately.

### Page 15, Culinary (1 page)

A paragraph narrating the culinary journey of the evening (drawn from `menu.md` intro). Then a structured but restrained menu list: 3-4 dishes named with 1-line descriptions. Service style noted in a small caption.

If the event is food-forward, expand to 2 pages.

### Page 16, Operations (1 page)

Short paragraphs on:
- The venue (1 paragraph)
- Technical dimensions (1 paragraph: sound, light, staging as a whole)
- How many people make the event happen (staffing headcount, 1 line)

The full operational document does not go to the client. They trust Bold to know this.

### Pages 17-18, Investment (2 pages)

**Page 17 (Summary table):** Top-level categories with totals. Not every line item. Typical rows:
- ניהול הפקה
- תפאורה ובינוי
- אור, סאונד, וידאו
- קייטרינג ובר
- תוכן, שילוט, מתנות
- צוות, אבטחה, נגישות
- גיבוי ורווח
- סה"כ לפני מע"מ
- מע"מ
- **סה"כ לתשלום**

Then, in a visually distinct block below: **שורות מותנות** as a separate table with the conditional items and their triggers.

**Page 18 (Payment terms):** Payment schedule (typical: 40% on signing, 40% two weeks before event, 20% post-event), bank details block, note pointing to the accompanying Excel for the full line-item breakdown.

### Page 19, Timeline (1 page)

A horizontal timeline from today to the event date. 4-6 milestones:
- היום: חתימה על ההצעה
- [שבועיים לפני]: אישור קונספט סופי
- [שלושה שבועות לפני]: סגירת ספקים
- [יום לפני]: חזרה גנרלית
- **יום האירוע**
- [24 שעות אחרי]: הודעת תודה לאורחים ודוח סיכום

### Page 20, About Bold (1 page, optional)

Include only if this is a new client. For existing relationships, skip.

Short: who Bold is, 3-4 past events with 1-line descriptions, what Bold does differently. No founding story. No team photo grid. The proposal itself is the portfolio.

### Page 21, Next steps + contact (1 page, always)

Clean layout, no visuals.

**Right half:** Decision points with dates:
- החלטה עקרונית: עד [תאריך]
- פגישת kickoff: [תאריך]
- אישור קונספט: [תאריך]

**Left half:** Contact:
Bold Productions
Hemi Michaeli
hemi.michaeli@gmail.com
[phone if appropriate]

**Footer:** "ההצעה תקפה עד [תאריך]" in small text.

No "thank you". No "we look forward to partnering with you". No handshake imagery.

---

## Typography rules across all pages

- Display font: headings only (event name, section titles).
- Text font: everything else.
- H1 size: roughly 48-72pt depending on font weight.
- Body: 10-11pt, line height 1.5-1.6.
- Margins: generous. At least 2.5cm on all sides for A4. Asymmetric margins (more on one side) can feel more editorial if the brand system supports it.

## Color rules

- Backgrounds: neutral light (from palette) or pure white. Never full-bleed colored backgrounds across all pages.
- Accents: primary color for headings, accent color for small emphatic elements (pull quotes, section numbers, links).
- Images: let them carry the color. Captions and typography stay restrained.

## Grid

Use a 6-column grid as a baseline. Allows most layouts (full-width, 2/3 + 1/3, split 50/50, thirds). Don't use 12-column; that's web thinking and it shows.

---

## RTL handling

Everything Hebrew is right-to-left. The grid flows right-to-left. Page numbers (if used) sit at the bottom left (which is the "end" of the page in RTL). Images can flow either direction; just be consistent.

---

## File format targets

- PDF/A where possible (long-term readability).
- Embedded fonts (always; never expect the client to have your font).
- PDF file size: under 20 MB ideally. If the mockups push it over, downsample to 200-300 DPI (still print-quality, not web-quality).
- Hyperlinks live where applicable: video URL, bank details, email addresses.

---

## When to deviate

Events of specific type may justify structural adjustments:

- **Pitch event for a small audience (under 40):** compress to 10-12 pages. Drop page 20, merge 13-14, reduce visualization to 3 images.
- **Multi-day conference:** add a per-day section (could add 3-5 pages).
- **Product launch with reveal:** lean heavily on visualization (5-7 pages of imagery), compress operations.
- **Private/intimate event (e.g., 50th birthday):** softer tone throughout, more storytelling, less operational detail.

The spine above is for a typical mid-scale corporate or brand event (100-400 guests, ₪200K-₪800K budget). Adjust proportionally for smaller or larger.
