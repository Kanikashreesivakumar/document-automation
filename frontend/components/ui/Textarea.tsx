import React from 'react';
import { UseFormRegisterReturn } from 'react-hook-form';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
  register?: UseFormRegisterReturn;
  hint?: string;
}

export const Textarea: React.FC<TextareaProps> = ({ label, error, register, hint, className = '', ...props }) => {
  return (
    <div className={`flex flex-col gap-1 ${className}`}>
      <label className="text-sm font-semibold text-gray-800">{label}</label>
      <textarea
        {...register}
        {...props}
        className={`
          px-3 py-2 text-gray-900 border rounded-md shadow-sm resize-y
          placeholder:text-gray-400
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
          disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed
          ${error ? 'border-red-400 bg-red-50' : 'border-gray-400 bg-white'}
        `}
      />
      {hint && !error && <span className="text-xs text-gray-400">{hint}</span>}
      {error && <span className="text-xs text-red-600 font-medium">{error}</span>}
    </div>
  );
};
