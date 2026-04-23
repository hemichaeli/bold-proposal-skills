# Bold Logo Assets

The three official Bold Productions logo assets used in client-facing proposals.

## Files in this folder (text-only in repo, binaries added at package time)

| File | Format | Original filename | Used where |
|---|---|---|---|
| `bold-black-opening.jpg` | JPG, black version | `Black Logo-01.jpg` | Opening slide of every proposal deck, centered, full-size |
| `bold-white-footer.jpg` | JPG, white version | `White JPG-01.jpg` | Footer of every slide, bottom-left corner, small (roughly 120-150px wide) |

**Note on the repo vs the .skill package:** The binary JPGs are NOT stored in this Git repo (the GitHub API used to commit files here is text-based). They live in Hemi's local skill-staging directory at `/home/claude/bold-proposal-builder/assets/logos/` and are included when the skill is packaged via `skill-creator/scripts/package_skill.py`. When the .skill file is uploaded to Claude, the logos travel with it.

If you're cloning this repo for editing and need the logos, copy them manually from:
- `Black Logo-01.jpg` in Bold's shared Drive → `assets/logos/bold-black-opening.jpg`
- `White JPG-01.jpg` in Bold's shared Drive → `assets/logos/bold-white-footer.jpg`

## Files NOT in this folder (too large to embed in skill package)

| File | Format | Original filename | Used where | Where it lives |
|---|---|---|---|---|
| `bold-closing.mp4` | MP4 video, ~30MB | `Black.mp4` | Closing slide of every proposal deck, full-bleed, auto-play | Hemi's Google Drive / Bold shared drive; request path at Stage 6 start |

When Stage 6 needs the closing video, `bold-closing.mp4` must be fetched from Hemi's Drive (path like `K:\My Drive\macshare\Booper` or the Bold shared Drive). Keep the reference in `proposals/<slug>/06-assembly/assets/bold-closing.mp4` during assembly, remove after delivery.

## Layout rules (summary, full spec in `assets/bold-presentation-template-spec.md`)

Every slide in a Bold proposal deck has this footer stripe:

```
 [White logo, bottom-left]           [Client logo, bottom-right]
                     A Bold Presentation© 2026
```

- Footer text: `A Bold Presentation© [current year]`, centered horizontally, Verdana 14pt, gray 808080
- Bottom-left: `bold-white-footer.jpg` on white background, roughly 120-150px wide
- Bottom-right: client logo (requested in brief at Stage 1, received as file)
- First slide (cover): `bold-black-opening.jpg` centered on black background, NO footer on cover
- Last slide (closing): `bold-closing.mp4` full-bleed auto-play, NO footer on closing

## Do not use

- Do not use any color variant or "Bold" logo found online. Only these three files.
- Do not scale the black opening logo beyond 60% of slide width.
- Do not place the white footer logo on anything darker than #F5F5F5 (near-white).
- Do not put a Bold credit anywhere except the footer (specifically: no watermarks, no "brought to you by Bold", no on-slide Bold logos in the body).

## Reference metadata

Both JPGs stored as originals without resize or re-encode. If they need optimization for final PDF export, resize to max 2000px wide, JPEG quality 90. Do not use PNG, the originals are JPG by design.
