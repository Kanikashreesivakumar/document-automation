"""
Mapping module — converts a single ShipmentFull dict into a template context dict.

Architecture rules:
  • This is the ONLY place where DB field names are mapped to template variable names.
  • Static exporter constants live here — never in the DB, never in the form.
  • Every document generator calls one of these functions to get its context.
  • Adding a new document = adding a new function here. The DB schema never changes.
  • No database imports. No calculation logic. Pure data transformation.
"""
from typing import Any, Optional


# ─── Static exporter constants ────────────────────────────────────────────────
# These values come from the uploaded template and NEVER change per shipment.
# They are injected here so no user ever needs to type them.

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
    "description": "FRESH WHITE SHELL TABLE EGGS (CHICKEN).",
    "dbk_clause":  "This shipment to covering under DBK scheme.",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _s(val: Any, default: str = "") -> str:
    """Safe string: return str(val) or default if None/empty."""
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
    """
    Build the shared context from a ShipmentFull dict.
    All document-specific mappers call this first, then add their own keys.
    """
    inv  = shipment.get("invoice_info") or {}
    buy  = shipment.get("buyer") or {}
    det  = shipment.get("shipment_details") or {}
    prod = shipment.get("product") or {}
    pkg  = shipment.get("package") or {}
    pri  = shipment.get("pricing") or {}
    wt   = shipment.get("weight") or {}
    tf   = shipment.get("trade_facility") or {}

    # ── Invoice info ──────────────────────────────────────────────────────────
    invoice_no   = _s(inv.get("invoice_no"))
    invoice_date = _s(inv.get("invoice_date"))

    # ── Package quantities ────────────────────────────────────────────────────
    cartons         = pkg.get("cartons") or 0
    trays_per_carton = pkg.get("trays_per_carton") or 0
    eggs_per_tray   = pkg.get("eggs_per_tray") or 0
    eggs_per_carton = pkg.get("eggs_per_carton") or 0
    total_eggs      = pkg.get("total_eggs") or 0

    # ── Pricing ───────────────────────────────────────────────────────────────
    rate_per_egg_usd = pri.get("rate_per_egg_usd") or 0
    amount_usd       = pri.get("amount_usd") or 0
    amount_in_words  = _s(pri.get("amount_in_words"))

    # ── Weight ────────────────────────────────────────────────────────────────
    net_weight_per_carton   = wt.get("net_weight_per_carton") or 0
    gross_weight_per_carton = wt.get("gross_weight_per_carton") or 0
    net_weight   = wt.get("net_weight") or 0
    gross_weight = wt.get("gross_weight") or 0

    return {
        # ── Shipment identity ────────────────────────────────────────────────
        "shipment_number": _s(shipment.get("shipment_number")),

        # ── Static exporter (never from user) ────────────────────────────────
        "exporter_name":    EXPORTER["name"],
        "exporter_address": EXPORTER["address"],
        "exporter_email":   EXPORTER["email"],
        "exporter_gstin":   EXPORTER["gstin"],
        "exporter_pan":     EXPORTER["pan"],
        "exporter_hsn":     EXPORTER["hsn"],
        "exporter_iec":     EXPORTER["iec"],

        # ── Invoice info ─────────────────────────────────────────────────────
        "invoice_no":                    invoice_no,
        "invoice_date":                  invoice_date,
        "buyer_order_no_date":           _s(inv.get("buyer_order_no_date")),
        "reference_proforma_invoice_no": _s(inv.get("reference_proforma_invoice_no")),
        "shipping_bill_no":              _s(inv.get("shipping_bill_no")),
        "shipping_bill_date":            _s(inv.get("shipping_bill_date")),

        # ── Buyer / Consignee ─────────────────────────────────────────────────
        "consignee_name":   _s(buy.get("consignee_name")),
        "buyer_name":       _s(buy.get("buyer_name")),
        "buyer_address":    _s(buy.get("buyer_address")),
        "buyer_postal_code": _s(buy.get("buyer_postal_code")),
        "buyer_country":    _s(buy.get("buyer_country")),

        # ── Shipment details ─────────────────────────────────────────────────
        "pre_carriage_by":              _s(det.get("pre_carriage_by")),
        "vessel_flight_no":             _s(det.get("vessel_flight_no")),
        "place_of_receipt":             _s(det.get("place_of_receipt")),
        "port_of_loading":              _s(det.get("port_of_loading")),
        "port_of_discharge":            _s(det.get("port_of_discharge")),
        "final_destination":            _s(det.get("final_destination")),
        "country_of_origin":            _s(det.get("country_of_origin")),
        "country_of_final_destination": _s(det.get("country_of_final_destination")),
        "terms_of_delivery":            _s(det.get("terms_of_delivery")),

        # ── Product ──────────────────────────────────────────────────────────
        "brand_name":     _s(prod.get("brand_name")),
        "product_name":   _s(prod.get("product_name"), STATIC_PRODUCT["description"]),
        "container_type": _s(prod.get("container_type")),
        "container_no":   _s(prod.get("container_no")),
        
        # ── Global Shared Container Info (from Trade Facility if available) ───
        "seal_no":        _s(tf.get("seal_number")),
        "truck_no":       _s(tf.get("truck_number")),

        # ── Package quantities (raw + formatted) ─────────────────────────────
        "cartons":           str(cartons),
        "trays_per_carton":  str(trays_per_carton),
        "eggs_per_tray":     str(eggs_per_tray),
        "eggs_per_carton":   str(eggs_per_carton),
        "total_eggs":        str(total_eggs),
        "total_eggs_fmt":    _fmt_int(total_eggs),

        # ── Pricing (raw + formatted) ─────────────────────────────────────────
        "rate_per_egg_usd":     _fmt_number(rate_per_egg_usd, 6),
        "amount_usd":           _fmt_number(amount_usd, 2),
        "amount_usd_display":   f"USD {_fmt_number(amount_usd, 2)}",
        "amount_in_words":      amount_in_words,

        # ── Weight (raw + formatted) ──────────────────────────────────────────
        "net_weight_per_carton":    _fmt_number(net_weight_per_carton, 3),
        "gross_weight_per_carton":  _fmt_number(gross_weight_per_carton, 3),
        "net_weight":               _fmt_number(net_weight, 3),
        "gross_weight":             _fmt_number(gross_weight, 3),
        "net_weight_display":       f"{_fmt_number(net_weight, 3)} KGS",
        "gross_weight_display":     f"{_fmt_number(gross_weight, 3)} KGS",

        # ── Static product text ───────────────────────────────────────────────
        "product_description": STATIC_PRODUCT["description"],
        "dbk_clause":          STATIC_PRODUCT["dbk_clause"],
    }


