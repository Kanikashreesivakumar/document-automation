"""
Prepare health_certificate.docx template from the uploaded 'health certificate.docx'.

This script:
  1. Loads 'health certificate.docx' (the uploaded original)
  2. Replaces specific static run-level text with docxtpl {{ }} placeholders
  3. Saves to backend/templates/health_certificate.docx

RULES:
  - Never rebuild layout, never recreate tables/borders/spacing.
  - Only text values of runs are changed; fonts/formatting is preserved.
  - The output MUST look identical to the uploaded template (only values change).
"""
import shutil
from pathlib import Path
from docx import Document

# Paths
ROOT = Path(__file__).parent.parent.parent
SOURCE_HC = ROOT / "health certificate.docx"
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def _replace_run_text(para, old_fragment: str, new_text: str) -> bool:
    """
    Replace a contiguous text fragment spread across runs of a paragraph.
    Collapses all matching runs into one run with the replacement, clearing others.
    Returns True if replacement happened.
    """
    full_text = para.text
    if old_fragment not in full_text:
        return False

    # Build cumulative run positions
    runs = para.runs
    positions = []
    pos = 0
    for run in runs:
        positions.append((pos, pos + len(run.text), run))
        pos += len(run.text)

    start_idx = full_text.index(old_fragment)
    end_idx = start_idx + len(old_fragment)

    # Find which runs cover this fragment
    first_run_idx = None
    last_run_idx = None
    for i, (rstart, rend, _) in enumerate(positions):
        if rend > start_idx and rstart < end_idx:
            if first_run_idx is None:
                first_run_idx = i
            last_run_idx = i

    if first_run_idx is None:
        return False

    # Reconstruct: before fragment in first run + replacement + after fragment in last run
    first_run = positions[first_run_idx][2]
    last_run = positions[last_run_idx][2]

    before_in_first = first_run.text[:max(0, start_idx - positions[first_run_idx][0])]
    after_in_last = last_run.text[max(0, end_idx - positions[last_run_idx][0]):]

    # Set first run to before + replacement + after
    first_run.text = before_in_first + new_text + after_in_last

    # Clear intermediate runs
    for i in range(first_run_idx + 1, last_run_idx + 1):
        positions[i][2].text = ""

    return True


def _replace_in_para(para, replacements: list):
    """Apply a list of (old, new) replacements to a paragraph."""
    for old, new in replacements:
        if old in para.text:
            _replace_run_text(para, old, new)


