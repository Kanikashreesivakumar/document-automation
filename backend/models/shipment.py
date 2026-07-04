"""
SQLAlchemy ORM models — normalized schema.

Design principles:
  • Every data element exists EXACTLY ONCE in the database.
  • 7 normalized tables hold all shipment data (one record per shipment each).
  • The existing 5 document tables (vet_certificate, vet_annexure,
    insurance_letter, examination_report, export_declaration) are unchanged.
  • GeneratedDocument is unchanged.
  • Adding a new export document NEVER requires adding columns here —
    the mapping layer handles the projection.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Text,
    DateTime, ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base


def _gen_uuid() -> str:
    return str(uuid.uuid4())


# ─── Shipment (root record) ────────────────────────────────────────────────────

class Shipment(Base):
    __tablename__ = "shipments"

    id              = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_number = Column(String(50), unique=True, nullable=False, index=True)
    status          = Column(String(30), default="draft")   # draft | in_progress | complete
    created_at      = Column(DateTime, default=datetime.utcnow)
    updated_at      = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ── Normalized sub-records (one-to-one) ───────────────────────────────────
    invoice_info     = relationship("InvoiceInfo",     back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    proforma_invoice = relationship("ProformaInvoice", back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    buyer            = relationship("Buyer",           back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    shipment_details = relationship("ShipmentDetails", back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    product          = relationship("Product",         back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    package          = relationship("Package",         back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    pricing          = relationship("Pricing",         back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    weight           = relationship("Weight",          back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    trade_facility   = relationship("TradeFacility",   back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    export_insurance = relationship("ExportInsurance",  back_populates="shipment", uselist=False, cascade="all, delete-orphan")
    animal_certificate = relationship("AnimalCertificate", back_populates="shipment", uselist=False, cascade="all, delete-orphan")

    animal_annexure = relationship("AnimalAnnexure", back_populates="shipment", uselist=False, cascade="all, delete-orphan")

    generated_documents = relationship("GeneratedDocument", back_populates="shipment", cascade="all, delete-orphan")


# ─── Normalized shipment data tables ──────────────────────────────────────────

class AnimalCertificate(Base):
    __tablename__ = "animal_certificates"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    serial_no               = Column(String(100))
    issue_date              = Column(String(50))
    date_of_inspection      = Column(String(50))
    vet_officer_name        = Column(String(200))
    vet_officer_designation = Column(String(200))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="animal_certificate")


class InvoiceInfo(Base):
    """Invoice header fields entered by the user."""
    __tablename__ = "invoice_info"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    invoice_no                   = Column(String(100))
    invoice_date                 = Column(String(20))
    buyer_order_no_date          = Column(String(200))
    reference_proforma_invoice_no = Column(String(200))
    shipping_bill_no             = Column(String(100))
    shipping_bill_date           = Column(String(20))
    exporter_reference           = Column(String(200))
    other_reference              = Column(String(200))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="invoice_info")


class ProformaInvoice(Base):
    __tablename__ = "proforma_invoices"
    id = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)
    
    po_number = Column(String(100))
    po_date = Column(String(20))
    proforma_invoice_number = Column(String(100))
    buyer_trn = Column(String(100))
    consignee_trn = Column(String(100))
    notify_party = Column(String(300))
    notify_party_address = Column(Text)
    payment_terms = Column(String(200))
    expiry_date = Column(String(20))
    no_and_kind_of_packages = Column(String(200))
    intermediate_bank_name = Column(String(200))
    intermediate_bank_account_number = Column(String(100))
    intermediate_bank_swift = Column(String(100))
    intermediate_bank_routing_number = Column(String(100))
    correspondent_bank = Column(String(200))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="proforma_invoice")


class TradeFacility(Base):
    __tablename__ = "trade_facilities"
    id = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)
    
    date_of_examination = Column(String(50))
    stuffing_start_time = Column(String(50))
    stuffing_completion_time = Column(String(50))
    stuffing_duration = Column(String(50))
    authorized_signatory_name = Column(String(200))
    authorized_signatory_designation = Column(String(200))
    seal_number = Column(String(100))
    truck_number = Column(String(100))
    container_to_cfs_start_time = Column(String(50))
    e_seal_number = Column(String(100))
    goods_description_verified = Column(String(10), default="Yes")
    branch_code = Column(String(100))
    bin_number = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="trade_facility")


class ExportInsurance(Base):
    """Export Insurance letter fields — only fields NOT in Shipment."""
    __tablename__ = "export_insurances"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    date                 = Column(String(50))
    respected_sir        = Column(String(200))
    marine_policy_number = Column(String(100))
    cif_policy_number    = Column(String(100))
    risk_cover           = Column(String(100), default="ICCA")
    importer_name        = Column(String(300))
    importer_address     = Column(Text)
    sum_assured          = Column(String(200))
    dollar_value         = Column(String(200))
    port_of_delivery     = Column(String(200))
    insurance_remarks    = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="export_insurance")


class Buyer(Base):
    """Consignee / buyer details."""
    __tablename__ = "buyers"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    consignee_name  = Column(String(300))
    buyer_name      = Column(String(300))
    buyer_address   = Column(Text)
    buyer_postal_code = Column(String(20))
    buyer_country   = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="buyer")


class ShipmentDetails(Base):
    """Transport / routing details."""
    __tablename__ = "shipment_details"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    pre_carriage_by              = Column(String(100))
    vessel_flight_no             = Column(String(100))
    place_of_receipt             = Column(String(100))
    port_of_loading              = Column(String(100))
    port_of_discharge            = Column(String(100))
    final_destination            = Column(String(200))
    country_of_origin            = Column(String(100))
    country_of_final_destination = Column(String(100))
    terms_of_delivery            = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="shipment_details")


class Product(Base):
    """Product / container identity."""
    __tablename__ = "products"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    brand_name     = Column(String(100))
    product_name   = Column(String(200))
    container_type = Column(String(100))
    container_no   = Column(String(100))
    
    shipment_declaration = Column(Text)
    production_date      = Column(String(50))
    expiry_date          = Column(String(50))
    lot_number           = Column(String(100))
    epcg_licence_number  = Column(String(100))
    dt                   = Column(String(100))
    egg_size             = Column(String(100))
    pan_number           = Column(String(100))
    gstin                = Column(String(100))
    hsn_code             = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="product")


class Package(Base):
    """Packaging quantities — inputs + auto-calculated fields stored for reference."""
    __tablename__ = "packages"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    # User inputs
    cartons         = Column(Integer)
    trays_per_carton = Column(Integer)
    eggs_per_tray   = Column(Integer)

    # Auto-calculated (stored for audit / downstream docs)
    eggs_per_carton = Column(Integer)
    total_eggs      = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="package")


class Pricing(Base):
    """Pricing — user input rate + auto-calculated totals."""
    __tablename__ = "pricings"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    # User input
    rate_per_egg_usd = Column(Float)

    # Auto-calculated
    amount_usd      = Column(Float)
    amount_in_words = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="pricing")


class Weight(Base):
    """Weight per carton (user input) + totals (calculated)."""
    __tablename__ = "weights"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    # User inputs
    net_weight_per_carton   = Column(Float)
    gross_weight_per_carton = Column(Float)

    # Auto-calculated
    net_weight   = Column(Float)
    gross_weight = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="weight")


class AnimalAnnexure(Base):
    __tablename__ = "animal_annexures"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False, unique=True)

    producer_name    = Column(String(300))
    producer_address = Column(Text)
    certificate_number = Column(String(100))
    date_of_issue    = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="animal_annexure")


# ─── Generated Document Registry ──────────────────────────────────────────────

class GeneratedDocument(Base):
    __tablename__ = "generated_documents"

    id          = Column(UUID(as_uuid=False), primary_key=True, default=_gen_uuid)
    shipment_id = Column(UUID(as_uuid=False), ForeignKey("shipments.id"), nullable=False)
    doc_type    = Column(String(50))       # invoice | packing_list | vet_certificate | …
    file_name   = Column(String(300))
    file_path   = Column(String(500))
    file_format = Column(String(10))       # docx | pdf
    generated_at = Column(DateTime, default=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="generated_documents")
