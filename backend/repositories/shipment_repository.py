"""
Repository layer — all database I/O for shipments.

Rules:
  • No business logic here. No calculations here.
  • Each repository exposes only upsert() and get() for its table.
  • The generic _upsert() helper handles insert-or-update transparently.
"""
from sqlalchemy.orm import Session
from models.shipment import (
    Shipment, ProformaInvoice, TradeFacility, ExportInsurance,
    InvoiceInfo, Buyer, ShipmentDetails, Product, Package, Pricing, Weight,
    AnimalCertificate, AnimalAnnexure, GeneratedDocument,
)
from typing import Optional, List


# ─── Generic upsert helper ────────────────────────────────────────────────────

def _upsert(db: Session, model_cls, shipment_id: str, data: dict):
    """
    Insert or update a single normalized record linked to a shipment.
    Skips None values on update so partial payloads don't overwrite existing data.
    """
    obj = db.query(model_cls).filter(model_cls.shipment_id == shipment_id).first()
    if obj is None:
        obj = model_cls(shipment_id=shipment_id, **{k: v for k, v in data.items() if v is not None})
        db.add(obj)
    else:
        for k, v in data.items():
            if v is not None:
                setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def _upsert_full(db: Session, model_cls, shipment_id: str, data: dict):
    """
    Insert or update — writes ALL fields including None (full replacement).
    Used when calculated fields must be stored as None until computed.
    """
    obj = db.query(model_cls).filter(model_cls.shipment_id == shipment_id).first()
    if obj is None:
        obj = model_cls(shipment_id=shipment_id, **data)
        db.add(obj)
    else:
        for k, v in data.items():
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


# ─── Shipment ─────────────────────────────────────────────────────────────────

class ShipmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, shipment_number: str) -> Shipment:
        obj = Shipment(shipment_number=shipment_number, status="draft")
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_by_id(self, shipment_id: str) -> Optional[Shipment]:
        return self.db.query(Shipment).filter(Shipment.id == shipment_id).first()

    def list_all(self) -> List[Shipment]:
        return self.db.query(Shipment).order_by(Shipment.created_at.desc()).all()

    def update_status(self, shipment_id: str, status: str) -> Optional[Shipment]:
        obj = self.get_by_id(shipment_id)
        if obj:
            obj.status = status
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def delete(self, shipment_id: str) -> bool:
        """Deletes the shipment and all cascaded children."""
        obj = self.get_by_id(shipment_id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False


# ─── Normalized shipment-data repositories ────────────────────────────────────

class InvoiceInfoRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> InvoiceInfo:
        return _upsert(self.db, InvoiceInfo, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[InvoiceInfo]:
        return self.db.query(InvoiceInfo).filter(InvoiceInfo.shipment_id == shipment_id).first()


class BuyerRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> Buyer:
        return _upsert(self.db, Buyer, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[Buyer]:
        return self.db.query(Buyer).filter(Buyer.shipment_id == shipment_id).first()


class ShipmentDetailsRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> ShipmentDetails:
        return _upsert(self.db, ShipmentDetails, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[ShipmentDetails]:
        return self.db.query(ShipmentDetails).filter(ShipmentDetails.shipment_id == shipment_id).first()


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> Product:
        return _upsert(self.db, Product, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.shipment_id == shipment_id).first()


class PackageRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> Package:
        """
        data must already include calculated eggs_per_carton and total_eggs
        — the service layer is responsible for computing them before calling here.
        """
        return _upsert_full(self.db, Package, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[Package]:
        return self.db.query(Package).filter(Package.shipment_id == shipment_id).first()


class PricingRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> Pricing:
        return _upsert_full(self.db, Pricing, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[Pricing]:
        return self.db.query(Pricing).filter(Pricing.shipment_id == shipment_id).first()


class WeightRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> Weight:
        return _upsert_full(self.db, Weight, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[Weight]:
        return self.db.query(Weight).filter(Weight.shipment_id == shipment_id).first()


class ProformaInvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> ProformaInvoice:
        return _upsert(self.db, ProformaInvoice, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[ProformaInvoice]:
        return self.db.query(ProformaInvoice).filter(ProformaInvoice.shipment_id == shipment_id).first()

    def get_by_shipment_id(self, shipment_id: str) -> Optional[ProformaInvoice]:
        return self.get(shipment_id)


class TradeFacilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> TradeFacility:
        return _upsert(self.db, TradeFacility, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[TradeFacility]:
        return self.db.query(TradeFacility).filter(TradeFacility.shipment_id == shipment_id).first()

    def get_by_shipment_id(self, shipment_id: str) -> Optional[TradeFacility]:
        return self.get(shipment_id)


class ExportInsuranceRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> ExportInsurance:
        return _upsert(self.db, ExportInsurance, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[ExportInsurance]:
        return self.db.query(ExportInsurance).filter(ExportInsurance.shipment_id == shipment_id).first()


class AnimalCertificateRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> AnimalCertificate:
        return _upsert(self.db, AnimalCertificate, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[AnimalCertificate]:
        return self.db.query(AnimalCertificate).filter(AnimalCertificate.shipment_id == shipment_id).first()


class AnimalAnnexureRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, shipment_id: str, data: dict) -> AnimalAnnexure:
        return _upsert(self.db, AnimalAnnexure, shipment_id, data)

    def get(self, shipment_id: str) -> Optional[AnimalAnnexure]:
        return self.db.query(AnimalAnnexure).filter(AnimalAnnexure.shipment_id == shipment_id).first()


# ─── Generated Documents ──────────────────────────────────────────────────────

class GeneratedDocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        shipment_id: str,
        doc_type: str,
        file_name: str,
        file_path: str,
        file_format: str,
    ) -> GeneratedDocument:
        existing = self.db.query(GeneratedDocument).filter(
            GeneratedDocument.shipment_id == shipment_id,
            GeneratedDocument.doc_type == doc_type,
            GeneratedDocument.file_format == file_format,
        ).first()
        if existing:
            existing.file_name = file_name
            existing.file_path = file_path
            self.db.commit()
            self.db.refresh(existing)
            return existing
        obj = GeneratedDocument(
            shipment_id=shipment_id,
            doc_type=doc_type,
            file_name=file_name,
            file_path=file_path,
            file_format=file_format,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list_by_shipment(self, shipment_id: str) -> List[GeneratedDocument]:
        return self.db.query(GeneratedDocument).filter(
            GeneratedDocument.shipment_id == shipment_id
        ).all()
