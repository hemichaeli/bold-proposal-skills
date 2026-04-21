#!/usr/bin/env python3
"""
extract-proposal-patterns.py

Reads high-quality past proposals from K:/My Drive/macshare/events (Bold's
reference collection of best presentations) and extracts patterns that will
guide Stage 6 assembly of new proposals.

Extracted patterns include:
- Typical page structure and order for a Bold proposal deck
- Cover treatment conventions (typography, image placement, client logo usage)
- How strategic reading is written (voice, tone, paragraph structure)
- Budget summary layouts
- Closing page / next-steps conventions
- Specific phrases and turns-of-language to reuse
- Anti-patterns observed in weaker proposals (documented to avoid)

Output: data/proposal-patterns.md (human-readable, not JSON — Claude reads this
like a style guide at Stage 6).

Pseudocode flow (to be driven by Claude interactively):

1. Via Google Drive MCP, list all files in K:/My Drive/macshare/events
2. For each PPT/PPTX/PDF, extract:
     - structure (page count, section headers, order)
     - images per page (count, types: photo / diagram / illustration)
     - typography observations (if extractable from file)
     - copy samples (short quotable lines that feel "Bold")
3. Aggregate into proposal-patterns.md with sections:
     ## Cover conventions
     ## Opening pages
     ## Concept presentation
     ## Visualization
     ## Budget summary presentation
     ## Closing
     ## Voice samples (10-20 Hebrew sentences that feel exemplary Bold)
     ## Anti-patterns observed (things NOT to do)

Claude reads this file at Stage 6 before assembling the PDF, gamma prompt,
and summary. It acts as a style reference, not a prescriptive template.

Running:

    python3 extract-proposal-patterns.py --dry-run
    python3 extract-proposal-patterns.py --run
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Extract proposal patterns from macshare/events")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--output", default="data/proposal-patterns.md")
    args = parser.parse_args()

    if not any([args.dry_run, args.run]):
        print("ERROR: pass --dry-run or --run", file=sys.stderr)
        sys.exit(2)

    print("=" * 60)
    print("Proposal Patterns Extraction")
    print("=" * 60)
    print()
    print("This script is a blueprint. Actual extraction must be driven by")
    print("Claude in an interactive session because it requires Drive MCP")
    print("and per-file judgment on what constitutes a 'pattern'.")
    print()
    print("When Hemi asks 'refresh the proposal patterns', Claude should:")
    print("  1. List files in K:/My Drive/macshare/events via Drive MCP")
    print("  2. Read 10-20 strongest past proposals (Hemi picks which)")
    print("  3. Extract: structure, voice, cover treatment, budget layout")
    print(f"  4. Write human-readable style guide to {args.output}")
    print()

    if args.dry_run:
        print("Dry-run complete.")
        return

    if args.run:
        print("ERROR: extraction must be driven by Claude with Drive MCP.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
