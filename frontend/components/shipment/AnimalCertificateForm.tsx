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
import { AnimalCertificatePreview } from './AnimalCertificatePreview';
import { animalCertificateSchema, AnimalCertificateFormData } from '../../schemas/animalCertificate';

interface AnimalCertificateFormProps {
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

export default function AnimalCertificateForm({ shipmentId }: AnimalCertificateFormProps) {
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
  } = useForm<AnimalCertificateFormData>({
    resolver: zodResolver(animalCertificateSchema),
    defaultValues: {
      vet_officer_name: 'Dr. R. MANIVEL B.V.Sc',
    },
  });

  // Load existing data when shipment loads
  useEffect(() => {
    if (!shipment?.animal_certificate) return;
    const ac = shipment.animal_certificate;
    reset({
      serial_no:               ac.serial_no               || '',
      issue_date:              ac.issue_date               || '',
      date_of_inspection:      ac.date_of_inspection       || '',
      vet_officer_name:        ac.vet_officer_name         || 'Dr. R. MANIVEL B.V.Sc',
      vet_officer_designation: ac.vet_officer_designation  || '',
    });
  }, [shipment, reset]);

  // Watch form fields for live preview
  const w_serial_no               = useWatch({ control, name: 'serial_no' });
  const w_issue_date              = useWatch({ control, name: 'issue_date' });
  const w_date_of_inspection      = useWatch({ control, name: 'date_of_inspection' });
  const w_vet_officer_name        = useWatch({ control, name: 'vet_officer_name' });
  const w_vet_officer_designation = useWatch({ control, name: 'vet_officer_designation' });

  const onSubmit: SubmitHandler<AnimalCertificateFormData> = async (data) => {
    setIsSubmitting(true);
    try {
      await shipmentApi.saveAnimalCertificate(shipmentId, data as any);
      // Next step: Animal Annexure
      router.push(`/shipment/${shipmentId}/animal-annexure`);
    } catch {
      setToast({ message: 'Failed to save Animal Health Certificate.', type: 'error' });
      setIsSubmitting(false);
    }
  };

  // Derive auto-populated values from shipment
  const pkg = shipment?.package;
  const inv = shipment?.invoice_info;
  const buy = shipment?.buyer;
  const det = shipment?.shipment_details;
  const wt  = shipment?.weight;
  const pi  = shipment?.proforma_invoice;
  const prod = shipment?.product;
  const tf  = shipment?.trade_facility;

  const previewData = {
    // Static heading
    ...STATIC,

    // User inputs (live)
    serial_no:               w_serial_no,
    issue_date:              w_issue_date,
    date_of_inspection:      w_date_of_inspection,
    vet_officer_name:        w_vet_officer_name || 'Dr. R. MANIVEL B.V.Sc',
    vet_officer_designation: w_vet_officer_designation,

    // Auto-populated: Exporter (static constants)
    exporter_name:    'RASI FOODS',
    exporter_address: 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',

    // Auto-populated: Importer / Consignee
    importer_name:    buy?.consignee_name || buy?.buyer_name || '',
    importer_address: buy?.buyer_address || '',
    addressee:        buy?.consignee_name || '',

    // Auto-populated: Product & Package
    number_of_cartons: pkg?.cartons?.toString() || '',
    gross_weight:      wt?.gross_weight ? `${wt.gross_weight} KGS` : '',
    production_date:   pi?.expiry_date || '',
    expiry_date:       pi?.expiry_date || '',

    // Auto-populated: Shipment
    port_of_shipment: det?.port_of_loading || '',
    container_no:     prod?.container_no || '',
    truck_no:         tf?.truck_number || '',
    invoice_no:       inv?.invoice_no || '',
    invoice_date:     inv?.invoice_date || '',
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
          <SectionHeader title="Certificate Details" />
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

          <SectionHeader title="Veterinary Officer Details" />
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

          <FormNavigator
            shipmentId={shipmentId}
            isSubmitting={isSubmitting}
            prevStepPath="insurance"
          />
        </form>

        {/* ─── Right: Live Preview ───────────────────────────────────────────────── */}
        <div className="flex-1 bg-gray-50 p-6 rounded-xl border border-gray-200 overflow-x-auto min-w-[850px] shadow-inner">
          <AnimalCertificatePreview data={previewData} />
        </div>
      </div>
    </>
  );
}
