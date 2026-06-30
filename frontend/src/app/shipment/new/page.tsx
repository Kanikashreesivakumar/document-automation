"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { shipmentApi } from '@/services/shipmentApi';
import Header from '@/components/Header';
import { Toast } from '@/components/ui/Toast';
import { Button } from '@/components/ui/Button';

export default function NewShipmentPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const initShipment = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("Creating shipment...");
      const response = await shipmentApi.createShipment();
      console.log(response.data);
      if (response.data?.id) {
        router.push(`/shipment/${response.data.id}/invoice`);
      } else {
        throw new Error("Invalid response from server: Missing shipment ID");
      }
    } catch (err: any) {
      console.error("Failed to create shipment", err);
      setError(err.response?.data?.detail || err.message || "Failed to connect to the backend. Is it running?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    initShipment();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />
      {error && <Toast message={error} type="error" onClose={() => setError(null)} />}
      <main className="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 flex justify-center items-center">
        <div className="text-center bg-white p-10 rounded-xl shadow-sm border border-gray-200">
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h2 className="text-xl font-semibold text-gray-700">Initializing new shipment...</h2>
            </>
          ) : (
            <>
              <h2 className="text-xl font-semibold text-red-600 mb-4">Failed to initialize shipment</h2>
              <p className="text-gray-600 mb-6">{error}</p>
              <Button variant="primary" onClick={initShipment}>Retry</Button>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
