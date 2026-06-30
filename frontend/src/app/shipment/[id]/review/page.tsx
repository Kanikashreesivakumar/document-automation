"use client";

import React, { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Header from '@/components/Header';
import { FormNavigator } from '@/components/shipment/FormNavigator';
import { shipmentApi } from '@/services/shipmentApi';
import { Toast } from '@/components/ui/Toast';

export default function ReviewPage() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [generatedDocs, setGeneratedDocs] = useState<any[]>([]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const res = await shipmentApi.generateDocuments(id);
      if (res.data?.success) {
        setGeneratedDocs(res.data.documents);
        setToast({ message: 'Documents generated successfully!', type: 'success' });
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      const msg = typeof detail === 'string' ? detail : 'Failed to generate documents.';
      setToast({ message: msg, type: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNewShipment = async () => {
    try {
      const res = await shipmentApi.createShipment();
      const newId = res.data?.id;
      if (newId) {
        router.push(`/shipment/${newId}/invoice`);
      }
    } catch {
      setToast({ message: 'Failed to create new shipment.', type: 'error' });
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* ─── Navigation bar ─── */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={() => router.push(`/shipment/${id}/animal-annexure`)}
              className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-blue-700 transition-colors group"
            >
              <svg className="w-4 h-4 transition-transform group-hover:-translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Animal Annexure
            </button>
            <span className="text-gray-300">|</span>
            <button
              type="button"
              onClick={() => router.push('/shipment')}
              className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-blue-700 transition-colors"
            >
              🏠 Back to Shipments
            </button>
          </div>
        </div>

        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Review & Generate</h2>
          <p className="text-gray-500 mt-1">Review your shipment and generate all final documents.</p>
        </div>

        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

        <div className="bg-white p-6 md:p-8 rounded-xl shadow-sm border border-gray-200">
          <form onSubmit={handleGenerate}>
            <div className="text-center py-10">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to generate?</h3>
              <p className="text-gray-500 max-w-md mx-auto mb-8">
                Clicking generate will compile all forms and build pixel-perfect Word Documents matching your reference PDFs.
              </p>
            </div>

            {generatedDocs.length > 0 && (
              <div className="mt-8 border-t border-gray-100 pt-8">
                <h4 className="text-lg font-medium text-gray-900 mb-4">Generated Documents</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                  {generatedDocs.map((doc) => (
                    <a
                      key={doc.id}
                      href={shipmentApi.getDownloadUrl(id, doc.doc_type)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-4 border border-blue-200 bg-blue-50 rounded-lg flex items-center justify-between hover:bg-blue-100 transition-colors"
                    >
                      <span className="font-medium text-blue-900 truncate mr-2" title={doc.file_name}>
                        {doc.file_name}
                      </span>
                      <svg className="w-5 h-5 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                    </a>
                  ))}
                </div>

                {/* ─── Download all + navigation buttons ─── */}
                <div className="flex flex-wrap items-center justify-between gap-4 pt-6 border-t border-gray-100">
                  <button
                    type="button"
                    onClick={() => router.push('/shipment')}
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg border border-gray-300 text-sm font-medium text-slate-700 hover:bg-gray-50 transition-colors"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Back to Shipments
                  </button>

                  <div className="flex gap-3">
                    <a
                      href={shipmentApi.getAllDownloadUrl(id)}
                      className="inline-flex justify-center py-2 px-6 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                    >
                      Download All as ZIP
                    </a>
                    <button
                      type="button"
                      onClick={handleNewShipment}
                      className="inline-flex items-center gap-1.5 px-5 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm"
                    >
                      + New Shipment
                    </button>
                  </div>
                </div>
              </div>
            )}

            {!generatedDocs.length && (
              <FormNavigator
                shipmentId={id}
                isSubmitting={isSubmitting}
                prevStepPath="animal-annexure"
                isReview={true}
              />
            )}
          </form>
        </div>
      </main>
    </div>
  );
}
