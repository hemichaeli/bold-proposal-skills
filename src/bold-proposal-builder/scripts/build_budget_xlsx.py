#!/usr/bin/env python3
"""
build_budget_xlsx.py, v3.0

Produces budget.xlsx in Bold Productions' exact canonical template format
("טמפלט תקציב 01", in use at Bold since 2010). This is a full rewrite from v2.x:
the previous generic 3-sheet layout has been replaced with the single-sheet,
two-section, 13-column Bold template exactly as Hemi uses it.

Input:  budget.json (schema below)
Output: budget.xlsx (Bold canonical format, RTL, Hebrew headers)

USAGE
  python build_budget_xlsx.py <budget.json> <output.xlsx>

INPUT SCHEMA (budget.json)
{
  "project_meta": {
    "project_number": "2026-042",      # optional
    "client_name": "...",              # Hebrew or English
    "producer_name": "Hemi Michaeli",  # the Bold producer
    "project_name": "..."              # event name
  },
  "main_lines": [                      # Lines in the main budget section
    {
      "category": "כללי",              # MUST be one of the 6 canonical categories:
                                       # כללי / תקשור מקדים / מיתוג ושילוט /
                                       # טכני / כח אדם ולוגיסטיקה / שונות
      "service": "שירותי הפקה",        # פרוט השירות (col 8)
      "units": 1,                      # מספר יחידות (col 9)
      "unit_price": 25000,             # מחיר יחידה (col 10), client-facing
      "vendor": "Bold internal",       # שם הספק (col 1)
      "invoice_number": "",            # חש' (col 2)
      "actual_spend": 0,               # הוצאה בפועל (col 3)
      "payment_terms": "שוטף 30",      # תנאי תשלום (col 4)
      "unit_cost": 20000               # עלות יחידה (col 5), internal
    },
    ...
  ],
  "conditional_lines": [               # Same schema, go into "אופציות" section
    ...
  ],
  "production_fee_rate": 0.15          # Default 15%, Hemi can override
}

The category field on each main_line is required and drives grouping.
Lines are sorted in canonical category order:
  1. כללי
  2. תקשור מקדים
  3. מיתוג ושילוט
  4. טכני
  5. כח אדם ולוגיסטיקה
  6. שונות

Conditional lines do not subdivide; they all sit under one "כללי" header
in the options section, matching Bold's practice.

OUTPUT STRUCTURE (one sheet, "טמפלט ריק", matches original byte-for-byte
in layout terms)

  Row 2:  project_number | blank | client_name
  Row 3:  producer_name  | blank | project_name
  Row 5:  Column headers (13 columns, RTL order)
  Rows 6+: Main section
    - Category marker row (only col 7 "סעיף תקציבי" filled)
    - One row per line item
    - Repeat for all 6 categories in order
  Production fee row:  "דמי ארגון והפקה" + rate + computed value
  Total row:           "סה"כ" + computed total
  Blank rows
  Options header row:  "אופציות" (col 7)
  Options column headers (same 13)
  Options category marker "כללי"
  Options line rows
  Options production fee row
  Options total row: "סה"כ חשבונית"

COLUMN MAP (1-indexed to match the original spreadsheet)

 C1  שם הספק             vendor name (internal)
 C2  חש'                 invoice number (internal)
 C3  הוצאה בפועל          actual spend (internal)
 C4  תנאי תשלום           payment terms (internal)
 C5  עלות יחידה            unit cost (internal)
 C6  סה"כ עלות            total cost (internal, computed)
 C7  סעיף תקציבי           category (client-facing on markers; blank on line rows)
 C8  פרוט השירות          service description (client-facing)
 C9  מספר יחידות           units (client-facing)
 C10 מחיר יחידה           unit price (client-facing)
 C11 סה"כ חיוב            total charge (client-facing, computed)
 C12 רווחיות               profitability (internal, computed: C11 - C6)
 C13 %                    margin percent (internal, computed)

All currency cells are formatted "#,##0". Percent cells as 0%.
RTL reading order is set at the sheet level.
"""

import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


# Canonical category order. DO NOT change without consulting Hemi.
CANONICAL_CATEGORIES = [
    "כללי",
    "תקשור מקדים",
    "מיתוג ושילוט",
    "טכני",
    "כח אדם ולוגיסטיקה",
    "שונות",
]

