"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '../ui/Button';

interface FormNavigatorProps {
  shipmentId: string;
  isSubmitting: boolean;
  onSaveDraft?: () => void;
  prevStepPath?: string;
  nextLabel?: string;
  isReview?: boolean;
}

export const FormNavigator: React.FC<FormNavigatorProps> = ({
  shipmentId,
  isSubmitting,
  onSaveDraft,
  prevStepPath,
  nextLabel = 'Save & Continue',
  isReview = false,
}) => {
  const router = useRouter();

  return (
    <div className="pt-8 mt-8 border-t border-gray-200 flex flex-wrap justify-between gap-4">
      <div>
        {prevStepPath && (
          <Button
            type="button"
            variant="secondary"
            onClick={() => router.push(`/shipment/${shipmentId}/${prevStepPath}`)}
          >
            ← Previous
          </Button>
        )}
      </div>
      <div className="flex gap-4">
        {onSaveDraft && !isReview && (
          <Button type="button" variant="secondary" onClick={onSaveDraft}>
            Save Draft
          </Button>
        )}
        
        {isReview ? (
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? 'Generating...' : 'Generate Documents'}
          </Button>
        ) : (
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : nextLabel}
          </Button>
        )}
      </div>
    </div>
  );
};
