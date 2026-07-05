"""
Shipment service — business logic layer.

Rules:
  • All DB access goes through repositories.
  • All calculations go through the calculations module.
  • All document generation goes through the document_generator.
  • This layer orchestrates; it does not implement business rules itself.
"""
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from repositories.shipment_repository import (
    ShipmentRepository, ProformaInvoiceRepository, TradeFacilityRepository, ExportInsuranceRepository,
    AnimalCertificateRepository, AnimalAnnexureRepository,
    InvoiceInfoRepository, BuyerRepository, ShipmentDetailsRepository,
    ProductRepository, PackageRepository, PricingRepository, WeightRepository,
    GeneratedDocumentRepository,
)
from schemas.shipment import (
    ShipmentDataCreate, ProformaInvoiceCreate, TradeFacilityCreate, ExportInsuranceCreate,
    AnimalCertificateCreate, AnimalAnnexureCreate,
)
from calculations import compute_all
from services.document_generator import generate_all, create_zip, ensure_templates_exist
from pathlib import Path


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _generate_shipment_number() -> str:
    today = datetime.utcnow().strftime("%Y%m%d")
    short = uuid.uuid4().hex[:6].upper()
    return f"SHP-{today}-{short}"


def _orm_to_dict(obj) -> dict | None:
    """Convert a SQLAlchemy ORM object to a plain dict (non-recursive)."""
    if obj is None:
        return None
    result = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        result[col.name] = val.isoformat() if isinstance(val, datetime) else val
    return result


def _shipment_to_dict(shipment) -> dict:
    """
    Build the canonical shipment data dict from a Shipment ORM object.
    This dict is the single input to both the mapping layer and API responses.
    """
    return {
        "id":              str(shipment.id),
        "shipment_number": shipment.shipment_number,
        "status":          shipment.status,
        "created_at":      shipment.created_at.isoformat(),
        "updated_at":      shipment.updated_at.isoformat() if shipment.updated_at else None,

        # Normalized sub-records
        "invoice_info":     _orm_to_dict(shipment.invoice_info),
        "proforma_invoice": _orm_to_dict(shipment.proforma_invoice),
        "trade_facility":   _orm_to_dict(shipment.trade_facility),
        "export_insurance":  _orm_to_dict(shipment.export_insurance),
        "animal_certificate": _orm_to_dict(shipment.animal_certificate),
        "animal_annexure":  _orm_to_dict(shipment.animal_annexure),
        "buyer":            _orm_to_dict(shipment.buyer),
        "shipment_details": _orm_to_dict(shipment.shipment_details),
        "product":          _orm_to_dict(shipment.product),
        "package":          _orm_to_dict(shipment.package),
        "pricing":          _orm_to_dict(shipment.pricing),
        "weight":           _orm_to_dict(shipment.weight),

        "generated_documents": [_orm_to_dict(d) for d in shipment.generated_documents],
    }


# ─── Shipment CRUD ────────────────────────────────────────────────────────────

def create_shipment(db: Session) -> dict:
    repo = ShipmentRepository(db)
    number = _generate_shipment_number()
    shipment = repo.create(number)
    return {
        "id":              str(shipment.id),
        "shipment_number": shipment.shipment_number,
        "status":          shipment.status,
    }


def list_shipments(db: Session):
    repo = ShipmentRepository(db)
    shipments = repo.list_all()
    # For list view, we just need basic info and invoice_no if exists
    return [
        {
            "id": str(s.id),
            "shipment_number": s.shipment_number,
            "status": s.status,
            "created_at": s.created_at.isoformat(),
            "invoice_no": s.invoice_info.invoice_no if s.invoice_info else None,
        }
        for s in shipments
    ]


def delete_shipment(shipment_id: str, db: Session):
    repo = ShipmentRepository(db)
    success = repo.delete(shipment_id)
    if success:
        import shutil
        # Delete generated output dir
        generated_dir = Path(__file__).parent.parent / "generated" / shipment_id
        if generated_dir.exists():
            try:
                shutil.rmtree(generated_dir)
            except Exception as exc:
                print(f"[ShipmentService] ERROR deleting generated dir {generated_dir}: {exc}")
    return success


def get_shipment(shipment_id: str, db: Session) -> dict | None:
    repo = ShipmentRepository(db)
    shipment = repo.get_by_id(shipment_id)
    if not shipment:
        return None
    return _shipment_to_dict(shipment)

