"""
Pydantic schemas — input validation and output serialization.

Design:
  • ShipmentDataCreate  — the single unified POST body (27 user-editable fields)
  • Individual Read schemas — one per normalized model (for GET responses)
  • ShipmentFull — aggregated response for GET /api/shipments/{id}
"""
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


# ─── Shipment ─────────────────────────────────────────────────────────────────

class ShipmentRead(BaseModel):
    id: str
    shipment_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ShipmentListItem(BaseModel):
    id: str
    shipment_number: str
    status: str
    created_at: datetime
    invoice_no: Optional[str] = None
    model_config = {"from_attributes": True}


# ─── Unified input (27 user-editable fields only) ─────────────────────────────

class ShipmentDataCreate(BaseModel):
    """
    Single POST body for all user-editable shipment data.
    Static fields (exporter, GSTIN, HSN, etc.) are NEVER included here —
    they come from the mapping layer's STATIC_EXPORTER constant.
    Auto-calculated fields are NEVER included here — the service computes them.
    """

    # Invoice Info
    invoice_no: Optional[str] = None
    invoice_date: Optional[str] = None
    buyer_order_no_date: Optional[str] = None
    reference_proforma_invoice_no: Optional[str] = None
    shipping_bill_no: Optional[str] = None
    shipping_bill_date: Optional[str] = None
    exporter_reference: Optional[str] = None
    other_reference: Optional[str] = None

    # Buyer / Consignee
    consignee_name: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_address: Optional[str] = None
    buyer_postal_code: Optional[str] = None
    buyer_country: Optional[str] = None

    # Shipment Details
    pre_carriage_by: Optional[str] = None
    vessel_flight_no: Optional[str] = None
    place_of_receipt: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    final_destination: Optional[str] = None
    country_of_origin: Optional[str] = None
    country_of_final_destination: Optional[str] = None
    terms_of_delivery: Optional[str] = None

    # Product
    brand_name: Optional[str] = None
    product_name: Optional[str] = None
    container_type: Optional[str] = None
    container_no: Optional[str] = None
    
    shipment_declaration: Optional[str] = None
    production_date: Optional[str] = None
    expiry_date: Optional[str] = None
    production_duration: Optional[str] = None
    lot_number: Optional[str] = None
    epcg_licence_number: Optional[str] = None
    dt: Optional[str] = None
    egg_size: Optional[str] = None
    pan_number: Optional[str] = None
    gstin: Optional[str] = None
    hsn_code: Optional[str] = None

    # Package (user inputs only; eggs_per_carton & total_eggs are calculated)
    cartons: Optional[int] = None
    trays_per_carton: Optional[int] = None
    eggs_per_tray: Optional[int] = None

    # Pricing (rate only; amount_usd & amount_in_words are calculated)
    rate_per_egg_usd: Optional[float] = None

    # Weight (per-carton only; net_weight & gross_weight are calculated)
    net_weight_per_carton: Optional[float] = None
    gross_weight_per_carton: Optional[float] = None


# ─── Read schemas for normalized sub-models ───────────────────────────────────

class InvoiceInfoRead(BaseModel):
    id: str
    shipment_id: str
    invoice_no: Optional[str] = None
    invoice_date: Optional[str] = None
    buyer_order_no_date: Optional[str] = None
    reference_proforma_invoice_no: Optional[str] = None
    shipping_bill_no: Optional[str] = None
    shipping_bill_date: Optional[str] = None
    exporter_reference: Optional[str] = None
    other_reference: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ProformaInvoiceCreate(BaseModel):
    po_number: Optional[str] = None
    po_date: Optional[str] = None
    proforma_invoice_number: Optional[str] = None
    buyer_trn: Optional[str] = None
    consignee_trn: Optional[str] = None
    notify_party: Optional[str] = None
    notify_party_address: Optional[str] = None
    payment_terms: Optional[str] = None
    expiry_date: Optional[str] = None
    no_and_kind_of_packages: Optional[str] = None
    intermediate_bank_name: Optional[str] = None
    intermediate_bank_account_number: Optional[str] = None
    intermediate_bank_swift: Optional[str] = None
    intermediate_bank_routing_number: Optional[str] = None
    correspondent_bank: Optional[str] = None

    # Company bank details (user-editable; defaults come from frontend pre-fill)
    company_account_name:   Optional[str] = None
    company_account_number: Optional[str] = None
    company_bank_name:      Optional[str] = None
    company_branch:         Optional[str] = None
    company_swift:          Optional[str] = None


class ProformaInvoiceRead(ProformaInvoiceCreate):
    id: str
    shipment_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class TradeFacilityCreate(BaseModel):
    date_of_examination: Optional[str] = None
    stuffing_start_time: Optional[str] = None
    stuffing_completion_time: Optional[str] = None
    stuffing_duration: Optional[str] = None
    authorized_signatory_name: Optional[str] = None
    authorized_signatory_designation: Optional[str] = None
    seal_number: Optional[str] = None
    truck_number: Optional[str] = None
    container_to_cfs_start_time: Optional[str] = None
    e_seal_number: Optional[str] = None
    goods_description_verified: Optional[str] = "Yes"
    branch_code: Optional[str] = None
    bin_number: Optional[str] = None


