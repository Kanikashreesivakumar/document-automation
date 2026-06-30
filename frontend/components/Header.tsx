import React from 'react';

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-30 w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-4">
            {/* Logo placeholder */}
            <div className="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center shadow-sm">
              <span className="text-white font-bold text-xl">DA</span>
            </div>
            <h1 className="text-xl font-semibold text-gray-900 tracking-tight">
              Document Template Automation System
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Optional profile / settings icon placeholder */}
            <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center border border-gray-200">
              <span className="text-sm font-medium text-gray-600">AD</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
