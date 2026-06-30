import React from 'react';
import Header from '@/components/Header';
import { StepIndicator } from '@/components/shipment/StepIndicator';
import AnimalCertificateForm from '@/components/shipment/AnimalCertificateForm';
import { BackButton } from '@/components/shipment/BackButton';

export default async function AnimalCertificatePage({ params }: { params: Promise<{ id: string }> }) {
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
              <h1 className="text-2xl font-bold text-slate-800">Animal Health Certificate</h1>
              <p className="text-slate-500 mt-1">
                Veterinary certificate for export — most fields are auto-populated from shipment data.
              </p>
            </div>
          </div>
          <StepIndicator currentStep={6} shipmentId={id} />
          <AnimalCertificateForm shipmentId={id} />
        </div>
      </main>
    </div>
  );
}
