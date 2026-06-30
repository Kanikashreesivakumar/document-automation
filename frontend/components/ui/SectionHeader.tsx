import React from 'react';

interface SectionHeaderProps {
  title: string;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({ title }) => {
  return (
    <div className="border-b border-gray-200 pb-2 mb-4 mt-8 first:mt-0">
      <h3 className="text-lg font-medium text-gray-900">{title}</h3>
    </div>
  );
};