# Column headers in the exact order of the original template (RTL, C1-C13).
COLUMN_HEADERS = [
    "שם הספק",      # C1
    "חש'",           # C2
    "הוצאה בפועל",   # C3
    "תנאי תשלום",    # C4
    "עלות יחידה",    # C5
    "סה\"כ עלות",    # C6
    "סעיף תקציבי",   # C7
    "פרוט השירות",   # C8
    "מספר יחידות",   # C9
    "מחיר יחידה",    # C10
    "סה\"כ חיוב",    # C11
    "רווחיות",       # C12
    "%",            # C13
]


# Styling primitives
def _border(style: str = "thin") -> Border:
    side = Side(style=style, color="000000")
    return Border(left=side, right=side, top=side, bottom=side)


HEADER_FILL = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
CATEGORY_MARKER_FILL = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
TOTAL_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

TAHOMA_REGULAR = Font(name="Tahoma", size=10)
TAHOMA_BOLD = Font(name="Tahoma", size=10, bold=True)
TAHOMA_HEADER = Font(name="Tahoma", size=11, bold=True)
CENTER_WRAP = Alignment(horizontal="center", vertical="center", wrap_text=True, readingOrder=2)
RIGHT_WRAP = Alignment(horizontal="right", vertical="center", wrap_text=True, readingOrder=2)


def _set_column_widths(ws):
    """Match the approximate widths of the original template."""
    widths = {
        1: 18,   # שם הספק
        2: 10,   # חש'
        3: 13,   # הוצאה בפועל
        4: 14,   # תנאי תשלום
        5: 12,   # עלות יחידה
        6: 12,   # סה"כ עלות
        7: 18,   # סעיף תקציבי
        8: 28,   # פרוט השירות
        9: 10,   # מספר יחידות
        10: 12,  # מחיר יחידה
        11: 13,  # סה"כ חיוב
        12: 11,  # רווחיות
        13: 8,   # %
    }
    for col, w in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = w


def _write_header_band(ws, meta: dict) -> int:
    """Rows 2-3 carry project metadata. Returns the next free row."""
    # Row 2
    ws.cell(row=2, column=5, value="מספר פרויקט: " + str(meta.get("project_number", ""))).font = TAHOMA_BOLD
    ws.cell(row=2, column=5).alignment = RIGHT_WRAP
    ws.cell(row=2, column=9, value="הלקוח: " + str(meta.get("client_name", ""))).font = TAHOMA_BOLD
    ws.cell(row=2, column=9).alignment = RIGHT_WRAP

    # Row 3
    ws.cell(row=3, column=5, value="המפיק: " + str(meta.get("producer_name", "Hemi Michaeli"))).font = TAHOMA_BOLD
    ws.cell(row=3, column=5).alignment = RIGHT_WRAP
    ws.cell(row=3, column=9, value="שם פרויקט: " + str(meta.get("project_name", ""))).font = TAHOMA_BOLD
    ws.cell(row=3, column=9).alignment = RIGHT_WRAP

    return 5  # Column headers go on row 5


def _write_column_headers(ws, row_idx: int) -> int:
    for col, header in enumerate(COLUMN_HEADERS, start=1):
        cell = ws.cell(row=row_idx, column=col, value=header)
        cell.font = TAHOMA_HEADER
        cell.fill = HEADER_FILL
        cell.alignment = CENTER_WRAP
        cell.border = _border()
    ws.row_dimensions[row_idx].height = 30
    return row_idx + 1


def _write_category_marker(ws, row_idx: int, category: str) -> int:
    """Only col 7 is filled; the marker row is visually lighter."""
    for col in range(1, 14):
        cell = ws.cell(row=row_idx, column=col)
        cell.fill = CATEGORY_MARKER_FILL
        cell.border = _border()
    mark = ws.cell(row=row_idx, column=7, value=category)
    mark.font = TAHOMA_BOLD
    mark.alignment = CENTER_WRAP
    return row_idx + 1


