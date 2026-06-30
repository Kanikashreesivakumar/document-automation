"""
Document generation service.

Architecture:
  • This module generates DOCX files from templates using docxtpl.
  • It NEVER reads the database. It only receives a shipment_data dict.
  • It calls the mapping module to get a template context.
  • Templates are in backend/templates/. Generated files go to backend/generated/.
  • Adding a new document = add its template to templates/ + add an entry to DOC_REGISTRY.
"""
import zipfile
from pathlib import Path
from docxtpl import DocxTemplate

from mapping import get_context

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
GENERATED_DIR = Path(__file__).parent.parent / "generated"


# ─── Document registry ────────────────────────────────────────────────────────
# Each entry: (doc_type, template_filename)
# To add a new document: add its .docx template to templates/ and register here.

DOC_REGISTRY = [
    ("invoice",            "invoice.docx"),
    ("packing_list",       "packing_list.docx"),
    ("proforma_invoice",   "proforma_invoice.docx"),
    ("trade_facility",     "trade_facility.docx"),
    ("export_insurance",   "export_insurance.docx"),
    ("animal_certificate", "animal_certificate.docx"),
    ("animal_annexure",    "animal_annexure.docx"),
]


def _ensure_output_dir(shipment_id: str) -> Path:
    out = GENERATED_DIR / shipment_id
    out.mkdir(parents=True, exist_ok=True)
    return out


def generate_all(shipment_data: dict) -> list[dict]:
    """
    Generate all available DOCX documents for a shipment.

    For each registered doc_type:
      1. Resolve its template path (skip if not built yet).
      2. Ask the mapping layer for the context dict.
      3. Render via docxtpl.
      4. Save to generated/<shipment_id>/<doc_type>_<shipment_number>.docx.

    Returns a list of result dicts for the repository to persist.
    """
    shipment_id = shipment_data["id"]
    shipment_number = shipment_data.get("shipment_number", shipment_id)
    output_dir = _ensure_output_dir(shipment_id)
    results = []

    for doc_type, template_file in DOC_REGISTRY:
        template_path = TEMPLATES_DIR / template_file
        if not template_path.exists():
            print(f"[DocumentGenerator] Template not found, skipping: {template_file}")
            continue

        file_name = f"{doc_type}_{shipment_number}.docx"
        file_path = str(output_dir / file_name)

        try:
            ctx = get_context(doc_type, shipment_data)
            tpl = DocxTemplate(str(template_path))
            tpl.render(ctx)
            tpl.save(file_path)
            results.append({
                "doc_type":    doc_type,
                "file_name":   file_name,
                "file_path":   file_path,
                "file_format": "docx",
            })
            print(f"[DocumentGenerator] Generated: {file_name}")
        except Exception as exc:
            # Log and continue — don't fail the whole batch for one doc
            print(f"[DocumentGenerator] ERROR generating {doc_type}: {exc}")

    return results


def create_zip(shipment_id: str, shipment_number: str) -> str:
    """Zip all generated DOCX files for a shipment and return the zip path."""
    output_dir = GENERATED_DIR / shipment_id
    zip_name = f"shipment_{shipment_number}_all_documents.zip"
    zip_path = str(output_dir / zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in output_dir.glob("*.docx"):
            zf.write(f, arcname=f.name)

    return zip_path


def ensure_templates_exist():
    """
    Build invoice.docx and packing_list.docx from the uploaded source template
    if they don't exist yet. Other templates (vet, insurance, etc.) are built
    separately via their own builder.
    """
    invoice_path = TEMPLATES_DIR / "invoice.docx"
    pl_path = TEMPLATES_DIR / "packing_list.docx"

    if not invoice_path.exists() or not pl_path.exists():
        print("[DocumentGenerator] Building invoice/packing_list templates...")
        try:
            from services.template_builder import build_templates
            build_templates()
        except Exception as exc:
            print(f"[DocumentGenerator] Template build failed: {exc}")

