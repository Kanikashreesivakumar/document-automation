"""
Document generation service.

Architecture:
  • This module generates DOCX files from templates using python-docx.
  • It NEVER reads the database. It only receives a shipment_data dict.
  • It calls the mapping module to get a template context.
  • Templates are in backend/templates/. Generated files go to backend/generated/.
  • Adding a new document = add its template to templates/ + add an entry to DOC_REGISTRY.

Only these 6 documents are generated (no obsolete documents):
  Invoice, PackingList, ProformaInvoice, TradeFacility, ExportInsurance, HealthCertificate

Performance optimisations:
  • All DOCX files are rendered (placeholder fill) concurrently via ThreadPoolExecutor.
  • A single reused Word COM instance converts all DOCX → PDF sequentially (Word COM is
    not safe to call from multiple threads simultaneously on Windows).
  • Template objects are not cached globally (each generation is independent).
"""
import os
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from mapping import get_context

try:
    from services.docx_template_engine import fill_docx_template
except ImportError:
    from docx_template_engine import fill_docx_template

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
GENERATED_DIR = Path(__file__).parent.parent / "generated"

# ─── Document registry ────────────────────────────────────────────────────────
# Each entry: (doc_type, template_filename, output_filename)
# Exactly 6 documents — no obsolete types.

DOC_REGISTRY = [
    ("invoice",            "invoice.docx",            "Invoice"),
    ("packing_list",       "packing_list.docx",        "PackingList"),
    ("proforma_invoice",   "proforma_invoice.docx",    "ProformaInvoice"),
    ("trade_facility",     "trade_facility.docx",      "TradeFacility"),
    ("export_insurance",   "export_insurance.docx",    "ExportInsurance"),
    ("health_certificate", "health_certificate.docx",  "HealthCertificate"),
]


def _ensure_output_dir(shipment_id: str) -> Path:
    out = GENERATED_DIR / shipment_id
    out.mkdir(parents=True, exist_ok=True)
    return out


def _ensure_templates():
    """
    Validate that required templates exist in the templates directory.
    Template generation is now handled as a separate developer step.
    """
    required = ["invoice.docx", "packing_list.docx", "proforma_invoice.docx",
                "trade_facility.docx", "export_insurance.docx", "health_certificate.docx"]
    missing = [t for t in required if not (TEMPLATES_DIR / t).exists()]

    if missing:
        error_msg = f"Missing required templates: {missing}. Please run the template preparation scripts."
        print(f"[DocumentGenerator] ERROR: {error_msg}")
        raise FileNotFoundError(error_msg)


def _fill_one_docx(doc_type: str, template_file: str, output_name: str,
                   shipment_data: dict, output_dir: Path) -> tuple[str, str, str, str] | None:
    """
    Render a single DOCX template (placeholder fill). Pure Python / python-docx,
    fully thread-safe.

    Returns (doc_type, output_name, file_path_docx, file_path_pdf) or None on failure.
    """
    template_path = TEMPLATES_DIR / template_file
    if not template_path.exists():
        print(f"[DocumentGenerator] Template not found, skipping: {template_file}")
        return None

    file_path_docx = str((output_dir / f"{output_name}.docx").resolve())
    file_path_pdf  = str((output_dir / f"{output_name}.pdf").resolve())

    try:
        ctx = get_context(doc_type, shipment_data)



        fill_docx_template(template_path, file_path_docx, ctx)
        return doc_type, output_name, file_path_docx, file_path_pdf
    except Exception as exc:
        print(f"[DocumentGenerator] ERROR filling template for {doc_type}: {exc}")
        import traceback
        traceback.print_exc()
        return None


def _batch_convert_to_pdf(docx_pdf_pairs: list[tuple[str, str]]) -> list[str]:
    """
    Convert a batch of DOCX files to PDF using a single persistent Word COM instance.

    Word COM must be used from a single thread. We open one Word instance, convert
    all files through it, then quit — dramatically reducing startup overhead compared
    to opening a new Word process per document.

    Returns the list of successfully generated PDF paths.
    """
    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()
    word = None
    successful_pdfs = []

    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False

        for docx_path, pdf_path in docx_pdf_pairs:
            try:
                doc = word.Documents.Open(docx_path)
                doc.SaveAs(pdf_path, FileFormat=17)  # 17 = wdFormatPDF
                doc.Close(False)
                os.remove(docx_path)
                name = os.path.basename(pdf_path)
                print(f"[DocumentGenerator] Generated PDF: {name}")
                successful_pdfs.append(pdf_path)
            except Exception as exc:
                docx_name = os.path.basename(docx_path)
                print(f"[DocumentGenerator] ERROR converting {docx_name}: {exc}")
                import traceback
                traceback.print_exc()
    finally:
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()

    return successful_pdfs


