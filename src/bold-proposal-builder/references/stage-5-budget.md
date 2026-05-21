# Stage 5, Budget Reference (v3.0)

## Purpose

The budget is the credibility test of the proposal. Beautiful concepts get rejected when the numbers feel arbitrary. Stage 5 produces a structured, defensible budget grounded in real supplier quotes from Bold's Drive archive, applies Bold's dual-layer margin model, and outputs Excel in Bold's canonical 13-column RTL template.

Output: `05-budget/budget.json`, rendered to Excel in Stage 6 by `scripts/build_budget_xlsx.py` v4.0.

## What changed in v3.0 (from v2)

The biggest change: the margin model is **dual-layer**, not single-layer.

Previous (incorrect) understanding: "Production fee is the margin. 15% on the bottom line, that's it."

Actual Bold practice: TWO 15% layers.

1. **Per-line embedded markup of 15%.** Every line item in budget.json carries the supplier's `unit_cost`. The script automatically derives the client unit price as `unit_cost * 1.15`. This 15% is invisible to the client. No column, no label, no row says "15%". It manifests only as the gap between supplier cost (col F) and client charge (col K), surfaced in the gray profit columns L-M (for Bold's internal eyes only).

2. **Production fee of 15% on the section subtotal.** A dedicated visible line "דמי ארגון והפקה" appears after the main section subtotal, valued at 15% of the section's client charge total. The client sees this explicitly.

Effective Bold margin per shekel charged: 1.15 * 1.15 = 1.3225, or roughly 32%.

The script enforces this model. Stage 5's job is just to populate `unit_cost` (supplier price) per line and leave client pricing entirely to the script.

## Vendor quote sourcing

Every non-internal line item must trace back to a real supplier quote from Bold's Drive archive. The skill maintains `data/vendor-registry.json` as its working memory. See `references/vendor-quote-monitoring.md` for the full delta-check protocol that runs at the start of every proposal.

In short: at Stage 1 or Stage 5 open (whichever comes first), the skill scans the two Drive folders for new quotes since the last sync, parses them, and updates `vendor-registry.json`. Stage 5 then queries the registry by category + description to populate `unit_cost`.

If no quote matches a needed line, Stage 5 writes the line with `unit_cost: null` and Hemi decides how to proceed (fresh quote, placeholder, or drop the line). The script will not invent prices.

## The canonical 6-category tree

Bold has used these 6 top-level categories since 2010. Stage 5 does NOT invent categories; every line must map to one of these six.

```
1. כללי              (General)
2. תקשור מקדים        (Pre-event communications)
3. מיתוג ושילוט       (Branding & signage)
4. טכני              (Technical)
5. כח אדם ולוגיסטיקה   (Staff & logistics)
6. שונות             (Miscellaneous)
```

Underneath the six sit 30 sub-categories and ~140 typical line items. Full taxonomy in `assets/budget-categories-reference.md`. The script auto-rolls non-canonical categories into שונות with a `[WARN]` to stderr; if such warnings appear, Stage 5 should be revisited because the categorization slipped.

## budget.json schema (v3.0)

Only `unit_cost`, `qty`, `description`, and `category` are required per item. Everything else is optional. The script derives all client-facing pricing.

```json
{
  "meta": {
    "proposal_name": "השקת מוצר X",
    "client": "פיניקס",
    "event_date": "2026-06-15",
    "guest_count": 200,
    "currency": "ILS",
    "valid_until": "2026-06-01"
  },
  "categories": [
    {
      "name": "טכני",
      "items": [
        {
          "description": "מערכת הגברה PA קלאסי",
          "qty": 1,
          "unit": "אירוע",
          "unit_cost": 8500,
          "vendor_name": "ABC הגברה",
          "payment_terms": "שוטף+30",
          "source_deliverable": "operations/logistics.md sec 3",
          "source_vendor_registry": "1abc_drive_file_id"
        }
      ]
    },
    {
      "name": "כח אדם ולוגיסטיקה",
      "items": [
        {
          "description": "מנהל הפקה ראשי",
          "qty": 1,
          "unit": "אירוע",
          "unit_cost": 9000,
          "vendor_name": "Bold internal",
          "source_deliverable": "operations/logistics.md sec 6"
        }
      ]
    }
  ],
  "conditional_items": [
    {
      "description": "תאורת חצר נוספת",
      "qty": 1,
      "unit": "אירוע",
      "unit_cost": 3200,
      "vendor_name": "תאורה XYZ",
      "trigger_condition": "outdoor extension if weather permits",
      "source_deliverable": "operations/logistics.md sec 3.2"
    }
  ]
}
```

### Important: client pricing is never specified in budget.json

There is no `unit_price`, no `total_charge`, no `production_fee` field in this schema. All of those are derived by the script. The only price input is `unit_cost` (the supplier's price to Bold). This is the load-bearing principle of the dual-margin model: per-line markup is a script-internal calculation, never a manual field that could leak the 15% to the client.

### Required fields per item

- `description`
- `qty`
- `unit_cost` (or `null` with a `[WARN]` if no quote available)

### Strongly recommended per item

- `unit` (default "אירוע" if omitted)
- `vendor_name` (so the supplier side of the XLSX is filled)
- `source_deliverable` (audit trail back to a Stage 1-4 artifact)
- `source_vendor_registry` (audit trail back to a Drive quote file)

### Optional

- `payment_terms`
- `trigger_condition` (for conditional items)
- `notes`

## Sanity checks before closing Stage 5

1. **Deliverable coverage:** every Stage-4 output has at least one budget line.
2. **No phantom lines:** every budget line has `source_deliverable`.
3. **Quote coverage:** at least 70% of non-internal lines have `source_vendor_registry`. Lower than 70% means too many invented prices; either get more quotes or flag the proposal as preliminary.
4. **No client-price fields:** budget.json contains zero references to `unit_price`, `total_charge`, or markup percentages. If any appear, fix immediately.
5. **Per-guest sanity:** total client charge divided by guest count looks sensible for this client tier.
6. **Top three categories** match the client's stated priorities from brief field 3.
7. **Conditional items** are genuinely optional, not bundled extras Bold needs to maximize the win rate.
8. **Production fee not duplicated:** budget.json must NOT contain any line with description containing "דמי ארגון" or "production fee". The script adds the visible 15% line automatically.

## What "done" looks like

A finance-literate client reading the rendered Excel can:
- See clearly what they're paying for, line by line
- See clearly what is optional (in the אופציות section)
- Understand per-guest and per-category spending
- Trace any number back to a deliverable

A Bold operator reading the same Excel can:
- See supplier costs in columns A-F (right side)
- See client charges in columns G-K (middle)
- See profit in ₪ and % in columns L-M (left, gray)
- Spot any line where margin is unexpectedly low and renegotiate the vendor

And Bold's effective ~32% margin is protected end-to-end, with no client-facing mention of the per-line 15%.