# ─── Document-specific context builders ───────────────────────────────────────

def invoice_context(shipment: dict) -> dict:
    """
    Build the template context dict for the Invoice document.
    The invoice template uses ALL fields from the base context.
    """
    ctx = _build_base_context(shipment)

    pkg = shipment.get("package") or {}
    cartons = pkg.get("cartons") or 0
    eggs_per_carton = pkg.get("eggs_per_carton") or 0
    total_eggs = pkg.get("total_eggs") or 0

    # Invoice-specific compound description line used in the goods table
    ctx["goods_description_line"] = (
        f"{ctx['product_description']} {ctx['dbk_clause']}\n"
        f"TOTAL {cartons} CARTONS, {ctx['trays_per_carton']} TRAYS IN EACH CARTON\n"
        f"{ctx['eggs_per_tray']} EGGS IN EACH TRAY, {eggs_per_carton} EGGS IN EACH BOX\n"
        f"EACH CARTON PRINTED WITH PRODUCTION DATE & EXPIRY DATE.(THREE MONTHS)\n"
        f"TOTAL {cartons} X {eggs_per_carton} = {_fmt_int(total_eggs)} EGGS\n"
        f"{ctx['container_type']} REEFER CONTAINER\n"
        f"Pan No:{ctx['exporter_pan']}\n"
        f"GSTIN No:{ctx['exporter_gstin']}\n"
        f"HSN CODE NO:{ctx['exporter_hsn']}"
    )

    ctx["weight_summary_line"] = (
        f"Each carton — {eggs_per_carton} Nos.\n"
        f"{eggs_per_carton} x {cartons} cartons = Total {_fmt_int(total_eggs)} Nos.\n"
        f"Nett Weight : {ctx['net_weight_display']}\n"
        f"Gross Weight: {ctx['gross_weight_display']}"
    )

    return ctx