def get_recent_documents(db: Session) -> list:
    repo = ShipmentRepository(db)
    # Query all completed shipments
    shipments = [s for s in repo.list_all() if s.status == "complete"]
    result = []
    
    for s in shipments:
        # Sort generated documents to get the latest generated_at
        docs = s.generated_documents
        doc_count = len(docs)
        if doc_count == 0:
            continue
            
        latest_doc = max(docs, key=lambda x: x.generated_at)
        
        result.append({
            "shipment_id": str(s.id),
            "shipment_number": s.shipment_number,
            "invoice_number": s.invoice_info.invoice_no if s.invoice_info else None,
            "generated_at": latest_doc.generated_at.isoformat(),
            "status": s.status,
            "document_count": doc_count,
            "zip_filename": f"shipment_{s.shipment_number}_all_documents.zip",
            "zip_download_url": f"/api/shipments/{s.id}/download-all"
        })
    
    # Sort by generated_at descending
    result.sort(key=lambda x: x["generated_at"], reverse=True)
    return result


# ─── Unified shipment data save ────────────────────────────────────────────────

def save_shipment_data(shipment_id: str, data: ShipmentDataCreate, db: Session) -> dict:
    """
    Save all user-supplied shipment data in one call.
    Calculations are run here before persisting to the Package, Pricing,
    and Weight tables. Each normalized table is upserted independently.
    """
    d = data.model_dump()

    # ── Run calculations ───────────────────────────────────────────────────────
    # Fallback to existing records for missing fields in partial updates (e.g. from saveDraft)
    d = data.model_dump(exclude_unset=True)
    
    pkg_repo = PackageRepository(db)
    pkg = pkg_repo.get(shipment_id)
    cartons             = d.get("cartons") if "cartons" in d else (pkg.cartons if pkg and pkg.cartons is not None else 0)
    trays_per_carton    = d.get("trays_per_carton") if "trays_per_carton" in d else (pkg.trays_per_carton if pkg and pkg.trays_per_carton is not None else 0)
    eggs_per_tray       = d.get("eggs_per_tray") if "eggs_per_tray" in d else (pkg.eggs_per_tray if pkg and pkg.eggs_per_tray is not None else 0)

    pri_repo = PricingRepository(db)
    pri = pri_repo.get(shipment_id)
    rate_per_egg_usd    = d.get("rate_per_egg_usd") if "rate_per_egg_usd" in d else (pri.rate_per_egg_usd if pri and pri.rate_per_egg_usd is not None else 0.0)

    wt_repo = WeightRepository(db)
    wt = wt_repo.get(shipment_id)
    net_wt_per_carton   = d.get("net_weight_per_carton") if "net_weight_per_carton" in d else (wt.net_weight_per_carton if wt and wt.net_weight_per_carton is not None else 0.0)
    gross_wt_per_carton = d.get("gross_weight_per_carton") if "gross_weight_per_carton" in d else (wt.gross_weight_per_carton if wt and wt.gross_weight_per_carton is not None else 0.0)

    calc = compute_all(
        cartons=cartons,
        trays_per_carton=trays_per_carton,
        eggs_per_tray=eggs_per_tray,
        rate_per_egg_usd=rate_per_egg_usd,
        net_weight_per_carton=net_wt_per_carton,
        gross_weight_per_carton=gross_wt_per_carton,
    )

    # ── Upsert each normalized table ───────────────────────────────────────────
    InvoiceInfoRepository(db).upsert(shipment_id, {
        "invoice_no":                    d.get("invoice_no"),
        "invoice_date":                  d.get("invoice_date"),
        "buyer_order_no_date":           d.get("buyer_order_no_date"),
        "reference_proforma_invoice_no": d.get("reference_proforma_invoice_no"),
        "shipping_bill_no":              d.get("shipping_bill_no"),
        "shipping_bill_date":            d.get("shipping_bill_date"),
        "exporter_reference":            d.get("exporter_reference"),
        "other_reference":               d.get("other_reference"),
    })

    BuyerRepository(db).upsert(shipment_id, {
        "consignee_name":   d.get("consignee_name"),
        "buyer_name":       d.get("buyer_name"),
        "buyer_address":    d.get("buyer_address"),
        "buyer_postal_code": d.get("buyer_postal_code"),
        "buyer_country":    d.get("buyer_country"),
    })

    ShipmentDetailsRepository(db).upsert(shipment_id, {
        "pre_carriage_by":              d.get("pre_carriage_by"),
        "vessel_flight_no":             d.get("vessel_flight_no"),
        "place_of_receipt":             d.get("place_of_receipt"),
        "port_of_loading":              d.get("port_of_loading"),
        "port_of_discharge":            d.get("port_of_discharge"),
        "final_destination":            d.get("final_destination"),
        "country_of_origin":            d.get("country_of_origin"),
        "country_of_final_destination": d.get("country_of_final_destination"),
        "terms_of_delivery":            d.get("terms_of_delivery"),
    })

    ProductRepository(db).upsert(shipment_id, {
        "brand_name":     d.get("brand_name"),
        "product_name":   d.get("product_name"),
        "container_type": d.get("container_type"),
        "container_no":   d.get("container_no"),
        "shipment_declaration": d.get("shipment_declaration"),
        "production_date":      d.get("production_date"),
        "expiry_date":          d.get("expiry_date"),
        "production_duration":  d.get("production_duration"),
        "lot_number":           d.get("lot_number"),
        "epcg_licence_number":  d.get("epcg_licence_number"),
        "dt":                   d.get("dt"),
        "egg_size":             d.get("egg_size"),
        "pan_number":           d.get("pan_number"),
        "gstin":                d.get("gstin"),
        "hsn_code":             d.get("hsn_code"),
    })

    PackageRepository(db).upsert(shipment_id, {
        "cartons":          cartons,
        "trays_per_carton": trays_per_carton,
        "eggs_per_tray":    eggs_per_tray,
        "eggs_per_carton":  calc["eggs_per_carton"],
        "total_eggs":       calc["total_eggs"],
    })

    PricingRepository(db).upsert(shipment_id, {
        "rate_per_egg_usd": rate_per_egg_usd,
        "amount_usd":       calc["amount_usd"],
        "amount_in_words":  calc["amount_in_words"],
    })

    WeightRepository(db).upsert(shipment_id, {
        "net_weight_per_carton":   net_wt_per_carton,
        "gross_weight_per_carton": gross_wt_per_carton,
        "net_weight":              calc["net_weight"],
        "gross_weight":            calc["gross_weight"],
    })

    ShipmentRepository(db).update_status(shipment_id, "in_progress")

    return {"success": True, "calculated": calc}


