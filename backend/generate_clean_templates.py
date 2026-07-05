import os
import sys
import docx
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Add backend to path to import mapping
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mapping import _build_base_context

# All valid backend mapping keys
VALID_KEYS = set(_build_base_context({}).keys())

def set_cell_border(cell, **kwargs):
    """
    Set cell's border
    Usage: set_cell_border(cell, top={"sz": 12, "val": "single", "color": "#000000"}, bottom=...)
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))

def make_table_borders_invisible(table):
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(
                cell,
                top={"val": "nil"},
                bottom={"val": "nil"},
                left={"val": "nil"},
                right={"val": "nil"},
                insideH={"val": "nil"},
                insideV={"val": "nil"}
            )

def add_header(doc, header_img_path):
    section = doc.sections[0]
    section.header_distance = Cm(0)
    section.different_first_page_header_footer = True
    header = section.first_page_header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    if os.path.exists(header_img_path):
        run = p.add_run()
        run.add_picture(header_img_path, width=Inches(7.0))
    else:
        p.add_run("COMPANY LOGO / HEADER NOT FOUND").bold = True

def add_spacer(doc, pt=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(pt)
    run = p.add_run()
    run.font.size = Pt(2)

def set_cell_padding(cell, top=1, bottom=1, start=3, end=3):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin, val in [('top', int(top*20)), ('bottom', int(bottom*20)), ('left', int(start*20)), ('right', int(end*20))]:
        node = OxmlElement(f'w:{margin}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def apply_style(run, bold=False, size=10):
    run.font.name = 'Arial'
    run.font.size = Pt(size)
    run.bold = bold

def add_kv_pair(cell, key, value, size=9, line_spacing=1.0):
    p = cell.paragraphs[0]
    if p.text:
        p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = line_spacing
    run_key = p.add_run(f"{key}: ")
    apply_style(run_key, bold=True, size=size)
    run_val = p.add_run(value)
    apply_style(run_val, size=size)

def add_text(cell, text, bold=False, size=9, align=None, line_spacing=1.0):
    p = cell.paragraphs[0]
    if p.text:
        p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = line_spacing
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    apply_style(run, bold=bold, size=size)

def extract_placeholders_from_doc(doc):
    import re
    placeholders = set()
    pattern = re.compile(r'\{\{\s*(\w+)\s*\}\}')
    for p in doc.paragraphs:
        for match in pattern.finditer(p.text):
            placeholders.add(match.group(1))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for match in pattern.finditer(p.text):
                        placeholders.add(match.group(1))
    return placeholders

def add_professional_footer(doc):
    doc.add_paragraph()
    t9 = doc.add_table(rows=1, cols=2)
    make_table_borders_invisible(t9)
    c_decl = t9.cell(0, 0)
    add_text(c_decl, "Declaration:", bold=True, size=9)
    add_text(c_decl,
        "We hereby certify that the goods described in this invoice are of Indian Origin "
        "and that the particulars given in this invoice are true and correct.",
        size=8)

    c_sign = t9.cell(0, 1)
    add_text(c_sign, "For RASI FOODS", bold=True, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_text(c_sign, "\n\n", size=9)
    add_text(c_sign, "Authorised Signatory & Company Seal", size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_text(c_sign, "{{ exporter_name }}", size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_text(c_sign, "{{ exporter_address }}", size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_text(c_sign, "Email: {{ exporter_email }}", size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_text(c_sign, "GSTIN: {{ exporter_gstin }}", size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_text(c_sign, "PAN: {{ exporter_pan }}", size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)

def create_invoice_base(doc_path, title, is_proforma=False):
    doc = docx.Document()
    
    # Setup sections for A4
    sections = doc.sections
    for section in sections:
        section.page_height = Cm(29.7)
        section.page_width = Cm(21.0)
        section.left_margin = Cm(0.8)
        section.right_margin = Cm(0.8)
        section.top_margin = Cm(0.2)
        section.bottom_margin = Cm(0.25)

    # Header
    add_header(doc, r'd:\Form Automation\backend\templates\header_img.jpeg')
    add_spacer(doc, pt=4)
    
    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(title)
    apply_style(run, bold=True, size=11)
    
    add_spacer(doc, pt=4)

    # Invisible layout table 1: Invoice info (top right)
    table_info = doc.add_table(rows=1, cols=2)
    table_info.autofit = False
    table_info.columns[0].width = Inches(3.5)
    table_info.columns[1].width = Inches(4.0)
    make_table_borders_invisible(table_info)
    
    cell_left = table_info.cell(0, 0)
    cell_right = table_info.cell(0, 1)
    
    # Exporter Details on left
    add_text(cell_left, "Exporter:", bold=True, size=10)
    add_text(cell_left, "{{ exporter_name }}", bold=True)
    add_text(cell_left, "{{ exporter_address }}")
    add_kv_pair(cell_left, "GSTIN", "{{ exporter_gstin }}")
    add_kv_pair(cell_left, "PAN", "{{ exporter_pan }}")
    add_kv_pair(cell_left, "IEC", "{{ exporter_iec }}")

    # Invoice info on right
    if is_proforma:
        add_kv_pair(cell_right, "Proforma Invoice No", "{{ proforma_invoice_no }}")
        add_kv_pair(cell_right, "Date", "{{ invoice_date }}")
    else:
        add_kv_pair(cell_right, "Invoice No", "{{ invoice_no }}")
        add_kv_pair(cell_right, "Invoice Date", "{{ invoice_date }}")
    
    add_kv_pair(cell_right, "Exporter's Ref", "{{ exporter_reference }}")
    add_kv_pair(cell_right, "Other Reference", "{{ other_reference }}")
    add_kv_pair(cell_right, "Buyer's Order No & Date", "{{ buyer_order_no_date }}")
    add_kv_pair(cell_right, "Reference Proforma Invoice No", "{{ reference_proforma_invoice_no }}")
    if not is_proforma:
        add_kv_pair(cell_right, "Shipping Bill No", "{{ shipping_bill_no }}")
        add_kv_pair(cell_right, "Shipping Bill Date", "{{ shipping_bill_date }}")

    add_spacer(doc, pt=6)

    # Invisible layout table 2: Consignee & Buyer
    table_parties = doc.add_table(rows=1, cols=2)
    table_parties.autofit = False
    table_parties.columns[0].width = Inches(3.75)
    table_parties.columns[1].width = Inches(3.75)
    make_table_borders_invisible(table_parties)
    
    c_consignee = table_parties.cell(0, 0)
    c_buyer = table_parties.cell(0, 1)
    
    add_text(c_consignee, "Consignee:", bold=True, size=10)
    add_text(c_consignee, "{{ consignee_name }}", bold=True)
    add_text(c_consignee, "{{ consignee_address }}")
    
    add_text(c_buyer, "Buyer (if different):", bold=True, size=10)
    add_text(c_buyer, "{{ buyer_name }}", bold=True)
    add_text(c_buyer, "{{ buyer_address }}")

    add_spacer(doc, pt=6)

    # Shipment Details Table (Visible)
    table_shipment = doc.add_table(rows=3, cols=4)
    table_shipment.style = 'Table Grid'
    for row in table_shipment.rows:
        for cell in row.cells:
            set_cell_padding(cell, top=1, bottom=1, start=3, end=3)
            
    s_cells = table_shipment.rows[0].cells
    add_kv_pair(s_cells[0], "Pre-Carriage By", "{{ pre_carriage_by }}")
    add_kv_pair(s_cells[1], "Place of Receipt", "{{ place_of_receipt }}")
    add_kv_pair(s_cells[2], "Country of Origin", "{{ country_of_origin }}")
    add_kv_pair(s_cells[3], "Country of Final Dest.", "{{ country_of_destination }}")
    
    s_cells2 = table_shipment.rows[1].cells
    add_kv_pair(s_cells2[0], "Vessel / Flight", "{{ vessel_flight_no }}")
    add_kv_pair(s_cells2[1], "Port of Loading", "{{ port_of_loading }}")
    add_kv_pair(s_cells2[2], "Port of Discharge", "{{ port_of_discharge }}")
    add_kv_pair(s_cells2[3], "Final Destination", "{{ final_destination }}")
    
    # Merge row 3
    s_cells3 = table_shipment.rows[2].cells
    s_cells3[0].merge(s_cells3[3])
    add_kv_pair(s_cells3[0], "Terms of Delivery and Payment", "{{ terms_of_delivery }}")

    add_spacer(doc, pt=6)

    # Description of Goods Table (Visible)
    table_goods = doc.add_table(rows=2, cols=6)
    table_goods.style = 'Table Grid'
    table_goods.autofit = False
    
    widths = [Inches(1.05), Inches(0.9), Inches(3.25), Inches(0.75), Inches(0.75), Inches(0.9)]
    for row in table_goods.rows:
        for idx, width in enumerate(widths):
            cell = row.cells[idx]
            cell.width = width
            set_cell_padding(cell, top=2, bottom=2, start=3, end=3)
            
    headers = ["Marks & Nos / Container Nos", "No. & Kind of Packages", "Description of Goods", "Quantity", "Rate in USD per Number", "Amount in USD"]
    for i, h in enumerate(headers):
        add_text(table_goods.cell(0, i), h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        
    add_text(table_goods.cell(1, 0), "{{ container_no }}\n{{ seal_no }}")
    add_text(table_goods.cell(1, 1), "{{ no_and_kind_of_packages }}\n{{ container_type }}")
    add_text(table_goods.cell(1, 2), "{{ description_of_goods }}")
    add_text(table_goods.cell(1, 3), "{{ quantity_of_goods }}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(table_goods.cell(1, 4), "${{ rate_per_egg_usd }}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(table_goods.cell(1, 5), "{{ amount_usd }}", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_spacer(doc, pt=6)

    # Totals
    table_totals = doc.add_table(rows=1, cols=2)
    make_table_borders_invisible(table_totals)
    t_cells = table_totals.rows[0].cells
    add_kv_pair(t_cells[0], "Amount Chargeable (in words)", "{{ amount_in_words }}")
    
    add_kv_pair(t_cells[1], "Total Net Weight", "{{ net_weight }} KGS")
    add_kv_pair(t_cells[1], "Total Gross Weight", "{{ gross_weight }} KGS")
    
    add_spacer(doc, pt=6)

    add_professional_footer(doc)

    # Save and verify
    placeholders = extract_placeholders_from_doc(doc)
    missing = placeholders - VALID_KEYS
    if missing:
        print(f"ERROR in {title}: Missing backend mappings for placeholders: {missing}")
        sys.exit(1)
        
    doc.save(doc_path)
    print(f"Generated {doc_path}")

def create_packing_list(doc_path):
    doc = docx.Document()
    
    sections = doc.sections
    for section in sections:
        section.page_height = Cm(29.7)
        section.page_width = Cm(21.0)
        section.left_margin = Cm(0.8)
        section.right_margin = Cm(0.8)
        section.top_margin = Cm(0.25)
        section.bottom_margin = Cm(0.25)

    add_header(doc, r'd:\Form Automation\backend\templates\header_img.jpeg')
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("PACKING LIST")
    apply_style(run, bold=True, size=11)

    # Info
    table_info = doc.add_table(rows=1, cols=2)
    table_info.columns[0].width = Inches(3.75)
    table_info.columns[1].width = Inches(3.75)
    make_table_borders_invisible(table_info)
    
    add_text(table_info.cell(0, 0), "Exporter:", bold=True)
    add_text(table_info.cell(0, 0), "{{ exporter_name }}\n{{ exporter_address }}")
    
    add_kv_pair(table_info.cell(0, 1), "Invoice No", "{{ invoice_no }}")
    add_kv_pair(table_info.cell(0, 1), "Invoice Date", "{{ invoice_date }}")
    add_kv_pair(table_info.cell(0, 1), "Buyer's Order No & Date", "{{ buyer_order_no_date }}")

    doc.add_paragraph()

    table_parties = doc.add_table(rows=1, cols=2)
    make_table_borders_invisible(table_parties)
    add_text(table_parties.cell(0, 0), "Consignee:", bold=True)
    add_text(table_parties.cell(0, 0), "{{ consignee_name }}\n{{ consignee_address }}")
    
    add_text(table_parties.cell(0, 1), "Buyer (if different):", bold=True)
    add_text(table_parties.cell(0, 1), "{{ buyer_name }}\n{{ buyer_address }}")

    doc.add_paragraph()

    # Shipment details
    table_ship = doc.add_table(rows=2, cols=3)
    table_ship.style = 'Table Grid'
    add_kv_pair(table_ship.cell(0, 0), "Pre-Carriage By", "{{ pre_carriage_by }}")
    add_kv_pair(table_ship.cell(0, 1), "Vessel / Flight", "{{ vessel_flight_no }}")
    add_kv_pair(table_ship.cell(0, 2), "Port of Loading", "{{ port_of_loading }}")
    
    add_kv_pair(table_ship.cell(1, 0), "Port of Discharge", "{{ port_of_discharge }}")
    add_kv_pair(table_ship.cell(1, 1), "Final Destination", "{{ final_destination }}")
    add_kv_pair(table_ship.cell(1, 2), "Container No", "{{ container_no }}")
    
    doc.add_paragraph()

    # Packing Table
    table_pack = doc.add_table(rows=2, cols=5)
    table_pack.style = 'Table Grid'
    table_pack.autofit = False
    table_pack.columns[0].width = Inches(0.8)
    table_pack.columns[1].width = Inches(0.8)
    table_pack.columns[2].width = Inches(4.3)
    table_pack.columns[3].width = Inches(0.6)
    table_pack.columns[4].width = Inches(1.1)
    headers = ["Marks & Nos / Container Nos", "No. & Kind of Packages", "Description of Goods", "Quantity", "Remarks"]
    for i, h in enumerate(headers):
        add_text(table_pack.cell(0, i), h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        
    add_text(table_pack.cell(1, 0), "{{ container_no }}\n{{ seal_no }}")
    add_text(table_pack.cell(1, 1), "{{ no_and_kind_of_packages }}\n{{ container_type }}")
    add_text(table_pack.cell(1, 2), "{{ description_of_goods }}")
    add_text(table_pack.cell(1, 3), "{{ quantity_of_goods }}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(table_pack.cell(1, 4), "Net wt/carton:\n{{ net_weight }} KGS (Total)\n\nGross wt/carton:\n{{ gross_weight_per_egg }} KGS")

    add_professional_footer(doc)
    
    # Save and verify
    placeholders = extract_placeholders_from_doc(doc)
    missing = placeholders - VALID_KEYS
    if missing:
        print(f"ERROR in Packing List: Missing backend mappings for placeholders: {missing}")
        sys.exit(1)
        
    doc.save(doc_path)
    print(f"Generated {doc_path}")

def create_proforma_invoice(doc_path):
    """
    Build the expanded clean Proforma Invoice template.
    Sections:
      - Header (company logo)
      - Title + Proforma reference info
      - Buyer / Consignee / Notify Party
      - Shipment Details
      - Goods Table (Marks, Packages, Description, Qty, Rate, Amount)
      - Totals & Amount in Words
      - Bank Details (Company constants + Intermediate Bank)
      - Payment Section
      - Terms & Conditions
      - Declaration
      - Signatures & Footer
    """
    doc = docx.Document()

    for section in doc.sections:
        section.page_height = Cm(29.7)
        section.page_width  = Cm(21.0)
        section.left_margin  = Cm(0.8)
        section.right_margin = Cm(0.8)
        section.top_margin   = Cm(0.0)
        section.bottom_margin = Cm(0.0)

    add_header(doc, r'd:\Form Automation\backend\templates\header_img.jpeg')

    # Hook into the default initial paragraph to avoid adding an extra blank one at the top
    p = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("PROFORMA INVOICE")
    apply_style(run, bold=True, size=11)

    # ── Section 1: Exporter (left) + Proforma Reference (right) ───────────────
    t1 = doc.add_table(rows=1, cols=2)
    t1.autofit = False
    t1.columns[0].width = Inches(3.5)
    t1.columns[1].width = Inches(4.0)
    make_table_borders_invisible(t1)

    c_exp = t1.cell(0, 0)
    add_text(c_exp, "Exporter:", bold=True, size=10)
    add_text(c_exp, "{{ exporter_name }}", bold=True, line_spacing=1.15)
    add_text(c_exp, "{{ exporter_address }}", line_spacing=1.15)
    add_kv_pair(c_exp, "GSTIN",  "{{ exporter_gstin }}", line_spacing=1.15)
    add_kv_pair(c_exp, "PAN",    "{{ exporter_pan }}", line_spacing=1.15)
    add_kv_pair(c_exp, "IEC",    "{{ exporter_iec }}", line_spacing=1.15)
    add_kv_pair(c_exp, "Email",  "{{ exporter_email }}", line_spacing=1.15)

    c_ref = t1.cell(0, 1)
    add_kv_pair(c_ref, "Proforma Invoice No",        "{{ proforma_invoice_no }}")
    add_kv_pair(c_ref, "Date",                        "{{ invoice_date }}")
    add_kv_pair(c_ref, "PO Number",                   "{{ po_number }}")
    add_kv_pair(c_ref, "PO Date",                     "{{ po_date }}")
    add_kv_pair(c_ref, "Exporter's Ref",              "{{ exporter_reference }}")
    add_kv_pair(c_ref, "Other Reference",             "{{ other_reference }}")
    add_kv_pair(c_ref, "Buyer's Order No & Date",     "{{ buyer_order_no_date }}")

    # ── Section 2: Consignee, Buyer & Notify Party (Combined) ─────────────────
    t2 = doc.add_table(rows=1, cols=3)
    t2.style = 'Table Grid'
    t2.autofit = False
    
    # 3 equal columns: ~2.53 inches each
    t2.columns[0].width = Inches(2.53)
    t2.columns[1].width = Inches(2.53)
    t2.columns[2].width = Inches(2.54)
    
    for cell in t2.rows[0].cells:
        set_cell_padding(cell, top=1, bottom=1, start=3, end=3)

    c_con = t2.cell(0, 0)
    add_text(c_con, "Consignee:", bold=True, size=9)
    add_text(c_con, "{{ consignee_name }}", bold=True, size=9, line_spacing=1.15)
    add_text(c_con, "{{ consignee_address }}", size=8, line_spacing=1.15)
    add_kv_pair(c_con, "TRN", "{{ consignee_trn }}", line_spacing=1.15)

    c_buy = t2.cell(0, 1)
    add_text(c_buy, "Buyer (if other than Consignee):", bold=True, size=9)
    add_text(c_buy, "{{ buyer_name }}", bold=True, size=9, line_spacing=1.15)
    add_text(c_buy, "{{ buyer_address }}", size=8, line_spacing=1.15)
    add_kv_pair(c_buy, "TRN",     "{{ buyer_trn }}", line_spacing=1.15)
    add_kv_pair(c_buy, "Country", "{{ buyer_country }}", line_spacing=1.15)

    c_np = t2.cell(0, 2)
    add_text(c_np, "Notify Party:", bold=True, size=9)
    add_text(c_np, "{{ notify_party }}", bold=True, size=9, line_spacing=1.15)
    add_text(c_np, "{{ notify_party_address }}", size=8, line_spacing=1.15)

    # ── Section 3: Shipment Details ───────────────────────────────────────────
    t4 = doc.add_table(rows=3, cols=4)
    t4.style = 'Table Grid'
    for row in t4.rows:
        for cell in row.cells:
            set_cell_padding(cell, top=1, bottom=1, start=3, end=3)

    r0 = t4.rows[0].cells
    add_kv_pair(r0[0], "Pre-Carriage By",    "{{ pre_carriage_by }}")
    add_kv_pair(r0[1], "Place of Receipt",   "{{ place_of_receipt }}")
    add_kv_pair(r0[2], "Country of Origin",  "{{ country_of_origin }}")
    add_kv_pair(r0[3], "Country of Dest.",   "{{ country_of_destination }}")

    r1 = t4.rows[1].cells
    add_kv_pair(r1[0], "Vessel / Flight",    "{{ vessel_flight_no }}")
    add_kv_pair(r1[1], "Port of Loading",    "{{ port_of_loading }}")
    add_kv_pair(r1[2], "Port of Discharge",  "{{ port_of_discharge }}")
    add_kv_pair(r1[3], "Final Destination",  "{{ final_destination }}")

    r2 = t4.rows[2].cells
    r2[0].merge(r2[3])
    add_kv_pair(r2[0], "Terms of Delivery & Payment", "{{ terms_of_delivery }}")

    # ── Section 4: Goods Table ────────────────────────────────────────────────
    # Columns: Marks & Numbers | No & Kind of Packages | Description | Qty | Rate | Amount
    t5 = doc.add_table(rows=2, cols=6)
    t5.style = 'Table Grid'
    t5.autofit = False
    
    widths = [Inches(1.05), Inches(0.9), Inches(3.25), Inches(0.75), Inches(0.75), Inches(0.9)]
    for row in t5.rows:
        for idx, width in enumerate(widths):
            cell = row.cells[idx]
            cell.width = width
            set_cell_padding(cell, top=2, bottom=2, start=3, end=3)
            

    hdrs = ["Marks & Nos / Container Nos", "No. & Kind of Packages", "Description of Goods",
            "Quantity", "Rate in USD per Number", "Amount in USD"]
    for i, h in enumerate(hdrs):
        add_text(t5.cell(0, i), h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_text(t5.cell(1, 0), "{{ container_no }}\n{{ seal_no }}")
    add_text(t5.cell(1, 1), "{{ no_and_kind_of_packages }}\n{{ container_type }}")
    add_text(t5.cell(1, 2), "{{ description_of_goods }}", line_spacing=1.15)
    add_text(t5.cell(1, 3), "{{ quantity_of_goods }}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(t5.cell(1, 4), "${{ rate_per_egg_usd }}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(t5.cell(1, 5), "{{ amount_usd }}", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_spacer(doc, pt=2)

    # ── Section 5: Totals row ─────────────────────────────────────────────────
    t6 = doc.add_table(rows=1, cols=2)
    make_table_borders_invisible(t6)
    tc0 = t6.rows[0].cells[0]
    tc1 = t6.rows[0].cells[1]
    add_kv_pair(tc0, "Amount Chargeable (in words)", "{{ amount_in_words }}")
    add_kv_pair(tc1, "Total Net Weight",   "{{ net_weight }} KGS")
    add_kv_pair(tc1, "Total Gross Weight", "{{ gross_weight }} KGS")
    add_kv_pair(tc1, "Total Payment",      "{{ total_payment }}")

    # ── Section 6: Payment Terms ──────────────────────────────────────────────
    t7 = doc.add_table(rows=1, cols=2)
    make_table_borders_invisible(t7)
    tp0 = t7.rows[0].cells[0]
    tp1 = t7.rows[0].cells[1]
    add_kv_pair(tp0, "Payment Terms", "{{ payment_terms }}")
    add_kv_pair(tp1, "Expiry Date",   "{{ expiry_date }}")

    # ── Section 7: Bank Details ───────────────────────────────────────────────
    t8 = doc.add_table(rows=1, cols=2)
    t8.style = 'Table Grid'

    c_co_bank = t8.cell(0, 0)
    add_text(c_co_bank, "Company Bank Details", bold=True, size=10)
    add_kv_pair(c_co_bank, "Account Name",   "{{ company_account_name }}", line_spacing=1.15)
    add_kv_pair(c_co_bank, "Account Number", "{{ company_account_number }}", line_spacing=1.15)
    add_kv_pair(c_co_bank, "Bank Name",      "{{ company_bank_name }}", line_spacing=1.15)
    add_kv_pair(c_co_bank, "Branch",         "{{ company_branch }}", line_spacing=1.15)
    add_kv_pair(c_co_bank, "SWIFT Code",     "{{ company_swift }}", line_spacing=1.15)

    c_int_bank = t8.cell(0, 1)
    add_text(c_int_bank, "Intermediate / Correspondent Bank", bold=True, size=10)
    add_kv_pair(c_int_bank, "Bank Name",        "{{ intermediate_bank_name }}", line_spacing=1.15)
    add_kv_pair(c_int_bank, "Account Number",   "{{ intermediate_bank_account_number }}", line_spacing=1.15)
    add_kv_pair(c_int_bank, "SWIFT",            "{{ intermediate_bank_swift }}", line_spacing=1.15)
    add_kv_pair(c_int_bank, "Routing Number",   "{{ intermediate_bank_routing_number }}", line_spacing=1.15)
    add_kv_pair(c_int_bank, "Correspondent",    "{{ correspondent_bank }}", line_spacing=1.15)

    add_spacer(doc, pt=2)

    # ── Section 9: Horizontal Terms, Declaration & Company ────────────────────
    t9 = doc.add_table(rows=1, cols=3)
    t9.style = 'Table Grid'
    t9.autofit = False
    t9.columns[0].width = Inches(2.53)
    t9.columns[1].width = Inches(2.53)
    t9.columns[2].width = Inches(2.54)
    
    # Left Column: Terms
    c_terms = t9.cell(0, 0)
    add_text(c_terms, "Terms & Conditions:", bold=True, size=9)
    terms_text = (
        "1. All goods are shipped at buyer's risk.\n"
        "2. Any discrepancy must be reported within 7 days of receipt of goods.\n"
        "3. Subject to Namakkal Jurisdiction only.\n"
        "4. This is a computer-generated Proforma Invoice."
    )
    add_text(c_terms, terms_text, size=8)
    
    # Middle Column: Declaration
    c_decl = t9.cell(0, 1)
    add_text(c_decl, "Declaration:", bold=True, size=9)
    add_text(c_decl, 
        "We declare that this invoice shows the actual price of the goods described and that all particulars are true and correct.", 
        size=8)
        
    # Right Column: Company Info
    c_comp = t9.cell(0, 2)
    add_text(c_comp, "For RASI FOODS", bold=True, size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_text(c_comp, "\n\n\nAuthorised Signatory & Company Seal", size=8, align=WD_ALIGN_PARAGRAPH.RIGHT)

    add_spacer(doc, pt=2)

    # ── Section 10: Horizontal Signatures ─────────────────────────────────────
    t10 = doc.add_table(rows=1, cols=3)
    t10.style = 'Table Grid'
    t10.autofit = False
    t10.columns[0].width = Inches(2.53)
    t10.columns[1].width = Inches(2.53)
    t10.columns[2].width = Inches(2.54)
    
    c_sig_conf = t10.cell(0, 0)
    c_sig_cons = t10.cell(0, 1)
    c_sig_exp  = t10.cell(0, 2)

    add_text(c_sig_conf, "Confirmation for Proforma Invoice", bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    add_text(c_sig_cons, "Consignee Signature", bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    add_text(c_sig_exp, "Exporter Signature", bold=True, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_spacer(doc, pt=2)

    # ── Section 11: Footer ────────────────────────────────────────────────────
    t_foot = doc.add_table(rows=1, cols=1)
    make_table_borders_invisible(t_foot)
    c_foot = t_foot.cell(0, 0)
    add_text(c_foot, "{{ exporter_name }}", bold=True, size=8, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15)
    add_text(c_foot, "{{ exporter_address }}", size=8, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15)
    add_text(c_foot, "Email: {{ exporter_email }} | GSTIN: {{ exporter_gstin }} | PAN: {{ exporter_pan }}", size=8, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15)
    
    # Root Cause Fix for 2nd page:
    # Word COM objects automatically insert a default 11pt paragraph after the last table if none exists.
    # By providing a 1pt paragraph explicitly, we prevent Word from adding the massive default spacing.
    final_p = doc.add_paragraph()
    final_p.paragraph_format.space_before = Pt(0)
    final_p.paragraph_format.space_after = Pt(0)
    final_p.paragraph_format.line_spacing = Pt(1)
    # Using EXACTLY rule to force 1pt height
    from docx.enum.text import WD_LINE_SPACING
    final_p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    run = final_p.add_run()
    run.font.size = Pt(1)

    # ── Validate and save ──────────────────────────────────────────────────────
    placeholders = extract_placeholders_from_doc(doc)
    missing = placeholders - VALID_KEYS
    if missing:
        print(f"ERROR in Proforma Invoice: Missing backend mappings for: {missing}")
        import sys
        sys.exit(1)

    doc.save(doc_path)
    print(f"Generated {doc_path}")


def generate_all_clean_templates():
    import os
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(backend_dir, 'templates')

    create_invoice_base(os.path.join(templates_dir, 'invoice.docx'), "COMMERCIAL INVOICE")
    create_proforma_invoice(os.path.join(templates_dir, 'proforma_invoice.docx'))
    create_packing_list(os.path.join(templates_dir, 'packing_list.docx'))

if __name__ == "__main__":
    generate_all_clean_templates()
