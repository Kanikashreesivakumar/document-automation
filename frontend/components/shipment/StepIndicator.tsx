"use client";

import React from 'react';
import Link from 'next/link';

interface StepIndicatorProps {
  currentStep: number;
  shipmentId: string;
}

export const StepIndicator: React.FC<StepIndicatorProps> = ({ currentStep, shipmentId }) => {
  const steps = [
    { num: 1, name: 'Invoice',          path: 'invoice' },
    { num: 2, name: 'Packing List',     path: 'packing-list' },
    { num: 3, name: 'Proforma',         path: 'proforma-invoice' },
    { num: 4, name: 'Trade Facility',   path: 'trade-facility' },
    { num: 5, name: 'Export Insurance', path: 'insurance' },
    { num: 6, name: 'Health Cert',      path: 'health-certificate' },
  ];

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <React.Fragment key={step.num}>
            <div className="flex flex-col items-center">
              <Link
                href={`/shipment/${shipmentId}/${step.path}`}
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold text-sm transition-colors ${
                  currentStep === step.num
                    ? 'bg-blue-600 text-white shadow-md'
                    : currentStep > step.num
                    ? 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                    : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                }`}
              >
                {step.num}
              </Link>
              <span className={`text-xs mt-2 font-medium hidden sm:block ${
                currentStep === step.num ? 'text-blue-700' : 'text-gray-500'
              }`}>
                {step.name}
              </span>
            </div>
            {index < steps.length - 1 && (
              <div className={`flex-1 h-1 mx-2 sm:mx-4 rounded ${
                currentStep > step.num ? 'bg-blue-200' : 'bg-gray-100'
              }`} />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};