def save_proforma_invoice(shipment_id: str, data: ProformaInvoiceCreate, db: Session):
    repo = ProformaInvoiceRepository(db)
    record = repo.upsert(shipment_id, data.model_dump(exclude_none=False))
    return {"success": True, "id": str(record.id)}


def get_proforma_invoice(shipment_id: str, db: Session) -> dict | None:
    repo = ProformaInvoiceRepository(db)
    record = repo.get_by_shipment_id(shipment_id)
    if not record:
        return None
    return _orm_to_dict(record)


def save_trade_facility(shipment_id: str, data: TradeFacilityCreate, db: Session):
    repo = TradeFacilityRepository(db)
    # The frontend auto-calculates stuffing_duration and passes it to us.
    record = repo.upsert(shipment_id, data.model_dump(exclude_none=False))
    return {"success": True, "id": str(record.id)}


def get_trade_facility(shipment_id: str, db: Session) -> dict | None:
    repo = TradeFacilityRepository(db)
    record = repo.get_by_shipment_id(shipment_id)
    if not record:
        return None
    return _orm_to_dict(record)


# ─── Export Insurance ─────────────────────────────────────────────────────────

def save_export_insurance(shipment_id: str, data: ExportInsuranceCreate, db: Session):
    repo = ExportInsuranceRepository(db)
    record = repo.upsert(shipment_id, data.model_dump(exclude_none=False))
    return {"success": True, "id": str(record.id)}


def get_export_insurance(shipment_id: str, db: Session) -> dict | None:
    repo = ExportInsuranceRepository(db)
    record = repo.get(shipment_id)
    if not record:
        return None
    return _orm_to_dict(record)


# ─── Animal Certificate ───────────────────────────────────────────────────────

def save_animal_certificate(shipment_id: str, data: AnimalCertificateCreate, db: Session):
    repo = AnimalCertificateRepository(db)
    record = repo.upsert(shipment_id, data.model_dump(exclude_none=False))
    return {"success": True, "id": str(record.id)}


def get_animal_certificate(shipment_id: str, db: Session) -> dict | None:
    repo = AnimalCertificateRepository(db)
    record = repo.get(shipment_id)
    if not record:
        return None
    return _orm_to_dict(record)


# ─── Animal Annexure ──────────────────────────────────────────────────────────

