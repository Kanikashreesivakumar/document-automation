import { z } from 'zod';

export const tradeFacilitySchema = z.object({
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
});

export type TradeFacilityFormData = z.infer<typeof tradeFacilitySchema>;
