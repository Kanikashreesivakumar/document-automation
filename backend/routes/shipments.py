"""
Shipment routes — REST API endpoints.

Routing decisions:
  • POST /api/shipments/{id}/data  — unified endpoint replacing /invoice + /packing-list
  • Health Certificate replaces animal-certificate (same data, renamed endpoint)
  • All obsolete routes (animal-annexure as separate, etc.) removed
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid

from core.database import get_db
from schemas.shipment import (
    ShipmentDataCreate, ProformaInvoiceCreate, TradeFacilityCreate, ExportInsuranceCreate,
    AnimalCertificateCreate, AnimalAnnexureCreate,
)
from controllers.shipment_controller import (
    create_shipment_ctrl, list_shipments_ctrl, get_shipment_ctrl, delete_shipment_ctrl,
    save_shipment_data_ctrl, save_proforma_invoice_ctrl, get_proforma_invoice_ctrl,
    save_trade_facility_ctrl, get_trade_facility_ctrl,
    save_export_insurance_ctrl, get_export_insurance_ctrl,
    save_animal_certificate_ctrl, get_animal_certificate_ctrl,
    save_animal_annexure_ctrl, get_animal_annexure_ctrl,
    generate_documents_ctrl, get_document_path_ctrl, get_zip_path_ctrl,
    get_recent_documents_ctrl,
)

router = APIRouter(prefix="/api/shipments", tags=["shipments"])


# ── Shipment CRUD ──────────────────────────────────────────────────────────────

@router.post("")
def create_shipment(db: Session = Depends(get_db)):
    return create_shipment_ctrl(db)


@router.get("")
def list_shipments(db: Session = Depends(get_db)):
    return list_shipments_ctrl(db)


@router.get("/recent-documents")
def get_recent_documents(db: Session = Depends(get_db)):
    return get_recent_documents_ctrl(db)


@router.get("/{shipment_id}")
def get_shipment(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_shipment_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return result


@router.delete("/{shipment_id}", status_code=204)
def delete_shipment(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    success = delete_shipment_ctrl(shipment_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Shipment not found or could not be deleted")
    return None


@router.put("/{shipment_id}")
def update_shipment(shipment_id: str, db: Session = Depends(get_db)):
    result = get_shipment_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"success": True, "message": f"Shipment {shipment_id} updated"}


# ── Unified shipment data endpoint ─────────────────────────────────────────────

@router.post("/{shipment_id}/data")
def save_shipment_data(
    shipment_id: str,
    data: ShipmentDataCreate,
    db: Session = Depends(get_db),
):
    """
    Save all user-supplied shipment data in one call.
    Populates: invoice_info, buyer, shipment_details, product, package, pricing, weight.
    Auto-calculates: eggs_per_carton, total_eggs, amount_usd, amount_in_words,
                     net_weight, gross_weight.
    """
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_shipment_data_ctrl(shipment_id, data, db)


@router.post("/{shipment_id}/proforma")
def save_proforma_invoice(
    shipment_id: str,
    data: ProformaInvoiceCreate,
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_proforma_invoice_ctrl(shipment_id, data, db)


@router.get("/{shipment_id}/proforma")
def get_proforma_invoice(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_proforma_invoice_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Proforma Invoice not found")
    return result


@router.post("/{shipment_id}/trade-facility")
def save_trade_facility(
    shipment_id: str,
    data: TradeFacilityCreate,
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_trade_facility_ctrl(shipment_id, data, db)


@router.get("/{shipment_id}/trade-facility")
def get_trade_facility(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_trade_facility_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Trade Facility not found")
    return result


@router.post("/{shipment_id}/insurance")
def save_export_insurance(
    shipment_id: str,
    data: ExportInsuranceCreate,
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_export_insurance_ctrl(shipment_id, data, db)


@router.get("/{shipment_id}/insurance")
def get_export_insurance(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_export_insurance_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Export Insurance not found")
    return result


# ── Health Certificate (Step 6: Certificate + Annexure in one form) ───────────
# Reuses the existing animal_certificate + animal_annexure DB tables.
# The generated document combines both into one HealthCertificate.docx.

@router.post("/{shipment_id}/health-certificate")
def save_health_certificate(
    shipment_id: str,
    data: AnimalCertificateCreate,
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_animal_certificate_ctrl(shipment_id, data, db)


@router.get("/{shipment_id}/health-certificate")
def get_health_certificate(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_animal_certificate_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Health Certificate not found")
    return result


@router.post("/{shipment_id}/health-certificate/annexure")
def save_health_certificate_annexure(
    shipment_id: str,
    data: AnimalAnnexureCreate,
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_animal_annexure_ctrl(shipment_id, data, db)


@router.get("/{shipment_id}/health-certificate/annexure")
def get_health_certificate_annexure(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_animal_annexure_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Health Certificate Annexure not found")
    return result


# ── Backward-compatible aliases (keep old routes working for existing data) ────

@router.post("/{shipment_id}/animal-certificate")
def save_animal_certificate_compat(
    shipment_id: str,
    data: AnimalCertificateCreate,
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_animal_certificate_ctrl(shipment_id, data, db)


@router.get("/{shipment_id}/animal-certificate")
def get_animal_certificate_compat(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_animal_certificate_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Health Certificate not found")
    return result


@router.post("/{shipment_id}/animal-annexure")
def save_animal_annexure_compat(
    shipment_id: str,
    data: AnimalAnnexureCreate,
    db: Session = Depends(get_db),
):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    return save_animal_annexure_ctrl(shipment_id, data, db)


@router.get("/{shipment_id}/animal-annexure")
def get_animal_annexure_compat(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_animal_annexure_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Animal Annexure not found")
    return result


# ── Document generation & download ────────────────────────────────────────────

@router.post("/{shipment_id}/generate")
def generate_documents(shipment_id: str, db: Session = Depends(get_db)):
    result = generate_documents_ctrl(shipment_id, db)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error", "Generation failed"))
    return result


@router.get("/{shipment_id}/download/{doc_type}")
def download_document(shipment_id: str, doc_type: str, db: Session = Depends(get_db)):
    path = get_document_path_ctrl(shipment_id, doc_type, db)
    if not path:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{doc_type}' not found or not yet generated.",
        )
    from pathlib import Path
    file_path = Path(path)
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/pdf",
    )


from fastapi import Request, BackgroundTasks
import os

def remove_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

@router.post("/{shipment_id}/preview-pdf/{doc_type}")
async def preview_pdf(shipment_id: str, doc_type: str, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from services.shipment_service import get_shipment, generate_single_document
    # For now we will NOT actually update the DB so we don't accidentally save invalid state from a 2-second debounce,
    # or wait, the user agreed to "Live Preview will now act as an auto-save". Let's save it.
    # Wait, the incoming data is just part of the form, it varies by doc_type.
    # So we must call the appropriate save controller depending on doc_type.
    
    try:
        live_fields = await request.json()
    except Exception:
        live_fields = {}

    try:
        if live_fields:
            if doc_type in ["invoice", "packing_list"]:
                from schemas.shipment import ShipmentDataCreate
                from services.shipment_service import save_shipment_data
                save_shipment_data(shipment_id, ShipmentDataCreate(**live_fields), db)
            elif doc_type == "proforma_invoice":
                from schemas.shipment import ProformaInvoiceCreate
                from controllers.shipment_controller import save_proforma_invoice_ctrl
                save_proforma_invoice_ctrl(shipment_id, ProformaInvoiceCreate(**live_fields), db)
            elif doc_type == "trade_facility":
                from schemas.shipment import TradeFacilityCreate
                from services.shipment_service import save_trade_facility_ctrl
                save_trade_facility_ctrl(shipment_id, TradeFacilityCreate(**live_fields), db)
            elif doc_type == "export_insurance":
                from schemas.shipment import ExportInsuranceCreate
                from services.shipment_service import save_export_insurance_ctrl
                save_export_insurance_ctrl(shipment_id, ExportInsuranceCreate(**live_fields), db)
            elif doc_type == "health_certificate":
                # Note: health certificate uses animal certificate schemas and annexure schemas
                from schemas.shipment import AnimalCertificateCreate, AnimalAnnexureCreate
                from services.shipment_service import save_animal_certificate_ctrl, save_animal_annexure_ctrl
                save_animal_certificate_ctrl(shipment_id, AnimalCertificateCreate(**live_fields), db)
                save_animal_annexure_ctrl(shipment_id, AnimalAnnexureCreate(**live_fields), db)
            db.commit()
    except Exception as e:
        print(f"[Preview] Auto-save skipped or failed: {e}")
        # Ignore validation/save errors and just attempt generation with existing DB data
        pass

    try:
        gen_result = generate_single_document(shipment_id, doc_type, db)
        if not gen_result.get("success"):
            raise HTTPException(status_code=500, detail=gen_result.get("error", "Generation failed"))
            
        file_path = gen_result["file_path"]
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {e}")


@router.get("/{shipment_id}/download-all")
def download_all(shipment_id: str, db: Session = Depends(get_db)):
    path = get_zip_path_ctrl(shipment_id, db)
    if not path:
        raise HTTPException(status_code=404, detail="No generated documents found.")
    from pathlib import Path
    file_path = Path(path)
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/zip",
    )
