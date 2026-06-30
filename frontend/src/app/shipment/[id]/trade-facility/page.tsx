import React from 'react';
import Header from '@/components/Header';
import { StepIndicator } from '@/components/shipment/StepIndicator';
import TradeFacilityForm from '@/components/shipment/TradeFacilityForm';
import { BackButton } from '@/components/shipment/BackButton';

export default async function TradeFacilityPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-2">
          <BackButton />
        </div>
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Trade Facility</h2>
          <p className="text-gray-500 mt-1">
            Step 4: Additional details for Self-Sealed Container. Shipment data is auto-populated.
          </p>
        </div>
        <StepIndicator currentStep={4} shipmentId={id} />
        <TradeFacilityForm shipmentId={id} />
      </main>
    </div>
  );
}