def generate_all(shipment_data: dict) -> list[dict]:
    """
    Generate all 6 PDF documents for a shipment.

    Performance strategy:
    1. Fill all DOCX templates concurrently (pure Python, thread-safe).
    2. Convert all generated DOCX files to PDF through a single Word COM session
       (sequential, but Word is opened only once — huge startup saving vs 6 opens).

    Returns a list of result dicts for the repository to persist.
    """
    _ensure_templates()

    shipment_id = shipment_data["id"]
    output_dir = _ensure_output_dir(shipment_id)

    # ── Step 1: Render all DOCX templates concurrently ──────────────────────────
    rendered = []  # list of (doc_type, output_name, docx_path, pdf_path)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(
                _fill_one_docx, doc_type, template_file, output_name, shipment_data, output_dir
            ): output_name
            for doc_type, template_file, output_name in DOC_REGISTRY
        }
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                rendered.append(result)

    if not rendered:
        return []

    # Sort in registry order so Word opens them in a predictable sequence
    order = {entry[0]: i for i, entry in enumerate(DOC_REGISTRY)}
    rendered.sort(key=lambda r: order.get(r[0], 99))

    # ── Step 2: Batch-convert all rendered DOCX → PDF via one Word instance ─────
    docx_pdf_pairs = [(item[2], item[3]) for item in rendered]
    successful_pdfs = set(_batch_convert_to_pdf(docx_pdf_pairs))

    # ── Build result list ────────────────────────────────────────────────────────
    results = []
    for doc_type, output_name, docx_path, pdf_path in rendered:
        if pdf_path in successful_pdfs:
            results.append({
                "doc_type":    doc_type,
                "file_name":   f"{output_name}.pdf",
                "file_path":   pdf_path,
                "file_format": "pdf",
            })

    return results


def _convert_to_pdf_single(file_path_docx: str, file_path_pdf: str) -> None:
    """Convert a single DOCX to PDF (used for preview/on-demand). Opens Word once."""
    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        doc = word.Documents.Open(file_path_docx)
        doc.SaveAs(file_path_pdf, FileFormat=17)
        doc.Close(False)
        if os.path.exists(file_path_docx):
            os.remove(file_path_docx)
    finally:
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def generate_single(shipment_data: dict, target_doc_type: str) -> dict | None:
    """
    Generate a single PDF document for a shipment. Used for live preview and on-demand generation.
    Returns the result dict or None on failure. Raises on error so the preview endpoint can return 500.
    """
    _ensure_templates()

    shipment_id = shipment_data["id"]
    output_dir = _ensure_output_dir(shipment_id)

    target_entry = next((entry for entry in DOC_REGISTRY if entry[0] == target_doc_type), None)
    if not target_entry:
        return None

    doc_type, template_file, output_name = target_entry
    template_path = TEMPLATES_DIR / template_file
    if not template_path.exists():
        print(f"[DocumentGenerator] Template not found: {template_file}")
        return None

    file_name_docx = f"{output_name}.docx"
    file_path_docx = str((output_dir / file_name_docx).resolve())
    file_name_pdf = f"{output_name}.pdf"
    file_path_pdf = str((output_dir / file_name_pdf).resolve())

    try:
        ctx = get_context(doc_type, shipment_data)
        fill_docx_template(template_path, file_path_docx, ctx)
        _convert_to_pdf_single(file_path_docx, file_path_pdf)

        return {
            "doc_type":    doc_type,
            "file_name":   file_name_pdf,
            "file_path":   file_path_pdf,
            "file_format": "pdf",
        }
    except Exception as exc:
        print(f"[DocumentGenerator] ERROR generating {doc_type}: {exc}")
        import traceback
        traceback.print_exc()
        raise exc


def create_zip(shipment_id: str, shipment_number: str) -> str:
    """Zip all generated PDF files for a shipment and return the zip path."""
    output_dir = GENERATED_DIR / shipment_id
    zip_name = f"shipment_{shipment_number}_all_documents.zip"
    zip_path = str(output_dir / zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in output_dir.glob("*.pdf"):
            zf.write(f, arcname=f.name)

    return zip_path


# Legacy alias kept for backward compatibility
def ensure_templates_exist():
    _ensure_templates()