def packing_list_context(shipment: dict) -> dict:
    """
    Build the template context dict for the Packing List document.
    Uses the same base — different compound fields.
    """
    ctx = _build_base_context(shipment)

    pkg = shipment.get("package") or {}
    cartons = pkg.get("cartons") or 0
    eggs_per_carton = pkg.get("eggs_per_carton") or 0
    total_eggs = pkg.get("total_eggs") or 0

    ctx["goods_description_line"] = (
        f"{ctx['product_description']}\n"
        f"{ctx['dbk_clause']}\n"
        f"TOTAL {cartons} CARTONS, {ctx['trays_per_carton']} TRAYS IN EACH CARTON\n"
        f"{ctx['eggs_per_tray']} EGGS IN EACH TRAY, {eggs_per_carton} EGGS IN EACH BOX\n"
        f"EACH CARTON PRINTED WITH PRODUCTION DATE & EXPIRY DATE.(THREE MONTHS)\n"
        f"TOTAL {cartons} X {eggs_per_carton} = {_fmt_int(total_eggs)} EGGS\n"
        f"{ctx['container_type']} REEFER CONTAINER\n"
        f"Pan No:{ctx['exporter_pan']}  GSTIN No:{ctx['exporter_gstin']}\n"
        f"HSN CODE NO:{ctx['exporter_hsn']}"
    )

    ctx["packing_remarks"] = (
        f"Each carton\n"
        f"{ctx['net_weight_per_carton']} Kgs Nett\n"
        f"Each carton\n"
        f"{ctx['gross_weight_per_carton']} Kgs Gross"
    )

    ctx["weight_summary_line"] = (
        f"Each carton — {eggs_per_carton} Nos.\n"
        f"{eggs_per_carton} x {cartons} cartons = Total {_fmt_int(total_eggs)} Nos.\n"
        f"Nett Weight : {ctx['net_weight_display']}     "
        f"Gross Weight: {ctx['gross_weight_display']}"
    )

    return ctx


def proforma_invoice_context(shipment: dict) -> dict:
    """
    Build the template context dict for the Proforma Invoice document.
    Uses the base context + unique proforma fields.
    """
    ctx = _build_base_context(shipment)
    pi = shipment.get("proforma_invoice") or {}

    pkg = shipment.get("package") or {}
    cartons = pkg.get("cartons") or 0
    eggs_per_carton = pkg.get("eggs_per_carton") or 0
    total_eggs = pkg.get("total_eggs") or 0

    ctx.update({
        "po_number":                        _s(pi.get("po_number")),
        "po_date":                          _s(pi.get("po_date")),
        "proforma_invoice_number":          _s(pi.get("proforma_invoice_number")),
        "buyer_trn":                        _s(pi.get("buyer_trn")),
        "consignee_trn":                    _s(pi.get("consignee_trn")),
        "notify_party":                     _s(pi.get("notify_party")),
        "notify_party_address":             _s(pi.get("notify_party_address")),
        "payment_terms":                    _s(pi.get("payment_terms")),
        "expiry_date":                      _s(pi.get("expiry_date")),
        "no_and_kind_of_packages":          _s(pi.get("no_and_kind_of_packages")),
        "intermediate_bank_name":           _s(pi.get("intermediate_bank_name")),
        "intermediate_bank_account_number": _s(pi.get("intermediate_bank_account_number")),
        "intermediate_bank_swift":          _s(pi.get("intermediate_bank_swift")),
        "intermediate_bank_routing_number": _s(pi.get("intermediate_bank_routing_number")),
        "correspondent_bank":               _s(pi.get("correspondent_bank")),
    })

    ctx["goods_description_line"] = (
        f"{ctx['product_description']} {ctx['dbk_clause']}\n"
        f"TOTAL {cartons} CARTONS, {ctx['trays_per_carton']} TRAYS IN EACH CARTON\n"
        f"{ctx['eggs_per_tray']} EGGS IN EACH TRAY, {eggs_per_carton} EGGS IN EACH BOX\n"
        f"EACH CARTON PRINTED WITH PRODUCTION DATE & EXPIRY DATE.(THREE MONTHS)\n"
        f"TOTAL {cartons} X {eggs_per_carton} = {_fmt_int(total_eggs)} EGGS\n"
        f"{ctx['container_type']} REEFER CONTAINER\n"
        f"Pan No:{ctx['exporter_pan']}\n"
        f"GSTIN No:{ctx['exporter_gstin']}\n"
        f"HSN CODE NO:{ctx['exporter_hsn']}"
    )

    ctx["weight_summary_line"] = (
        f"Each carton — {eggs_per_carton} Nos.\n"
        f"{eggs_per_carton} x {cartons} cartons = Total {_fmt_int(total_eggs)} Nos.\n"
        f"Nett Weight : {ctx['net_weight_display']}\n"
        f"Gross Weight: {ctx['gross_weight_display']}"
    )

    return ctx


