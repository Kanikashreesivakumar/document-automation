/**
 * Typed API calls for all shipment endpoints.
 */
import api from './api';

export const shipmentApi = {
  // ── Shipment lifecycle ────────────────────────────────────────────────────────
  createShipment: () => api.post('/shipments'),
  listShipments:  () => api.get('/shipments'),
  getShipment:    (id: string) => api.get(`/shipments/${id}`),
  deleteShipment: (id: string) => api.delete(`/shipments/${id}`),

  getRecentDocuments: () => api.get('/shipments/recent-documents'),

  // ── Unified shipment data ─────────────────────────────────────────────────────
  saveShipmentData: (id: string, data: Record<string, unknown>) =>
    api.post(`/shipments/${id}/data`, data),
  saveProformaInvoice: (id: string, data: Record<string, unknown>) =>
    api.post(`/shipments/${id}/proforma`, data),
  saveTradeFacility: (id: string, data: Record<string, unknown>) =>
    api.post(`/shipments/${id}/trade-facility`, data),
  saveExportInsurance: (id: string, data: Record<string, unknown>) =>
    api.post(`/shipments/${id}/insurance`, data),

  saveHealthCertificate: (id: string, data: Record<string, unknown>) =>
    api.post(`/shipments/${id}/health-certificate`, data),
  getHealthCertificate: (id: string) =>
    api.get(`/shipments/${id}/health-certificate`),

  saveHealthCertificateAnnexure: (id: string, data: Record<string, unknown>) =>
    api.post(`/shipments/${id}/health-certificate/annexure`, data),
  getHealthCertificateAnnexure: (id: string) =>
    api.get(`/shipments/${id}/health-certificate/annexure`),

  // ── Generation & download ─────────────────────────────────────────────────────
  generateDocuments: (id: string) => api.post(`/shipments/${id}/generate`),
  getDownloadUrl: (id: string, docType: string) =>
    `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/shipments/${id}/download/${docType}`,
  getAllDownloadUrl: (id: string) =>
    `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/shipments/${id}/download-all`,
};
