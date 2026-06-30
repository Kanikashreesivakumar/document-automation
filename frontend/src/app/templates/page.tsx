import React from 'react';
import Header from '@/components/Header';

export default function TemplatesPage() {
  const templates = [
    { name: "Master_Commercial_Invoice_v2", type: "DOCX", lastUpdated: "2026-06-25" },
    { name: "Packing_List_Template_EU", type: "DOCX", lastUpdated: "2026-06-20" },
    { name: "Vet_Certificate_Standard", type: "DOCX", lastUpdated: "2026-05-15" },
    { name: "General_Annexure", type: "DOCX", lastUpdated: "2026-06-01" },
    { name: "Insurance_Declaration", type: "DOCX", lastUpdated: "2026-04-10" },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 flex justify-between items-end">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Template Management</h2>
            <p className="text-gray-500 mt-1">Manage and update your dynamic DOCX templates.</p>
          </div>
          <button disabled className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium text-sm shadow-sm opacity-50 cursor-not-allowed">
            Upload Template
          </button>
        </div>
        
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="px-6 py-4 text-sm font-medium text-gray-500 uppercase tracking-wider">Template Name</th>
                  <th className="px-6 py-4 text-sm font-medium text-gray-500 uppercase tracking-wider">File Type</th>
                  <th className="px-6 py-4 text-sm font-medium text-gray-500 uppercase tracking-wider">Last Updated</th>
                  <th className="px-6 py-4 text-sm font-medium text-gray-500 uppercase tracking-wider text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {templates.map((tpl, idx) => (
                  <tr key={idx} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-3">
                        <svg width="20" height="20" className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                        </svg>
                        <span className="font-medium text-gray-900">{tpl.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-semibold">{tpl.type}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{tpl.lastUpdated}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                      <button disabled className="text-blue-600 hover:text-blue-900 font-medium mr-4 opacity-50 cursor-not-allowed">Edit</button>
                      <button disabled className="text-red-600 hover:text-red-900 font-medium opacity-50 cursor-not-allowed">Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
