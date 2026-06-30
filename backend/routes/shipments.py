"""
Shipment routes — REST API endpoints.

Routing decisions:
  • POST /api/shipments/{id}/data  — unified endpoint replacing /invoice + /packing-list
  • All other existing routes are preserved (vet, insurance, examination, export, generate, download)
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
)

router = APIRouter(prefix="/api/shipments", tags=["shipments"])


# ── Shipment CRUD ──────────────────────────────────────────────────────────────

@router.post("")
def create_shipment(db: Session = Depends(get_db)):
    return create_shipment_ctrl(db)


@router.get("")
def list_shipments(db: Session = Depends(get_db)):
    return list_shipments_ctrl(db)


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


@router.post("/{shipment_id}/animal-certificate")
def save_animal_certificate(
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
def get_animal_certificate(shipment_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    result = get_animal_certificate_ctrl(shipment_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Animal Health Certificate not found")
    return result


# ── Animal Annexure ───────────────────────────────────────────────────────────

@router.post("/{shipment_id}/animal-annexure")
def save_animal_annexure(
    shipment_id: str,
    data: AnimalAnnexureCreate,
    db: Session = Depends(get_db),
):
    print(f"[Animal Annexure] Received shipment_id: {shipment_id}")
    print(f"[Animal Annexure] Received payload: {data.model_dump()}")
    try:
        uuid.UUID(shipment_id)
    except ValueError:
        print("[Animal Annexure] Validation: Invalid shipment ID format")
        raise HTTPException(status_code=400, detail="Invalid shipment ID format")
    
    print("[Animal Annexure] Validation successful. Proceeding to database insert...")
    result = save_animal_annexure_ctrl(shipment_id, data, db)
    print(f"[Animal Annexure] Returned response: {result}")
    return result


@router.get("/{shipment_id}/animal-annexure")
def get_animal_annexure(shipment_id: str, db: Session = Depends(get_db)):
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
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


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
