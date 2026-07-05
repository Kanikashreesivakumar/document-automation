/**
 * Zod schema for the unified shipment data form.
 *
 * Rules:
 *   - Only the 27 user-editable fields appear here.
 *   - Auto-calculated fields (eggs_per_carton, total_eggs, amount_usd,
 *     amount_in_words, net_weight, gross_weight) are NEVER in this schema.
 *   - Static exporter fields (name, address, GSTIN, PAN, HSN) are NEVER here.
 */
import { z } from "zod";

const str  = (label: string) => z.string().min(1, `${label} is required`);
const strO = ()              => z.string().optional().or(z.literal(""));
const numR = (label: string) =>
  z.number()
   .min(0.000001, `${label} must be greater than 0`);
const intR = (label: string) =>
  z.number()
   .int(`${label} must be a whole number`)
   .min(1, `${label} must be at least 1`);

export const shipmentDataSchema = z.object({
  // ── Invoice Information ────────────────────────────────────────────────────
  invoice_no:                    str("Invoice No."),
  invoice_date:                  str("Invoice Date"),
  buyer_order_no_date:           strO(),
  reference_proforma_invoice_no: strO(),
  shipping_bill_no:              strO(),
  shipping_bill_date:            strO(),
  exporter_reference:            strO(),
  other_reference:               strO(),

  // ── Buyer / Consignee ──────────────────────────────────────────────────────
  consignee_name:   str("Consignee Name"),
  buyer_name:       strO(),
  buyer_address:    strO(),
  buyer_postal_code: strO(),
  buyer_country:    str("Buyer Country"),

  // ── Shipment Details ───────────────────────────────────────────────────────
  pre_carriage_by:              str("Pre-Carriage By"),
  vessel_flight_no:             strO(),
  place_of_receipt:             str("Place of Receipt"),
  port_of_loading:              str("Port of Loading"),
  port_of_discharge:            str("Port of Discharge"),
  final_destination:            str("Final Destination"),
  country_of_origin:            str("Country of Origin"),
  country_of_final_destination: str("Country of Final Destination"),
  terms_of_delivery:            str("Terms of Delivery"),

  // ── Product ────────────────────────────────────────────────────────────────
  brand_name:     str("Brand Name"),
  product_name:   strO(),
  container_type: str("Container Type"),
  container_no:   str("Container No."),
  
  shipment_declaration: strO(),
  production_date:      strO(),
  expiry_date:          strO(),
  production_duration:  strO(),
  lot_number:           strO(),
  epcg_licence_number:  strO(),
  dt:                   strO(),
  egg_size:             strO(),
  pan_number:           strO(),
  gstin:                strO(),
  hsn_code:             strO(),

  // ── Package ────────────────────────────────────────────────────────────────
  cartons:         intR("Cartons"),
  trays_per_carton: intR("Trays per Carton"),
  eggs_per_tray:   intR("Eggs per Tray"),

  // ── Pricing ────────────────────────────────────────────────────────────────
  rate_per_egg_usd: numR("Rate per Egg (USD)"),

  // ── Weight ─────────────────────────────────────────────────────────────────
  net_weight_per_carton:   numR("Net Weight per Carton"),
  gross_weight_per_carton: numR("Gross Weight per Carton"),
});

export type ShipmentDataForm = z.infer<typeof shipmentDataSchema>;
