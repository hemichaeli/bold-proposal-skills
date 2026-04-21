# data/

This folder holds cross-proposal data that Claude consults during the flow:

## vendor-registry.json
Populated by `scripts/extract-vendor-data.py`. Stage 5 (Budget) reads it to price line items from historical Bold quotes, adjusted for CPI.

Refresh quarterly or when Stage 7 debrief surfaces material price shifts.

## proposal-patterns.md
Populated by `scripts/extract-proposal-patterns.py`. Stage 6 (Assembly) reads it as a style reference for the PDF and Gamma deck.

Refresh when Bold's aesthetic evolves or when adding significant new reference material to `K:/My Drive/macshare/events`.

## cpi-israel.json
Reference table of Israeli CPI by month, normalized. Used by Stage 5 to adjust historical vendor quotes to today's prices.

Format:
```json
{
  "_base_month": "2024-03",
  "_base_value": 100.0,
  "values": {
    "2020-01": 93.2,
    "2020-02": 93.1,
    "...": "...",
    "2026-04": 108.4
  }
}
```

Source: Israeli Central Bureau of Statistics (CBS). Refresh monthly or as needed.

## client-profiles/
One `.md` file per Bold client. Populated at Stage 7 (Debrief) with learnings that seed future Stage 1 (Brief) sessions for the same client.

See `client-profiles/README.md` for the file format.
