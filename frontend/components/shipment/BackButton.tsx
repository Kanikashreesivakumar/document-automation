"use client";

import React from 'react';
import { useRouter } from 'next/navigation';

interface BackButtonProps {
  /** Where to navigate. Defaults to /shipment (the shipments dashboard). */
  href?: string;
  label?: string;
}

/**
 * A reusable "← Back to Shipments" button that uses Next.js client-side routing.
 * Displayed at the top-left of every shipment document page.
 */
export const BackButton: React.FC<BackButtonProps> = ({
  href = '/shipment',
  label = '← Back to Shipments',
}) => {
  const router = useRouter();

  return (
    <button
      type="button"
      onClick={() => router.push(href)}
      className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-blue-700 transition-colors group"
    >
      <svg
        className="w-4 h-4 transition-transform group-hover:-translate-x-0.5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
      </svg>
      {label}
    </button>
  );
};
