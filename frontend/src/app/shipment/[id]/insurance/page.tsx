import React from 'react';
import Header from '@/components/Header';
import { StepIndicator } from '@/components/shipment/StepIndicator';
import ExportInsuranceForm from '@/components/shipment/ExportInsuranceForm';
import { BackButton } from '@/components/shipment/BackButton';

export default async function ExportInsurancePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      <main className="flex-1 overflow-auto p-4 md:p-8">
        <div className="max-w-[1400px] mx-auto w-full">
          <div className="mb-2">
            <BackButton />
          </div>
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-slate-800">Export Insurance</h1>
              <p className="text-slate-500 mt-1">Review and fill the details for Export Insurance.</p>
            </div>
          </div>
          <StepIndicator currentStep={5} shipmentId={id} />
          <ExportInsuranceForm shipmentId={id} />
        </div>
      </main>
    </div>
  );
}
