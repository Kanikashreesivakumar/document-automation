import { z } from 'zod';

export const exportInsuranceSchema = z.object({
  date: z.string().optional(),
  respected_sir: z.string().optional(),
  marine_policy_number: z.string().optional(),
  cif_policy_number: z.string().optional(),
  risk_cover: z.string().optional(),
  importer_name: z.string().optional(),
  importer_address: z.string().optional(),
  sum_assured: z.string().optional(),
  dollar_value: z.string().optional(),
  port_of_delivery: z.string().optional(),
  insurance_remarks: z.string().optional(),
});

export type ExportInsuranceFormData = z.infer<typeof exportInsuranceSchema>;
