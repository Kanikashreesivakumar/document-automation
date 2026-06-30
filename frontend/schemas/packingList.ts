import { z } from 'zod';

const str = () => z.string().optional();
const num = () => z.number().optional();

export const packingListSchema = z.object({
  // Pre-filled from Invoice (kept as optional so prefill works)
  invoice_no: str(),
  invoice_date: str(),
  exporters_ref: str(),
  buyers_order_no: str(),
  reference_proforma_invoice_no: str(),
  other_reference: str(),
  shipping_bill_no: str(),
  shipping_bill_date: str(),

  exporter_name: str(),
  exporter_address: str(),
  exporter_gstin: str(),
  exporter_email: str(),

  consignee: str(),
  buyer: str(),
  buyer_address: str(),
  buyer_trn: str(),

  pre_carriage_by: str(),
  vessel_flight_no: str(),
  place_of_receipt: str(),
  port_of_loading: str(),
  port_of_discharge: str(),
  final_destination: str(),
  country_of_origin_of_goods: str(),
  country_of_final_destination: str(),
  terms_of_delivery: str(),

  // Packing-specific
  container_no: str(),
  container_type: str(),
  brand_name: str(),
  marks_and_nos: str(),
  description_of_goods: str(),
  hsn_code: str(),
  pan_no: str(),
  product_gstin: str(),
  lot_no: str(),
  epcg_licence_no: str(),
  egg_size: str(),
  production_date: str(),
  expiry_date: str(),

  number_of_cartons: num(),
  trays_per_carton: num(),
  eggs_per_tray: num(),
  eggs_per_carton: num(),
  total_eggs: num(),
  net_weight_per_carton: num(),
  gross_weight_per_carton: num(),
  net_weight_kgs: num(),
  gross_weight_kgs: num(),

  remarks: str(),
  signature_name: str(),
  signature_date: str(),
});

export type PackingListFormData = z.infer<typeof packingListSchema>;
