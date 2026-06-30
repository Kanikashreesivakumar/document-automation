"""
Shipment controller — thin layer between routes and services.
No business logic. Just calls the appropriate service function.
"""
from sqlalchemy.orm import Session
from schemas.shipment import (
    ShipmentDataCreate, ProformaInvoiceCreate, TradeFacilityCreate, ExportInsuranceCreate,
    AnimalCertificateCreate, AnimalAnnexureCreate,
)
import services.shipment_service as svc


def create_shipment_ctrl(db: Session):
    return svc.create_shipment(db)


def list_shipments_ctrl(db: Session):
    return svc.list_shipments(db)


def get_shipment_ctrl(shipment_id: str, db: Session):
    return svc.get_shipment(shipment_id, db)


def delete_shipment_ctrl(shipment_id: str, db: Session):
    return svc.delete_shipment(shipment_id, db)


def get_recent_documents_ctrl(db: Session):
    return svc.get_recent_documents(db)


# ── Unified shipment data ──────────────────────────────────────────────────────
def save_shipment_data_ctrl(shipment_id: str, data: ShipmentDataCreate, db: Session):
    return svc.save_shipment_data(shipment_id, data, db)


def save_proforma_invoice_ctrl(shipment_id: str, data: ProformaInvoiceCreate, db: Session):
    return svc.save_proforma_invoice(shipment_id, data, db)


def get_proforma_invoice_ctrl(shipment_id: str, db: Session):
    return svc.get_proforma_invoice(shipment_id, db)


def save_trade_facility_ctrl(shipment_id: str, data: TradeFacilityCreate, db: Session):
    return svc.save_trade_facility(shipment_id, data, db)


def get_trade_facility_ctrl(shipment_id: str, db: Session):
    return svc.get_trade_facility(shipment_id, db)


def save_export_insurance_ctrl(shipment_id: str, data: ExportInsuranceCreate, db: Session):
    return svc.save_export_insurance(shipment_id, data, db)


def get_export_insurance_ctrl(shipment_id: str, db: Session):
    return svc.get_export_insurance(shipment_id, db)


def save_animal_certificate_ctrl(shipment_id: str, data: AnimalCertificateCreate, db: Session):
    return svc.save_animal_certificate(shipment_id, data, db)


def get_animal_certificate_ctrl(shipment_id: str, db: Session):
    return svc.get_animal_certificate(shipment_id, db)


# ── Animal Annexure ───────────────────────────────────────────────────────────
def save_animal_annexure_ctrl(shipment_id: str, data: AnimalAnnexureCreate, db: Session):
    return svc.save_animal_annexure(shipment_id, data, db)


def get_animal_annexure_ctrl(shipment_id: str, db: Session):
    return svc.get_animal_annexure(shipment_id, db)


# ── Generation & download ──────────────────────────────────────────────────────
def generate_documents_ctrl(shipment_id: str, db: Session):
    return svc.generate_documents(shipment_id, db)


def get_document_path_ctrl(shipment_id: str, doc_type: str, db: Session):
    return svc.get_document_path(shipment_id, doc_type, db)


def get_zip_path_ctrl(shipment_id: str, db: Session):
    return svc.get_zip_path(shipment_id, db)