class TradeFacilityRead(TradeFacilityCreate):
    id: str
    shipment_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ExportInsuranceCreate(BaseModel):
    date: Optional[str] = None
    respected_sir: Optional[str] = None
    marine_policy_number: Optional[str] = None
    cif_policy_number: Optional[str] = None
    risk_cover: Optional[str] = "ICCA"
    importer_name: Optional[str] = None
    importer_address: Optional[str] = None
    sum_assured: Optional[str] = None
    dollar_value: Optional[str] = None
    port_of_delivery: Optional[str] = None


class ExportInsuranceRead(ExportInsuranceCreate):
    id: str
    shipment_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class AnimalCertificateCreate(BaseModel):
    serial_no: Optional[str] = None
    issue_date: Optional[str] = None
    date_of_inspection: Optional[str] = None
    vet_officer_name: Optional[str] = None
    vet_officer_designation: Optional[str] = None


class AnimalCertificateRead(AnimalCertificateCreate):
    id: str
    shipment_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class BuyerRead(BaseModel):
    id: str
    shipment_id: str
    consignee_name: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_address: Optional[str] = None
    buyer_postal_code: Optional[str] = None
    buyer_country: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ShipmentDetailsRead(BaseModel):
    id: str
    shipment_id: str
    pre_carriage_by: Optional[str] = None
    vessel_flight_no: Optional[str] = None
    place_of_receipt: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    final_destination: Optional[str] = None
    country_of_origin: Optional[str] = None
    country_of_final_destination: Optional[str] = None
    terms_of_delivery: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ProductRead(BaseModel):
    id: str
    shipment_id: str
    brand_name: Optional[str] = None
    product_name: Optional[str] = None
    container_type: Optional[str] = None
    container_no: Optional[str] = None
    shipment_declaration: Optional[str] = None
    production_date: Optional[str] = None
    expiry_date: Optional[str] = None
    production_duration: Optional[str] = None
    lot_number: Optional[str] = None
    epcg_licence_number: Optional[str] = None
    dt: Optional[str] = None
    egg_size: Optional[str] = None
    pan_number: Optional[str] = None
    gstin: Optional[str] = None
    hsn_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class PackageRead(BaseModel):
    id: str
    shipment_id: str
    cartons: Optional[int] = None
    trays_per_carton: Optional[int] = None
    eggs_per_tray: Optional[int] = None
    eggs_per_carton: Optional[int] = None
    total_eggs: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class PricingRead(BaseModel):
    id: str
    shipment_id: str
    rate_per_egg_usd: Optional[float] = None
    amount_usd: Optional[float] = None
    amount_in_words: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class WeightRead(BaseModel):
    id: str
    shipment_id: str
    net_weight_per_carton: Optional[float] = None
    gross_weight_per_carton: Optional[float] = None
    net_weight: Optional[float] = None
    gross_weight: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


# ─── New Animal Annexure ───────────────────────────────────────────────────────

class AnimalAnnexureCreate(BaseModel):
    producer_name: Optional[str] = None
    producer_address: Optional[str] = None
    certificate_number: Optional[str] = None
    date_of_issue: Optional[str] = None


class AnimalAnnexureRead(AnimalAnnexureCreate):
    id: str
    shipment_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


# ─── Generated Document ────────────────────────────────────────────────────────

class GeneratedDocumentRead(BaseModel):
    id: str
    doc_type: str
    file_name: str
    file_format: str
    generated_at: datetime
    model_config = {"from_attributes": True}


# ─── Aggregated Full Shipment Response ────────────────────────────────────────

class ShipmentFull(BaseModel):
    """Complete shipment record — all normalized sub-models aggregated."""
    id: str
    shipment_number: str
    status: str
    created_at: datetime
    updated_at: datetime

    # Normalized tables
    invoice_info: Optional[InvoiceInfoRead] = None
    proforma_invoice: Optional[ProformaInvoiceRead] = None
    buyer: Optional[BuyerRead] = None
    shipment_details: Optional[ShipmentDetailsRead] = None
    product: Optional[ProductRead] = None
    package: Optional[PackageRead] = None
    pricing: Optional[PricingRead] = None
    weight: Optional[WeightRead] = None

    # New
    trade_facility: Optional[TradeFacilityRead] = None
    export_insurance: Optional[ExportInsuranceRead] = None
    animal_certificate: Optional[AnimalCertificateRead] = None
    animal_annexure: Optional[AnimalAnnexureRead] = None
    generated_documents: List[GeneratedDocumentRead] = []

    model_config = {"from_attributes": True}