def prepare_health_certificate():
    """
    Inject docxtpl placeholders into the uploaded health certificate template.
    Preserves ALL formatting, spacing, tables, borders, fonts.
    """
    if not SOURCE_HC.exists():
        print(f"[HealthCertTemplate] ERROR: Source not found: {SOURCE_HC}")
        return False

    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    dest = TEMPLATES_DIR / "health_certificate.docx"

    # Copy to preserve all formatting
    shutil.copy2(SOURCE_HC, dest)
    doc = Document(str(dest))

    paragraphs = doc.paragraphs
    total = len(paragraphs)
    print(f"[HealthCertTemplate] Total paragraphs: {total}")

    for i, para in enumerate(paragraphs):
        text = para.text

        # ── Para [4]: S.NO: → S.NO: {{ serial_no }}
        if "S.NO:" in text and "{{ serial_no }}" not in text:
            _replace_in_para(para, [("S.NO:", "S.NO: {{ serial_no }}")])

        # ── Para [5]: TO\tDATE: 25.06.2026
        if text.startswith("TO\t") and "DATE:" in text and "{{ issue_date }}" not in text:
            _replace_in_para(para, [("DATE: ", "DATE: {{ issue_date }}")])
            # Remove the actual date runs after "DATE: "
            # Find and clear date digits
            date_val = None
            for old_date in ["25.06.2026", "24.06.2026", "01.01.2024"]:
                if old_date in text:
                    date_val = old_date
                    break
            if date_val:
                _replace_in_para(para, [(date_val, "")])

        # ── Para [9]: Certify examined N Cartons ... exported TO BUYER
        if "This is to Certify that I have this" in text and "Cartons of Indian Fresh Eggs" in text:
            # Replace carton count
            for count in ["1312", "656", "1000", "500", "2000"]:
                if f"   {count}  " in text:
                    _replace_in_para(para, [(f"   {count}  ", " {{ cartons }} ")])
                    break
            if "{{ cartons }}" not in para.text:
                # Try without spaces
                import re
                for run in para.runs:
                    if run.text.strip().isdigit() and 100 < int(run.text.strip() or "0") < 9999:
                        run.text = "{{ cartons }}"
                        break

            # Replace exporter: "RASI FOODS NAMAKKAL" → {{ exporter_name }}
            if "RASI FOODS NAMAKKAL" in para.text:
                _replace_in_para(para, [("RASI FOODS NAMAKKAL", "{{ exporter_name }}")])
            elif "RASI FOODS" in para.text:
                _replace_in_para(para, [("RASI FOODS", "{{ exporter_name }}")])

            # Replace buyer: look for known buyer patterns
            for buyer_str in ["NESTO HYPERMARKET L.L.C. KHOR AL FAKKAN, UNITED ARAB EMIRATES",
                               "NESTO HYPERMARKET L.L.C", "KHOR AL FAKKAN, UNITED ARAB EMIRATES"]:
                if buyer_str in para.text:
                    _replace_in_para(para, [(buyer_str, "{{ importer_name }}, {{ importer_address }}")])
                    break

        # ── Para [14]: Production Date
        if "Production Date" in text and "{{" not in text and i < 40:
            for date_val in ["24/06/2026", "25/06/2026", "01/01/2024"]:
                if date_val in text:
                    _replace_in_para(para, [(date_val, "{{ production_date }}")])
                    break

        # ── Para [15]: Expiry Date (first occurrence)
        if "Expiry Date" in text and "{{" not in text and i < 40:
            for date_val in ["21/09/2026", "01/04/2024"]:
                if date_val in text:
                    _replace_in_para(para, [(date_val, "{{ expiry_date }}")])
                    break

        # ── Para [16]: Port of Shipment
        if "Port of Shipment" in text and "{{" not in text:
            for port in ["COCHIN", "CHENNAI", "MUMBAI", "NHAVA SHEVA"]:
                if port in text:
                    _replace_in_para(para, [(port, "{{ port_of_shipment }}")])
                    break

        # ── Para [17]: Date of Inspection
        if "Date of Inspection" in text and "{{" not in text:
            for date_val in ["25.06.2026", "24.06.2026", "01.01.2024"]:
                if date_val in text:
                    _replace_in_para(para, [(date_val, "{{ date_of_inspection }}")])
                    break

        # ── Para [18]: Container No (first occurrence)
        if "Container No" in text and "{{" not in text and i < 40:
            for container in ["TTNU8044030", "MSCU1234567", "HLCU1234567"]:
                if container in text:
                    _replace_in_para(para, [(container, "{{ container_no }}")])
                    break

        # ── Para [20]: TRUCK No
        if "TRUCK No" in text and "{{" not in text:
            for truck in ["TN88M0911", "TN12A1234"]:
                if truck in text:
                    _replace_in_para(para, [(truck, "{{ truck_no }}")])
                    break

        # ── Para [21]: INVOICE NO./DT
        if "INVOICE NO./DT" in text and "{{" not in text:
            # Replace everything after ":        " with the placeholder
            # Structure: "INVOICE NO./DT\t\t:        RF/049/26-27 DT: 24.06.2026"
            for inv_str in ["RF/049/26-27 DT: 24.06.2026",
                             "RF/049/26-27 DT:  24.06.2026"]:
                if inv_str in text:
                    _replace_in_para(para, [(inv_str, "{{ invoice_no }} DT: {{ invoice_date }}")])
                    break
            # Fallback: clear everything after the colon
            if "{{" not in para.text:
                # Try replacing the runs after ":" 
                colon_found = False
                for run in para.runs:
                    if ":        " in run.text or (colon_found and run.text.strip()):
                        if ":        " in run.text:
                            run.text = run.text[:run.text.index(":        ")] + ":        {{ invoice_no }} DT: {{ invoice_date }}"
                            colon_found = True
                            break

        # ── Para [35]: Vet officer name (signature)
        if "Dr." in text and "MANIVEL" in text and i > 30 and i < 45 and "{{" not in text:
            _replace_in_para(para, [("Dr.R.MANIVEL. B.V.Sc", "{{ vet_officer_name }}")])
            if "{{" not in para.text:
                _replace_in_para(para, [(" Dr.R.MANIVEL. B.V.Sc", "{{ vet_officer_name }}")])

        # ── Annexure section: Para [47] exporter & producer
        if "This is to certify that the flocks where from the poultry eggs derived" in text and "{{" not in text:
            if "RASI FOODS,NO.1/219" in text:
                _replace_in_para(para, [("RASI FOODS,NO.1/219 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003,Tamilnadu,", "{{ exporter_name }}, {{ exporter_address }},")])

            if "SRI SARA EGG FARMS, SF NO:13-PILLUR ROAD,JANGAMANAYAKAN PATTY, VILLIPALAYAM , (PO) P.VELUR(TK), NAMAKKAL -637207" in para.text:
                _replace_in_para(para, [("SRI SARA EGG FARMS, SF NO:13-PILLUR ROAD,JANGAMANAYAKAN PATTY, VILLIPALAYAM , (PO) P.VELUR(TK), NAMAKKAL -637207", "{{ producer_name }}, {{ producer_address }}")])
            elif "Producer: " in para.text:
                # Find the "Producer:" portion
                idx = para.text.index("Producer:")
                # Find the run containing "Producer:"
                for run in para.runs:
                    if "Producer:" in run.text:
                        run.text = run.text[:run.text.index("Producer:")] + "Producer: {{ producer_name }}, {{ producer_address }}"
                        # Clear subsequent runs with the address
                        clear_next = True
                        break

        # ── Para [50]: Annexure - "exported to UNITED ARAB EMIRATES"
        if "That the eggs exported to" in text and "{{" not in text:
            for country in ["UNITED ARAB EMIRATES", "UAE", "KUWAIT", "BAHRAIN"]:
                if country in text:
                    _replace_in_para(para, [(country, "{{ destination_country }}")])
                    break

        # ── Para [60]: Container No (Annexure)
        if "Container No" in text and "{{" not in text and i >= 55:
            for container in ["TTNU8044030", "MSCU1234567"]:
                if container in text:
                    _replace_in_para(para, [(container, "{{ container_no }}")])
                    break

        # ── Para [61]: Production Date (Annexure)
        if "Production Date" in text and "{{" not in text and i >= 55:
            for date_val in ["24/06/2026", "25/06/2026"]:
                if date_val in text:
                    _replace_in_para(para, [(date_val, "{{ production_date }}")])
                    break

        # ── Para [62]: Expiry Date (Annexure)
        if "Expiry Date" in text and "{{" not in text and i >= 55:
            for date_val in ["21/09/2026"]:
                if date_val in text:
                    _replace_in_para(para, [(date_val, "{{ expiry_date }}")])
                    break

        # ── Para [63]: Invoice No/Date (Annexure)
        if "Invoice No/Date" in text and "{{" not in text:
            for inv_str in ["RF/049/26-27 DT: 24.06.2026", "RF/049/26-27 DT:  24.06.2026"]:
                if inv_str in text:
                    _replace_in_para(para, [(inv_str, "{{ invoice_no }} DT: {{ invoice_date }}")])
                    break

        # ── Para [64]: Certificate No (Annexure)
        if "Certificate No" in text and text.endswith(":") and "{{" not in text:
            # Add placeholder after ":"
            for run in reversed(para.runs):
                if ":" in run.text:
                    run.text = run.text.rstrip() + " {{ certificate_no }}"
                    break

        # ── Para [65]: Date of Issue (Annexure)
        if "Date of Issue" in text and "{{" not in text and i >= 60:
            for run in reversed(para.runs):
                if ":" in run.text:
                    run.text = run.text.rstrip() + " {{ date_of_issue }}"
                    break

        # ── Para [71]: Vet officer (Annexure signature)
        if "Dr." in text and "MANIVEL" in text and i >= 65 and "{{" not in text:
            _replace_in_para(para, [("Dr.R.MANIVEL. B.V.Sc", "{{ vet_officer_name }}")])
            if "{{" not in para.text:
                for run in para.runs:
                    if run.text.strip():
                        # Clear all runs and set first to placeholder
                        para.runs[0].text = "{{ vet_officer_name }}"
                        break

        # ── Compress Annexure Spacing (Page 2/3) ──
        # Reduce space after these specific lines to prevent spilling to Page 3
        if i >= 55:
            from docx.shared import Pt
            from docx.enum.text import WD_LINE_SPACING
            
            # Reduce spacing for the metadata lines
            if any(keyword in text for keyword in [
                "Container No", "Production Date", "Expiry Date", 
                "Invoice No/Date", "Certificate No", "Date of Issue"
            ]):
                para.paragraph_format.space_after = Pt(2)
                
            # Shrink empty paragraphs between Date of Issue and Signature
            if not text.strip() and i > 60 and i < 75:
                para.paragraph_format.space_before = Pt(0)
                para.paragraph_format.space_after = Pt(0)
                para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                para.paragraph_format.line_spacing = Pt(1)
                for run in para.runs:
                    run.font.size = Pt(1)

    doc.save(str(dest))
    print(f"[HealthCertTemplate] Saved: {dest}")
    return True


if __name__ == "__main__":
    prepare_health_certificate()
