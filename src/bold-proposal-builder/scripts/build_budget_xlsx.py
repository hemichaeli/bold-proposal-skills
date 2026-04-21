#!/usr/bin/env python3
"""
build_budget_xlsx.py

Builds the final budget.xlsx from the budget.json produced by stage 5 of the
bold-proposal-builder skill.

Usage:
    python3 build_budget_xlsx.py --input budget.json --output budget.xlsx

Requires: openpyxl
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: openpyxl is required. Install with: pip install openpyxl --break-system-packages", file=sys.stderr)
    sys.exit(1)


# Bold default brand colors. Overridden if budget.json has "brand_colors"
DEFAULT_PRIMARY = "0E0E0E"
DEFAULT_ACCENT = "C9A961"
DEFAULT_NEUTRAL = "F5F1EA"
DEFAULT_TEXT = "1A1A1A"


def load_budget(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def colors_from_budget(budget: dict) -> dict:
    bc = budget.get("brand_colors", {})
    return {
        "primary": bc.get("primary", DEFAULT_PRIMARY).lstrip("#"),
        "accent": bc.get("accent", DEFAULT_ACCENT).lstrip("#"),
        "neutral": bc.get("neutral", DEFAULT_NEUTRAL).lstrip("#"),
        "text": bc.get("text", DEFAULT_TEXT).lstrip("#"),
    }


def make_styles(colors: dict) -> dict:
    thin = Side(border_style="thin", color="BBBBBB")
    border_all = Border(left=thin, right=thin, top=thin, bottom=thin)

    header_font = Font(name="Arial", size=12, bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor=colors["primary"])

    category_font = Font(name="Arial", size=11, bold=True, color=colors["text"])
    category_fill = PatternFill("solid", fgColor=colors["neutral"])

    item_font = Font(name="Arial", size=10, color=colors["text"])

    total_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    total_fill = PatternFill("solid", fgColor=colors["accent"])

    subtotal_font = Font(name="Arial", size=10, bold=True, color=colors["text"])
    subtotal_fill = PatternFill("solid", fgColor="EEEEEE")

    note_font = Font(name="Arial", size=9, italic=True, color="666666")

    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    right = Alignment(horizontal="right", vertical="center", wrap_text=True)
    left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    return {
        "border": border_all,
        "header_font": header_font,
        "header_fill": header_fill,
        "category_font": category_font,
        "category_fill": category_fill,
        "item_font": item_font,
        "total_font": total_font,
        "total_fill": total_fill,
        "subtotal_font": subtotal_font,
        "subtotal_fill": subtotal_fill,
        "note_font": note_font,
        "center": center,
        "right": right,
        "left": left,
    }


def apply_rtl(ws):
    ws.sheet_view.rightToLeft = True


def set_column_widths(ws, widths: list):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def build_detail_sheet(wb, budget: dict, styles: dict) -> tuple:
    """
    Build the detailed non-conditional items sheet.
    Returns (sheet_name, subtotal_cell_reference) so the summary sheet can refer to it.
    """
    ws = wb.create_sheet("פירוט תקציב")
    apply_rtl(ws)

    # Column layout (A-H): #, Category, Item, Qty, Unit, Unit cost, Total, Notes
    headers = ["#", "קטגוריה", "פריט", "כמות", "יחידה", "מחיר ליח'", "סה\"כ", "הערות"]
    for col, h in enumerate(headers, start=1):
        c = ws.cell(row=1, column=col, value=h)
        c.font = styles["header_font"]
        c.fill = styles["header_fill"]
        c.alignment = styles["center"]
        c.border = styles["border"]
    ws.row_dimensions[1].height = 24

    set_column_widths(ws, [5, 22, 36, 8, 10, 14, 14, 40])

    current_row = 2
    item_num = 1
    category_subtotal_rows = []

    for cat in budget.get("categories", []):
        # Category header row
        cat_name = cat.get("name", "")
        cat_cell = ws.cell(row=current_row, column=2, value=cat_name)
        cat_cell.font = styles["category_font"]
        cat_cell.fill = styles["category_fill"]
        cat_cell.alignment = styles["right"]
        # Fill the whole row
        for col in range(1, 9):
            c = ws.cell(row=current_row, column=col)
            c.fill = styles["category_fill"]
            c.border = styles["border"]
        current_row += 1

        category_first_data_row = current_row
        any_non_conditional = False

        for item in cat.get("items", []):
            if item.get("conditional"):
                continue
            any_non_conditional = True

            ws.cell(row=current_row, column=1, value=item_num).alignment = styles["center"]
            ws.cell(row=current_row, column=3, value=item.get("name", "")).alignment = styles["right"]
            ws.cell(row=current_row, column=4, value=item.get("qty", 0)).alignment = styles["center"]
            ws.cell(row=current_row, column=5, value=item.get("unit", "")).alignment = styles["center"]

            unit_cost = item.get("unit_cost")
            unit_cell = ws.cell(row=current_row, column=6, value=unit_cost if unit_cost is not None else "להשלמה")
            unit_cell.alignment = styles["center"]
            if unit_cost is not None:
                unit_cell.number_format = '#,##0 "₪"'

            # Total formula: qty * unit_cost
            if unit_cost is not None:
                total_formula = f"=D{current_row}*F{current_row}"
                total_cell = ws.cell(row=current_row, column=7, value=total_formula)
                total_cell.number_format = '#,##0 "₪"'
            else:
                total_cell = ws.cell(row=current_row, column=7, value="")
            total_cell.alignment = styles["center"]

            ws.cell(row=current_row, column=8, value=item.get("notes", "")).alignment = styles["right"]

            for col in range(1, 9):
                c = ws.cell(row=current_row, column=col)
                c.font = styles["item_font"] if col != 8 else styles["note_font"]
                c.border = styles["border"]

            item_num += 1
            current_row += 1

        # Category subtotal row (only if the category had non-conditional items)
        if any_non_conditional:
            category_last_data_row = current_row - 1
            sub_label = ws.cell(row=current_row, column=6, value=f"סה\"כ {cat_name}")
            sub_label.font = styles["subtotal_font"]
            sub_label.fill = styles["subtotal_fill"]
            sub_label.alignment = styles["right"]

            sub_formula = f"=SUM(G{category_first_data_row}:G{category_last_data_row})"
            sub_cell = ws.cell(row=current_row, column=7, value=sub_formula)
            sub_cell.font = styles["subtotal_font"]
            sub_cell.fill = styles["subtotal_fill"]
            sub_cell.alignment = styles["center"]
            sub_cell.number_format = '#,##0 "₪"'

            for col in range(1, 9):
                c = ws.cell(row=current_row, column=col)
                c.fill = styles["subtotal_fill"]
                c.border = styles["border"]

            category_subtotal_rows.append(current_row)
            current_row += 1

        # Blank row between categories
        current_row += 1

    # Grand subtotal
    subtotal_row = current_row
    label_cell = ws.cell(row=subtotal_row, column=6, value="סה\"כ לפני גיבוי ורווח")
    label_cell.font = styles["total_font"]
    label_cell.fill = styles["total_fill"]
    label_cell.alignment = styles["right"]

    if category_subtotal_rows:
        sum_expr = "+".join([f"G{r}" for r in category_subtotal_rows])
        sub_formula = f"={sum_expr}"
    else:
        sub_formula = 0

    total_cell = ws.cell(row=subtotal_row, column=7, value=sub_formula)
    total_cell.font = styles["total_font"]
    total_cell.fill = styles["total_fill"]
    total_cell.alignment = styles["center"]
    total_cell.number_format = '#,##0 "₪"'

    for col in range(1, 9):
        c = ws.cell(row=subtotal_row, column=col)
        c.fill = styles["total_fill"]
        c.border = styles["border"]

    return (ws.title, f"G{subtotal_row}")


def build_conditional_sheet(wb, budget: dict, styles: dict) -> tuple:
    """
    Build the conditional items sheet.
    Returns (sheet_name, total_cell_reference) or (None, None) if no conditional items.
    """
    has_conditional = any(
        item.get("conditional")
        for cat in budget.get("categories", [])
        for item in cat.get("items", [])
    )
    if not has_conditional:
        return (None, None)

    ws = wb.create_sheet("שורות מותנות")
    apply_rtl(ws)

    headers = ["#", "קטגוריה", "פריט", "כמות", "יחידה", "מחיר ליח'", "סה\"כ", "תנאי הפעלה", "הערות"]
    for col, h in enumerate(headers, start=1):
        c = ws.cell(row=1, column=col, value=h)
        c.font = styles["header_font"]
        c.fill = styles["header_fill"]
        c.alignment = styles["center"]
        c.border = styles["border"]
    ws.row_dimensions[1].height = 24
    set_column_widths(ws, [5, 20, 32, 8, 10, 14, 14, 36, 30])

    current_row = 2
    item_num = 1
    data_rows = []

    for cat in budget.get("categories", []):
        for item in cat.get("items", []):
            if not item.get("conditional"):
                continue

            ws.cell(row=current_row, column=1, value=item_num).alignment = styles["center"]
            ws.cell(row=current_row, column=2, value=cat.get("name", "")).alignment = styles["right"]
            ws.cell(row=current_row, column=3, value=item.get("name", "")).alignment = styles["right"]
            ws.cell(row=current_row, column=4, value=item.get("qty", 0)).alignment = styles["center"]
            ws.cell(row=current_row, column=5, value=item.get("unit", "")).alignment = styles["center"]

            unit_cost = item.get("unit_cost")
            unit_cell = ws.cell(row=current_row, column=6, value=unit_cost if unit_cost is not None else "להשלמה")
            unit_cell.alignment = styles["center"]
            if unit_cost is not None:
                unit_cell.number_format = '#,##0 "₪"'

            if unit_cost is not None:
                total_formula = f"=D{current_row}*F{current_row}"
                total_cell = ws.cell(row=current_row, column=7, value=total_formula)
                total_cell.number_format = '#,##0 "₪"'
                data_rows.append(current_row)
            else:
                total_cell = ws.cell(row=current_row, column=7, value="")
            total_cell.alignment = styles["center"]

            ws.cell(row=current_row, column=8, value=item.get("trigger_condition", "")).alignment = styles["right"]
            ws.cell(row=current_row, column=9, value=item.get("notes", "")).alignment = styles["right"]

            for col in range(1, 10):
                c = ws.cell(row=current_row, column=col)
                c.font = styles["item_font"] if col not in (8, 9) else styles["note_font"]
                c.border = styles["border"]

            item_num += 1
            current_row += 1

    # Total of conditional items (if all were activated)
    total_row = current_row + 1
    label_cell = ws.cell(row=total_row, column=6, value="סה\"כ אם כל השורות יאושרו")
    label_cell.font = styles["total_font"]
    label_cell.fill = styles["total_fill"]
    label_cell.alignment = styles["right"]

    if data_rows:
        sum_expr = "+".join([f"G{r}" for r in data_rows])
        total_formula = f"={sum_expr}"
    else:
        total_formula = 0

    total_cell = ws.cell(row=total_row, column=7, value=total_formula)
    total_cell.font = styles["total_font"]
    total_cell.fill = styles["total_fill"]
    total_cell.alignment = styles["center"]
    total_cell.number_format = '#,##0 "₪"'

    for col in range(1, 10):
        c = ws.cell(row=total_row, column=col)
        c.fill = styles["total_fill"]
        c.border = styles["border"]

    return (ws.title, f"G{total_row}")


def build_summary_sheet(wb, budget: dict, styles: dict, detail_ref: tuple, cond_ref: tuple):
    ws = wb.create_sheet("סיכום", 0)  # First position
    apply_rtl(ws)

    meta = budget.get("meta", {})
    margin_pct = meta.get("margin_pct", 22) / 100.0
    contingency_pct = meta.get("contingency_pct", 8) / 100.0
    vat_applicable = meta.get("vat_applicable", True)
    vat_pct = meta.get("vat_pct", 18) / 100.0

    set_column_widths(ws, [30, 20, 30])

    # Title block
    title = ws.cell(row=1, column=1, value=f"הצעת מחיר | {meta.get('proposal_name', '')}")
    title.font = Font(name="Arial", size=16, bold=True, color=styles["header_fill"].fgColor.value)
    title.alignment = styles["right"]
    ws.row_dimensions[1].height = 28

    info_rows = [
        ("לקוח", meta.get("client", "")),
        ("תאריך", meta.get("date", "")),
        ("מספר מוזמנים", meta.get("guest_count", "")),
        ("מטבע", meta.get("currency", "ILS")),
        ("תוקף עד", meta.get("valid_until", "")),
    ]

    r = 3
    for label, value in info_rows:
        lab = ws.cell(row=r, column=1, value=label)
        lab.font = styles["category_font"]
        lab.alignment = styles["right"]
        val = ws.cell(row=r, column=2, value=value)
        val.font = styles["item_font"]
        val.alignment = styles["right"]
        r += 1

    # Summary calculations
    r += 2
    detail_sheet, detail_cell = detail_ref
    subtotal_ref = f"'{detail_sheet}'!{detail_cell}"

    # Subtotal
    sub_label = ws.cell(row=r, column=1, value="תת-סכום (עלויות ישירות)")
    sub_label.font = styles["category_font"]
    sub_label.alignment = styles["right"]
    sub_val = ws.cell(row=r, column=2, value=f"={subtotal_ref}")
    sub_val.font = styles["item_font"]
    sub_val.number_format = '#,##0 "₪"'
    sub_val.alignment = styles["right"]
    subtotal_row_num = r
    r += 1

    # Contingency
    cont_label = ws.cell(row=r, column=1, value=f"גיבוי ({int(contingency_pct*100)}%)")
    cont_label.font = styles["category_font"]
    cont_label.alignment = styles["right"]
    cont_val = ws.cell(row=r, column=2, value=f"=B{subtotal_row_num}*{contingency_pct}")
    cont_val.font = styles["item_font"]
    cont_val.number_format = '#,##0 "₪"'
    cont_val.alignment = styles["right"]
    contingency_row_num = r
    r += 1

    # Margin
    marg_label = ws.cell(row=r, column=1, value=f"רווח הפקה ({int(margin_pct*100)}%)")
    marg_label.font = styles["category_font"]
    marg_label.alignment = styles["right"]
    marg_val = ws.cell(row=r, column=2, value=f"=(B{subtotal_row_num}+B{contingency_row_num})*{margin_pct}")
    marg_val.font = styles["item_font"]
    marg_val.number_format = '#,##0 "₪"'
    marg_val.alignment = styles["right"]
    margin_row_num = r
    r += 1

    # Total pre-VAT
    tot_label = ws.cell(row=r, column=1, value="סה\"כ לפני מע\"מ")
    tot_label.font = styles["total_font"]
    tot_label.fill = styles["total_fill"]
    tot_label.alignment = styles["right"]
    tot_val = ws.cell(row=r, column=2, value=f"=B{subtotal_row_num}+B{contingency_row_num}+B{margin_row_num}")
    tot_val.font = styles["total_font"]
    tot_val.fill = styles["total_fill"]
    tot_val.number_format = '#,##0 "₪"'
    tot_val.alignment = styles["right"]
    pre_vat_row_num = r
    r += 1

    if vat_applicable:
        vat_label = ws.cell(row=r, column=1, value=f"מע\"מ ({int(vat_pct*100)}%)")
        vat_label.font = styles["category_font"]
        vat_label.alignment = styles["right"]
        vat_val = ws.cell(row=r, column=2, value=f"=B{pre_vat_row_num}*{vat_pct}")
        vat_val.font = styles["item_font"]
        vat_val.number_format = '#,##0 "₪"'
        vat_val.alignment = styles["right"]
        vat_row_num = r
        r += 1

        final_label = ws.cell(row=r, column=1, value="סה\"כ כולל מע\"מ")
        final_label.font = styles["total_font"]
        final_label.fill = styles["total_fill"]
        final_label.alignment = styles["right"]
        final_val = ws.cell(row=r, column=2, value=f"=B{pre_vat_row_num}+B{vat_row_num}")
        final_val.font = styles["total_font"]
        final_val.fill = styles["total_fill"]
        final_val.number_format = '#,##0 "₪"'
        final_val.alignment = styles["right"]
        r += 1

    # Conditional total reference
    if cond_ref and cond_ref[0]:
        r += 1
        cond_sheet, cond_cell = cond_ref
        cond_label = ws.cell(row=r, column=1, value="שורות מותנות (אם יאושרו)")
        cond_label.font = styles["category_font"]
        cond_label.alignment = styles["right"]
        cond_val = ws.cell(row=r, column=2, value=f"='{cond_sheet}'!{cond_cell}")
        cond_val.font = styles["item_font"]
        cond_val.number_format = '#,##0 "₪"'
        cond_val.alignment = styles["right"]
        note = ws.cell(row=r, column=3, value="(לא נכלל בסה\"כ למעלה)")
        note.font = styles["note_font"]
        note.alignment = styles["right"]

    # Footer note
    r += 3
    footer = ws.cell(row=r, column=1, value="הצעה זו תקפה עד התאריך המצוין למעלה. שורות מותנות יופעלו רק בהסכמת הלקוח.")
    footer.font = styles["note_font"]
    footer.alignment = styles["right"]
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)


def main():
    parser = argparse.ArgumentParser(description="Build budget.xlsx from budget.json")
    parser.add_argument("--input", required=True, help="Path to budget.json")
    parser.add_argument("--output", required=True, help="Path to write budget.xlsx")
    args = parser.parse_args()

    budget = load_budget(Path(args.input))
    colors = colors_from_budget(budget)
    styles = make_styles(colors)

    wb = Workbook()
    # Delete the default sheet (we'll create our own, summary first)
    default = wb.active
    wb.remove(default)

    # Build sheets (summary is inserted at position 0 later)
    detail_ref = build_detail_sheet(wb, budget, styles)
    cond_ref = build_conditional_sheet(wb, budget, styles)
    build_summary_sheet(wb, budget, styles, detail_ref, cond_ref)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"✓ Wrote {out}")


if __name__ == "__main__":
    main()
