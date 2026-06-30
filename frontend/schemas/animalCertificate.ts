import { z } from 'zod';

export const animalCertificateSchema = z.object({
  serial_no:               z.string().optional(),
  issue_date:              z.string().optional(),
  date_of_inspection:      z.string().optional(),
  vet_officer_name:        z.string().optional(),
  vet_officer_designation: z.string().optional(),
});

export type AnimalCertificateFormData = z.infer<typeof animalCertificateSchema>;