def _write_line_row(ws, row_idx: int, line: dict) -> int:
    """
    Write one line item row. Computed cells use formulas so the XLSX
    is interactive when Hemi opens it in Excel (totals update if he edits).
    """
    # C1 vendor
    ws.cell(row=row_idx, column=1, value=line.get("vendor", "")).font = TAHOMA_REGULAR
    # C2 invoice number
    ws.cell(row=row_idx, column=2, value=line.get("invoice_number", "")).font = TAHOMA_REGULAR
    # C3 actual spend
    c3 = ws.cell(row=row_idx, column=3, value=line.get("actual_spend", 0))
    c3.font = TAHOMA_REGULAR
    c3.number_format = "#,##0"
    # C4 payment terms
    ws.cell(row=row_idx, column=4, value=line.get("payment_terms", "")).font = TAHOMA_REGULAR
    # C5 unit cost (internal)
    c5 = ws.cell(row=row_idx, column=5, value=line.get("unit_cost", 0))
    c5.font = TAHOMA_REGULAR
    c5.number_format = "#,##0"
    # C6 total cost = C5 * C9
    c6 = ws.cell(row=row_idx, column=6, value=f"=E{row_idx}*I{row_idx}")
    c6.font = TAHOMA_REGULAR
    c6.number_format = "#,##0"
    # C7 category blank on line rows
    ws.cell(row=row_idx, column=7, value="")
    # C8 service description
    c8 = ws.cell(row=row_idx, column=8, value=line.get("service", ""))
    c8.font = TAHOMA_REGULAR
    c8.alignment = RIGHT_WRAP
    # C9 units
    c9 = ws.cell(row=row_idx, column=9, value=line.get("units", 1))
    c9.font = TAHOMA_REGULAR
    c9.alignment = CENTER_WRAP
    # C10 unit price (client-facing)
    c10 = ws.cell(row=row_idx, column=10, value=line.get("unit_price", 0))
    c10.font = TAHOMA_REGULAR
    c10.number_format = "#,##0"
    # C11 total charge = C9 * C10
    c11 = ws.cell(row=row_idx, column=11, value=f"=I{row_idx}*J{row_idx}")
    c11.font = TAHOMA_REGULAR
    c11.number_format = "#,##0"
    # C12 profitability = C11 - C6
    c12 = ws.cell(row=row_idx, column=12, value=f"=K{row_idx}-F{row_idx}")
    c12.font = TAHOMA_REGULAR
    c12.number_format = "#,##0"
    # C13 margin percent = C12 / C11 (guard div-zero)
    c13 = ws.cell(row=row_idx, column=13, value=f"=IF(K{row_idx}=0,0,L{row_idx}/K{row_idx})")
    c13.font = TAHOMA_REGULAR
    c13.number_format = "0%"
    # Borders
    for col in range(1, 14):
        ws.cell(row=row_idx, column=col).border = _border()
    return row_idx + 1


def _write_production_fee(ws, row_idx: int, first_line_row: int, last_line_row: int,
                          fee_rate: float) -> int:
    """
    Production fee row: col 2 says "אחוזים מלמעלה:" and col 3 has the markup-from-top
    fee rate; col 5 "אחוזים מלמטה:" and col 6 has the markdown-from-bottom rate;
    col 9 "דמי ארגון והפקה", col 10 the rate, col 11 the computed total fee.
    """
    ws.cell(row=row_idx, column=2, value="אחוזים מלמעלה:").font = TAHOMA_REGULAR
    ws.cell(row=row_idx, column=2).alignment = RIGHT_WRAP
    ws.cell(row=row_idx, column=3, value=fee_rate).number_format = "0%"
    ws.cell(row=row_idx, column=5, value="אחוזים מלמטה:").font = TAHOMA_REGULAR
    ws.cell(row=row_idx, column=5).alignment = RIGHT_WRAP
    ws.cell(row=row_idx, column=6, value=fee_rate).number_format = "0%"

    ws.cell(row=row_idx, column=9, value="דמי ארגון והפקה").font = TAHOMA_BOLD
    ws.cell(row=row_idx, column=9).alignment = RIGHT_WRAP
    ws.cell(row=row_idx, column=10, value=fee_rate).number_format = "0%"

    # The fee line total (C11) = SUM(C11 over line range) * fee_rate
    if last_line_row >= first_line_row:
        c11 = ws.cell(
            row=row_idx, column=11,
            value=f"=SUM(K{first_line_row}:K{last_line_row})*J{row_idx}"
        )
    else:
        c11 = ws.cell(row=row_idx, column=11, value=0)
    c11.font = TAHOMA_BOLD
    c11.number_format = "#,##0"

    for col in range(1, 14):
        ws.cell(row=row_idx, column=col).border = _border()
    return row_idx + 1


