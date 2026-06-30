"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import { zodResolver } from '@hookform/resolvers/zod';
import { proformaInvoiceSchema, ProformaInvoiceForm } from '../../schemas/proformaInvoice';
import { Input } from '../ui/Input';
import { Textarea } from '../ui/Textarea';
import { SectionHeader } from '../ui/SectionHeader';
import { Toast } from '../ui/Toast';
import { FormNavigator } from './FormNavigator';
import { shipmentApi } from '../../services/shipmentApi';
import { useShipmentData } from '../../hooks/useShipmentData';
import { ProformaInvoicePreview } from './ProformaInvoicePreview';
import { numberToWords } from '../../utils/numberToWords';

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
    formState: { errors },
  } = useForm<ProformaInvoiceForm>({
    resolver: zodResolver(proformaInvoiceSchema),
    defaultValues: {},
  });

  // Load existing proforma data when shipment loads
  useEffect(() => {
    if (!shipment?.proforma_invoice) return;
    const pi = shipment.proforma_invoice;
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
    });
  }, [shipment, reset]);

  // Watch proforma fields for live preview
  const wPoNumber                    = useWatch({ control, name: 'po_number' });
  const wPoDate                      = useWatch({ control, name: 'po_date' });
  const wProformaInvoiceNumber       = useWatch({ control, name: 'proforma_invoice_number' });
  const wBuyerTrn                    = useWatch({ control, name: 'buyer_trn' });
  const wConsigneeTrn                = useWatch({ control, name: 'consignee_trn' });
  const wNotifyParty                 = useWatch({ control, name: 'notify_party' });
  const wNotifyPartyAddress          = useWatch({ control, name: 'notify_party_address' });
  const wPaymentTerms                = useWatch({ control, name: 'payment_terms' });
  const wExpiryDate                  = useWatch({ control, name: 'expiry_date' });
  const wNoAndKindOfPackages         = useWatch({ control, name: 'no_and_kind_of_packages' });
  const wIntermediateBankName        = useWatch({ control, name: 'intermediate_bank_name' });
  const wIntermediateBankAccountNo   = useWatch({ control, name: 'intermediate_bank_account_number' });
  const wIntermediateBankSwift       = useWatch({ control, name: 'intermediate_bank_swift' });
  const wIntermediateBankRouting     = useWatch({ control, name: 'intermediate_bank_routing_number' });
  const wCorrespondentBank           = useWatch({ control, name: 'correspondent_bank' });

  // Build shipment-derived preview data (auto-reused, never re-asked)
  const inv  = shipment?.invoice_info || {};
  const buy  = shipment?.buyer || {};
  const det  = shipment?.shipment_details || {};
  const prod = shipment?.product || {};
  const pkg  = shipment?.package || {};
  const pri  = shipment?.pricing || {};
  const wt   = shipment?.weight || {};

  const amountUSD   = pri.amount_usd || 0;
  const amountWords = amountUSD > 0 ? numberToWords(amountUSD) : '—';

  const previewData = {
    // From Shipment — auto-reused
    invoiceNo:           inv.invoice_no,
    invoiceDate:         inv.invoice_date,
    consigneeName:       buy.consignee_name,
    buyerName:           buy.buyer_name,
    buyerAddress:        buy.buyer_address,
    buyerCountry:        buy.buyer_country,
    preCarriageBy:       det.pre_carriage_by,
    vesselFlightNo:      det.vessel_flight_no,
    portOfLoading:       det.port_of_loading,
    portOfDischarge:     det.port_of_discharge,
    finalDestination:    det.final_destination,
    countryOfOrigin:     det.country_of_origin,
    termsOfDelivery:     det.terms_of_delivery,
    brandName:           prod.brand_name,
    productName:         prod.product_name,
    containerType:       prod.container_type,
    containerNo:         prod.container_no,
    cartons:             pkg.cartons,
    eggsPerCarton:       pkg.eggs_per_carton,
    totalEggs:           pkg.total_eggs,
    ratePerEggUsd:       pri.rate_per_egg_usd,
    amountUsd:           amountUSD,
    amountInWords:       amountWords,
    netWeight:           wt.net_weight,
    grossWeight:         wt.gross_weight,
    // Proforma-specific — from live form
    proformaInvoiceNumber:          wProformaInvoiceNumber,
    poNumber:                       wPoNumber,
    poDate:                         wPoDate,
    buyerTrn:                       wBuyerTrn,
    consigneeTrn:                   wConsigneeTrn,
    notifyParty:                    wNotifyParty,
    notifyPartyAddress:             wNotifyPartyAddress,
    paymentTerms:                   wPaymentTerms,
    expiryDate:                     wExpiryDate,
    noAndKindOfPackages:            wNoAndKindOfPackages,
    intermediateBankName:           wIntermediateBankName,
    intermediateBankAccountNumber:  wIntermediateBankAccountNo,
    intermediateBankSwift:          wIntermediateBankSwift,
    intermediateBankRoutingNumber:  wIntermediateBankRouting,
    correspondentBank:              wCorrespondentBank,
  };

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
      const values = control._formValues as ProformaInvoiceForm;
      await shipmentApi.saveProformaInvoice(shipmentId, values as Record<string, unknown>);
      setToast({ message: 'Draft saved.', type: 'success' });
    } catch {
      setToast({ message: 'Failed to save draft.', type: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  }, [control, shipmentId]);

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

          {/* ── 5. Banking Details ─────────────────────────────────────────── */}
          <SectionHeader title="5. Banking Details" />
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
            <div className="bg-gray-800 text-white px-4 py-2 text-xs font-semibold uppercase tracking-widest rounded-t-xl">
              Live Proforma Invoice Preview
            </div>
            <div className="bg-white border border-gray-200 rounded-b-xl shadow-sm overflow-auto max-h-[85vh]">
              <ProformaInvoicePreview data={previewData} />
            </div>
          </div>
        </div>

      </div>
    </>
  );
}
