import { z } from 'zod';

export const tradeFacilitySchema = z.object({
  // ── Editable Trade Facility fields ────────────────────────────────────────
  date_of_examination: z.string().min(1, 'Date of examination is required'),
  stuffing_start_time: z.string().min(1, 'Stuffing start time is required'),
  stuffing_completion_time: z.string().min(1, 'Stuffing completion time is required'),
  stuffing_duration: z.string().optional(),
  authorized_signatory_name: z.string().min(1, 'Signatory name is required'),
  authorized_signatory_designation: z.string().min(1, 'Signatory designation is required'),
  seal_number: z.string().min(1, 'Seal number is required'),
  truck_number: z.string().min(1, 'Truck number is required'),
  container_to_cfs_start_time: z.string().min(1, 'Container to CFS start time is required'),
  e_seal_number: z.string().min(1, 'E-Seal number is required'),
  goods_description_verified: z.string().optional(),
  branch_code: z.string().optional(),
  bin_number: z.string().optional(),

  // ── Inherited read-only fields (populated from DB, travel through payload) ─
  exporter_name: z.string().optional(),
  exporter_address: z.string().optional(),
  exporter_gstin: z.string().optional(),
  exporter_iec: z.string().optional(),
  exporter_pan: z.string().optional(),
  invoice_no: z.string().optional(),
  invoice_date: z.string().optional(),
  shipping_bill_no: z.string().optional(),
  consignee_name: z.string().optional(),
  consignee_address: z.string().optional(),
  port_of_loading: z.string().optional(),
  final_destination: z.string().optional(),
  country_of_destination: z.string().optional(),
  container_no: z.string().optional(),
  container_type: z.string().optional(),
  cartons: z.string().optional(),
  total_eggs: z.string().optional(),
  net_weight: z.string().optional(),
  gross_weight: z.string().optional(),
});

export type TradeFacilityFormData = z.infer<typeof tradeFacilitySchema>;
