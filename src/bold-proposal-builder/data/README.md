# data/

Indexes pointing at Bold's vendor pricing sources in Google Drive. Read by `bold-proposal-builder` at session start to harvest fresh supplier costs for Stage 5 (budget).

## Files

### `vendor-registry.seed.json` (SEED, not live)

Starter scaffold. Confirmed file IDs, best-guess categorizations, and the Drive scan strategy.
Promote to `vendor-registry.json` only after Hemi confirms each entry's category and after stale entries are refreshed.

## Discovery notes from the 2026-05-22 scan

The two folder IDs originally listed as canonical vendor folders did not pan out:

- `0B7TFmdvhXcItS1JxM2xIZG5YeUU` resolves but contains the project archive root (year folders 2012 through 2026 plus client folders), not vendor data.
- `0B7TFmdvhXcItZnVaVllQZmZOS0U` resolves but is empty.

Bold has no single canonical vendor folder. Vendor pricelists are scattered across per-vendor folders. The reliable harvest pattern is a Drive-wide name search:

```
name contains 'מחירון' and trashed = false
name contains 'הצעת מחיר' and trashed = false and modifiedTime > '2024-01-01T00:00:00Z'
```

The `הצעת מחיר` results are dominated by quotes Bold sends OUT to clients (pinui-binui sales, e.g. אשרמן, הטייסים, מעונות ים). Filter those out at parse time.

The highest-fidelity source for current supplier rates is the recent Bold-authored project budget XLSXes (`תקציב`), not the vendor pricelist PDFs. Pricelists give catalog rates; the project budgets show what Hemi actually paid.

## Schema sketch

```jsonc
{
  "vendor_pricelists": [
    {
      "vendor_key": "...",
      "vendor_label_he": "...",
      "category_guess": "כללי | תקשור מקדים | מיתוג ושילוט | טכני | כח אדם ולוגיסטיקה | שונות",
      "category_confirmed": false,
      "file_id": "...",
      "file_name": "...",
      "mime_type": "...",
      "modified": "YYYY-MM-DD",
      "parent_folder_id": "..."
    }
  ],
  "reference_budgets": [
    {
      "budget_key": "...",
      "client": "...",
      "event_date": "YYYY-MM-DD",
      "file_id": "...",
      "parent_folder_id": "..."
    }
  ]
}
```

## Open questions

Listed in the seed JSON under `open_questions`. The big ones:

1. Confirm each `category_guess`.
2. Decide whether wine and catering files get their own category or stay in `שונות`.
3. Decide whether to extract supplier costs from the Phoenix and Tzion 3 budgets and back-fill them as live unit costs.