def save_animal_annexure(shipment_id: str, data: AnimalAnnexureCreate, db: Session):
    repo = AnimalAnnexureRepository(db)
    record = repo.upsert(shipment_id, data.model_dump(exclude_none=False))
    return {"success": True, "id": str(record.id)}


def get_animal_annexure(shipment_id: str, db: Session) -> dict | None:
    repo = AnimalAnnexureRepository(db)
    record = repo.get(shipment_id)
    if not record:
        return None
    return _orm_to_dict(record)


# ─── Document generation ──────────────────────────────────────────────────────

def generate_documents(shipment_id: str, db: Session) -> dict:
    """Generate all DOCX documents for a shipment."""
    s_repo = ShipmentRepository(db)
    shipment = s_repo.get_by_id(shipment_id)
    if not shipment:
        return {"success": False, "error": "Shipment not found"}

    missing_fields = []
    


    
    if not shipment.invoice_info or not shipment.invoice_info.invoice_no:
        missing_fields.append("invoice_no")
    if not shipment.invoice_info or not shipment.invoice_info.invoice_date:
        missing_fields.append("invoice_date")
    if not shipment.buyer or not shipment.buyer.consignee_name:
        missing_fields.append("consignee_name")
    if not shipment.buyer or not shipment.buyer.buyer_country:
        missing_fields.append("buyer_country")
    if not shipment.shipment_details or not shipment.shipment_details.port_of_loading:
        missing_fields.append("port_of_loading")
    if not shipment.product or not shipment.product.container_no:
        missing_fields.append("container_no")
    if not shipment.package or not shipment.package.cartons:
        missing_fields.append("cartons")
    if not shipment.pricing or not shipment.pricing.rate_per_egg_usd:
        missing_fields.append("rate_per_egg_usd")
    
    if missing_fields:
        return {"success": False, "error": f"Cannot generate documents. Missing required fields: {', '.join(missing_fields)}"}

    ensure_templates_exist()

    shipment_data = _shipment_to_dict(shipment)
    generated = generate_all(shipment_data)

    doc_repo = GeneratedDocumentRepository(db)
    saved = []
    for g in generated:
        record = doc_repo.create(
            shipment_id=shipment_id,
            doc_type=g["doc_type"],
            file_name=g["file_name"],
            file_path=g["file_path"],
            file_format=g["file_format"],
        )
        saved.append({
            "id":         str(record.id),
            "doc_type":   record.doc_type,
            "file_name":  record.file_name,
            "file_format": record.file_format,
        })

    s_repo.update_status(shipment_id, "complete")
    return {"success": True, "documents": saved}


def generate_single_document(shipment_id: str, doc_type: str, db: Session) -> dict:
    """Generate a single document for a shipment and save its record."""
    s_repo = ShipmentRepository(db)
    shipment = s_repo.get_by_id(shipment_id)
    if not shipment:
        return {"success": False, "error": "Shipment not found"}

    from services.document_generator import generate_single
    
    shipment_data = _shipment_to_dict(shipment)
    generated = generate_single(shipment_data, doc_type)
    if not generated:
        return {"success": False, "error": f"Failed to generate {doc_type}"}

    doc_repo = GeneratedDocumentRepository(db)
    
    existing = doc_repo.list_by_shipment(shipment_id)
    record = None
    for d in existing:
        if d.doc_type == doc_type:
            record = d
            break
            
    if record:
        record.file_name = generated["file_name"]
        record.file_path = generated["file_path"]
        record.file_format = generated["file_format"]
        db.commit()
    else:
        record = doc_repo.create(
            shipment_id=shipment_id,
            doc_type=generated["doc_type"],
            file_name=generated["file_name"],
            file_path=generated["file_path"],
            file_format=generated["file_format"],
        )
        
    return {"success": True, "file_path": record.file_path}


def get_document_path(shipment_id: str, doc_type: str, db: Session) -> str | None:
    doc_repo = GeneratedDocumentRepository(db)
    for d in doc_repo.list_by_shipment(shipment_id):
        if d.doc_type == doc_type:
            p = Path(d.file_path)
            if p.exists():
                return str(p)
    return None


def get_zip_path(shipment_id: str, db: Session) -> str | None:
    s_repo = ShipmentRepository(db)
    shipment = s_repo.get_by_id(shipment_id)
    if not shipment:
        return None
    try:
        return create_zip(shipment_id, shipment.shipment_number)
    except Exception as e:
        print(f"[ShipmentService] ZIP error: {e}")
        return None
