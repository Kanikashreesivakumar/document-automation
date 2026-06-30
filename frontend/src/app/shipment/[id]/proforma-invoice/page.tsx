import React from 'react';
import Header from '@/components/Header';
import { StepIndicator } from '@/components/shipment/StepIndicator';
import ProformaInvoiceForm from '@/components/shipment/ProformaInvoiceForm';
import { BackButton } from '@/components/shipment/BackButton';

export default async function ProformaInvoicePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-2">
          <BackButton />
        </div>
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Proforma Invoice</h2>
          <p className="text-gray-500 mt-1">
            Step 3: Fill in the Proforma Invoice details. All shipment data is auto-reused.
          </p>
        </div>
        <StepIndicator currentStep={3} shipmentId={id} />
        <ProformaInvoiceForm shipmentId={id} />
      </main>
    </div>
  );
}
