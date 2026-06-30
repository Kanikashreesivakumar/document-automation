"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import { zodResolver } from '@hookform/resolvers/zod';
import { shipmentDataSchema, ShipmentDataForm } from '../../schemas/shipment';
import { Input } from '../ui/Input';
import { Textarea } from '../ui/Textarea';
import { SectionHeader } from '../ui/SectionHeader';
import { CalcField } from '../ui/CalcField';
import { Toast } from '../ui/Toast';
import { FormNavigator } from './FormNavigator';
import { numberToWords } from '../../utils/numberToWords';
import { shipmentApi } from '../../services/shipmentApi';
import { useShipmentData } from '../../hooks/useShipmentData';
import { InvoicePreview, EXPORTER } from './InvoicePreview';

const DEFAULT_VALUES: Partial<ShipmentDataForm> = {
  pre_carriage_by:              'REEFER CONTAINER',
  country_of_origin:            'INDIA',
  container_type:               '1 X 40 FEET',
  terms_of_delivery:            'CIF SALALAH',
  product_name:                 'FRESH WHITE SHELL TABLE EGGS (CHICKEN).',
  brand_name:                   'RASI',
  trays_per_carton:             12,
  eggs_per_tray:                30,
  rate_per_egg_usd:             0.090278,
  net_weight_per_carton:        18.0,
  gross_weight_per_carton:      19.5,
};

interface ShipmentDataFormProps {
  shipmentId: string;
}

