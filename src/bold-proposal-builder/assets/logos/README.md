# Bold Logo Assets

The three official Bold Productions logo assets used in client-facing proposals.

## Files in this folder (text-only in repo, binaries added at package time)

| File | Format | Original filename | Used where | Source of truth |
|---|---|---|---|---|
| `bold-black-opening.jpg` | JPG, black version | `Black Logo-01.jpg` | Opening slide hero, full-bleed, centered on black background | packaged with .skill |
| `bold-white-footer.jpg` | JPG, white version | `White JPG-01.jpg` | Body-slide bottom-left corner, small (~120-150px wide) | packaged with .skill |
| `bold-closing.mp4` | MP4 video, ~30MB | `Black.mp4` | Closing slide hero, full-bleed, autoplay | Bold's Google Drive (canonical); this packaged copy is fallback only |

**Note on the repo vs the .skill package:** None of the binaries are stored in this Git repo (the GitHub API used to commit files here is text-based). They live in Hemi's local skill-staging directory at `/home/claude/bold-proposal-builder/assets/logos/` and are included when the skill is packaged via `skill-creator/scripts/package_skill.py`. When the .skill file is uploaded to Claude, the assets travel with it.

If you're cloning this repo for editing and need the assets, copy them manually from:
- `Black Logo-01.jpg` in Bold's shared Drive → `assets/logos/bold-black-opening.jpg`
- `White JPG-01.jpg` in Bold's shared Drive → `assets/logos/bold-white-footer.jpg`
- `Black.mp4` in Bold's shared Drive (path like `K:\My Drive\macshare\Booper`) → `assets/logos/bold-closing.mp4`

## Runtime behaviour for `bold-closing.mp4`

The MP4 follows a packaged-fallback + Drive-canonical model. At Stage 6, the assembly logic:

1. Attempts to fetch `bold-closing.mp4` from Bold's Google Drive via the Drive MCP.
2. If the fetch succeeds, uses that copy and stages it at `proposals/<slug>/06-assembly/assets/bold-closing.mp4` for the duration of assembly.
3. If the fetch fails (Drive MCP unavailable, file moved, no network), falls back to the packaged copy in `assets/logos/bold-closing.mp4`.
4. After delivery, removes the per-proposal staged copy. The packaged copy and the Drive original are never touched.

This way the Drive copy stays canonical (Hemi can update the closing animation in one place and every future proposal picks it up) while offline runs still produce a complete closing slide.

## Per-slide-type layout rules (canonical, in use since 2010)

| Slide type | Hero / main visual | Bottom-left | Bottom-right | Centered footer text |
|---|---|---|---|---|
| Opening | `bold-black-opening.jpg` (full bleed, centered) | none | none | none |
| Body slides | content | `bold-white-footer.jpg` (~120-150px wide) | client logo (small) | `A Bold Presentation© [year]` |
| Closing | `bold-closing.mp4` (full bleed, autoplay) | none | none | none |

The `[year]` token is replaced with the event year (4 digits, Western numerals) at deck-assembly time.

Footer text rendering: Verdana 14pt, gray `#808080`, horizontally centered.

The body-slide footer stripe looks like this:

```
 [White Bold logo, bottom-left]                              [Client logo, bottom-right]
                                A Bold Presentation© 2026
```

Client logo is requested in the brief at Stage 1 and dropped into `data/client-assets/<slug>/`.

## Do not use

- Do not use any color variant or "Bold" logo found online. Only these three files.
- Do not scale the black opening logo beyond 60% of slide width.
- Do not place the white footer logo on anything darker than `#F5F5F5` (near-white).
- Do not put a Bold credit anywhere except the body-slide footer (specifically: no watermarks, no "brought to you by Bold", no on-slide Bold logos in the body content area).
- Do not put any footer or bottom-left logo on the opening or closing slides. Their hero asset is the entire slide.

## Reference metadata

Both JPGs stored as originals without resize or re-encode. If they need optimization for final PDF export, resize to max 2000px wide, JPEG quality 90. Do not use PNG, the originals are JPG by design.

The MP4 is stored as the original master from Bold's Drive. Do not re-encode unless the file is too large for a specific surface (Canva: 100MB cap per video, Gamma: 50MB cap).
