# Stage 5 — Budget Reference (v2)

## Purpose

The budget is the credibility test of the proposal. Beautiful concepts get rejected when the numbers feel arbitrary. Stage 5 v2 builds a structured, defensible budget where every line ties to a deliverable AND to a real historical price from Bold's own archive, adjusted for inflation.

Output: `05-budget/budget.json`, rendered to Excel in Stage 6.

**Key change from v1:** Instead of inventing or guessing unit costs, Stage 5 consults `data/vendor-registry.json`, which is populated by `scripts/extract-vendor-data.py` from Bold's historical proposals in Drive.

---

## The canonical cost-category tree

Bold's budgets organize by these top-level categories. Not every event has every category; drop the ones that are not relevant. Do not invent new top-level categories without reason.

```
1. ניהול הפקה (Production management)
2. קונספט ועיצוב (Concept & design)
3. תפאורה ובינוי (Scenography & build)
4. תאורה (Lighting)
5. סאונד והגברה (Sound)
6. וידאו ותצוגות (Video & display)
7. חשמל וגנרציה (Power)
8. ריהוט וציוד (Furniture & equipment)
9. קייטרינג ואירוח (Catering & hospitality)
10. בר ומשקאות (Bar & beverage)
11. תוכן ותקשורת (Content & communications)
12. מנחה, אמנים, מופעים (MC, talent, performances)
13. אושרים וצוות אירוע (Hostesses & event staff)
14. אבטחה ורפואה (Security & medical)
15. הפקה חזותית, תמונות וסרטונים (Visual content production)
16. הדפסות ושילוט (Print & signage)
17. מתנות ומזכרות (Gifts & takeaways)
18. הסעות וחניה (Transport & parking)
19. היתרים ואגרות (Permits & fees)
20. גיבוי והתרעות (Contingency)
21. רווח Bold (Bold margin)
```

---

## The vendor registry, how it feeds Stage 5

### What the registry contains

`data/vendor-registry.json` is structured like this:

```json
{
  "_meta": {
    "extracted_on": "2026-04-21",
    "source_folders": ["J:/My Drive/Efrat", "J:/My Drive/Keren"],
    "total_records": 284,
    "cpi_adjustment_table": "data/cpi-israel.json"
  },
  "vendors": [
    {
      "vendor_name": "חברת במות הצפון",
      "category": "תפאורה ובינוי",
      "items": [
        {
          "item_name": "במה 6x4 מ', גובה 60 ס\"מ",
          "quote_date": "2024-03-15",
          "unit_cost_ils": 4200,
          "unit": "אירוע",
          "source_proposal": "Keren/Biotech Launch Mar 2024.pdf",
          "notes": "כולל הובלה והקמה"
        },
        {
          "item_name": "במה 6x4 מ', גובה 60 ס\"מ",
          "quote_date": "2022-09-08",
          "unit_cost_ils": 3600,
          "unit": "אירוע",
          "source_proposal": "Efrat/Pharma Conference Sep 2022.pdf",
          "notes": "כולל הובלה, בלי הקמה"
        }
      ],
      "contact": {
        "phone": "...",
        "email": "..."
      }
    }
  ]
}
```

### How to use it during Stage 5

For each line item Claude wants to price:

1. **Look up the category + item in the registry.**
2. **Find the most recent quote.** If there are multiple, prefer the latest.
3. **Apply CPI adjustment** from the quote date to today using `data/cpi-israel.json`.
4. **Write the line** with the adjusted number and cite the source in `notes`.

Example:

Registry entry: 
- Item: "במה 6x4 מ'"
- Quote date: 2024-03-15
- Unit cost: ₪4,200

CPI adjustment (Israel):
- March 2024 CPI: 100.0 (baseline)
- April 2026 CPI: 108.4 (hypothetical; actual from cpi-israel.json)
- Adjusted unit cost: ₪4,200 × 1.084 = ₪4,553

Budget line:
```json
{
  "name": "במה 6x4 מ', גובה 60 ס\"מ",
  "qty": 1,
  "unit": "אירוע",
  "unit_cost": 4553,
  "vendor_role": "Scenography supplier",
  "notes": "בסיס: חברת במות הצפון 2024-03. התאמה לפי מדד מחירים + כולל הובלה והקמה",
  "source_deliverable": "operations/logistics.md §2",
  "source_vendor_registry": "vendor-registry.json#vendors[0].items[0]"
}
```

### When no registry entry exists

