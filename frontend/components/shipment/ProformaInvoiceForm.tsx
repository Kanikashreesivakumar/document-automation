"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import { zodResolver } from '@hookform/resolvers/zod'
import { proformaInvoiceSchema, ProformaInvoiceForm } from '../../schemas/proformaInvoice';
import { Input } from '../ui/Input';
import { Textarea } from '../ui/Textarea';
import { SectionHeader } from '../ui/SectionHeader';
import { Toast } from '../ui/Toast';
import { FormNavigator } from './FormNavigator';
import { shipmentApi } from '../../services/shipmentApi';
import { useShipmentData } from '../../hooks/useShipmentData';
import { PDFPreviewViewer } from './PDFPreviewViewer';

// ─── Company bank defaults (must match COMPANY_BANK in backend/mapping/__init__.py) ──
const COMPANY_BANK_DEFAULTS = {
  company_account_name:   'RASI FOODS',
  company_account_number: '50200082616067',
  company_bank_name:      'HDFC BANK LTD',
  company_branch:         'NAMAKKAL',
  company_swift:          'HDFCINBB',
};

interface ProformaInvoiceFormProps {
  shipmentId: string;
}

export default function ProformaInvoiceFormComponent({ shipmentId }: ProformaInvoiceFormProps) {
  const router = useRouter();
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { data: shipment, loading } = useShipmentData(shipmentId);

  const {
    register,
    handleSubmit,
    control,
    reset,
    getValues,
    formState: { errors },
  } = useForm<ProformaInvoiceForm>({
    resolver: zodResolver(proformaInvoiceSchema),
    defaultValues: { ...COMPANY_BANK_DEFAULTS },
  });

  // ── Load existing proforma data when shipment loads ──────────────────────────
  useEffect(() => {
    if (!shipment) return;
    const pi = shipment.proforma_invoice || {};
    reset({
      po_number:                        pi.po_number || '',
      po_date:                          pi.po_date || '',
      proforma_invoice_number:          pi.proforma_invoice_number || '',
      buyer_trn:                        pi.buyer_trn || '',
      consignee_trn:                    pi.consignee_trn || '',
      notify_party:                     pi.notify_party || '',
      notify_party_address:             pi.notify_party_address || '',
      payment_terms:                    pi.payment_terms || '',
      expiry_date:                      pi.expiry_date || '',
      no_and_kind_of_packages:          pi.no_and_kind_of_packages || '',
      intermediate_bank_name:           pi.intermediate_bank_name || '',
      intermediate_bank_account_number: pi.intermediate_bank_account_number || '',
      intermediate_bank_swift:          pi.intermediate_bank_swift || '',
      intermediate_bank_routing_number: pi.intermediate_bank_routing_number || '',
      correspondent_bank:               pi.correspondent_bank || '',
      // Company bank — use DB value if saved, otherwise use defaults
      company_account_name:   pi.company_account_name   || COMPANY_BANK_DEFAULTS.company_account_name,
      company_account_number: pi.company_account_number || COMPANY_BANK_DEFAULTS.company_account_number,
      company_bank_name:      pi.company_bank_name      || COMPANY_BANK_DEFAULTS.company_bank_name,
      company_branch:         pi.company_branch         || COMPANY_BANK_DEFAULTS.company_branch,
      company_swift:          pi.company_swift          || COMPANY_BANK_DEFAULTS.company_swift,
    });
  }, [shipment, reset]);

  const onSubmit = async (data: ProformaInvoiceForm) => {
    setIsSubmitting(true);
    try {
      await shipmentApi.saveProformaInvoice(shipmentId, data as Record<string, unknown>);
      setToast({ message: 'Proforma Invoice saved successfully!', type: 'success' });
      setTimeout(() => router.push(`/shipment/${shipmentId}/trade-facility`), 800);
    } catch {
      setToast({ message: 'Failed to save Proforma Invoice.', type: 'error' });
      setIsSubmitting(false);
    }
  };

  const handleSaveDraft = useCallback(async () => {
    setIsSubmitting(true);
    try {
      const values = getValues();
      await shipmentApi.saveProformaInvoice(shipmentId, values as Record<string, unknown>);
      setToast({ message: 'Draft saved.', type: 'success' });
    } catch {
      setToast({ message: 'Failed to save draft.', type: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  }, [getValues, shipmentId]);

  // ── Build full preview data: shipment base + live form values ────────────────
  // This ensures intermediate bank and company bank always appear in preview
  const liveValues = useWatch({ control });
  const previewData = {
    // Shipment base data
    invoice_no:                    shipment?.invoice_info?.invoice_no,
    invoice_date:                  shipment?.invoice_info?.invoice_date,
    buyer_order_no_date:           shipment?.invoice_info?.buyer_order_no_date,
    exporter_reference:            shipment?.invoice_info?.exporter_reference,
    other_reference:               shipment?.invoice_info?.other_reference,
    reference_proforma_invoice_no: shipment?.invoice_info?.reference_proforma_invoice_no,
    consignee_name:    shipment?.buyer?.consignee_name,
    buyer_name:        shipment?.buyer?.buyer_name,
    buyer_address:     shipment?.buyer?.buyer_address,
    buyer_postal_code: shipment?.buyer?.buyer_postal_code,
    buyer_country:     shipment?.buyer?.buyer_country,
    pre_carriage_by:              shipment?.shipment_details?.pre_carriage_by,
    vessel_flight_no:             shipment?.shipment_details?.vessel_flight_no,
    place_of_receipt:             shipment?.shipment_details?.place_of_receipt,
    port_of_loading:              shipment?.shipment_details?.port_of_loading,
    port_of_discharge:            shipment?.shipment_details?.port_of_discharge,
    final_destination:            shipment?.shipment_details?.final_destination,
    country_of_origin:            shipment?.shipment_details?.country_of_origin,
    country_of_final_destination: shipment?.shipment_details?.country_of_final_destination,
    terms_of_delivery:            shipment?.shipment_details?.terms_of_delivery,
    brand_name:     shipment?.product?.brand_name,
    product_name:   shipment?.product?.product_name,
    container_type: shipment?.product?.container_type,
    container_no:   shipment?.product?.container_no,
    cartons:          shipment?.package?.cartons,
    trays_per_carton: shipment?.package?.trays_per_carton,
    eggs_per_tray:    shipment?.package?.eggs_per_tray,
    rate_per_egg_usd: shipment?.pricing?.rate_per_egg_usd,
    net_weight_per_carton:   shipment?.weight?.net_weight_per_carton,
    gross_weight_per_carton: shipment?.weight?.gross_weight_per_carton,
    // Live proforma form values (always up-to-date, overrides stale DB values)
    ...liveValues,
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

      <div className="flex flex-col xl:flex-row gap-6">

        {/* ── Proforma-Specific Form ─────────────────────────────────────────── */}
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex-1 space-y-6 bg-white p-6 md:p-8 rounded-xl shadow-sm border border-gray-200"
          noValidate
        >
          {/* Shipment data reuse notice */}
          <div className="bg-green-50 border border-green-200 rounded-lg px-4 py-3">
            <p className="text-xs font-semibold text-green-700 uppercase tracking-wide mb-1">
              Shipment Data Auto-Reused ✓
            </p>
            <p className="text-sm text-green-800">
              All Invoice, Buyer, Ports, Product, Pricing &amp; Weight data from Step 1 is automatically applied to this document.
              Only fill in the fields unique to the Proforma Invoice below.
            </p>
          </div>

          {/* ── 1. Proforma Invoice Reference ──────────────────────────────── */}
          <SectionHeader title="1. Proforma Invoice Reference" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <Input
              label="Proforma Invoice Number"
              id="proforma_invoice_number"
              register={register('proforma_invoice_number')}
              error={errors.proforma_invoice_number?.message}
            />
            <Input
              label="PO Number"
              id="po_number"
              register={register('po_number')}
            />
            <Input
              label="PO Date"
              id="po_date"
              register={register('po_date')}
              placeholder="e.g. 30.06.2026"
            />
          </div>

          {/* ── 2. Buyer & Consignee TRN ───────────────────────────────────── */}
          <SectionHeader title="2. Tax Registration Numbers (TRN)" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Input
              label="Buyer TRN"
              id="buyer_trn"
              register={register('buyer_trn')}
            />
            <Input
              label="Consignee TRN"
              id="consignee_trn"
              register={register('consignee_trn')}
            />
          </div>

          {/* ── 3. Notify Party ────────────────────────────────────────────── */}
          <SectionHeader title="3. Notify Party" />
          <div className="grid grid-cols-1 gap-5">
            <Input
              label="Notify Party Name"
              id="notify_party"
              register={register('notify_party')}
            />
            <Textarea
              label="Notify Party Address"
              id="notify_party_address"
              register={register('notify_party_address')}
              rows={3}
            />
          </div>

          {/* ── 4. Payment & Delivery ──────────────────────────────────────── */}
          <SectionHeader title="4. Payment & Delivery Terms" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <Input
              label="Payment Terms"
              id="payment_terms"
              register={register('payment_terms')}
              className="sm:col-span-2"
            />
            <Input
              label="Expiry Date"
              id="expiry_date"
              register={register('expiry_date')}
              placeholder="e.g. 30.07.2026"
            />
            <Input
              label="No. & Kind of Packages"
              id="no_and_kind_of_packages"
              register={register('no_and_kind_of_packages')}
              className="sm:col-span-2 lg:col-span-3"
            />
          </div>

          {/* ── 5. Company Bank Details ────────────────────────────────────── */}
          <SectionHeader title="5. Company Bank Details" />
          <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-2 mb-1">
            <p className="text-xs text-blue-700">Pre-filled with company defaults. Edit only if required.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <Input
              label="Account Name"
              id="company_account_name"
              register={register('company_account_name')}
              className="sm:col-span-2"
            />
            <Input
              label="Account Number"
              id="company_account_number"
              register={register('company_account_number')}
            />
            <Input
              label="Bank Name"
              id="company_bank_name"
              register={register('company_bank_name')}
              className="sm:col-span-2"
            />
            <Input
              label="Branch"
              id="company_branch"
              register={register('company_branch')}
            />
            <Input
              label="SWIFT Code"
              id="company_swift"
              register={register('company_swift')}
            />
          </div>

          {/* ── 6. Intermediate / Correspondent Bank ───────────────────────── */}
          <SectionHeader title="6. Intermediate / Correspondent Bank" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Input
              label="Intermediate Bank Name"
              id="intermediate_bank_name"
              register={register('intermediate_bank_name')}
              className="sm:col-span-2"
            />
            <Input
              label="Intermediate Bank Account Number"
              id="intermediate_bank_account_number"
              register={register('intermediate_bank_account_number')}
            />
            <Input
              label="Intermediate Bank SWIFT"
              id="intermediate_bank_swift"
              register={register('intermediate_bank_swift')}
            />
            <Input
              label="Intermediate Bank Routing Number"
              id="intermediate_bank_routing_number"
              register={register('intermediate_bank_routing_number')}
            />
            <Input
              label="Correspondent Bank"
              id="correspondent_bank"
              register={register('correspondent_bank')}
            />
          </div>

          <FormNavigator
            shipmentId={shipmentId}
            isSubmitting={isSubmitting}
            onSaveDraft={handleSaveDraft}
            prevStepPath="packing-list"
            nextLabel="Save & Continue →"
          />
        </form>

        {/* ── Live Preview Panel ─────────────────────────────────────────────── */}
        <div className="hidden xl:block w-[580px] shrink-0">
          <div className="sticky top-6">
            <div className="bg-white border border-gray-200 rounded-b-xl shadow-sm overflow-auto max-h-[85vh]">
              <PDFPreviewViewer shipmentId={shipmentId} docType="proforma_invoice" data={previewData} />
            </div>
          </div>
        </div>

      </div>
    </>
  );
}