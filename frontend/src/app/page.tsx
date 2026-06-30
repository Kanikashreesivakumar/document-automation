import React from 'react';
import Header from '@/components/Header';
import DashboardCard from '@/components/DashboardCard';
import RecentDocuments from '@/components/RecentDocuments';

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Welcome to your Workspace</h2>
          <p className="text-gray-500 mt-1">Manage your templates and automate your document workflows.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10 max-w-4xl mx-auto">
          <DashboardCard 
            title="Create Shipment" 
            description="Initialize a new shipment and prepare forms."
            colorClass="bg-blue-50 text-blue-600"
            href="/shipment"
            icon={
              <svg width="24" height="24" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            }
          />
          <DashboardCard 
            title="Templates" 
            description="Manage your dynamic DOCX templates."
            colorClass="bg-amber-50 text-amber-600"
            href="/templates"
            icon={
              <svg width="24" height="24" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            }
          />
        </div>

        <RecentDocuments />
      </main>
    </div>
  );
}
