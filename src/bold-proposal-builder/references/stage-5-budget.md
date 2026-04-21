# Stage 5 — Budget Reference

## Purpose

The budget is the credibility test of the proposal. Beautiful concepts get rejected when the numbers feel arbitrary. Stage 5 builds a structured, defensible budget where every line ties to a deliverable from stages 1 to 4.

Output: `05-budget/budget.json` — a structured JSON that will be rendered into the final Excel file in stage 6.

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
15. הפקה חזותית — תמונות וסרטונים (Visual content production)
16. הדפסות ושילוט (Print & signage)
17. מתנות ומזכרות (Gifts & takeaways)
18. הסעות וחניה (Transport & parking)
19. היתרים ואגרות (Permits & fees)
20. גיבוי והתרעות (Contingency)
21. רווח Bold (Bold margin)
```

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
    "vat_pct": 18
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
          "source_deliverable": "operations/logistics.md §6"
        }
      ]
    },
    {
      "id": "scenography",
      "name": "תפאורה ובינוי",
      "items": [
        {
          "name": "ספק תפאורה - הרחבה (אם נדרש)",
          "qty": 1,
          "unit": "חבילה",
          "unit_cost": 6000,
          "vendor_role": "Scenography supplier",
          "conditional": true,
          "trigger_condition": "אם הלקוח יאשר הרחבה של קיר ה-Reveal ל-6x4 מ' במקום 4x3 מ'",
          "notes": "שורה מותנית - להוסיף לסיכום רק אם מופעל",
          "source_deliverable": "operations/logistics.md §2 + brand-heart motif"
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

Set `summary` values to `null` in the JSON. The `build_budget_xlsx.py` script will calculate and inject them into the Excel file. Keeping them null in the JSON forces a single source of truth.

---

## Item-level rules

### Every item must reference a deliverable

Every line has a `source_deliverable` pointing back to a stage 1-4 artifact. If you cannot point, the line does not belong. This prevents "phantom" budget items like "miscellaneous decor ₪8,000" that later get removed by the client for being vague.

### Units must be concrete

- `"unit": "אירוע"` — flat fee for the whole event
- `"unit": "יח'"` — per unit (chair, table, sign)
- `"unit": "שעה"` — per hour of service
- `"unit": "סועד"` — per guest (catering)
- `"unit": "חבילה"` — package (explain in notes)
- `"unit": "יום"` — per day (multi-day events)

### Vendor roles, not vendor names (yet)

In stage 5, write the vendor *role* (e.g., "Scenography supplier", "Lighting designer", "Catering company"). Actual vendor names are assigned later when Hemi confirms which vendor Bold is using for this proposal. This separation lets the same budget template work across different vendor combinations.

Exceptions:
- "Bold internal" for roles Bold fills with its own team.
- Specific vendor names that the client has mandated (from stage 1's "mandatory suppliers" field) — use the actual name and mark it in `notes`.

### Conditional items

Conditional items (`"conditional": true`) have a `trigger_condition` field explaining when they activate. The canonical example is Bold's 6,000 ₪ scenography expansion line. Conditional items:
- Do NOT appear in the main subtotal.
- DO appear in a separate section of the Excel called "שורות מותנות".
- DO appear in the `total_with_conditional` summary as a separate total the client sees.

This lets the client see the baseline price clearly and understand what adds what. No surprises.

### Notes fields

Short, direct. "Includes setup and breakdown" is good. "This is a very important element for the ambiance of the event" is filler; delete it.

---

## How to populate the budget — the method

### Step 1: Extract line items from stage-4 documents

Walk through each stage-4 deliverable and list every tangible or services item it implies:
- From `logistics.md` § build: every structure, every piece of furniture, every signage element.
- From `logistics.md` § technical: every sound/light/video/power item.
- From `content/scripts.md`: printed invitations, signage, menu cards.
- From `culinary/menu.md`: catering, bar, rentals specific to food service.
- From `visual/mockups/` and mood-direction.md: signage, installations, light treatments beyond standard.
- From agenda.md: any talent, MC, performers implied.

### Step 2: Quantify and unit-price

For each item:
- **Quantity:** from the physical plan (how many chairs? how many spotlights?).
- **Unit cost:** from Bold's historical data in Drive, from industry rates, from current market. If unknown, put `"unit_cost": null` and flag in notes: "Awaiting vendor quote". Do not invent numbers.

### Step 3: Apply contingency and margin

- **Contingency** is a % of the subtotal that absorbs surprises. Typical 5 to 10%. Set 8% as default unless the event is unusually stable (low contingency, 5%) or unusually risky (high, 12%).
- **Margin** is Bold's profit. Typical 20 to 28%. Default 22%. Negotiated down only for strategic clients or loss-leader events.

### Step 4: VAT and final totals

Israeli VAT in 2026 is 18%. If the client is a business that can reclaim VAT, present pre-VAT prominently. If the client is a consumer or a non-reclaiming entity (certain nonprofits, individuals), present with-VAT prominently.

### Step 5: Conditional items

For each genuinely optional enhancement the client could add, add a conditional line. Don't load 15 conditional items; 2 to 4 is usually right. Over-loading reads as upselling.

---

## Sanity checks before closing stage 5

Before marking stage 5 complete, run these:

1. **Deliverable coverage.** Every stage-4 output has at least one budget line. No orphans.
2. **No phantom lines.** Every budget line has a `source_deliverable`. No orphans.
3. **Per-guest sanity.** Divide the subtotal by guest count. Does the per-guest cost look sensible for the event type and standard? If it's ₪350/guest for a premium seated dinner, plausible. If it's ₪1,800/guest, something is inflated or the event is unusually premium and the client knows it.
4. **Top three categories.** Which three categories are the biggest? Do they match the client's stated priorities from the brief? If the hero moment is a reveal, scenography should be top-heavy. If it's a chef's dinner, catering. If they don't match, something is off.
5. **Conditional items are genuinely optional.** If the event doesn't work without the conditional item, it's not conditional; promote it.

---

## Historical seeding from Drive

When Hemi grants access to Drive proposals:
- Pull 3 to 5 past Bold proposals with similar event type and guest count.
- Extract their line-item structures and typical unit costs.
- Use them as priors, not as gospel. Prices change; events differ.
- Cite the source in `notes`: `"Baseline from Phoenix Group 2025 opening, adjusted +8% for 2026 inflation"`.

This turns each new proposal into a compounding asset: Bold's historical knowledge gets more useful, not less, over time.

---

## What "done" looks like

A finance-literate client reviewer reading the budget Excel can:
- See clearly what they're paying for.
- See clearly what is optional.
- Understand per-guest and per-category spending.
- Trace any number back to a deliverable.

And Bold's margin is protected but transparent.
