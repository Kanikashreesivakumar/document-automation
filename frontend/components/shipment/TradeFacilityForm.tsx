"use client";

import React, { useEffect, useState } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import { zodResolver } from '@hookform/resolvers/zod';
import { tradeFacilitySchema, TradeFacilityFormData } from '../../schemas/tradeFacility';
import { Input } from '../ui/Input';
import { SectionHeader } from '../ui/SectionHeader';
import { Toast } from '../ui/Toast';
import { FormNavigator } from './FormNavigator';
import { shipmentApi } from '../../services/shipmentApi';
import { useShipmentData } from '../../hooks/useShipmentData';
import { PDFPreviewViewer } from './PDFPreviewViewer';

interface TradeFacilityFormProps {
  shipmentId: string;
}

export default function TradeFacilityForm({ shipmentId }: TradeFacilityFormProps) {
  const router = useRouter();
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { data: shipment, loading } = useShipmentData(shipmentId);

  const {
    register,
    handleSubmit,
    control,
    reset,
    setValue,
    formState: { errors },
  } = useForm<TradeFacilityFormData>({
    resolver: zodResolver(tradeFacilitySchema),
    defaultValues: {},
  });

  // Load existing trade facility data when shipment loads
  useEffect(() => {
    if (!shipment?.trade_facility) return;
    const tf = shipment.trade_facility;
    reset({
      date_of_examination: tf.date_of_examination || '',
      stuffing_start_time: tf.stuffing_start_time || '',
      stuffing_completion_time: tf.stuffing_completion_time || '',
      stuffing_duration: tf.stuffing_duration || '',
      authorized_signatory_name: tf.authorized_signatory_name || '',
      authorized_signatory_designation: tf.authorized_signatory_designation || '',
      seal_number: tf.seal_number || '',
      truck_number: tf.truck_number || '',
      container_to_cfs_start_time: tf.container_to_cfs_start_time || '',
      e_seal_number: tf.e_seal_number || '',
      goods_description_verified: tf.goods_description_verified || 'Yes',
    });
  }, [shipment, reset]);

  // Watch fields for live preview and duration calculation
  const w_date_of_examination = useWatch({ control, name: 'date_of_examination' });
  const w_start_time = useWatch({ control, name: 'stuffing_start_time' });
  const w_completion_time = useWatch({ control, name: 'stuffing_completion_time' });
  const w_duration = useWatch({ control, name: 'stuffing_duration' });
  const w_signatory_name = useWatch({ control, name: 'authorized_signatory_name' });
  const w_signatory_designation = useWatch({ control, name: 'authorized_signatory_designation' });
  const w_seal_number = useWatch({ control, name: 'seal_number' });
  const w_truck_number = useWatch({ control, name: 'truck_number' });
  const w_cfs_time = useWatch({ control, name: 'container_to_cfs_start_time' });
  const w_e_seal = useWatch({ control, name: 'e_seal_number' });
  const w_verified = useWatch({ control, name: 'goods_description_verified' }) || 'Yes';

  // Auto-calculate stuffing duration
  useEffect(() => {
    if (!w_start_time || !w_completion_time) {
      setValue('stuffing_duration', '');
      return;
    }
    try {
      const parseTime = (timeStr: string) => {
        const parts = timeStr.trim().split(/(am|pm)/i);
        const time = parts[0];
        const modifier = parts[1] || '';
        let [hours, minutes] = time.split(':').map(n => parseInt(n, 10));
        if (modifier.toUpperCase() === 'PM' && hours < 12) hours += 12;
        if (modifier.toUpperCase() === 'AM' && hours === 12) hours = 0;
        return hours * 60 + (minutes || 0);
      };
      const startMins = parseTime(w_start_time);
      const endMins = parseTime(w_completion_time);
      if (isNaN(startMins) || isNaN(endMins)) return;

      let diffMins = endMins - startMins;
      if (diffMins < 0) diffMins += 24 * 60;

      const h = Math.floor(diffMins / 60);
      const m = diffMins % 60;
      let durationStr = '';
      if (h > 0 && m > 0) durationStr = `${h} Hours ${m} Minutes`;
      else if (h > 0) durationStr = `${h} Hours`;
      else if (m > 0) durationStr = `${m} Minutes`;
      else durationStr = '0 Minutes';

      if (durationStr !== w_duration) {
        setValue('stuffing_duration', durationStr, { shouldDirty: true });
      }
    } catch {
      // ignore
    }
  }, [w_start_time, w_completion_time, setValue, w_duration]);

  const onSubmit = async (data: TradeFacilityFormData) => {
    setIsSubmitting(true);
    try {
      await shipmentApi.saveTradeFacility(shipmentId, data);
      // Next is Export Insurance (Step 5)
      router.push(`/shipment/${shipmentId}/insurance`);
    } catch {
      setToast({ message: 'Failed to save Trade Facility.', type: 'error' });
      setIsSubmitting(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

      <div className="flex flex-col xl:flex-row gap-8 items-start w-full">
        <form onSubmit={handleSubmit(onSubmit)} className="w-full xl:w-[450px] space-y-6 bg-white p-6 rounded-xl shadow-sm border border-gray-200">

          <div className="bg-emerald-50 text-emerald-800 p-4 rounded-lg border border-emerald-100 text-sm">
            <p className="font-semibold mb-1">Automatic Data Reuse</p>
            <p>Shipment data (IEC, GSTIN, Address, Invoice No, Description, etc.) is automatically injected into the Trade Facility template.</p>
          </div>

          <SectionHeader title="Examination Details" />
          <div className="space-y-4">
            <Input label="Date of Examination" register={register('date_of_examination')} error={errors.date_of_examination?.message} placeholder="e.g. 15-06-2026" />
            <Input label="Stuffing Start Time" register={register('stuffing_start_time')} error={errors.stuffing_start_time?.message} placeholder="e.g. 10:00 AM" />
            <Input label="Stuffing Completion Time" register={register('stuffing_completion_time')} error={errors.stuffing_completion_time?.message} placeholder="e.g. 11:30 AM" />
            <Input label="Time Taken for Stuffing (Auto-calculated)" register={register('stuffing_duration')} error={errors.stuffing_duration?.message} readOnly />
            <Input label="Container moving to CFS Start Time" register={register('container_to_cfs_start_time')} error={errors.container_to_cfs_start_time?.message} placeholder="e.g. 12:00 PM" />
          </div>

          <SectionHeader title="Container & Seal Details" />
          <div className="space-y-4">
            <Input label="Seal Number" register={register('seal_number')} error={errors.seal_number?.message} />
            <Input label="E-Seal Number" register={register('e_seal_number')} error={errors.e_seal_number?.message} />
            <Input label="Truck Number" register={register('truck_number')} error={errors.truck_number?.message} />
          </div>

          <SectionHeader title="Authorized Signatory" />
          <div className="space-y-4">
            <Input label="Name" register={register('authorized_signatory_name')} error={errors.authorized_signatory_name?.message} />
            <Input label="Designation" register={register('authorized_signatory_designation')} error={errors.authorized_signatory_designation?.message} />
          </div>

          <SectionHeader title="Goods Description" />
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Is description of goods, quantity, and value as per Export GST Invoice?
              </label>
              <select
                {...register('goods_description_verified')}
                className="w-full px-3 py-2 bg-white text-gray-900 border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              >
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>
            </div>
          </div>

          <FormNavigator
            shipmentId={shipmentId}
            isSubmitting={isSubmitting}
            prevStepPath="proforma-invoice"
          />
        </form>

        <div className="flex-1 w-full bg-gray-100 rounded-xl overflow-x-auto min-h-[600px] flex justify-center border border-gray-200">
          <PDFPreviewViewer shipmentId={shipmentId} docType="trade_facility" data={control._formValues} />
        </div>
      </div>
    </>
  );
}
