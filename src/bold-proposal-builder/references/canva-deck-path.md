# Canva Deck Path Reference (v2.0, default surface)

## Purpose

Stage 6 of bold-proposal-builder produces two default deck surfaces: Canva and Gamma. This file documents the Canva flow. The Gamma flow stays in `stage-6-assembly.md` section 3.

As of v2.7, Canva is no longer optional. It is the visual flagship deck, replacing the prior premium-deck-strategist PDF as the polished deliverable.

When `premium-deck-strategist` is pushed to the repo (currently lives only on Claude.ai), this content moves there as a generic Canva output mode for any deck request, and Stage 6 becomes a thin wrapper.

## Pre-requisites

- Canva MCP connected (`mcp.canva.com/mcp`). Check with `/mcp` in Claude Code.
- (Optional) Bold Canva brand kit ID, fetched once via `Canva:list-brand-kits` and cached in `data/canva-config.json`.

## The flow (5 calls)

### Step 1: Resolve brand kit (cached after first run)

If `data/canva-config.json` exists, read `brand_kit_id` from there. Otherwise:

```
Canva:list-brand-kits()
```

Cache the result:

```json
{
  "brand_kit_id": "BAFsomething",
  "brand_kit_name": "Bold",
  "default_folder_id": "FOLDsomething",
  "fetched_on": "2026-04-27"
}
```

If no Bold brand kit exists, proceed without one. The deck styles itself from the prompt and `style` parameter.

### Step 2: Outline review (mandatory gateway)

Canva requires an explicit outline review step before generation. One-shot, not back-and-forth.

```
Canva:request-outline-review(
  topic: <event name>,
  audience: <brief.md field 6, one phrase>,
  length: "balanced",          // ~16 cards
  style: <"minimalist" | "elegant" | "modular" | "geometric" | custom>,
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
- Approves (clicks "Generate Design") → flow proceeds to Step 3
- Requests changes → call `request-outline-review` again with updated pages, do NOT proceed to Step 3
- Rejects → fall back to Gamma-only delivery (note in summary.md)

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

Returns design candidates, multiple stylistic interpretations of the same outline. Each has `candidate_id`, preview thumbnail, URL.

Hemi reviews and picks one in chat. The flow stops and waits.

### Step 4: Create the design from chosen candidate

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

Canva URL: `https://canva.com/design/<design_id>`. Live, editable.

## Aspect ratio

16:9, Canva default. v2.7 dropped the prior 4:3 enforcement; no resize step needed.

## Footer composition

Canva MCP does not expose programmatic logo placement. Three options for the Bold footer:

1. **Brand kit handles it (preferred)**: Configure the Bold Canva brand kit once with the white logo as a default footer element. From then on every Canva deck inherits it.
2. **Manual paste post-export**: After Step 4, open the design in Canva UI and paste the white logo bottom-left + client logo bottom-right onto each body slide. One-time per deck.
3. **Skip logos, rely on text only**: Pass the centered text "A Bold Presentation© [year]" via `additionalInstructions`. Acceptable for first iterations.

For first-time generation without a configured brand kit, Option 3 is fine. Flag in summary.md that the deck has only the centered footer text and that Hemi may want to add logos manually.

## Returning clients

Canva does not have a direct "remix from prior deck" tool equivalent to `gamma_generate_from_template`. Three workarounds:

1. **Brand kit reuse**: same `brand_kit_id` keeps color/font/logo consistent across decks.
2. **Manual duplication**: Hemi duplicates the prior design in Canva's UI before Stage 6, then this flow updates content.
3. **search-designs**: at Stage 1, call `Canva:search-designs(query: <client name>)` to surface prior decks for Hemi's reference.

## summary.md surface block

Stage 6 includes both Canva and Gamma surfaces in the summary. See `stage-6-assembly.md` section 5 for the canonical template. Short version:

```markdown
- **מצגת ב-Canva:** [canvaUrl], לעריכה ושיתוף בסביבת Canva
- **מצגת ב-Gamma:** [gammaUrl], לצפייה אינטראקטיבית ותגובות
- **PowerPoint להורדה:** מצורף proposal-canva.pptx + proposal-gamma.pptx
- **PDF להדפסה:** מצורף proposal-canva.pdf
```

## QA checklist (Canva-specific, complement to Stage 6 v2.7 checklist)

- [ ] Canva MCP connected and `request-outline-review` widget rendered
- [ ] Hemi explicitly approved the outline
- [ ] Punctuation stripped from outline before passing to generate-design-structured
- [ ] `generate-design-structured` returned candidates
- [ ] Hemi explicitly picked one candidate
- [ ] `create-design-from-candidate` returned `design_id`
- [ ] Both exports (PDF + PPTX) downloaded and open
- [ ] Canva URL captured for `summary.md`
- [ ] Footer status flagged: brand-kit-managed | manual-paste-pending | text-only

## Future migration

When `premium-deck-strategist` is pushed to the repo, this file moves to:

```
src/premium-deck-strategist/references/canva-output-mode.md
```

bold-proposal-builder Stage 6 then becomes a wrapper that calls premium-deck-strategist for both Canva and Gamma output modes. Until that migration, this file lives here and Stage 6 calls Canva MCP directly.
