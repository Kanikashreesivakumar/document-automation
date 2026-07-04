"""
Template builder — injects docxtpl {{ }} placeholders into the real uploaded
DOCX template ('invoice packing list.docx') and saves them as:
  backend/templates/invoice.docx
  backend/templates/packing_list.docx

This script is run ONCE (and again if the source template changes).
It preserves all original formatting, merged cells, fonts, and borders.
"""
import shutil
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

try:
    from services.docx_template_engine import ensure_letterhead_header
except ImportError:
    from docx_template_engine import ensure_letterhead_header


SOURCE = Path(__file__).parent.parent.parent / "invoice packing list.docx"
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def _clear_cell(cell):
    """Remove all text from a cell while keeping paragraph formatting."""
    for para in cell.paragraphs:
        for run in para.runs:
            run.text = ""
    # Keep first para, remove extras
    while len(cell.paragraphs) > 1:
        p = cell.paragraphs[-1]._element
        p.getparent().remove(p)


def _set_cell_text(cell, text: str, bold: bool = False, size_pt: int = None):
    """
    Set cell text. Clears existing content and writes fresh.
    Preserves the cell's existing paragraph alignment.
    """
    para = cell.paragraphs[0]
    # Clear existing runs
    for run in para.runs:
        run.text = ""
    if not para.runs:
        run = para.add_run(text)
    else:
        para.runs[0].text = text
        run = para.runs[0]
    run.bold = bold
    if size_pt:
        run.font.size = Pt(size_pt)
    # Remove excess paragraphs
    while len(cell.paragraphs) > 1:
        p_el = cell.paragraphs[-1]._element
        p_el.getparent().remove(p_el)


def build_invoice_template(doc: Document):
    """
    Inject docxtpl placeholders into Table 0 (Invoice) of the source doc.
    Row/column mapping derived from the exact template structure.
    """
    t = doc.tables[0]   # Invoice table

    # ── Row 1: Exporter (static) | Invoice No & Date | Exporter's Ref ─────────
    # [1,0] static exporter info — already correct in template, leave as-is
    # [1,3] Invoice No & Date
    _set_cell_text(t.cell(1, 3), "{{ invoice_no }}  DT: {{ invoice_date }}")
    # [1,5] Exporter's Ref (IEC number)
    _set_cell_text(t.cell(1, 5), "{{ exporter_iec }}")

    # ── Row 2: Buyer's Order No + Reference Proforma ──────────────────────────
    _set_cell_text(t.cell(2, 3),
        "Buyer's Order No & date :\n{{ buyer_order_no_date }}\n"
        "Reference Proforma Invoice No: {{ reference_proforma_invoice_no }}")

    # ── Row 3: Other Reference + Shipping Bill ────────────────────────────────
    _set_cell_text(t.cell(3, 3),
        "Other Reference\n"
        "SHIPPING BILL NO: {{ shipping_bill_no }}\tDATED: {{ shipping_bill_date }}")

    # ── Row 4-5: Consignee ────────────────────────────────────────────────────
    _set_cell_text(t.cell(4, 0), "Consignee\n{{ consignee_name }}", bold=False)

    # ── Row 5: Buyer ──────────────────────────────────────────────────────────
    _set_cell_text(t.cell(5, 3),
        "Buyer (if other than consignee)\n"
        "{{ buyer_name }}\n{{ buyer_address }}\n{{ buyer_country }}")

    # ── Row 6: Pre-Carriage | Place of Receipt | Country of Origin | Country of Final Dest ───
    _set_cell_text(t.cell(6, 0), "Pre- Carriage by\n{{ pre_carriage_by }}")
    _set_cell_text(t.cell(6, 2), "Place of receipt\n{{ place_of_receipt }}")
    _set_cell_text(t.cell(6, 3), "Country of Origin of goods\n{{ country_of_origin }}")
    _set_cell_text(t.cell(6, 5), "Country of final Destination\n{{ country_of_final_destination }}")

    # ── Row 7: Vessel/Flight No | Port of Loading ─────────────────────────────
    _set_cell_text(t.cell(7, 0), "Vessel/Flight No\n{{ vessel_flight_no }}")
    _set_cell_text(t.cell(7, 2), "Port of Loading\n{{ port_of_loading }}")

    # ── Row 8: Terms of Delivery ──────────────────────────────────────────────
    _set_cell_text(t.cell(8, 3), "Terms of Delivery and payment\n{{ terms_of_delivery }}")

    # ── Row 9: Port of Discharge | Final Destination ──────────────────────────
    _set_cell_text(t.cell(9, 0), "Port of discharge\n{{ port_of_discharge }}")
    _set_cell_text(t.cell(9, 2), "Final Destination\n{{ final_destination }}")

    # ── Row 11: Goods row ─────────────────────────────────────────────────────
    # [11,0] Brand Name + Container No
    _set_cell_text(t.cell(11, 0),
        "Brand Name\n{{ brand_name }}\nContainer No:\n{{ container_no }}\n{{ container_type }}")
    # [11,1] Number of cartons
    _set_cell_text(t.cell(11, 1), "{{ cartons }}\nCARTONS")
    # [11,2] Description of goods (compound)
    _set_cell_text(t.cell(11, 2), "{{ goods_description_line }}")
    # [11,4] Quantity
    _set_cell_text(t.cell(11, 4), "{{ total_eggs_fmt }}\nNos")
    # [11,5] Rate
    _set_cell_text(t.cell(11, 5), "USD\n{{ rate_per_egg_usd }}\nPER NUMBER")
    # [11,6] Amount
    _set_cell_text(t.cell(11, 6), "{{ amount_usd_display }}")

    # ── Row 12: Amount chargeable in words ────────────────────────────────────
    _set_cell_text(t.cell(12, 0),
        "Amount chargeable (in words)\nUS$: {{ amount_in_words }}")

    # ── Row 13: Weight summary ────────────────────────────────────────────────
    _set_cell_text(t.cell(13, 0), "{{ weight_summary_line }}")

    # ── Row 14: Declaration (static) | Signature ──────────────────────────────
    # Declaration text is static — leave as-is in the template
    _set_cell_text(t.cell(14, 4),
        "Signature & Date\n\n{{ exporter_name }}\n{{ invoice_date }}")


