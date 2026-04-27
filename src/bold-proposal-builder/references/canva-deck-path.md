# Stage 6, Canva Deck Path Reference (v1.0)

## Purpose

Stage 6 of bold-proposal-builder normally produces three client-facing surfaces: premium PDF (via premium-deck-strategist) + live Gamma URL + editable PPTX. This file documents a fourth, optional surface: a Canva-generated presentation.

Note: this integration currently lives inside bold-proposal-builder. When `premium-deck-strategist` is pushed to the repo, this content will move there as a generic Canva output mode for any deck request, and Stage 6 will become a thin wrapper that picks `output_mode: "pdf" | "canva" | "both"`.

## When to use Canva

Use Canva as a surface when:
- The client uses Canva natively for their marketing and wants editability there
- A Bold Canva brand kit is configured and applies more cleanly than Gamma's themes
- The proposal is for a returning client who liked a prior Canva deck
- Hemi specifically requests it ("בנה את ההצעה ב-Canva", "תפיק גם גרסת קנבה")

Use Gamma instead when:
- The client wants a shareable URL with comments
- Live editing during a meeting is the use case
- No Canva brand kit applies and Gamma's themes feel closer to the brand

The four surfaces are NOT mutually exclusive. Stage 6 can produce all four if Hemi wants. Default remains PDF + Gamma + PPTX.

## Pre-requisites

- Canva MCP connected (`mcp.canva.com/mcp`). Check with `/mcp` in Claude Code; should list "Canva".
- Optional: Bold Canva brand kit ID, fetched once via `Canva:list-brand-kits` and cached in `data/canva-config.json`.

## The flow (5 calls)

### Step 1: Resolve brand kit (optional, cached)

If `data/canva-config.json` exists, read `brand_kit_id` from there. Otherwise:

```
Canva:list-brand-kits()
```

Cache the result:

```json
// data/canva-config.json
{
  "brand_kit_id": "BAFsomething",
  "brand_kit_name": "Bold",
  "default_folder_id": "FOLDsomething",
  "fetched_on": "2026-04-27"
}
```

If no Bold brand kit exists, proceed without one. The deck styles itself from the prompt and the `style` parameter.

### Step 2: Outline review (mandatory gateway)

Canva requires an explicit outline review step before generation. This is one-shot, not back-and-forth.

```
Canva:request-outline-review(
  topic: <event name>,
  audience: <brief.md field 6, one phrase>,
  length: "balanced",  // ~16 cards
  style: <"minimalist" | "elegant" | "modular" | "geometric" | custom string>,
  brand_kit_id: <from canva-config.json or omit>,
  brand_kit_name: <ditto>,
  pages: [
    { title: "...", description: "- bullet 1\n- bullet 2\n- bullet 3" },
    ...
  ]
)
```

The 16 pages mirror the Gamma `inputText` outline:

1. Cover, tagline from brand-system.md §3
2. The moment, reason-why from brief field 1
3. Strategic reading, 3 insights from challenges.md
4. Concept, brand-system.md §1-2
5. Arrival mockup
6. Hero moment mockup
7. Main space mockup
8. Detail mockup
9. Culinary
10. Experience flow, 3 anchors from agenda.md
11. Operations
12. Investment
13. KPIs
14. Timeline
15. Next steps
16. Closing

**Critical Claude-specific rule**: strip ALL punctuation from titles and descriptions before passing them in. Periods, commas, colons, question marks, hyphens, quotes, all of it. Only alphanumeric and spaces remain. Example:

- Original title: "Strategic reading: three key insights"
- Cleaned title: "Strategic reading three key insights"

Apply the same rule to descriptions. Inside bullets, preserve the leading `- ` and `\n` line breaks but strip punctuation from the bullet text itself.

The widget renders in chat. Hemi:
- Approves (clicks "Generate Design") - flow proceeds to Step 3
- Requests changes - call `request-outline-review` again with updated pages, do NOT proceed to Step 3
- Rejects - fall back to Gamma path or premium-deck-strategist PDF

### Step 3: Generate the design (only after Hemi approved)

```
Canva:generate-design-structured(
  design_type: "presentation",
  topic: <same as Step 2>,
  audience: <same>,
  length: <same>,
  style: <same>,
  brand_kit_id: <same>,
  presentation_outlines: <approved outlines from widget, punctuation stripped>,
  asset_ids: <optional, up to 10 hero mockup asset IDs from upload-asset-from-url>
)
```

