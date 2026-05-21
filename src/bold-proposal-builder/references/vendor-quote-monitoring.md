# Vendor Quote Monitoring Reference (v1.0)

## Purpose

Bold's pricing in Stage 5 is grounded in real supplier quotes, not invented numbers. This reference defines the two Drive folders that hold those quotes, the delta-check mechanism that runs at the start of every new proposal, and the structure of the local `data/vendor-registry.json` that the skill maintains as its working memory of supplier prices.

## The two Drive source folders

| ID | URL | What it contains |
|---|---|---|
| `0B7TFmdvhXcItS1JxM2xIZG5YeUU` | https://drive.google.com/drive/folders/0B7TFmdvhXcItS1JxM2xIZG5YeUU | Vendor quotes folder 1 |
| `0B7TFmdvhXcItZnVaVllQZmZOS0U` | https://drive.google.com/drive/folders/0B7TFmdvhXcItZnVaVllQZmZOS0U | Vendor quotes folder 2 |

These folder IDs are stored in `data/vendor-registry.json` under `_meta.source_folders` so the skill can re-scan them on every run.

## When the delta check runs

At the start of every proposal (Stage 1 close-out or Stage 5 open, whichever comes first), the skill performs a vendor-quote delta check:

1. Read `data/vendor-registry.json` if present. Note the `_meta.last_scan_utc` timestamp.
2. For each source folder ID, list files (via Google Drive MCP) modified after `last_scan_utc`.
3. For each new file:
   - Read the file via `google_drive_fetch` (for Docs) or `gdrive_download_file` (for PDF/XLSX)
   - Parse the supplier name, line items, unit costs, and quote date out of the file
   - Update or append entries in `vendor-registry.json` under the matching category
4. Update `_meta.last_scan_utc` to now.
5. If no `vendor-registry.json` exists yet, do a full scan (no time filter) and create one.
6. Report to Hemi how many new quotes were ingested. Do not block on parser failures: log them in `_meta.parse_errors` and proceed with the rest.

The skill does not re-prompt Hemi about the same quote twice. Once a file is in the registry, it stays there until the source file is deleted from Drive.

## Parsing strategy

Quote files in the Drive folders are mostly PDFs (vendor email attachments) and XLSX (price lists). The parser is opportunistic, not strict.

### For PDF quotes

1. Extract text via `pdf-reading` skill or `pypdf`.
2. Look for: vendor letterhead (top of doc), date, line items (table rows with description + unit price + quantity + total).
3. If the parser cannot identify line items confidently, store the raw text under `vendors[<name>].raw_quote_text` for manual processing later and continue.

### For XLSX quotes

1. Open via `openpyxl` (or `xlrd` for `.xls`).
2. First-row headers usually include some combination of: שירות, פריט, יח', מחיר, סה"כ. If headers are missing, look for a row with 3+ numeric-only cells in a price-shaped pattern.
3. Stop at the first blank row.

### Quote metadata that always gets captured

For every recognized line item:

- `item_name` (Hebrew description as it appears)
- `unit` (אירוע / יחידה / שעה / מטר / etc., default אירוע if missing)
- `unit_cost_ils` (integer or float)
- `quote_date` (best guess from file or filename; fallback `null`)
- `source_drive_file_id`
- `source_drive_file_name`
- `notes` (anything else from the row that may be useful)

## The vendor-registry.json structure

```json
{
  "_meta": {
    "version": "2.0",
    "last_scan_utc": "2026-05-21T08:30:00Z",
    "source_folders": [
      "0B7TFmdvhXcItS1JxM2xIZG5YeUU",
      "0B7TFmdvhXcItZnVaVllQZmZOS0U"
    ],
    "files_seen": [
      "1abc...",
      "1xyz..."
    ],
    "parse_errors": [
      {
        "file_id": "1...",
        "file_name": "Vendor X quote 2026.pdf",
        "error": "could not detect line item table",
        "raw_text_preserved": true
      }
    ],
    "cpi_adjustment_table": "data/cpi-israel.json"
  },
  "vendors": [
    {
      "vendor_name": "חברת הגברה ABC",
      "primary_category": "טכני",
      "contact": {
        "phone": "...",
        "email": "..."
      },
      "items": [
        {
          "item_name": "מערכת הגברה PA קלאסי, בינוני",
          "unit": "אירוע",
          "unit_cost_ils": 6800,
          "quote_date": "2026-03-15",
          "source_drive_file_id": "1abc...",
          "source_drive_file_name": "ABC הגברה הצעת מחיר 03.2026.pdf",
          "notes": "כולל הובלה והקמה תוך 60 דק'",
          "ingested_utc": "2026-05-21T08:30:00Z"
        }
      ]
    }
  ]
}
```

The `files_seen` list lets the delta check skip files that were already ingested even if their `modifiedTime` is recent (because the file was renamed, for example).

## Using the registry in Stage 5

When Stage 5 builds a budget line:

1. Identify the category (one of the 6 canonicals) and the rough description (e.g., "מערכת הגברה" under טכני).
2. Search `vendor-registry.json` for items in that category whose `item_name` matches by substring or keyword.
3. If matches found, pick the most recent by `quote_date`.
4. Apply CPI adjustment from `quote_date` to today using `data/cpi-israel.json` if present, otherwise use the raw `unit_cost_ils`.
5. Populate the budget line:
   - `unit_cost` (supplier price) = adjusted cost
   - `vendor_name` = matched vendor
   - `payment_terms` = vendor's typical terms if known
   - `source_vendor_registry` = file id (audit trail)
6. The script will then derive the client unit_price (= unit_cost * 1.15) automatically. Hemi never specifies client prices.

## When no match exists

If no quote covers a needed line, the line is written with `unit_cost: null`. The XLSX shows it as an empty cell. Hemi sees a `[WARN]` in the build output and decides whether to:
- Get a fresh quote and re-run
- Use a placeholder estimate (manual entry in budget.json)
- Drop the line

## Privacy note

The vendor-registry.json file contains supplier names, phone numbers, and prices. It lives only in the skill's local `data/` directory (or syncs to a private repo). It is never embedded in client-facing artifacts. The XLSX template hides supplier-side columns in client previews via column grouping (not yet automated; Hemi hides columns A-F manually before sending).

## Future improvements

- Auto-OCR for scanned-image PDF quotes (currently `pdf-reading` handles text-extractable PDFs only)
- Confidence scoring on parsed line items
- Vendor consolidation when the same vendor appears under multiple spellings
- Quote validity tracking (most Israeli vendor quotes expire after 30-60 days; flag stale matches)

## Manual update path

Hemi can edit `data/vendor-registry.json` directly to:
- Add a vendor not yet in the folders
- Correct a parser mistake
- Pin a specific price even when a newer quote exists

Manual edits are preserved across re-scans. The skill never overwrites manually-added entries unless the source file's content changes.
