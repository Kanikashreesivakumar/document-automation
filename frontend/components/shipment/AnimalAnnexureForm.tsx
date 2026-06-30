'use client';

import React, { useEffect, useState } from 'react';
import { useForm, useWatch, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { Input } from '../ui/Input';
import { SectionHeader } from '../ui/SectionHeader';
import { Toast } from '../ui/Toast';
import { FormNavigator } from './FormNavigator';
import { shipmentApi } from '../../services/shipmentApi';
import { useShipmentData } from '../../hooks/useShipmentData';
import { AnimalAnnexurePreview } from './AnimalAnnexurePreview';
import { animalAnnexureSchema, AnimalAnnexureFormData } from '../../schemas/animalAnnexure';

interface AnimalAnnexureFormProps {
  shipmentId: string;
}

export default function AnimalAnnexureForm({ shipmentId }: AnimalAnnexureFormProps) {
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
  } = useForm<AnimalAnnexureFormData>({
    resolver: zodResolver(animalAnnexureSchema),
    defaultValues: {
      producer_name: 'RASI FOODS',
      producer_address: 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',
    },
  });

  // Load existing data when shipment loads
  useEffect(() => {
    if (!shipment?.animal_annexure) return;
    const aa = shipment.animal_annexure;
    reset({
      producer_name:      aa.producer_name || 'RASI FOODS',
      producer_address:   aa.producer_address || 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',
      certificate_number: aa.certificate_number || '',
      date_of_issue:      aa.date_of_issue || '',
    });
  }, [shipment, reset]);

  // Watch form fields for live preview
  const w_producer_name      = useWatch({ control, name: 'producer_name' });
  const w_producer_address   = useWatch({ control, name: 'producer_address' });
  const w_certificate_number = useWatch({ control, name: 'certificate_number' });
  const w_date_of_issue      = useWatch({ control, name: 'date_of_issue' });

  const onSubmit: SubmitHandler<AnimalAnnexureFormData> = async (data) => {
    setIsSubmitting(true);
    console.log("Animal Annexure Payload before submit:", data);
    console.log("Shipment ID:", shipmentId);
    
    try {
      const response = await shipmentApi.saveAnimalAnnexure(shipmentId, data as any);
      console.log("Animal Annexure Save Response:", response.data);
      // Next step: Review & Generate
      router.push(`/shipment/${shipmentId}/review`);
    } catch (err: any) {
      console.error("Animal Annexure Save Error:", err);
      let errorMsg = 'Failed to save Animal Annexure.';
      if (err.response?.data?.detail) {
        errorMsg = typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail);
      } else if (err.message) {
        errorMsg = err.message;
      }
      setToast({ message: errorMsg, type: 'error' });
      setIsSubmitting(false);
    }
  };

  // Derive auto-populated values from shipment
  const inv = shipment?.invoice_info;
  const det = shipment?.shipment_details;
  const pi  = shipment?.proforma_invoice;
  const prod = shipment?.product;
  const ac = shipment?.animal_certificate;

  const previewData = {
    // User inputs (live)
    producer_name:        w_producer_name || 'RASI FOODS',
    producer_address:     w_producer_address || 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',
    certificate_no:       w_certificate_number || ac?.serial_no || '',
    date_of_issue:        w_date_of_issue || ac?.issue_date || '',

    // Auto-populated: Exporter (static constants)
    exporter_name:    'RASI FOODS',
    exporter_address: 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',

    // Auto-populated
    destination_country:  det?.country_of_final_destination || '',
    container_no:         prod?.container_no || '',
    production_date:      pi?.expiry_date || '',
    expiry_date:          pi?.expiry_date || '',
    invoice_no:           inv?.invoice_no || '',
    invoice_date:         inv?.invoice_date || '',
    
    // Auto-populated from Animal Certificate
    vet_officer_name:        ac?.vet_officer_name || 'Dr. R. MANIVEL B.V.Sc',
    vet_officer_designation: ac?.vet_officer_designation || '',
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600" />
      </div>
    );
  }

  return (
    <>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

      <div className="flex flex-col xl:flex-row gap-8 items-start w-full">
        {/* ─── Left: Form ───────────────────────────────────────────────────────── */}
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="w-full xl:w-[450px] space-y-6 bg-white p-6 rounded-xl shadow-sm border border-gray-200"
        >
          {/* Auto-data banner */}
          <div className="bg-emerald-50 text-emerald-800 p-4 rounded-lg border border-emerald-100 text-sm">
            <p className="font-semibold mb-1">Automatic Data Reuse</p>
            <p>
              Destination, Container, Production/Expiry dates, Invoice, and Vet Officer details 
              are automatically populated from your shipment data.
            </p>
          </div>

          <SectionHeader title="Annexure Details" />
          <div className="space-y-4">
            <Input
              label="Certificate Number"
              register={register('certificate_number')}
              error={errors.certificate_number?.message}
              placeholder="e.g. 001/2024"
            />
            <Input
              label="Date of Issue"
              register={register('date_of_issue')}
              error={errors.date_of_issue?.message}
              placeholder="e.g. 01-01-2024"
            />
          </div>

          <SectionHeader title="Producer Details" />
          <div className="space-y-4">
            <Input
              label="Producer Name"
              register={register('producer_name')}
              error={errors.producer_name?.message}
              placeholder="RASI FOODS"
            />
            <Input
              label="Producer Address"
              register={register('producer_address')}
              error={errors.producer_address?.message}
              placeholder="Full address"
            />
          </div>

          <FormNavigator
            shipmentId={shipmentId}
            isSubmitting={isSubmitting}
            prevStepPath="animal-certificate"
          />
        </form>

        {/* ─── Right: Live Preview ───────────────────────────────────────────────── */}
        <div className="flex-1 bg-gray-50 p-6 rounded-xl border border-gray-200 overflow-x-auto min-w-[850px] shadow-inner">
          <AnimalAnnexurePreview data={previewData} />
        </div>
      </div>
    </>
  );
}