def trade_facility_context(shipment: dict) -> dict:
    """Build context for Trade Facility (Step 4)."""
    ctx = _build_base_context(shipment)
    tf = shipment.get("trade_facility") or {}
    er = shipment.get("examination_report") or {}
    
    # We map the inputs to the placeholders in trade_facility.docx
    ctx.update({
        "shipping_bill_no":      _s(ctx.get("shipping_bill_no")),
        "exporter_name":         EXPORTER["name"],
        "iec_no":                EXPORTER["iec"],
        "exporter_gstin":        EXPORTER["gstin"],
        "branch_code":           _s(tf.get("branch_code")) or _s(er.get("branch_code")) or "",
        "bin_number":            EXPORTER["pan"],
        "exporter_address":      EXPORTER["address"],
        "date_of_examination":   _s(tf.get("date_of_examination")) or _s(ctx.get("invoice_date")),
        "starting_time":         _s(tf.get("stuffing_start_time")),
        "completion_time":       _s(tf.get("stuffing_completion_time")),
        "time_taken":            _s(tf.get("stuffing_duration")),
        "description_of_cargo":  f"{_s(ctx.get('product_name'))} / {_s(ctx.get('cartons'))} CARTONS".strip(" /"),
        "country_of_destination": _s(ctx.get("country_of_final_destination")),
        "signatory_name":        _s(tf.get("authorized_signatory_name")),
        "signatory_designation": _s(tf.get("authorized_signatory_designation")),
        "invoice_no":            _s(ctx.get("invoice_no")),
        "invoice_date":          _s(ctx.get("invoice_date")),
        "total_packages":        _s(ctx.get("cartons")),
        "consignee_name":        _s(ctx.get("consignee_name")),
        "consignee_address":     _s(ctx.get("buyer_address")),
        "goods_description_verified": _s(tf.get("goods_description_verified"), "Yes"),
        "container_no":          _s(ctx.get("container_no")),
        "seal_no":               _s(tf.get("seal_number")),
        "truck_no":              _s(tf.get("truck_number")),
        "container_size":        _s(ctx.get("container_type")),
        "packages_in_container": _s(ctx.get("cartons")),
        "e_seal_number":         _s(tf.get("e_seal_number")),
        "e_seal_colour":         "White",
        "container_to_cfs_time": _s(tf.get("container_to_cfs_start_time")),
    })
    return ctx



def export_insurance_context(shipment: dict) -> dict:
    """Build context for Export Insurance letter."""
    ctx = _build_base_context(shipment)
    ei = shipment.get("export_insurance") or {}

    # Auto-populate from shipment
    invoice_no   = _s(ctx.get("invoice_no"))
    invoice_date = _s(ctx.get("invoice_date"))
    container_no = _s(ctx.get("container_no"))
    cartons      = _s(ctx.get("cartons"))
    product_name = _s(ctx.get("product_name"), STATIC_PRODUCT["description"])
    port_of_loading = _s(ctx.get("port_of_loading"))

    ctx.update({
        # Static exporter fields
        "exporter_name":    EXPORTER["name"],
        "exporter_address": EXPORTER["address"],
        "exporter_email":   EXPORTER["email"],
        "exporter_gstin":   EXPORTER["gstin"],
        "exporter_iec":     EXPORTER["iec"],
        # Shipment-sourced auto-fields
        "invoice_no":       invoice_no,
        "invoice_date":     invoice_date,
        "container_no":     container_no,
        "seal_nos":         _s(ctx.get("seal_number")),
        "truck_no":         _s(ctx.get("truck_number")),
        "place_of_loading": f"Rasi Foods, ({port_of_loading})",
        "name_of_goods":    product_name,
        "quantity_of_goods": f"{cartons} CARTONS",
        "coverage_route":   _s(ctx.get("country_of_final_destination")),
        # Insurance-specific fields from ExportInsurance table
        "date":                 _s(ei.get("date")),
        "respected_sir":        _s(ei.get("respected_sir")),
        "marine_policy_number": _s(ei.get("marine_policy_number")),
        "cif_policy_number":    _s(ei.get("cif_policy_number")),
        "risk_cover":           _s(ei.get("risk_cover"), "ICCA"),
        "importer_name":        _s(ei.get("importer_name")),
        "importer_address":     _s(ei.get("importer_address")),
        "sum_assured":          _s(ei.get("sum_assured")),
        "dollar_value":         _s(ei.get("dollar_value")),
        "port_of_delivery":     _s(ei.get("port_of_delivery")),
        "insurance_remarks":    _s(ei.get("insurance_remarks")),
    })
    return ctx


