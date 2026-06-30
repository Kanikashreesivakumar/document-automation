import { z } from 'zod';

export const animalAnnexureSchema = z.object({
  producer_name: z.string().optional(),
  producer_address: z.string().optional(),
  certificate_number: z.string().optional(),
  date_of_issue: z.string().optional(),
});

export type AnimalAnnexureFormData = z.infer<typeof animalAnnexureSchema>;
