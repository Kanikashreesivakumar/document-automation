"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { PackingListPreview } from './PackingListPreview';
import { useShipmentData } from '../../hooks/useShipmentData';

interface PackingListClientProps {
  shipmentId: string;
}

export default function PackingListClient({ shipmentId }: PackingListClientProps) {
  const router = useRouter();
  const { data: shipment, loading } = useShipmentData(shipmentId);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600" />
      </div>
    );
  }

  const inv  = shipment?.invoice_info || {};
  const buy  = shipment?.buyer || {};
  const det  = shipment?.shipment_details || {};
  const prod = shipment?.product || {};
  const pkg  = shipment?.package || {};
  const wt   = shipment?.weight || {};

  const previewData = {
    invoiceNo:           inv.invoice_no,
    invoiceDate:         inv.invoice_date,
    shippingBillNo:      inv.shipping_bill_no,
    shippingBillDate:    inv.shipping_bill_date,
    consigneeName:       buy.consignee_name,
    buyerName:           buy.buyer_name,
    buyerAddress:        buy.buyer_address,
    buyerCountry:        buy.buyer_country,
    preCarriageBy:       det.pre_carriage_by,
    vesselFlightNo:      det.vessel_flight_no,
    placeOfReceipt:      det.place_of_receipt,
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
    traysPerCarton:      pkg.trays_per_carton,
    eggsPerTray:         pkg.eggs_per_tray,
    eggsPerCarton:       pkg.eggs_per_carton,
    totalEggs:           pkg.total_eggs,
    netWeightPerCarton:  wt.net_weight_per_carton,
    grossWeightPerCarton: wt.gross_weight_per_carton,
    netWeight:           wt.net_weight,
    grossWeight:         wt.gross_weight,
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Preview Card */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="bg-gray-800 text-white px-4 py-2 text-xs font-semibold uppercase tracking-widest">
          Packing List Preview — Auto-Generated from Shipment Data
        </div>
        <div className="overflow-auto max-h-[75vh] p-2">
          <PackingListPreview data={previewData} />
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex flex-wrap gap-4 justify-between pt-4 border-t border-gray-200">
        <Link
          href={`/shipment/${shipmentId}/invoice`}
          className="inline-flex items-center px-5 py-2.5 bg-white text-gray-700 rounded-lg border border-gray-300 font-medium text-sm hover:bg-gray-50 transition-colors"
        >
          ← Back to Invoice
        </Link>
        <button
          onClick={() => router.push(`/shipment/${shipmentId}/proforma-invoice`)}
          className="inline-flex items-center px-6 py-2.5 bg-blue-600 text-white rounded-lg font-medium text-sm hover:bg-blue-700 transition-colors shadow-sm"
        >
          Continue to Proforma Invoice →
        </button>
      </div>
    </div>
  );
}