def build_packing_list_template(doc: Document):
    """
    Inject docxtpl placeholders into Table 1 (Packing List) of the source doc.
    """
    t = doc.tables[1]   # Packing List table

    # ── Row 0: PACKING LIST title (static header — leave as-is) ──────────────

    # ── Row 2: Exporter (static) | Invoice No & Date | Exporter's Ref ─────────
    _set_cell_text(t.cell(2, 3), "{{ invoice_no }}  DT: {{ invoice_date }}")
    _set_cell_text(t.cell(2, 5), "{{ exporter_iec }}")

    # ── Row 3: Buyer's Order No + Reference ───────────────────────────────────
    _set_cell_text(t.cell(3, 3),
        "Buyer's Order No & date :\n{{ buyer_order_no_date }}\n"
        "Reference Proforma Invoice No: {{ reference_proforma_invoice_no }}")

    # ── Row 4: Other Reference + Shipping Bill ────────────────────────────────
    _set_cell_text(t.cell(4, 3),
        "Other Reference\n"
        "SHIPPING BILL NO: {{ shipping_bill_no }}\tDATED: {{ shipping_bill_date }}")

    # ── Row 5-6: Consignee ────────────────────────────────────────────────────
    _set_cell_text(t.cell(5, 0), "Consignee\n{{ consignee_name }}")

    # ── Row 6: Buyer ──────────────────────────────────────────────────────────
    _set_cell_text(t.cell(6, 3),
        "Buyer (if other than consignee)\n"
        "{{ buyer_name }}\n{{ buyer_address }}\n{{ buyer_country }}")

    # ── Row 7: Pre-Carriage | Place of Receipt | Country of Origin | Country Final Dest ──
    _set_cell_text(t.cell(7, 0), "Pre- Carriage by\n{{ pre_carriage_by }}")
    _set_cell_text(t.cell(7, 2), "Place of receipt\n{{ place_of_receipt }}")
    _set_cell_text(t.cell(7, 3), "Country of Origin of goods\n{{ country_of_origin }}")
    _set_cell_text(t.cell(7, 5), "Country of final Destination\n{{ country_of_final_destination }}")

    # ── Row 8: Vessel | Port of Loading ───────────────────────────────────────
    _set_cell_text(t.cell(8, 0), "Vessel/Flight No\n{{ vessel_flight_no }}")
    _set_cell_text(t.cell(8, 2), "Port of Loading\n{{ port_of_loading }}")

    # ── Row 9: Terms of Delivery ──────────────────────────────────────────────
    _set_cell_text(t.cell(9, 3), "Terms of Delivery and payment\n{{ terms_of_delivery }}")

    # ── Row 10: Port of Discharge | Final Destination ─────────────────────────
    _set_cell_text(t.cell(10, 0), "Port of discharge\n{{ port_of_discharge }}")
    _set_cell_text(t.cell(10, 2), "Final Destination\n{{ final_destination }}")

    # ── Row 12: Goods row ─────────────────────────────────────────────────────
    _set_cell_text(t.cell(12, 0),
        "Brand Name\n{{ brand_name }}\nContainer No:\n{{ container_no }}")
    _set_cell_text(t.cell(12, 1), "{{ cartons }}\nCARTONS")
    _set_cell_text(t.cell(12, 2), "{{ goods_description_line }}")
    _set_cell_text(t.cell(12, 4), "{{ total_eggs_fmt }}\nNOS")
    _set_cell_text(t.cell(12, 5), "{{ packing_remarks }}")

    # ── Row 13-14: Weight summary ─────────────────────────────────────────────
    _set_cell_text(t.cell(13, 0), "Each carton — {{ eggs_per_carton }} Nos.")
    _set_cell_text(t.cell(14, 0), "{{ weight_summary_line }}")

    # ── Row 14: Signature ─────────────────────────────────────────────────────
    _set_cell_text(t.cell(14, 4),
        "Signature & Date\n\n{{ exporter_name }}\n{{ invoice_date }}")


def build_templates():
    """Entry point: build invoice.docx and packing_list.docx from the source template."""
    if not SOURCE.exists():
        print(f"[TemplateBuilder] ERROR: Source not found: {SOURCE}")
        return

    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    # ── Invoice ────────────────────────────────────────────────────────────────
    invoice_path = TEMPLATES_DIR / "invoice.docx"
    shutil.copy2(SOURCE, invoice_path)
    doc_inv = Document(str(invoice_path))
    build_invoice_template(doc_inv)
    ensure_letterhead_header(doc_inv, Path(__file__).parent.parent.parent / "frame.jpeg")
    doc_inv.save(str(invoice_path))
    print(f"[TemplateBuilder] Built: {invoice_path}")

    # ── Packing List ───────────────────────────────────────────────────────────
    pl_path = TEMPLATES_DIR / "packing_list.docx"
    shutil.copy2(SOURCE, pl_path)
    doc_pl = Document(str(pl_path))
    build_packing_list_template(doc_pl)
    ensure_letterhead_header(doc_pl, Path(__file__).parent.parent.parent / "frame.jpeg")
    doc_pl.save(str(pl_path))
    print(f"[TemplateBuilder] Built: {pl_path}")


if __name__ == "__main__":
    build_templates()
