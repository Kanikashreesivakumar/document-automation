"""
Prepare all DOCX templates for the Document Automation System.

Strategy:
 - Copy the original uploaded DOCX files to backend/templates/
 - Replace individual w:t text nodes that match known static values
 - For cross-run replacements (where static value spans multiple runs):
   merge adjacent runs in the same paragraph before replacing
 - NEVER rebuild tables, layouts, or formatting
"""
import shutil
import zipfile
from pathlib import Path
from lxml import etree
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_TAB_ALIGNMENT

try:
    from services.docx_template_engine import ensure_letterhead_header
except ImportError:
    from docx_template_engine import replace_text, ensure_letterhead_header

ROOT = Path(r"d:\Form Automation")
TEMPLATES_DIR = ROOT / "backend" / "templates"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"


def _get_all_text_in_para(para) -> str:
    """Concatenate all w:t text (ignoring tabs) in a paragraph."""
    return "".join(t.text or "" for t in para.iter(f"{W}t"))


def _replace_in_run_text(para, old: str, new: str) -> bool:
    """
    Try to replace `old` string in the paragraph text while keeping run structure.
    Only modifies w:t elements; does not destroy tabs, bookmarks, etc.
    Returns True if replacement happened.
    """
    # First pass: try simple single-run replacements
    for r in para.iter(f"{W}r"):
        t_els = list(r.iter(f"{W}t"))
        full_run_text = "".join(t.text or "" for t in t_els)
        if old in full_run_text:
            new_text = full_run_text.replace(old, new)
            if t_els:
                t_els[0].text = new_text
                t_els[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                for t_el in t_els[1:]:
                    t_el.text = ""
            return True
    
    # Second pass: try cross-run replacement by merging w:t elements in paragraph
    # We only merge adjacent runs that are within the same paragraph
    full_para = _get_all_text_in_para(para)
    if old not in full_para:
        return False
    
    # Collect all w:t elements in paragraph in order
    t_elements = list(para.iter(f"{W}t"))
    if not t_elements:
        return False
    
    full = "".join(t.text or "" for t in t_elements)
    if old not in full:
        return False
    
    # Replace in merged text, then put it all in first t element
    new_full = full.replace(old, new, 1)
    t_elements[0].text = new_full
    t_elements[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for t_el in t_elements[1:]:
        t_el.text = ""
    
    return True


def _apply_replacements(root, replacements: list[tuple[str, str]]):
    """Apply all replacements across all paragraphs in the document XML."""
    for para in root.iter(f"{W}p"):
        for old, new in replacements:
            full = _get_all_text_in_para(para)
            if old in full:
                _replace_in_run_text(para, old, new)


def prepare_with_xml(src_path: Path, dest_path: Path, replacements: list[tuple[str, str]], remove_table_idx=None):
    """
    Copy src to dest, apply text replacement preserving formatting, optionally remove a table.
    """
    shutil.copy2(src_path, dest_path)
    
    doc = Document(str(dest_path))
    if remove_table_idx is not None and remove_table_idx < len(doc.tables):
        tbl = doc.tables[remove_table_idx]._element
        tbl.getparent().remove(tbl)
    
    # replace_text preserves all run formatting (fonts, bold, etc)
    replace_text(doc, dict(replacements))
    
    doc.save(str(dest_path))
    print(f"  Saved: {dest_path.name}")


def prepare_export_insurance():
    print("Preparing Export Insurance...")
    replacements = [
        ("To \tDATE:  ", "To\tDATE: {{ date }}"),
        ("Date of loading                   :          ", "Date of loading                   : {{ invoice_date }}"),
        ("Invoice no/Date                  :                                    DT : ", "Invoice no/Date                  : {{ invoice_no }}                                   DT : {{ invoice_date }}\nContainer no                     : {{ container_no }}"),
        ("Seal No’s                            :          ", "Seal No’s                            : {{ seal_nos }}"),
        ("Truck                                  :        ", "Truck                                  : {{ truck_no }}"),
        ("Risk Cover  \t \t: \tICCA ", "Risk Cover                 :       {{ risk_cover }} "),
        (" Place of Loading   \t:          Rasi Foods,", " Place of Loading          :          {{ place_of_loading }}"),
        ("Name  and Address \nOf Importer       \t    ", "Name  and Address\nOf Importer\n{{ importer_name }}\n{{ importer_address }}"),
        ("Sum Assured                     :", "Sum Assured                     : {{ sum_assured }}"),
        ("Dollar                                 :         ", "Dollar                                 : {{ dollar_value }}"),
        ("Name of goods                  :         Fresh white shell table eggs(chicken). ", "Name of goods                  : {{ name_of_goods }}"),
        ("Quantity of goods            :         ", "Quantity of goods            : {{ quantity_of_goods }}"),
        ("Port of Delivery               :         ", "Port of Delivery               : {{ port_of_delivery }}"),
    ]
    prepare_with_xml(ROOT / "export insurance.docx", TEMPLATES_DIR / "export_insurance.docx", replacements)
    doc = Document(str(TEMPLATES_DIR / "export_insurance.docx"))
    ensure_letterhead_header(doc, ROOT / "frame.jpeg")
    doc.save(str(TEMPLATES_DIR / "export_insurance.docx"))
    print("  Applied shared header layout")


def prepare_trade_facility():
    print("Preparing Trade Facility...")
    replacements = [
        ("Shipping Bill No.                                                            :      ",
         "Shipping Bill No.                                                            : {{ shipping_bill_no }}"),
        ("NAME OF THE EXPORTER                                    :  RASI FOODS",
         "NAME OF THE EXPORTER                                    :  {{ exporter_name }}"),
        ("a. IEC NO.                                                                :  3215008319",
         "a. IEC NO.                                                                :  {{ iec_no }}"),
        ("GSTIN                                                                  : 33AASFR2685Q1Z8",
         "GSTIN                                                                  : {{ exporter_gstin }}"),
        ("Branch code                                                       : ",
         "Branch code                                                       : {{ branch_code }}"),
        ("4. Date of Examination                                               :  ",
         "4. Date of Examination                                               :  {{ date_of_examination }}"),
        ("       Starting Time                                                 : ",
         "       Starting Time                                                 : {{ starting_time }}"),
        ("       Completion Time                                          : ",
         "       Completion Time                                          : {{ completion_time }}"),
        ("       Time Taken for Stuffing                                : ",
         "       Time Taken for Stuffing                                : {{ time_taken }}"),
        ("Description of Cargo with quatity                     :  FRESH WHITE SHELL EGG  /1312 CARTONS",
         "Description of Cargo with quatity                     :  {{ description_of_cargo }}"),
        ("Country of final destination                               : ",
         "Country of final destination                               : {{ country_of_destination }}"),
        ("Signatory                                                               :  ",
         "Signatory                                                               :  {{ signatory_name }}, {{ signatory_designation }}"),
        ("Export Invoice No.                                      :                               DT : ",
         "Export Invoice No.                                      : {{ invoice_no }}                              DT : {{ invoice_date }}"),
        ("Total No of Packages                                  :  1312  CARTONS",
         "Total No of Packages                                  :  {{ total_packages }} CARTONS"),
        ("Name & Address of the Consignee          : ",
         "Name & Address of the Consignee          : {{ consignee_name }}, {{ consignee_address }}"),
        ("2.Starting Time (moving the container to CFS ): ",
         "2.Starting Time (moving the container to CFS ): {{ container_to_cfs_time }}"),
        ("The e-seal number is                                     , and the colour of the seal is White.",
         "The e-seal number is {{ e_seal_number }}, and the colour of the seal is {{ e_seal_colour }}."),
        ("Yes / No", "{{ goods_description_verified }}"),
    ]
    prepare_with_xml(ROOT / "trade facility.docx", TEMPLATES_DIR / "trade_facility.docx", replacements)


def main():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    print("=== Preparing all DOCX templates ===")
    prepare_export_insurance()
    prepare_trade_facility()
    print("\n=== All templates prepared ===")


if __name__ == "__main__":
    main()
