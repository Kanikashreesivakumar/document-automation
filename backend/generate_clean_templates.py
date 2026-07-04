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
    section.different_first_page_header_footer = True
    header = section.first_page_header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(header_img_path):
        run = p.add_run()
        run.add_picture(header_img_path, width=Inches(6.5))
    else:
        p.add_run("COMPANY LOGO / HEADER NOT FOUND").bold = True

def apply_style(run, bold=False, size=10):
    run.font.name = 'Arial'
    run.font.size = Pt(size)
    run.bold = bold

def add_kv_pair(cell, key, value, size=9):
    p = cell.paragraphs[0]
    if p.text:
        p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run_key = p.add_run(f"{key}: ")
    apply_style(run_key, bold=True, size=size)
    run_val = p.add_run(value)
    apply_style(run_val, size=size)

def add_text(cell, text, bold=False, size=9, align=None):
    p = cell.paragraphs[0]
    if p.text:
        p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
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

def create_invoice_base(doc_path, title, is_proforma=False):
    doc = docx.Document()
    
    # Setup sections for A4
    sections = doc.sections
    for section in sections:
        section.page_height = Cm(29.7)
        section.page_width = Cm(21.0)
        section.left_margin = Cm(1.27)
        section.right_margin = Cm(1.27)
        section.top_margin = Cm(1.27)
        section.bottom_margin = Cm(1.27)

    # Header
    add_header(doc, r'd:\Form Automation\backend\templates\header_img.jpeg')
    
    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    apply_style(run, bold=True, size=14)
    p.paragraph_format.space_after = Pt(12)

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

    doc.add_paragraph() # spacer

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
    
    doc.add_paragraph()

    # Shipment Details Table (Visible)
    table_shipment = doc.add_table(rows=3, cols=4)
    table_shipment.style = 'Table Grid'
    
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

    doc.add_paragraph()

    # Description of Goods Table (Visible)
    table_goods = doc.add_table(rows=2, cols=4)
    table_goods.style = 'Table Grid'
    table_goods.columns[0].width = Inches(4.5)
    table_goods.columns[1].width = Inches(1.0)
    table_goods.columns[2].width = Inches(1.0)
    table_goods.columns[3].width = Inches(1.0)
    
    headers = ["DESCRIPTION OF GOODS", "QUANTITY", "RATE", "AMOUNT"]
    for i, h in enumerate(headers):
        add_text(table_goods.cell(0, i), h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        
    goods_cell = table_goods.cell(1, 0)
    add_text(goods_cell, "{{ description_of_goods }}")
    
    add_text(table_goods.cell(1, 1), "{{ quantity_of_goods }}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(table_goods.cell(1, 2), "USD {{ rate_per_egg_usd }}", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(table_goods.cell(1, 3), "USD {{ amount_usd }}", align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.add_paragraph()

    # Totals
    table_totals = doc.add_table(rows=1, cols=2)
    make_table_borders_invisible(table_totals)
    t_cells = table_totals.rows[0].cells
    add_kv_pair(t_cells[0], "Amount Chargeable (in words)", "USD {{ amount_in_words }}")
    
    add_kv_pair(t_cells[1], "Total Net Weight", "{{ net_weight }} KGS")
    add_kv_pair(t_cells[1], "Total Gross Weight", "{{ gross_weight }} KGS")

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
        section.left_margin = Cm(1.27)
        section.right_margin = Cm(1.27)
        section.top_margin = Cm(1.27)
        section.bottom_margin = Cm(1.27)

    add_header(doc, r'd:\Form Automation\backend\templates\header_img.jpeg')
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("PACKING LIST")
    apply_style(run, bold=True, size=14)
    p.paragraph_format.space_after = Pt(12)

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
    # Table columns: Marks & Numbers, Description, Cartons, Trays, Eggs, Net Weight, Gross Weight
    # Trays, Eggs inside mapping is not directly exported as independent keys except `total_cartons`, `total_eggs`.
    # Wait, user said "Columns: Marks & Numbers, Description, Cartons, Trays, Eggs, Net Weight, Gross Weight"
    # But trays per carton is NOT in the mapping by default, unless I put it there.
    # The user said "DO NOT create new mapping keys... Use ONLY the existing backend mapping."
    # If the backend mapping does not have "trays_per_carton", I can just put placeholders and let it map to empty if it doesn't exist?
    # Actually, in the existing packing list, they put the entire description_of_goods or they put total_cartons, etc.
    # Let's map to the existing keys available!
    # Cartons -> total_cartons
    # Eggs -> total_eggs
    # Net Weight -> net_weight
    # Gross Weight -> gross_weight
    # Description -> description_of_goods
    
    table_pack = doc.add_table(rows=2, cols=6)
    table_pack.style = 'Table Grid'
    headers = ["Marks & Nos", "Description of Goods", "Quantity", "Net Weight", "Gross Weight", "Total Eggs"]
    for i, h in enumerate(headers):
        add_text(table_pack.cell(0, i), h, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        
    add_text(table_pack.cell(1, 0), "{{ container_no }}\n{{ seal_no }}")
    add_text(table_pack.cell(1, 1), "{{ description_of_goods }}")
    add_text(table_pack.cell(1, 2), "{{ quantity_of_goods }}")
    add_text(table_pack.cell(1, 3), "{{ net_weight }} KGS")
    add_text(table_pack.cell(1, 4), "{{ gross_weight }} KGS")
    add_text(table_pack.cell(1, 5), "{{ total_eggs }}")
    
    # Save and verify
    placeholders = extract_placeholders_from_doc(doc)
    missing = placeholders - VALID_KEYS
    if missing:
        print(f"ERROR in Packing List: Missing backend mappings for placeholders: {missing}")
        sys.exit(1)
        
    doc.save(doc_path)
    print(f"Generated {doc_path}")

def generate_all_clean_templates():
    import os
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(backend_dir, 'templates')
    
    create_invoice_base(os.path.join(templates_dir, 'invoice.docx'), "COMMERCIAL INVOICE")
    create_invoice_base(os.path.join(templates_dir, 'proforma_invoice.docx'), "PROFORMA INVOICE", is_proforma=True)
    create_packing_list(os.path.join(templates_dir, 'packing_list.docx'))

if __name__ == "__main__":
    generate_all_clean_templates()
