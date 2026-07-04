"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { PDFPreviewViewer } from './PDFPreviewViewer';
import { buildPackingListPreviewData } from './documentPreviewData';
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
    invoice_no:                    inv.invoice_no,
    invoice_date:                  inv.invoice_date,
    buyer_order_no_date:           inv.buyer_order_no_date,
    reference_proforma_invoice_no: inv.reference_proforma_invoice_no,
    shipping_bill_no:              inv.shipping_bill_no,
    shipping_bill_date:            inv.shipping_bill_date,
    exporter_reference:            inv.exporter_reference,
    other_reference:               inv.other_reference,
    
    consignee_name:    buy.consignee_name,
    buyer_name:        buy.buyer_name,
    buyer_address:     buy.buyer_address,
    buyer_postal_code: buy.buyer_postal_code,
    buyer_country:     buy.buyer_country,
    
    pre_carriage_by:              det.pre_carriage_by,
    vessel_flight_no:             det.vessel_flight_no,
    place_of_receipt:             det.place_of_receipt,
    port_of_loading:              det.port_of_loading,
    port_of_discharge:            det.port_of_discharge,
    final_destination:            det.final_destination,
    country_of_origin:            det.country_of_origin,
    country_of_final_destination: det.country_of_final_destination,
    terms_of_delivery:            det.terms_of_delivery,
    
    brand_name:           prod.brand_name,
    product_name:         prod.product_name,
    container_type:       prod.container_type,
    container_no:         prod.container_no,
    shipment_declaration: prod.shipment_declaration,
    production_date:      prod.production_date,
    expiry_date:          prod.expiry_date,
    lot_number:           prod.lot_number,
    epcg_licence_number:  prod.epcg_licence_number,
    dt:                   prod.dt,
    egg_size:             prod.egg_size,
    pan_number:           prod.pan_number,
    gstin:                prod.gstin,
    hsn_code:             prod.hsn_code,
    
    cartons:          pkg.cartons,
    trays_per_carton: pkg.trays_per_carton,
    eggs_per_tray:    pkg.eggs_per_tray,
    
    rate_per_egg_usd: shipment?.pricing?.rate_per_egg_usd,
    
    net_weight_per_carton:   wt.net_weight_per_carton,
    gross_weight_per_carton: wt.gross_weight_per_carton,
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Preview Card */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="overflow-auto max-h-[75vh]">
          <PDFPreviewViewer shipmentId={shipmentId} docType="packing_list" data={previewData} />
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
