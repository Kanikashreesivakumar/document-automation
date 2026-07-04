import { z } from 'zod';

export const healthCertificateSchema = z.object({
  serial_no:               z.string().optional(),
  issue_date:              z.string().optional(),
  date_of_inspection:      z.string().optional(),
  vet_officer_name:        z.string().optional(),
  vet_officer_designation: z.string().optional(),
  
  producer_name:           z.string().optional(),
  producer_address:        z.string().optional(),
  certificate_number:      z.string().optional(),
  date_of_issue:           z.string().optional(),
});

export type HealthCertificateFormData = z.infer<typeof healthCertificateSchema>;
