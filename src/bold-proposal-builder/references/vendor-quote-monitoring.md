# Vendor Quote Monitoring Reference (v2.0)

## Purpose

Bold's pricing in Stage 5 is grounded in real supplier costs, not invented numbers. This reference defines where quotes live in Drive, how the skill scans them, and how vendor-registry.json is maintained.

## Drive folder structure (verified May 2026)

Bold's Drive is organized by year, then by project, then by sub-folder. Vendor quotes are NOT at the root of the two source folders - they are nested 2-3 levels deep.

```
Root folder (0B7TFmdvhXcItS1JxM2xIZG5YeUU)
  2026/
    פניקס/
      הצעות מחיר ספקים/
        ארגוני במות/  <- PDF quotes here
        מיתוג/        <- PDF quotes here
    MAN 2026/
      הצעות/          <- PDF quotes here
      MAN12.05.xlsx   <- budget XLSX with supplier costs
    סופרין - טכנופארק אשדוד/
      תקציב/
    ציון 3/
      01 - תקציב ופיננסים/
  Efrat - 2025/
    MAN 09.25