This returns design candidates, multiple stylistic interpretations of the same outline. Each has `candidate_id`, preview thumbnail, and URL.

Hemi reviews and picks one in chat. The flow stops and waits.

### Step 4: Create the design from chosen candidate

After Hemi picks:

```
Canva:create-design-from-candidate(
  job_id: <from Step 3 response>,
  candidate_id: <Hemi's pick>
)
```

Returns `design_id`. From here, every further operation uses `design_id`, not `candidate_id`.

### Step 5: Export to PDF and PPTX

```
Canva:export-design(design_id: <from Step 4>, format: "pdf")
Canva:export-design(design_id: <from Step 4>, format: "pptx")
```

Save to:
- `proposals/<slug>/06-assembly/proposal-canva.pdf`
- `proposals/<slug>/06-assembly/proposal-canva.pptx`

The Canva URL (`https://canva.com/design/<design_id>`) is the live, editable surface.

## Aspect ratio limitation

Canva's `generate-design-structured` produces presentations at Canva's default aspect ratio (16:9). Bold's canonical template is 4:3. Two options:

**Option A, recommended:** accept 16:9 for the Canva surface. Document in `summary.md` that the Canva version is 16:9 while the PDF and Gamma versions are 4:3. This is a Canva platform limitation, not a Bold compromise.

**Option B, experimental:** after Step 4, call:

```
Canva:resize-design(design_id: <from Step 4>, ...)
```

`resize-design` supports custom dimensions: width=14.22 inches, height=10.66 inches. Canva's auto-layout may or may not survive cleanly. Hemi QAs the result.

## Footer composition

Canva's MCP API does not expose programmatic footer control. The Bold footer (white logo bottom-left + "A Bold Presentation© [year]" center + client logo bottom-right) cannot be auto-injected.

Workaround:
1. Include the centered text as part of `additionalInstructions` to `generate-design-structured`
2. After export, manually paste the white Bold logo and client logo onto each body slide via Canva's UI. One-time, then save as a Bold base template for reuse.

For first-time generation, accept that the footer will be incomplete. Flag in `summary.md`.

## Returning clients

Canva does not have a direct "remix from prior deck" tool equivalent to `gamma_generate_from_template`. Three workarounds:

1. **Brand kit reuse**: same `brand_kit_id` keeps color/font/logo consistent across decks
2. **Manual duplication**: Hemi duplicates the prior design in Canva's UI before Stage 6, then this flow updates content
3. **search-designs**: at Stage 1, call `Canva:search-designs(query: <client name>)` to surface prior decks for Hemi's reference

## QA additions (on top of Stage 6 v2.6 checklist)

When Canva surface is enabled:

- [ ] Canva MCP connected
- [ ] `data/canva-config.json` present (or brand_kit_id intentionally omitted)
- [ ] `request-outline-review` widget rendered in chat
- [ ] Hemi explicitly approved the outline (not just acknowledged)
- [ ] `generate-design-structured` returned candidates
- [ ] Hemi explicitly picked one candidate
- [ ] `create-design-from-candidate` returned `design_id`
- [ ] Both exports (PDF + PPTX) downloaded and open
- [ ] Canva URL captured for `summary.md`
- [ ] Aspect ratio status flagged (16:9 default, or 4:3 if resize attempted)
- [ ] Footer status flagged (incomplete, partial, or complete after manual paste)

## summary.md update for Canva surface

When Canva surface is enabled, the "three complementary surfaces" block in `summary.md` becomes four:

```markdown
**הצעה בארבע גרסאות משלימות:**
- **הצעה מעוצבת מלאה (PDF)**, נבנתה ב-premium-deck-strategist, לוועדה ולהדפסה
- **מצגת אינטראקטיבית ב-Gamma:** [gammaUrl], לצפייה ותגובות
- **גרסת PowerPoint (PPTX):** מצורפת, לעריכה חופשית
- **גרסת Canva:** [canvaUrl], לעריכה ושיתוף בסביבת Canva של הלקוח
```

If only Canva is the secondary surface (no Gamma), drop the Gamma + PPTX bullets and present "PDF + Canva" as the two surfaces.

## Future migration

When `premium-deck-strategist` is pushed to the repo, this file moves to:

```
src/premium-deck-strategist/references/canva-output-mode.md
```

bold-proposal-builder Stage 6 then becomes a wrapper:

```
At Stage 6, premium-deck-strategist is invoked with:
  output_mode: "pdf" | "canva" | "both"
```

Until that migration, this file lives here and Stage 6 calls Canva MCP directly.