def animal_certificate_context(shipment: dict) -> dict:
    """
    Build context for Animal Health Certificate (vet_certificate.docx).
    Pulls auto-populated data from shipment + new animal_certificate table fields.
    Static government text and certification paragraphs remain fixed in the template.
    """
    ctx = _build_base_context(shipment)
    ac  = shipment.get("animal_certificate") or {}
    buy = shipment.get("buyer") or {}
    pi  = shipment.get("proforma_invoice") or {}
    pkg = shipment.get("package") or {}

    cartons = pkg.get("cartons") or 0

    ctx.update({
        # ── Static government heading (never editable) ─────────────────────
        "issuing_dept":     "Animal Husbandry Department",
        "issuing_govt":     "Government of Tamil Nadu",
        "issuing_district": "Namakkal District",

        # ── Document-specific user inputs ──────────────────────────────────
        "serial_no":               _s(ac.get("serial_no")),
        "issue_date":              _s(ac.get("issue_date")),
        "date_of_inspection":      _s(ac.get("date_of_inspection")),
        "vet_officer_name":        _s(ac.get("vet_officer_name"), "Dr. R. MANIVEL B.V.Sc"),
        "vet_officer_designation": _s(ac.get("vet_officer_designation")),

        # ── Auto-populated: Exporter ───────────────────────────────────────
        "exporter_name":    EXPORTER["name"],
        "exporter_address": EXPORTER["address"],

        # ── Auto-populated: Importer / Consignee ───────────────────────────
        "importer_name":    _s(buy.get("consignee_name")) or _s(buy.get("buyer_name")),
        "importer_address": _s(buy.get("buyer_address")),
        "addressee":        _s(buy.get("consignee_name")),

        # ── Auto-populated: Product & Package ─────────────────────────────
        "number_of_cartons":    str(cartons),
        "description_of_goods": "Farm Fresh White Shell Eggs",
        "type_of_packing":      "Eggs laid in Trays & Packed in Carton",
        "gross_weight_per_egg": _s(ctx.get("gross_weight")),
        "production_date":      _s(pi.get("expiry_date")) or "",
        "expiry_date":          _s(pi.get("expiry_date")),

        # ── Auto-populated: Shipment ───────────────────────────────────────
        "port_of_shipment":  _s(ctx.get("port_of_loading")),
        "container_no":      _s(ctx.get("container_no")),
        "truck_no":          _s(ctx.get("truck_no")),
        "invoice_no":        _s(ctx.get("invoice_no")),
        "invoice_date":      _s(ctx.get("invoice_date")),

        # ── Static transport / packing values ──────────────────────────────
        "means_of_transport": "Reefer Container",
    })
    return ctx


def animal_annexure_context(shipment: dict) -> dict:
    """Build context for Animal Annexure document."""
    ctx = _build_base_context(shipment)
    aa  = shipment.get("animal_annexure") or {}
    buy = shipment.get("buyer") or {}
    pi  = shipment.get("proforma_invoice") or {}
    ac  = shipment.get("animal_certificate") or {}

    ctx.update({
        "exporter_name":         EXPORTER["name"],
        "exporter_address":      EXPORTER["address"],
        "producer_name":         _s(aa.get("producer_name"), EXPORTER["name"]),
        "producer_address":      _s(aa.get("producer_address"), EXPORTER["address"]),
        "destination_country":   _s(ctx.get("country_of_final_destination")),
        "container_no":          _s(ctx.get("container_no")),
        "production_date":       _s(pi.get("expiry_date")),
        "expiry_date":           _s(pi.get("expiry_date")),
        "invoice_no":            _s(ctx.get("invoice_no")),
        "invoice_date":          _s(ctx.get("invoice_date")),
        "certificate_no":        _s(aa.get("certificate_number")) or _s(ac.get("serial_no")),
        "date_of_issue":         _s(aa.get("date_of_issue")) or _s(ac.get("issue_date")),
        "vet_officer_name":      _s(ac.get("vet_officer_name"), "Dr. R. MANIVEL B.V.Sc"),
        "vet_officer_designation": _s(ac.get("vet_officer_designation")),
    })
    return ctx


# ─── Registry: doc_type → context builder ─────────────────────────────────────
# To add a new document: add its context function above and register it here.

CONTEXT_BUILDERS = {
    "invoice":             invoice_context,
    "packing_list":        packing_list_context,
    "proforma_invoice":    proforma_invoice_context,
    "trade_facility":      trade_facility_context,
    "export_insurance":    export_insurance_context,
    "animal_certificate":  animal_certificate_context,
    "animal_annexure":     animal_annexure_context,
}


def get_context(doc_type: str, shipment: dict) -> dict:
    """
    Public API for the mapping module.
    Returns the template context for any registered document type.
    """
    builder = CONTEXT_BUILDERS.get(doc_type)
    if builder is None:
        raise ValueError(f"Unknown document type: '{doc_type}'. "
                         f"Registered types: {list(CONTEXT_BUILDERS.keys())}")
    return builder(shipment)