export default function ShipmentDataFormComponent({ shipmentId }: ShipmentDataFormProps) {
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
  } = useForm<ShipmentDataForm>({
    resolver: zodResolver(shipmentDataSchema),
    defaultValues: DEFAULT_VALUES,
  });

  // ── Load existing data from backend ────────────────────────────────────────
  useEffect(() => {
    if (!shipment) return;
    const inv  = shipment.invoice_info || {};
    const buy  = shipment.buyer || {};
    const det  = shipment.shipment_details || {};
    const prod = shipment.product || {};
    const pkg  = shipment.package || {};
    const pri  = shipment.pricing || {};
    const wt   = shipment.weight || {};

    reset({
      ...DEFAULT_VALUES,
      invoice_no:                    inv.invoice_no || '',
      invoice_date:                  inv.invoice_date || '',
      buyer_order_no_date:           inv.buyer_order_no_date || '',
      reference_proforma_invoice_no: inv.reference_proforma_invoice_no || '',
      shipping_bill_no:              inv.shipping_bill_no || '',
      shipping_bill_date:            inv.shipping_bill_date || '',

      consignee_name:    buy.consignee_name || '',
      buyer_name:        buy.buyer_name || '',
      buyer_address:     buy.buyer_address || '',
      buyer_postal_code: buy.buyer_postal_code || '',
      buyer_country:     buy.buyer_country || '',

      pre_carriage_by:              det.pre_carriage_by || DEFAULT_VALUES.pre_carriage_by,
      vessel_flight_no:             det.vessel_flight_no || '',
      place_of_receipt:             det.place_of_receipt || '',
      port_of_loading:              det.port_of_loading || '',
      port_of_discharge:            det.port_of_discharge || '',
      final_destination:            det.final_destination || '',
      country_of_origin:            det.country_of_origin || DEFAULT_VALUES.country_of_origin,
      country_of_final_destination: det.country_of_final_destination || '',
      terms_of_delivery:            det.terms_of_delivery || DEFAULT_VALUES.terms_of_delivery,

      brand_name:     prod.brand_name || DEFAULT_VALUES.brand_name,
      product_name:   prod.product_name || DEFAULT_VALUES.product_name,
      container_type: prod.container_type || DEFAULT_VALUES.container_type,
      container_no:   prod.container_no || '',

      cartons:          pkg.cartons || undefined,
      trays_per_carton: pkg.trays_per_carton || DEFAULT_VALUES.trays_per_carton,
      eggs_per_tray:    pkg.eggs_per_tray || DEFAULT_VALUES.eggs_per_tray,

      rate_per_egg_usd:        pri.rate_per_egg_usd || DEFAULT_VALUES.rate_per_egg_usd,
      net_weight_per_carton:   wt.net_weight_per_carton || DEFAULT_VALUES.net_weight_per_carton,
      gross_weight_per_carton: wt.gross_weight_per_carton || DEFAULT_VALUES.gross_weight_per_carton,
    });
  }, [shipment, reset]);

  // ── Watched values for live calculations ──────────────────────────────────
  const cartons          = useWatch({ control, name: 'cartons' }) ?? 0;
  const traysPerCarton   = useWatch({ control, name: 'trays_per_carton' }) ?? 0;
  const eggsPerTray      = useWatch({ control, name: 'eggs_per_tray' }) ?? 0;
  const ratePerEgg       = useWatch({ control, name: 'rate_per_egg_usd' }) ?? 0;
  const netWtPerCarton   = useWatch({ control, name: 'net_weight_per_carton' }) ?? 0;
  const grossWtPerCarton = useWatch({ control, name: 'gross_weight_per_carton' }) ?? 0;

  // ── Additional watched fields for live preview ────────────────────────────
  const wInvoiceNo                  = useWatch({ control, name: 'invoice_no' });
  const wInvoiceDate                = useWatch({ control, name: 'invoice_date' });
  const wBuyerOrderNoDate           = useWatch({ control, name: 'buyer_order_no_date' });
  const wRefProformaInvoiceNo       = useWatch({ control, name: 'reference_proforma_invoice_no' });
  const wShippingBillNo             = useWatch({ control, name: 'shipping_bill_no' });
  const wShippingBillDate           = useWatch({ control, name: 'shipping_bill_date' });
  const wConsigneeName              = useWatch({ control, name: 'consignee_name' });
  const wBuyerName                  = useWatch({ control, name: 'buyer_name' });
  const wBuyerAddress               = useWatch({ control, name: 'buyer_address' });
  const wBuyerPostalCode            = useWatch({ control, name: 'buyer_postal_code' });
  const wBuyerCountry               = useWatch({ control, name: 'buyer_country' });
  const wPreCarriageBy              = useWatch({ control, name: 'pre_carriage_by' });
  const wVesselFlightNo             = useWatch({ control, name: 'vessel_flight_no' });
  const wPlaceOfReceipt             = useWatch({ control, name: 'place_of_receipt' });
  const wPortOfLoading              = useWatch({ control, name: 'port_of_loading' });
  const wPortOfDischarge            = useWatch({ control, name: 'port_of_discharge' });
  const wFinalDestination           = useWatch({ control, name: 'final_destination' });
  const wCountryOfOrigin            = useWatch({ control, name: 'country_of_origin' });
  const wCountryOfFinalDestination  = useWatch({ control, name: 'country_of_final_destination' });
  const wTermsOfDelivery            = useWatch({ control, name: 'terms_of_delivery' });
  const wBrandName                  = useWatch({ control, name: 'brand_name' });
  const wProductName                = useWatch({ control, name: 'product_name' });
  const wContainerType              = useWatch({ control, name: 'container_type' });
  const wContainerNo                = useWatch({ control, name: 'container_no' });

  // ── Auto-calculated values (pure, no side effects) ─────────────────────────
  const eggsPerCarton = Math.round(Number(traysPerCarton) * Number(eggsPerTray));
  const totalEggs     = Math.round(Number(cartons) * eggsPerCarton);
  const amountUSD     = Math.round(totalEggs * Number(ratePerEgg) * 100) / 100;
  const netWeight     = Math.round(Number(cartons) * Number(netWtPerCarton) * 1000) / 1000;
  const grossWeight   = Math.round(Number(cartons) * Number(grossWtPerCarton) * 1000) / 1000;
  const amountWords   = amountUSD > 0 ? numberToWords(amountUSD) : '—';

  // ── Form submission ────────────────────────────────────────────────────────
  const onSubmit = async (data: ShipmentDataForm) => {
    setIsSubmitting(true);
    try {
      await shipmentApi.saveShipmentData(shipmentId, data as Record<string, unknown>);
      setToast({ message: 'Shipment data saved successfully!', type: 'success' });
      // Navigate to vet-certificate (next step)
      setTimeout(() => router.push(`/shipment/${shipmentId}/packing-list`), 800);
    } catch {
      setToast({ message: 'Failed to save shipment data.', type: 'error' });
      setIsSubmitting(false);
    }
  };

  const handleSaveDraft = useCallback(async () => {
    setIsSubmitting(true);
    try {
      const values = control._formValues as ShipmentDataForm;
      await shipmentApi.saveShipmentData(shipmentId, values as Record<string, unknown>);
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

        {/* ── Form ─────────────────────────────────────────────────────────── */}
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex-1 space-y-6 bg-white p-6 md:p-8 rounded-xl shadow-sm border border-gray-200"
          noValidate
        >

          {/* ── Static exporter banner ────────────────────────────────────── */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
            <p className="text-xs font-semibold text-blue-700 uppercase tracking-wide mb-1">Exporter (Fixed)</p>
            <p className="text-sm text-blue-900 font-medium">{EXPORTER.name}</p>
            <p className="text-xs text-blue-700">{EXPORTER.address}</p>
            <p className="text-xs text-blue-600 mt-0.5">
              GSTIN: {EXPORTER.gstin} &nbsp;|&nbsp; PAN: {EXPORTER.pan} &nbsp;|&nbsp; HSN: {EXPORTER.hsn}
            </p>
          </div>

          {/* ── 1. Invoice Information ─────────────────────────────────────── */}
          <SectionHeader title="1. Invoice Information" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <Input
              label="Invoice No."
              id="invoice_no"
              register={register('invoice_no')}
              error={errors.invoice_no?.message}
            />
            <Input
              label="Invoice Date"
              id="invoice_date"
              register={register('invoice_date')}
              placeholder="e.g. 30.06.2026"
              error={errors.invoice_date?.message}
            />
            <Input
              label="Buyer's Order No. & Date"
              id="buyer_order_no_date"
              register={register('buyer_order_no_date')}
            />
            <Input
              label="Reference Proforma Invoice No."
              id="reference_proforma_invoice_no"
              register={register('reference_proforma_invoice_no')}
              className="sm:col-span-2"
            />
            <Input
              label="Shipping Bill No."
              id="shipping_bill_no"
              register={register('shipping_bill_no')}
            />
            <Input
              label="Shipping Bill Date"
              id="shipping_bill_date"
              register={register('shipping_bill_date')}
              placeholder="e.g. 30.06.2026"
            />
          </div>

          {/* ── 2. Buyer / Consignee ──────────────────────────────────────── */}
          <SectionHeader title="2. Buyer / Consignee" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <Input
              label="Consignee Name"
              id="consignee_name"
              register={register('consignee_name')}
              error={errors.consignee_name?.message}
            />
            <Input
              label="Buyer Name (if other than consignee)"
              id="buyer_name"
              register={register('buyer_name')}
            />
            <Textarea
              label="Buyer Address"
              id="buyer_address"
              register={register('buyer_address')}
              rows={3}
            />
            <div className="grid grid-cols-2 gap-5">
              <Input
                label="Postal Code"
                id="buyer_postal_code"
                register={register('buyer_postal_code')}
              />
              <Input
                label="Country"
                id="buyer_country"
                register={register('buyer_country')}
                error={errors.buyer_country?.message}
              />
            </div>
          </div>

          {/* ── 3. Shipment Details ───────────────────────────────────────── */}
          <SectionHeader title="3. Shipment Details" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <Input
              label="Pre-Carriage By"
              id="pre_carriage_by"
              register={register('pre_carriage_by')}
              error={errors.pre_carriage_by?.message}
            />
            <Input
              label="Vessel / Flight No."
              id="vessel_flight_no"
              register={register('vessel_flight_no')}
            />
            <Input
              label="Place of Receipt"
              id="place_of_receipt"
              register={register('place_of_receipt')}
              error={errors.place_of_receipt?.message}
            />
            <Input
              label="Port of Loading"
              id="port_of_loading"
              register={register('port_of_loading')}
              error={errors.port_of_loading?.message}
            />
            <Input
              label="Port of Discharge"
              id="port_of_discharge"
              register={register('port_of_discharge')}
              error={errors.port_of_discharge?.message}
            />
            <Input
              label="Final Destination"
              id="final_destination"
              register={register('final_destination')}
              error={errors.final_destination?.message}
            />
            <Input
              label="Country of Origin"
              id="country_of_origin"
              register={register('country_of_origin')}
              error={errors.country_of_origin?.message}
            />
            <Input
              label="Country of Final Destination"
              id="country_of_final_destination"
              register={register('country_of_final_destination')}
              error={errors.country_of_final_destination?.message}
            />
            <Input
              label="Terms of Delivery"
              id="terms_of_delivery"
              register={register('terms_of_delivery')}
              error={errors.terms_of_delivery?.message}
            />
          </div>

          {/* ── 4. Product ────────────────────────────────────────────────── */}
          <SectionHeader title="4. Product" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <Input
              label="Brand Name"
              id="brand_name"
              register={register('brand_name')}
              error={errors.brand_name?.message}
            />
            <Input
              label="Container Type"
              id="container_type"
              register={register('container_type')}
              error={errors.container_type?.message}
            />
            <Input
              label="Container No."
              id="container_no"
              register={register('container_no')}
              error={errors.container_no?.message}
              className="lg:col-span-2"
            />
            <Input
              label="Product Name / Description"
              id="product_name"
              register={register('product_name')}
              className="sm:col-span-2 lg:col-span-4"
            />
          </div>

          {/* ── 5. Package ────────────────────────────────────────────────── */}
          <SectionHeader title="5. Package" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <Input
              label="Cartons"
              id="cartons"
              type="number"
              register={register('cartons', { valueAsNumber: true })}
              error={errors.cartons?.message}
            />
            <Input
              label="Trays per Carton"
              id="trays_per_carton"
              type="number"
              register={register('trays_per_carton', { valueAsNumber: true })}
              error={errors.trays_per_carton?.message}
            />
            <Input
              label="Eggs per Tray"
              id="eggs_per_tray"
              type="number"
              register={register('eggs_per_tray', { valueAsNumber: true })}
              error={errors.eggs_per_tray?.message}
            />
            <CalcField
              label="Eggs per Carton (Auto)"
              value={eggsPerCarton > 0 ? eggsPerCarton.toLocaleString() : '—'}
            />
            <CalcField
              label="Total Eggs (Auto)"
              value={totalEggs > 0 ? totalEggs.toLocaleString() + ' Nos' : '—'}
              className="sm:col-span-2"
            />
          </div>

          {/* ── 6. Pricing ────────────────────────────────────────────────── */}
          <SectionHeader title="6. Pricing" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <Input
              label="Rate per Egg (USD)"
              id="rate_per_egg_usd"
              type="number"
              step="0.000001"
              register={register('rate_per_egg_usd', { valueAsNumber: true })}
              error={errors.rate_per_egg_usd?.message}
            />
            <CalcField
              label="Amount USD (Auto)"
              value={amountUSD > 0
                ? `USD ${amountUSD.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
                : '—'}
              className="sm:col-span-2"
            />
          </div>
          {amountUSD > 0 && (
            <div className="rounded-lg bg-amber-50 border border-amber-200 px-4 py-2 text-sm text-amber-800">
              <span className="font-semibold">Amount in Words: </span>{amountWords}
            </div>
          )}

          {/* ── 7. Weight ─────────────────────────────────────────────────── */}
          <SectionHeader title="7. Weight" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <Input
              label="Net Weight per Carton (KGS)"
              id="net_weight_per_carton"
              type="number"
              step="0.001"
              register={register('net_weight_per_carton', { valueAsNumber: true })}
              error={errors.net_weight_per_carton?.message}
            />
            <Input
              label="Gross Weight per Carton (KGS)"
              id="gross_weight_per_carton"
              type="number"
              step="0.001"
              register={register('gross_weight_per_carton', { valueAsNumber: true })}
              error={errors.gross_weight_per_carton?.message}
            />
            <CalcField
              label="Total Net Weight (Auto)"
              value={netWeight > 0 ? `${netWeight.toFixed(3)} KGS` : '—'}
            />
            <CalcField
              label="Total Gross Weight (Auto)"
              value={grossWeight > 0 ? `${grossWeight.toFixed(3)} KGS` : '—'}
            />
          </div>

          <FormNavigator
            shipmentId={shipmentId}
            isSubmitting={isSubmitting}
            onSaveDraft={handleSaveDraft}
            nextLabel="Save & Continue →"
          />
        </form>

        {/* ── Live Preview Panel ──────────────────────────────────────────── */}
        <div className="hidden xl:block w-[580px] shrink-0">
          <div className="sticky top-6">
            <div className="bg-gray-800 text-white px-4 py-2 text-xs font-semibold uppercase tracking-widest rounded-t-xl">
              Live Invoice Preview
            </div>
            <div className="bg-white border border-gray-200 rounded-b-xl shadow-sm overflow-auto max-h-[85vh]">
              <InvoicePreview data={{
                invoiceNo:                  wInvoiceNo,
                invoiceDate:                wInvoiceDate,
                buyerOrderNoDate:           wBuyerOrderNoDate,
                referenceProformaInvoiceNo: wRefProformaInvoiceNo,
                shippingBillNo:             wShippingBillNo,
                shippingBillDate:           wShippingBillDate,
                consigneeName:              wConsigneeName,
                buyerName:                  wBuyerName,
                buyerAddress:               wBuyerAddress,
                buyerPostalCode:            wBuyerPostalCode,
                buyerCountry:               wBuyerCountry,
                preCarriageBy:              wPreCarriageBy,
                vesselFlightNo:             wVesselFlightNo,
                placeOfReceipt:             wPlaceOfReceipt,
                portOfLoading:              wPortOfLoading,
                portOfDischarge:            wPortOfDischarge,
                finalDestination:           wFinalDestination,
                countryOfOrigin:            wCountryOfOrigin,
                countryOfFinalDestination:  wCountryOfFinalDestination,
                termsOfDelivery:            wTermsOfDelivery,
                brandName:                  wBrandName,
                productName:                wProductName,
                containerType:              wContainerType,
                containerNo:                wContainerNo,
                cartons:                    Number(cartons),
                traysPerCarton:             Number(traysPerCarton),
                eggsPerCarton,
                totalEggs,
                ratePerEggUsd:              Number(ratePerEgg),
                amountUsd:                  amountUSD,
                amountInWords:              amountWords,
                netWeight,
                grossWeight,
              }} />
            </div>
          </div>
        </div>

      </div>
    </>
  );
}
