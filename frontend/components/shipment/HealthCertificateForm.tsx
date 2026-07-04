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
import { PDFPreviewViewer } from './PDFPreviewViewer';
import { healthCertificateSchema, HealthCertificateFormData } from '../../schemas/healthCertificate';

interface HealthCertificateFormProps {
  shipmentId: string;
}

// Static values — never editable
const STATIC = {
  issuing_dept:     'Animal Husbandry Department',
  issuing_govt:     'Government of Tamil Nadu',
  issuing_district: 'Namakkal District',
  means_of_transport: 'Reefer Container',
  type_of_packing:  'Eggs laid in Trays & Packed in Carton',
  description_of_goods: 'Farm Fresh White Shell Eggs',
};

export default function HealthCertificateForm({ shipmentId }: HealthCertificateFormProps) {
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
  } = useForm<HealthCertificateFormData>({
    resolver: zodResolver(healthCertificateSchema),
    defaultValues: {
      vet_officer_name: 'Dr. R. MANIVEL B.V.Sc',
      producer_name: 'RASI FOODS',
      producer_address: 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',
    },
  });

  // Load existing data when shipment loads
  useEffect(() => {
    if (!shipment) return;
    const ac = shipment.animal_certificate || {};
    const aa = shipment.animal_annexure || {};
    reset({
      serial_no:               ac.serial_no               || '',
      issue_date:              ac.issue_date               || '',
      date_of_inspection:      ac.date_of_inspection       || '',
      vet_officer_name:        ac.vet_officer_name         || 'Dr. R. MANIVEL B.V.Sc',
      vet_officer_designation: ac.vet_officer_designation  || '',
      producer_name:           aa.producer_name || 'RASI FOODS',
      producer_address:        aa.producer_address || 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',
      certificate_number:      aa.certificate_number || '',
      date_of_issue:           aa.date_of_issue || '',
    });
  }, [shipment, reset]);

  // Watch form fields for live preview
  const w_serial_no               = useWatch({ control, name: 'serial_no' });
  const w_issue_date              = useWatch({ control, name: 'issue_date' });
  const w_date_of_inspection      = useWatch({ control, name: 'date_of_inspection' });
  const w_vet_officer_name        = useWatch({ control, name: 'vet_officer_name' });
  const w_vet_officer_designation = useWatch({ control, name: 'vet_officer_designation' });
  
  const w_producer_name           = useWatch({ control, name: 'producer_name' });
  const w_producer_address        = useWatch({ control, name: 'producer_address' });
  const w_certificate_number      = useWatch({ control, name: 'certificate_number' });
  const w_date_of_issue           = useWatch({ control, name: 'date_of_issue' });

  const onSubmit: SubmitHandler<HealthCertificateFormData> = async (data) => {
    setIsSubmitting(true);
    try {
      // Split the data to send to both endpoints
      const certData = {
        serial_no: data.serial_no,
        issue_date: data.issue_date,
        date_of_inspection: data.date_of_inspection,
        vet_officer_name: data.vet_officer_name,
        vet_officer_designation: data.vet_officer_designation,
      };
      
      const annexureData = {
        producer_name: data.producer_name,
        producer_address: data.producer_address,
        certificate_number: data.certificate_number,
        date_of_issue: data.date_of_issue,
      };

      await shipmentApi.saveHealthCertificate(shipmentId, certData);
      await shipmentApi.saveHealthCertificateAnnexure(shipmentId, annexureData);
      
      // Next step: Review
      router.push(`/shipment/${shipmentId}/review`);
    } catch {
      setToast({ message: 'Failed to save Health Certificate.', type: 'error' });
      setIsSubmitting(false);
    }
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
              Exporter, Importer, Invoice, Container, Truck, Weights, Production/Expiry
              dates and Port of Shipment are automatically populated from your shipment data.
            </p>
          </div>

          {/* Static government info (read-only display) */}
          <div className="bg-blue-50 text-blue-900 p-4 rounded-lg border border-blue-100 text-sm space-y-0.5">
            <p className="font-semibold mb-2">Government Heading (Static)</p>
            <p>🏛 {STATIC.issuing_dept}</p>
            <p>🏛 {STATIC.issuing_govt}</p>
            <p>🏛 {STATIC.issuing_district}</p>
          </div>

          {/* Document-specific user inputs */}
          <SectionHeader title="Certificate Details (Page 1)" />
          <div className="space-y-4">
            <Input
              label="Serial Number"
              register={register('serial_no')}
              error={errors.serial_no?.message}
              placeholder="e.g. 001/2024"
            />
            <Input
              label="Issue Date"
              register={register('issue_date')}
              error={errors.issue_date?.message}
              placeholder="e.g. 01-01-2024"
            />
            <Input
              label="Date of Inspection"
              register={register('date_of_inspection')}
              error={errors.date_of_inspection?.message}
              placeholder="e.g. 01-01-2024"
            />
          </div>

          <SectionHeader title="Veterinary Officer Details (Page 1 & 2)" />
          <div className="space-y-4">
            <Input
              label="Veterinary Officer Name"
              register={register('vet_officer_name')}
              error={errors.vet_officer_name?.message}
              placeholder="Dr. R. MANIVEL B.V.Sc"
            />
            <Input
              label="Veterinary Officer Designation"
              register={register('vet_officer_designation')}
              error={errors.vet_officer_designation?.message}
              placeholder="Assistant Director, AH Dept."
            />
          </div>

          <SectionHeader title="Annexure Details (Page 2)" />
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
            <Input
              label="Annexure Certificate Number"
              register={register('certificate_number')}
              error={errors.certificate_number?.message}
              placeholder="Leave blank to use Serial Number"
            />
            <Input
              label="Annexure Date of Issue"
              register={register('date_of_issue')}
              error={errors.date_of_issue?.message}
              placeholder="Leave blank to use Issue Date"
            />
          </div>

          <FormNavigator
            shipmentId={shipmentId}
            isSubmitting={isSubmitting}
            prevStepPath="insurance"
          />
        </form>

        {/* ─── Right: Live Preview ───────────────────────────────────────────────── */}
        <div className="flex-1 bg-gray-50 rounded-xl overflow-x-auto min-w-[700px] shadow-inner space-y-8">
          <PDFPreviewViewer shipmentId={shipmentId} docType="health_certificate" data={control._formValues} />
        </div>
      </div>
    </>
  );
}
