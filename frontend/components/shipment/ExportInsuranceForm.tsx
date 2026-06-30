'use client';

import React, { useEffect, useState } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { Input } from '../ui/Input';
import { SectionHeader } from '../ui/SectionHeader';
import { Toast } from '../ui/Toast';
import { FormNavigator } from './FormNavigator';
import { shipmentApi } from '../../services/shipmentApi';
import { useShipmentData } from '../../hooks/useShipmentData';
import { ExportInsurancePreview } from './ExportInsurancePreview';
import { exportInsuranceSchema, ExportInsuranceFormData } from '../../schemas/exportInsurance';

interface ExportInsuranceFormProps {
  shipmentId: string;
}

export default function ExportInsuranceForm({ shipmentId }: ExportInsuranceFormProps) {
  const router = useRouter();
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { data: shipment, loading } = useShipmentData(shipmentId);

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<ExportInsuranceFormData>({
    resolver: zodResolver(exportInsuranceSchema),
    defaultValues: {
      risk_cover: 'ICCA',
    },
  });

  // Load existing insurance data when shipment loads
  useEffect(() => {
    if (!shipment?.export_insurance) return;
    const ei = shipment.export_insurance;
    reset({
      date:                 ei.date || '',
      respected_sir:        ei.respected_sir || '',
      marine_policy_number: ei.marine_policy_number || '',
      cif_policy_number:    ei.cif_policy_number || '',
      risk_cover:           ei.risk_cover || 'ICCA',
      importer_name:        ei.importer_name || '',
      importer_address:     ei.importer_address || '',
      sum_assured:          ei.sum_assured || '',
      dollar_value:         ei.dollar_value || '',
      port_of_delivery:     ei.port_of_delivery || '',
      insurance_remarks:    ei.insurance_remarks || '',
    });
  }, [shipment, reset]);

  // Watch fields for live preview
  const w_date = useWatch({ control, name: 'date' });
  const w_respected_sir = useWatch({ control, name: 'respected_sir' });
  const w_marine_policy_number = useWatch({ control, name: 'marine_policy_number' });
  const w_cif_policy_number = useWatch({ control, name: 'cif_policy_number' });
  const w_risk_cover = useWatch({ control, name: 'risk_cover' }) || 'ICCA';
  const w_importer_name = useWatch({ control, name: 'importer_name' });
  const w_importer_address = useWatch({ control, name: 'importer_address' });
  const w_sum_assured = useWatch({ control, name: 'sum_assured' });
  const w_dollar_value = useWatch({ control, name: 'dollar_value' });
  const w_port_of_delivery = useWatch({ control, name: 'port_of_delivery' });
  const w_insurance_remarks = useWatch({ control, name: 'insurance_remarks' });

  const onSubmit = async (data: ExportInsuranceFormData) => {
    setIsSubmitting(true);
    try {
      await shipmentApi.saveExportInsurance(shipmentId, data as any);
      // Next is Animal Health Certificate (Step 6)
      router.push(`/shipment/${shipmentId}/animal-certificate`);
    } catch {
      setToast({ message: 'Failed to save Export Insurance.', type: 'error' });
      setIsSubmitting(false);
    }
  };

  // Compile data for the preview
  const previewData = {
    // Static fields
    exporter_name: "RASI FOODS",
    exporter_address: "NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA",
    exporter_email: "rasieggs@gmail.com",
    
    // Derived from shipment
    invoice_no: shipment?.invoice_info?.invoice_no,
    invoice_date: shipment?.invoice_info?.invoice_date,
    container_no: shipment?.product?.container_no,
    seal_nos: shipment?.trade_facility?.seal_number,
    truck_no: shipment?.trade_facility?.truck_number,
    place_of_loading: `Rasi Foods, (${shipment?.shipment_details?.port_of_loading || ''})`,
    name_of_goods: shipment?.product?.product_name || "FRESH WHITE SHELL TABLE EGGS (CHICKEN).",
    quantity_of_goods: `${shipment?.package?.cartons || ''} CARTONS`,
    coverage_route: shipment?.shipment_details?.country_of_final_destination,

    // Form data
    date: w_date,
    respected_sir: w_respected_sir,
    marine_policy_number: w_marine_policy_number,
    cif_policy_number: w_cif_policy_number,
    risk_cover: w_risk_cover,
    importer_name: w_importer_name,
    importer_address: w_importer_address,
    sum_assured: w_sum_assured,
    dollar_value: w_dollar_value,
    port_of_delivery: w_port_of_delivery,
    insurance_remarks: w_insurance_remarks,
  };

  if (loading) return <div>Loading...</div>;

  return (
    <>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      
      <div className="flex flex-col xl:flex-row gap-8 items-start w-full">
        <form onSubmit={handleSubmit(onSubmit)} className="w-full xl:w-[450px] space-y-6 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          
          <div className="bg-emerald-50 text-emerald-800 p-4 rounded-lg border border-emerald-100 text-sm">
            <p className="font-semibold mb-1">Automatic Data Reuse</p>
            <p>Exporter details, Invoice No, Container/Seal/Truck info, and Product data are automatically injected into the template.</p>
          </div>

          <SectionHeader title="Header Details" />
          <div className="space-y-4">
            <Input label="Date" register={register('date')} error={errors.date?.message} />
            <Input label="Respected Sir (Name)" register={register('respected_sir')} error={errors.respected_sir?.message} />
          </div>

          <SectionHeader title="Policy Details" />
          <div className="space-y-4">
            <Input label="Marine Policy Number" register={register('marine_policy_number')} error={errors.marine_policy_number?.message} />
            <Input label="CIF Policy Number" register={register('cif_policy_number')} error={errors.cif_policy_number?.message} />
            <Input label="Risk Cover" register={register('risk_cover')} error={errors.risk_cover?.message} />
          </div>

          <SectionHeader title="Importer Details" />
          <div className="space-y-4">
            <Input label="Importer Name" register={register('importer_name')} error={errors.importer_name?.message} />
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Importer Address</label>
              <textarea
                {...register('importer_address')}
                rows={3}
                className="w-full px-3 py-2 bg-white text-gray-900 border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <Input label="Port of Delivery" register={register('port_of_delivery')} error={errors.port_of_delivery?.message} />
          </div>

          <SectionHeader title="Value Details" />
          <div className="space-y-4">
            <Input label="Sum Assured" register={register('sum_assured')} error={errors.sum_assured?.message} placeholder="e.g. INR 25,00,000" />
            <Input label="Dollar Value" register={register('dollar_value')} error={errors.dollar_value?.message} placeholder="e.g. USD 30,000" />
            
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Insurance Remarks (Optional)</label>
              <textarea
                {...register('insurance_remarks')}
                rows={2}
                className="w-full px-3 py-2 bg-white text-gray-900 border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                placeholder="Optional remarks..."
              />
            </div>
          </div>

          <FormNavigator
            shipmentId={shipmentId}
            isSubmitting={isSubmitting}
            prevStepPath="trade-facility"
          />
        </form>

        <div className="flex-1 bg-gray-50 p-6 rounded-xl border border-gray-200 overflow-x-auto min-w-[850px] shadow-inner">
          <ExportInsurancePreview data={previewData} />
        </div>
      </div>
    </>
  );
}
