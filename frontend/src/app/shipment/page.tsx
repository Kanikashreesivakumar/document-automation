"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import { shipmentApi } from '@/services/shipmentApi';
import { Button } from '@/components/ui/Button';
import { Toast } from '@/components/ui/Toast';

export default function ShipmentsDashboard() {
  const router = useRouter();
  const [shipments, setShipments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Deletion state
  const [shipmentToDelete, setShipmentToDelete] = useState<string | null>(null);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  useEffect(() => {
    async function loadShipments() {
      try {
        const res = await shipmentApi.listShipments();
        setShipments(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadShipments();
  }, []);

  const handleDeleteConfirm = async () => {
    if (!shipmentToDelete) return;
    try {
      await shipmentApi.deleteShipment(shipmentToDelete);
      // Remove from table immediately
      setShipments(prev => prev.filter(s => s.id !== shipmentToDelete));
      setToast({ message: 'Shipment deleted successfully.', type: 'success' });
    } catch (err) {
      setToast({ message: 'Failed to delete shipment.', type: 'error' });
    } finally {
      setShipmentToDelete(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

        {/* Back to Home */}
        <div className="mb-4">
          <button
            type="button"
            onClick={() => router.push('/')}
            className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-600 hover:text-blue-700 transition-colors group"
          >
            <svg className="w-4 h-4 transition-transform group-hover:-translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            ← Back to Home
          </button>
        </div>
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Shipments</h1>
            <p className="text-gray-500 mt-1">Manage your document automation workflows.</p>
          </div>
          <Link href="/shipment/new">
            <Button variant="primary">+ New Shipment</Button>
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-10">Loading shipments...</div>
        ) : shipments.length === 0 ? (
          <div className="text-center bg-white p-10 rounded-xl shadow-sm border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-2">No shipments found</h3>
            <p className="text-gray-500 mb-6">Create your first shipment to start generating documents.</p>
            <Link href="/shipment/new">
              <Button variant="primary">Create Shipment</Button>
            </Link>
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Shipment No</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invoice No</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {shipments.map((s) => (
                  <tr key={s.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{s.shipment_number}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{s.invoice_no || '—'}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        s.status === 'complete' ? 'bg-green-100 text-green-800' :
                        s.status === 'in_progress' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {s.status.replace('_', ' ').toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(s.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium flex items-center justify-end gap-4">
                      {s.status === 'complete' ? (
                        <Link href={`/shipment/${s.id}/review`} className="text-indigo-600 hover:text-indigo-900">Download</Link>
                      ) : (
                        <Link href={`/shipment/${s.id}/invoice`} className="text-blue-600 hover:text-blue-900">Resume</Link>
                      )}
                      <button
                        onClick={() => setShipmentToDelete(s.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>

      {/* Delete Confirmation Modal */}
      {shipmentToDelete && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 px-4">
          <div className="bg-white rounded-lg shadow-xl max-w-sm w-full p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-2">Delete Shipment</h3>
            <p className="text-gray-500 text-sm mb-6">
              Are you sure you want to permanently delete this shipment?
              <br /><br />
              This action cannot be undone.
            </p>
            <div className="flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setShipmentToDelete(null)}>
                Cancel
              </Button>
              <button
                onClick={handleDeleteConfirm}
                className="px-4 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700 transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
