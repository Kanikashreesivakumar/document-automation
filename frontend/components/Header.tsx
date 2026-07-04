import React from 'react';
import Image from "next/image";

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-30 w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-4">
            <div className="h-12 w-12 rounded-lg overflow-hidden shadow-md">
              <Image
                src="/logo.png"
                alt="Document Template Automation Logo"
                width={48}
                height={48}
                className="object-contain w-full h-full"
                priority
              />
            </div>
            <h1 className="text-xl font-semibold text-gray-900 tracking-tight">
              Document Template Automation System
            </h1>
          </div>

          <div className="flex items-center gap-4">
          </div>
        </div>
      </div>
    </header>
  );
}
