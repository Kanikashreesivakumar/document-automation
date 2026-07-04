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
              onClick={() => router.push(`/shipment/${id}/health-certificate`)}
              className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-blue-700 transition-colors group"
            >
              <svg className="w-4 h-4 transition-transform group-hover:-translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Health Certificate
            </button>
            <span className="text-gray-300">|</span>
            <button
              type="button"
              onClick={() => router.push('/shipment')}
              className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-blue-700 transition-colors"
            >
                Back to Shipments
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
                Clicking generate will compile all forms and build pixel-perfect PDF Documents matching your reference PDFs.
              </p>
            </div>

            {generatedDocs.length > 0 && (
              <div className="mt-8 border-t border-gray-100 pt-8">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                      <h4 className="text-sm font-medium text-green-800">Documents generated successfully!</h4>
                      <p className="text-xs text-green-600 mt-0.5">
                        Generated at {new Date().toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <a
                    href={shipmentApi.getAllDownloadUrl(id)}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 transition-colors shadow-sm"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download All ZIP
                  </a>
                </div>

                <h4 className="text-lg font-medium text-gray-900 mb-4">Generated PDF Documents</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  {generatedDocs.map((doc) => (
                    <div key={doc.id} className="p-4 border border-blue-200 bg-blue-50 rounded-lg flex flex-col gap-3">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-blue-900 truncate" title={doc.file_name}>
                          {doc.file_name}
                        </span>
                        <span className="text-xs font-semibold text-blue-700 bg-blue-200 px-2 py-1 rounded-full uppercase">
                          {doc.file_format || 'PDF'}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 mt-auto pt-2 border-t border-blue-100">
                        <a
                          href={shipmentApi.getDownloadUrl(id, doc.doc_type)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex-1 inline-flex justify-center items-center gap-1.5 px-3 py-1.5 bg-white border border-blue-300 text-blue-700 text-sm font-medium rounded-md hover:bg-blue-50 transition-colors"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                          </svg>
                          Download PDF
                        </a>
                        <a
                          href={shipmentApi.getDownloadUrl(id, doc.doc_type)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex-1 inline-flex justify-center items-center gap-1.5 px-3 py-1.5 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                          Open Preview
                        </a>
                      </div>
                    </div>
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
                    <button
                      type="button"
                      onClick={handleNewShipment}
                      className="inline-flex items-center gap-1.5 px-5 py-2 rounded-lg bg-slate-800 text-white text-sm font-medium hover:bg-slate-900 transition-colors shadow-sm"
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
                prevStepPath="health-certificate"
                isReview={true}
              />
            )}
          </form>
        </div>
      </main>
    </div>
  );
}
