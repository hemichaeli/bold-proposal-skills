#!/usr/bin/env python3
"""
extract-vendor-data.py

Reads Bold's historical proposal archive from Google Drive (Efrat + Keren folders),
extracts vendor names, pricing, quote dates, and builds a structured vendor registry
for Stage 5 of the bold-proposal-builder skill to consult.

Usage (invoked from Claude chat):
    Step 1: Claude calls Google Drive MCP to list files in the two folders.
    Step 2: Claude reads each PDF/DOCX, calls an LLM extraction on it, and appends to the registry.
    Step 3: Merges duplicates, applies CPI table, writes data/vendor-registry.json.

This script is really a *blueprint* for Claude to follow when Hemi asks
"update the vendor registry". The actual extraction runs interactively
because it requires calls to Google Drive MCP and judgment on ambiguous
vendor/item naming.

Pseudocode flow:

1. Ensure data/cpi-israel.json exists. If not, fetch from CBS (Israeli Central
   Bureau of Statistics) API or web. Alternatively, prompt Hemi for a manual table.

2. Via Google Drive MCP:
     for folder in ["J:/My Drive/Efrat", "J:/My Drive/Keren"]:
         list all files
         for each file:
             if mime_type in [PDF, DOCX]:
                 download text representation
                 extract structured pricing data via LLM (one call per document)
                 append raw extractions to registry_raw.json

3. Merge and deduplicate:
     group by (vendor_name, item_name)
     for each group:
         keep all quote_date entries as history
         flag if item name varies significantly (possible same item, different wording)

4. Write data/vendor-registry.json with structure:
     {
       "_meta": {
         "extracted_on": "YYYY-MM-DD",
         "source_folders": [...],
         "total_records": N,
         "total_vendors": M,
         "cpi_adjustment_table": "data/cpi-israel.json"
       },
       "vendors": [
         {
           "vendor_name": "...",
           "category": "...",
           "contact": {"phone": "...", "email": "..."},
           "items": [
             {
               "item_name": "...",
               "quote_date": "YYYY-MM-DD",
               "unit_cost_ils": ...,
               "unit": "...",
               "source_proposal": "path/to/file.pdf",
               "notes": "..."
             }
           ]
         }
       ]
     }

5. Print summary:
     "✓ Extracted 284 records from 47 proposals across 23 vendors."
     "✓ Registry written to data/vendor-registry.json"
     "⚠ 12 entries flagged as possible duplicates, review manually"

LLM extraction prompt template (per document):

    You are extracting vendor pricing data from a Bold Productions historical
    event proposal. Return JSON only. Schema:
    
    {
      "proposal_name": "...",
      "proposal_date": "YYYY-MM-DD",
      "client": "...",
      "line_items": [
        {
          "vendor_name": "...",  # null if Bold internal
          "category": "one of the 21 canonical categories",
          "item_name": "...",
          "qty": N,
          "unit": "...",
          "unit_cost_ils": N,
          "total_ils": N,
          "notes": "..."
        }
      ]
    }
    
    Rules:
    - Skip items without a clear unit price.
    - Use the 21 canonical categories from the skill's stage-5-budget.md. If
      no category fits, use "other" and flag.
    - If a line says "Bold internal" or Bold's own staff role, set vendor_name=null.
    - Parse Hebrew vendor names carefully; do not transliterate.
    - If the document has multiple sections with different clients or dates,
      split into multiple extractions.

CPI adjustment function:

    def cpi_adjust(unit_cost_ils, quote_date, today):
        # Load data/cpi-israel.json: { "YYYY-MM": float, ... } with a base
        # month normalized to 100.0.
        cpi_quote = cpi_table.lookup(quote_date.strftime("%Y-%m"))
        cpi_today = cpi_table.lookup(today.strftime("%Y-%m"))
        return unit_cost_ils * (cpi_today / cpi_quote)

Running the script:

    python3 extract-vendor-data.py --dry-run
        prints what it would do, does not call Drive
    
    python3 extract-vendor-data.py --run
        performs actual extraction; requires Drive MCP available
    
    python3 extract-vendor-data.py --merge-only
        does not fetch from Drive; just re-merges and normalizes existing
        registry_raw.json
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


CANONICAL_CATEGORIES = [
    "ניהול הפקה",
    "קונספט ועיצוב",
    "תפאורה ובינוי",
    "תאורה",
    "סאונד והגברה",
    "וידאו ותצוגות",
    "חשמל וגנרציה",
    "ריהוט וציוד",
    "קייטרינג ואירוח",
    "בר ומשקאות",
    "תוכן ותקשורת",
    "מנחה, אמנים, מופעים",
    "אושרים וצוות אירוע",
    "אבטחה ורפואה",
    "הפקה חזותית",
    "הדפסות ושילוט",
    "מתנות ומזכרות",
    "הסעות וחניה",
    "היתרים ואגרות",
    "גיבוי והתרעות",
    "רווח Bold",
]


def main():
    parser = argparse.ArgumentParser(description="Extract vendor pricing from Drive archive")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without calling Drive")
    parser.add_argument("--run", action="store_true", help="Execute the extraction")
    parser.add_argument("--merge-only", action="store_true", help="Skip Drive, re-merge local raw data")
    parser.add_argument("--output", default="data/vendor-registry.json")
    args = parser.parse_args()

    if not any([args.dry_run, args.run, args.merge_only]):
        print("ERROR: pass --dry-run, --run, or --merge-only", file=sys.stderr)
        sys.exit(2)

    print("=" * 60)
    print("Vendor Registry Extraction")
    print("=" * 60)
    print()
    print("This script is a blueprint. Actual Drive extraction must be")
    print("driven by Claude in an interactive session because it requires")
    print("Google Drive MCP calls and per-document LLM extraction.")
    print()
    print("When Hemi asks 'update the vendor registry', Claude should:")
    print("  1. List files in J:/My Drive/Efrat and J:/My Drive/Keren via Drive MCP")
    print("  2. For each PDF/DOCX, extract pricing using the template in this file")
    print("  3. Merge, deduplicate, apply CPI normalization")
    print(f"  4. Write to {args.output}")
    print()
    print("Canonical categories the extraction must map to:")
    for i, cat in enumerate(CANONICAL_CATEGORIES, 1):
        print(f"  {i:2d}. {cat}")
    print()

    if args.dry_run:
        print("Dry-run complete. No changes made.")
        return

    if args.merge_only:
        raw_path = Path("data/registry_raw.json")
        if not raw_path.exists():
            print("ERROR: data/registry_raw.json not found; nothing to merge.", file=sys.stderr)
            sys.exit(1)
        # Merge logic would go here; placeholder for now
        print(f"Would merge {raw_path} into {args.output}.")
        return

    if args.run:
        print("ERROR: actual extraction must be driven by Claude with Drive MCP.", file=sys.stderr)
        print("Run this script in --dry-run mode for the blueprint, then ask Claude to proceed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