def _write_total_row(ws, row_idx: int, first_line_row: int, last_line_row: int,
                     fee_row: int, label: str = "סה\"כ") -> int:
    """Total = SUM(line-item totals) + production-fee total."""
    ws.cell(row=row_idx, column=7, value=label).font = TAHOMA_BOLD
    ws.cell(row=row_idx, column=7).alignment = RIGHT_WRAP
    if last_line_row >= first_line_row:
        total_cell = ws.cell(
            row=row_idx, column=11,
            value=f"=SUM(K{first_line_row}:K{last_line_row})+K{fee_row}"
        )
    else:
        total_cell = ws.cell(row=row_idx, column=11, value=f"=K{fee_row}")
    total_cell.font = TAHOMA_BOLD
    total_cell.number_format = "#,##0"
    total_cell.fill = TOTAL_FILL
    for col in range(1, 14):
        ws.cell(row=row_idx, column=col).border = _border()
    ws.cell(row=row_idx, column=7).fill = TOTAL_FILL
    return row_idx + 1


def _write_main_section(ws, main_lines: list, start_row: int, fee_rate: float) -> int:
    """
    Write the main budget section: for each of the 6 canonical categories
    in order, a marker row followed by its line items. Then the fee row
    and total row. Returns the next free row index.
    """
    # Group lines by category (preserving input order within each group)
    by_cat = {c: [] for c in CANONICAL_CATEGORIES}
    unknown = []
    for line in main_lines:
        c = line.get("category")
        if c in by_cat:
            by_cat[c].append(line)
        else:
            unknown.append(line)

    if unknown:
        # Non-canonical categories are not silently ignored; they get dumped
        # at the end of שונות with a warning comment.
        by_cat["שונות"].extend(unknown)
        print(
            f"WARNING: {len(unknown)} line(s) had non-canonical categories and were "
            f"rolled into שונות. Review: {[l.get('service') for l in unknown]}",
            file=sys.stderr,
        )

    row = start_row
    first_line_row = None
    last_line_row = None

    for cat in CANONICAL_CATEGORIES:
        # Category marker row always appears, even if category is empty
        row = _write_category_marker(ws, row, cat)
        for line in by_cat[cat]:
            if first_line_row is None:
                first_line_row = row
            row = _write_line_row(ws, row, line)
            last_line_row = row - 1

    # Edge case: if no lines at all
    if first_line_row is None:
        first_line_row = row
        last_line_row = row - 1

    # Production fee row
    fee_row = row
    row = _write_production_fee(ws, row, first_line_row, last_line_row, fee_rate)
    # Total row
    row = _write_total_row(ws, row, first_line_row, last_line_row, fee_row, label="סה\"כ")
    return row


def _write_options_section(ws, conditional_lines: list, start_row: int, fee_rate: float) -> int:
    """
    Options section: single כללי header, all conditional lines flat, then fee
    and total ("סה"כ חשבונית").
    """
    if not conditional_lines:
        return start_row

    # Gap
    row = start_row + 2

    # "אופציות" header row (col 7)
    header = ws.cell(row=row, column=7, value="אופציות")
    header.font = TAHOMA_HEADER
    header.fill = HEADER_FILL
    header.alignment = CENTER_WRAP
    for col in range(1, 14):
        ws.cell(row=row, column=col).border = _border()
    row += 1

    # Column headers (same as main)
    row = _write_column_headers(ws, row)

    # Single כללי category marker
    row = _write_category_marker(ws, row, "כללי")

    # Line rows
    first_line_row = row
    for line in conditional_lines:
        row = _write_line_row(ws, row, line)
    last_line_row = row - 1

    # Production fee row
    fee_row = row
    row = _write_production_fee(ws, row, first_line_row, last_line_row, fee_rate)
    # Total with options-specific label
    row = _write_total_row(ws, row, first_line_row, last_line_row, fee_row, label="סה\"כ חשבונית")
    return row


def build_budget_xlsx(budget_json: dict, output_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "טמפלט ריק"
    ws.sheet_view.rightToLeft = True  # RTL reading order

    _set_column_widths(ws)

    next_row = _write_header_band(ws, budget_json.get("project_meta", {}))
    next_row = _write_column_headers(ws, next_row)

    fee_rate = float(budget_json.get("production_fee_rate", 0.15))
    main_lines = budget_json.get("main_lines", [])
    conditional_lines = budget_json.get("conditional_lines", [])

    next_row = _write_main_section(ws, main_lines, next_row, fee_rate)
    _write_options_section(ws, conditional_lines, next_row, fee_rate)

    # Freeze the header band + column header row
    ws.freeze_panes = "A6"

    # Print setup: landscape, fit to page width
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    wb.save(output_path)


def main():
    if len(sys.argv) != 3:
        print("Usage: build_budget_xlsx.py <budget.json> <output.xlsx>", file=sys.stderr)
        sys.exit(2)
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    budget_json = json.loads(in_path.read_text(encoding="utf-8"))
    build_budget_xlsx(budget_json, out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