If the item is genuinely new (no historical precedent in Bold's archive):
1. Flag it in notes: `"Awaiting vendor quote, no historical baseline"`
2. Set `"unit_cost": null`
3. Ask Hemi to either provide a placeholder or contact a vendor

Do NOT invent a number. The registry exists precisely so Bold's prices are grounded in Bold's history, not Claude's imagination.

### Keeping the registry fresh

The registry should be refreshed quarterly by re-running `scripts/extract-vendor-data.py`. Additionally, Stage 7 Debrief can produce a registry update as a skill-level learning: "the actual price charged for X was ₪Y, 18% above the registry estimate. Update the baseline."

---

## JSON schema (v2, unchanged from v1 except for `source_vendor_registry` field)

```json
{
  "meta": {
    "proposal_name": "שם האירוע",
    "client": "שם הלקוח",
    "date": "YYYY-MM-DD",
    "guest_count": 210,
    "currency": "ILS",
    "valid_until": "YYYY-MM-DD",
    "margin_pct": 22,
    "contingency_pct": 8,
    "vat_applicable": true,
    "vat_pct": 18,
    "vendor_registry_version": "2026-04-21"
  },
  "categories": [
    {
      "id": "production_management",
      "name": "ניהול הפקה",
      "items": [
        {
          "name": "מנהל/ת הפקה ראשי/ת",
          "qty": 1,
          "unit": "אירוע",
          "unit_cost": 12000,
          "vendor_role": "Bold internal",
          "conditional": false,
          "trigger_condition": null,
          "notes": "ליווי מהקיקאוף עד אחרי האירוע",
          "source_deliverable": "operations/logistics.md §6",
          "source_vendor_registry": null
        }
      ]
    }
  ],
  "summary": {
    "subtotal": null,
    "contingency": null,
    "margin": null,
    "total_pre_vat": null,
    "vat": null,
    "total_with_vat": null,
    "total_with_conditional": null
  }
}
```

---

## Item-level rules (mostly unchanged from v1)

### Every item must reference a deliverable
Every line has a `source_deliverable` pointing back to a stage 1-4 artifact.

### NEW v2: Every non-Bold-internal item should reference the registry if possible
If the line is sourced from `vendor-registry.json`, populate `source_vendor_registry` with the JSON pointer. If not, leave null and flag in notes.

### Units must be concrete
`אירוע` / `יח'` / `שעה` / `סועד` / `חבילה` / `יום`.

### Vendor roles, not vendor names (in the budget itself)
In the budget line, write the vendor *role*. The registry holds actual vendor names; Hemi assigns them later.

### Conditional items
Conditional items (`conditional: true`) have a `trigger_condition` field.

### Notes fields
Short, direct. Include the registry source citation when applicable.

---

## How to populate the budget (v2 method)

### Step 1: Extract line items from stage-4 documents
Walk through each stage-4 deliverable and list every tangible or services item it implies.

### Step 2: Query the vendor registry
For each line item, search the registry:
```python
# pseudocode
for item in draft_line_items:
    matches = registry.find(category=item.category, item_name_like=item.name)
    if matches:
        most_recent = max(matches, key=lambda m: m.quote_date)
        item.unit_cost = cpi_adjust(most_recent.unit_cost_ils, most_recent.quote_date, today)
        item.source_vendor_registry = most_recent.pointer()
        item.notes += f" (בסיס: {most_recent.vendor} {most_recent.quote_date}, התאמת CPI)"
    else:
        item.unit_cost = None
        item.notes = "Awaiting vendor quote, no historical baseline"
```

### Step 3: Apply contingency and margin
- Contingency default: 8%
- Margin default: 22%

### Step 4: VAT and final totals
Israeli VAT in 2026: 18%.

### Step 5: Conditional items
2 to 4 conditional items typically. Don't overload.

---

## Sanity checks before closing stage 5

1. **Deliverable coverage.** Every stage-4 output has at least one budget line.
2. **No phantom lines.** Every budget line has a `source_deliverable`.
3. **Registry coverage.** At least 70% of non-internal lines should have `source_vendor_registry` populated. If less, the registry is under-populated and worth a refresh.
4. **Per-guest sanity.** Divide the subtotal by guest count. Does per-guest cost look sensible?
5. **Top three categories** match the client's stated priorities from the brief.
6. **Conditional items are genuinely optional.**

---

## What "done" looks like

A finance-literate client reviewer reading the budget Excel can:
- See clearly what they're paying for.
- See clearly what is optional.
- Understand per-guest and per-category spending.
- Trace any number back to a deliverable AND (for non-internal lines) to a historical Bold precedent.

And Bold's margin is protected but transparent.
