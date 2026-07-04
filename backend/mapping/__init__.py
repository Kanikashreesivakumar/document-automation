"""
Mapping module — converts a single ShipmentFull dict into a template context dict.

Architecture rules:
  • This is the ONLY place where DB field names are mapped to template variable names.
  • Static exporter constants live here — never in the DB, never in the form.
  • Every document generator calls one of these functions to get its context.
  • Adding a new document = adding a new function here. The DB schema never changes.
  • No database imports. No calculation logic. Pure data transformation.

Only 6 documents are registered:
  invoice, packing_list, proforma_invoice, trade_facility, export_insurance, health_certificate
"""
from typing import Any, Optional


# ─── Static exporter constants ────────────────────────────────────────────────
EXPORTER = {
    "name":    "RASI FOODS",
    "address": "NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA",
    "email":   "rasieggs@gmail.com",
    "gstin":   "33AASFR2685Q1Z8",
    "pan":     "AASFR2685Q",
    "hsn":     "04072100",
    "iec":     "3215008319",
}

STATIC_PRODUCT = {
    "description": "FRESH WHITE SHELL TABLE EGGS (CHICKEN). This shipment to covering under DBK scheme.",
    "dbk_clause":  "This shipment to covering under DBK scheme.",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _s(val: Any, default: str = "") -> str:
    if val is None:
        return default
    return str(val).strip() or default


def _fmt_number(val: Any, decimals: int = 2) -> str:
    if val is None:
        return ""
    try:
        return f"{float(val):,.{decimals}f}"
    except (ValueError, TypeError):
        return str(val)


def _fmt_int(val: Any) -> str:
    if val is None:
        return ""
    try:
        return f"{int(val):,}"
    except (ValueError, TypeError):
        return str(val)


# ─── Base context builder ─────────────────────────────────────────────────────

def _build_base_context(shipment: dict) -> dict:
    inv  = shipment.get("invoice_info") or {}
    buy  = shipment.get("buyer") or {}
    det  = shipment.get("shipment_details") or {}
    prod = shipment.get("product") or {}
    pkg  = shipment.get("package") or {}
    pri  = shipment.get("pricing") or {}
    wt   = shipment.get("weight") or {}
    tf   = shipment.get("trade_facility") or {}
    ei   = shipment.get("export_insurance") or {}
    ac   = shipment.get("animal_certificate") or {}
    aa   = shipment.get("animal_annexure") or {}
    pi   = shipment.get("proforma_invoice") or {}

    # Extract required values for dynamic Description of Goods
    cartons_str = str(pkg.get("cartons") or 0)
    trays_per_carton_str = str(pkg.get("trays_per_carton") or 0)
    eggs_per_tray_str = str(pkg.get("eggs_per_tray") or 0)
    eggs_per_carton_str = str(pkg.get("eggs_per_carton") or 0)
    total_eggs_str = str(pkg.get("total_eggs") or 0)
    
    shipment_decl = _s(prod.get("shipment_declaration"), STATIC_PRODUCT["dbk_clause"])
    container_type = _s(prod.get("container_type"))
    pan_no = _s(prod.get("pan_number"), EXPORTER["pan"])
    gstin_no = _s(prod.get("gstin"), EXPORTER["gstin"])
    hsn_code = _s(prod.get("hsn_code"), EXPORTER["hsn"])
    egg_size = _s(prod.get("egg_size"), "50 TO 55 GMS")
    production_date = _s(prod.get("production_date")) or _s(pi.get("expiry_date"))
    expiry_date = _s(prod.get("expiry_date")) or _s(pi.get("expiry_date"))
    lot_number = _s(prod.get("lot_number"))
    epcg_licence_no = _s(prod.get("epcg_licence_number"))
    dt = _s(prod.get("dt"))

    description_of_goods_text = f"""FRESH WHITE SHELL TABLE EGGS (CHICKEN).
{shipment_decl}
TOTAL {cartons_str} CARTONS,
{trays_per_carton_str} TRAYS IN EACH CARTON

{eggs_per_tray_str} EGGS IN EACH TRAY
{eggs_per_carton_str} EGGS IN EACH BOX

EACH CARTON PRINTED WITH
PRODUCTION DATE & EXPIRY DATE.

TOTAL {cartons_str} X {eggs_per_carton_str}
=
{total_eggs_str} EGGS

{container_type}

PAN No:
{pan_no}

GSTIN No:
{gstin_no}

HSN CODE:
{hsn_code}

EGG SIZE:
{egg_size}

DATE OF PRODUCTION:
{production_date}

DATE OF EXPIRY:
{expiry_date}

LOT NO:
{lot_number}

EPCG LICENCE NO:
{epcg_licence_no}

DT:
{dt}"""

    return {
        "shipment_number": _s(shipment.get("shipment_number")),
        
        "exporter_name":    EXPORTER["name"],
        "exporter_address": EXPORTER["address"],
        "exporter_email":   EXPORTER["email"],
        "exporter_gstin":   EXPORTER["gstin"],
        "exporter_pan":     EXPORTER["pan"],
        "exporter_hsn":     EXPORTER["hsn"],
        "exporter_iec":     EXPORTER["iec"],
        "iec_no":           EXPORTER["iec"],

        # Invoice Info
        "invoice_no":                    _s(inv.get("invoice_no")),
        "invoice_date":                  _s(inv.get("invoice_date")),
        "buyer_order_no_date":           _s(inv.get("buyer_order_no_date")),
        "reference_proforma_invoice_no": _s(inv.get("reference_proforma_invoice_no")),
        "shipping_bill_no":              _s(inv.get("shipping_bill_no")),
        "shipping_bill_date":            _s(inv.get("shipping_bill_date")),
        "exporter_reference":            _s(inv.get("exporter_reference")),
        "other_reference":               _s(inv.get("other_reference")),

        # Buyer / Consignee
        "consignee_name":   _s(buy.get("consignee_name")),
        "consignee_address":_s(buy.get("buyer_address")), 
        "buyer_name":       _s(buy.get("buyer_name")),
        "buyer_address":    _s(buy.get("buyer_address")),
        "buyer_postal_code":_s(buy.get("buyer_postal_code")),
        "buyer_country":    _s(buy.get("buyer_country")),
        "importer_name":    _s(buy.get("consignee_name")),
        "importer_address": _s(buy.get("buyer_address")),
        "addressee":        _s(buy.get("consignee_name")),

        # Shipment Details
        "pre_carriage_by":              _s(det.get("pre_carriage_by")),
        "vessel_flight_no":             _s(det.get("vessel_flight_no")),
        "place_of_receipt":             _s(det.get("place_of_receipt")),
        "port_of_loading":              _s(det.get("port_of_loading")),
        "port_of_discharge":            _s(det.get("port_of_discharge")),
        "final_destination":            _s(det.get("final_destination")),
        "country_of_origin":            _s(det.get("country_of_origin")),
        "country_of_destination":       _s(det.get("country_of_final_destination")),
        "destination_country":          _s(det.get("country_of_final_destination")),
        "terms_of_delivery":            _s(det.get("terms_of_delivery")),
        "means_of_transport":           _s(det.get("pre_carriage_by")) or "REEFER CONTAINER",

        # Product & Package
        "brand_name":     _s(prod.get("brand_name")),
        "product_name":   _s(prod.get("product_name"), STATIC_PRODUCT["description"]),
        "description_of_goods": description_of_goods_text,
        "shipment_declaration": shipment_decl,
        "container_type": _s(prod.get("container_type")),
        "container_no":   _s(prod.get("container_no")),
        "hsn_code":       _s(prod.get("hsn_code"), EXPORTER["hsn"]),
        "pan_number":     _s(prod.get("pan_number"), EXPORTER["pan"]),
        "gstin":          _s(prod.get("gstin"), EXPORTER["gstin"]),
        "exporter_hsn":   _s(prod.get("hsn_code"), EXPORTER["hsn"]),
        "exporter_pan":   _s(prod.get("pan_number"), EXPORTER["pan"]),
        "exporter_gstin": _s(prod.get("gstin"), EXPORTER["gstin"]),
        "egg_size":       _s(prod.get("egg_size"), "50 TO 55 GMS"),
        "lot_number":     _s(prod.get("lot_number")),
        "epcg_licence_number": _s(prod.get("epcg_licence_number")),
        "dt":             _s(prod.get("dt")),
        
        "total_cartons":     str(pkg.get("cartons") or 0),
        "cartons":           str(pkg.get("cartons") or 0),
        "number_of_cartons": str(pkg.get("cartons") or 0),
        "total_packages":    str(pkg.get("cartons") or 0),
        "packages_in_container": f"{pkg.get('cartons') or 0} CARTONS",
        "type_of_packing":   "CARTON",
        "total_eggs":        str(pkg.get("total_eggs") or 0),
        
        # Pricing & Weight
        "rate_per_egg_usd":     _fmt_number(pri.get("rate_per_egg_usd"), 6),
        "amount_usd":           _fmt_number(pri.get("amount_usd"), 2),
        "amount_in_words":      _s(pri.get("amount_in_words")),
        "net_weight":               _fmt_number(wt.get("net_weight"), 3),
        "gross_weight":             _fmt_number(wt.get("gross_weight"), 3),
        "gross_weight_per_egg":     _fmt_number(wt.get("gross_weight_per_carton"), 3),

        # Trade Facility specifics
        "seal_no":        _s(tf.get("seal_number")),
        "seal_nos":       _s(tf.get("seal_number")),
        "truck_no":       _s(tf.get("truck_number")),
        "branch_code": _s(tf.get("branch_code")),
        "bin_number": _s(tf.get("bin_number")),
        "date_of_examination": _s(tf.get("date_of_examination")),
        "starting_time": _s(tf.get("starting_time")),
        "completion_time": _s(tf.get("completion_time")),
        "time_taken": _s(tf.get("time_taken")),
        "description_of_cargo": f"FRESH WHITE SHELL EGG  /{pkg.get('cartons') or 0} CARTONS",
        "signatory_name": _s(tf.get("signatory_name")),
        "signatory_designation": _s(tf.get("signatory_designation")),
        "container_to_cfs_time": _s(tf.get("container_to_cfs_start_time")),
        "e_seal_number": _s(tf.get("seal_number")),
        "e_seal_colour": "White",
        "goods_description_verified": _s(tf.get("goods_description_verified"), "Yes"),
        "container_size": _s(prod.get("container_type")),

        # Export Insurance specifics
        "date": _s(ei.get("date")),
        "sum_assured": _s(ei.get("sum_assured")),
        "dollar_value": _s(ei.get("dollar_value")),
        "quantity_of_goods": f"{pkg.get('cartons') or 0} CARTONS",
        "port_of_delivery": _s(ei.get("port_of_delivery")) or _s(det.get("port_of_discharge")),
        "risk_cover": _s(ei.get("risk_cover"), "ICCA"),
        "place_of_loading": _s(det.get("port_of_loading"), "Rasi Foods"),
        "name_of_goods": _s(prod.get("product_name"), "Fresh white shell table eggs(chicken)."),
        "respected_sir": _s(ei.get("respected_sir")),

        # Health Certificate specifics
        "serial_no": _s(ac.get("serial_no")),
        "issue_date": _s(ac.get("issue_date")),
        "date_of_inspection": _s(ac.get("date_of_inspection")),
        "vet_officer_name": _s(ac.get("vet_officer_name")),
        "vet_officer_designation": _s(ac.get("vet_officer_designation")),
        "issuing_dept": "Department of Animal Husbandry",
        "issuing_district": "Namakkal",
        "issuing_govt": "Government of Tamil Nadu",
        "port_of_shipment": _s(det.get("port_of_loading")),
        
        # Animal Annexure specifics
        "producer_name": _s(aa.get("producer_name")),
        "producer_address": _s(aa.get("producer_address")),
        "certificate_no": _s(aa.get("certificate_number")),
        "date_of_issue": _s(aa.get("date_of_issue")),
        
        # Proforma & Annexure
        "proforma_invoice_no": _s(pi.get("proforma_invoice_number")),
        "po_number": _s(pi.get("po_number")),
        "po_date": _s(pi.get("po_date")),
        "buyer_trn": _s(pi.get("buyer_trn")),
        "consignee_trn": _s(pi.get("consignee_trn")),
        "notify_party": _s(pi.get("notify_party")),
        "notify_party_address": _s(pi.get("notify_party_address")),
        "payment_terms": _s(pi.get("payment_terms")),
        "expiry_date": _s(prod.get("expiry_date")) or _s(pi.get("expiry_date")),
        "no_and_kind_of_packages": _s(pi.get("no_and_kind_of_packages")),
        "intermediate_bank_name": _s(pi.get("intermediate_bank_name")),
        "intermediate_bank_account_number": _s(pi.get("intermediate_bank_account_number")),
        "intermediate_bank_swift": _s(pi.get("intermediate_bank_swift")),
        "intermediate_bank_routing_number": _s(pi.get("intermediate_bank_routing_number")),
        "correspondent_bank": _s(pi.get("correspondent_bank")),
        "production_date": _s(prod.get("production_date")) or _s(pi.get("expiry_date")),
    }

def invoice_context(shipment: dict) -> dict:
    return _build_base_context(shipment)

def packing_list_context(shipment: dict) -> dict:
    return _build_base_context(shipment)

def proforma_invoice_context(shipment: dict) -> dict:
    return _build_base_context(shipment)

def trade_facility_context(shipment: dict) -> dict:
    return _build_base_context(shipment)

def export_insurance_context(shipment: dict) -> dict:
    return _build_base_context(shipment)

def health_certificate_context(shipment: dict) -> dict:
    return _build_base_context(shipment)

CONTEXT_BUILDERS = {
    "invoice": invoice_context,
    "packing_list": packing_list_context,
    "proforma_invoice": proforma_invoice_context,
    "trade_facility": trade_facility_context,
    "export_insurance": export_insurance_context,
    "health_certificate": health_certificate_context,
}

def get_context(doc_type: str, shipment_data: dict) -> dict:
    builder = CONTEXT_BUILDERS.get(doc_type)
    if not builder:
        raise ValueError(f"No context builder found for document type: {doc_type}")
    return builder(shipment_data)
