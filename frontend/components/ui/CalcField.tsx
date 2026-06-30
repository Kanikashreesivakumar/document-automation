/** Read-only calculated field display — styled to match editable inputs but clearly disabled */
import React from 'react';

interface CalcFieldProps {
  label: string;
  value: string | number;
  className?: string;
}

export const CalcField: React.FC<CalcFieldProps> = ({ label, value, className = '' }) => (
  <div className={`flex flex-col gap-1 ${className}`}>
    <label className="text-sm font-semibold text-gray-800">{label}</label>
    <div className="px-3 py-2 text-gray-700 font-mono font-semibold border border-gray-300 rounded-md bg-blue-50 shadow-sm select-none">
      {value}
    </div>
  </div>
);
