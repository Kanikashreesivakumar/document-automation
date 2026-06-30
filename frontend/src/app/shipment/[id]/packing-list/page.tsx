import React from 'react';
import Header from '@/components/Header';
import { StepIndicator } from '@/components/shipment/StepIndicator';
import PackingListClient from '@/components/shipment/PackingListClient';
import { BackButton } from '@/components/shipment/BackButton';

export default async function PackingListPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-2">
          <BackButton />
        </div>
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Packing List</h2>
          <p className="text-gray-500 mt-1">
            Step 2: Auto-generated from your Shipment Data — no duplicate entry required.
          </p>
        </div>
        <StepIndicator currentStep={2} shipmentId={id} />
        <PackingListClient shipmentId={id} />
      </main>
    </div>
  );
}
