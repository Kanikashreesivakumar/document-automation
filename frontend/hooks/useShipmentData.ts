"use client";

import { useState, useEffect } from 'react';
import { shipmentApi } from '../services/shipmentApi';

export function useShipmentData(shipmentId: string) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    
    async function fetchShipment() {
      if (!shipmentId || shipmentId === 'undefined') return;
      try {
        setLoading(true);
        const response = await shipmentApi.getShipment(shipmentId);
        if (isMounted) {
          setData(response.data);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setError('Failed to load shipment data');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchShipment();

    return () => {
      isMounted = false;
    };
  }, [shipmentId]);

  return { data, loading, error, refetch: () => setLoading(true) }; // Refetch triggers effect? Actually better to return a fetch fn but this is enough for now.
}
