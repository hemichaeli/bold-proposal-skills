# Stage 5, Budget Reference (v2)

## Purpose

The budget is the credibility test of the proposal. Beautiful concepts get rejected when the numbers feel arbitrary. Stage 5 v2 builds a structured, defensible budget where every line ties to a deliverable AND to a real historical price from Bold's own archive, adjusted for inflation.

Output: `05-budget/budget.json`, rendered to Excel in Stage 6.

Key change from v1: Instead of inventing or guessing unit costs, Stage 5 consults `data/vendor-registry.json`, which is populated interactively from Bold's historical proposals in Drive (Efrat + Keren folders).

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

1. Look up the category + item in the registry.
2. Find the most recent quote. If multiple, prefer the latest.
3. Apply CPI adjustment from the quote date to today using `data/cpi-israel.json`.
4. Write the line with the adjusted number and cite the source in notes.

### When no registry entry exists

If the item is genuinely new:
1. Flag in notes: "Awaiting vendor quote, no historical baseline"
2. Set unit_cost to null
3. Ask Hemi to either provide a placeholder or contact a vendor

Do NOT invent a number.

### Keeping the registry fresh

Refresh quarterly or when Stage 7 debrief surfaces material price shifts.

---

## JSON schema

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

## Item-level rules

### Every item must reference a deliverable
Every line has `source_deliverable` pointing back to a stage 1-4 artifact.

### Every non-Bold-internal item should reference the registry if possible
If sourced from `vendor-registry.json`, populate `source_vendor_registry`.

### Units must be concrete
`אירוע` / `יח'` / `שעה` / `סועד` / `חבילה` / `יום`.

### Vendor roles, not vendor names
In the budget line, write the vendor role. The registry holds actual vendor names.

### Conditional items
Conditional items have a `trigger_condition` field.

### Notes fields
Short, direct. Include the registry source citation when applicable.

---

## Sanity checks before closing stage 5

1. Deliverable coverage: every stage-4 output has at least one budget line.
2. No phantom lines: every budget line has `source_deliverable`.
3. Registry coverage: at least 70% of non-internal lines have `source_vendor_registry`.
4. Per-guest sanity: subtotal divided by guest count looks sensible.
5. Top three categories match the client's stated priorities.
6. Conditional items are genuinely optional.

---

## What "done" looks like

A finance-literate client reviewer reading the budget Excel can:
- See clearly what they're paying for
- See clearly what is optional
- Understand per-guest and per-category spending
- Trace any number back to a deliverable AND (for non-internal lines) to a historical Bold precedent

And Bold's margin is protected but transparent.
