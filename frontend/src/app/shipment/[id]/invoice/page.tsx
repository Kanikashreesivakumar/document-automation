import React from 'react';
import ShipmentDataFormComponent from '@/components/shipment/ShipmentDataForm';
import Header from '@/components/Header';
import { StepIndicator } from '@/components/shipment/StepIndicator';
import { BackButton } from '@/components/shipment/BackButton';

export default async function InvoicePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-2">
          <BackButton />
        </div>
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Shipment Data</h2>
          <p className="text-gray-500 mt-1">
            Fill once — generates both Invoice and Packing List automatically.
          </p>
        </div>
        <StepIndicator currentStep={1} shipmentId={id} />
        <ShipmentDataFormComponent shipmentId={id} />
      </main>
    </div>
  );
}
