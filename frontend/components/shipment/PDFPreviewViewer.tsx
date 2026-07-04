import React, { useState, useEffect, useRef } from 'react';

interface PDFPreviewViewerProps {
  shipmentId: string;
  docType: string;
  data: any; // Live form data mapped to snake_case format
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * Cross-browser scrollbar-hiding styles injected once into the document <head>.
 * - Chrome/Edge: ::-webkit-scrollbar { display:none }
 * - Firefox:      scrollbar-width: none
 * - IE/Edge old:  -ms-overflow-style: none
 *
 * Applied to a wrapper class so it only affects preview containers, not the whole app.
 */
const SCROLLBAR_HIDE_CSS = `
  .pdf-preview-scroll::-webkit-scrollbar { display: none; }
  .pdf-preview-scroll { scrollbar-width: none; -ms-overflow-style: none; }
`;

function useInjectScrollbarCSS() {
  useEffect(() => {
    if (typeof document === 'undefined') return;
    const id = 'pdf-preview-scrollbar-hide';
    if (document.getElementById(id)) return;
    const style = document.createElement('style');
    style.id = id;
    style.textContent = SCROLLBAR_HIDE_CSS;
    document.head.appendChild(style);
    return () => {
      // Leave the style tag — removing it would flash scrollbars on other instances
    };
  }, []);
}

export function PDFPreviewViewer({ shipmentId, docType, data }: PDFPreviewViewerProps) {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const latestUrlRef = useRef<string | null>(null);

  useInjectScrollbarCSS();

  useEffect(() => {
    // Clean up URL on unmount
    return () => {
      if (latestUrlRef.current) {
        URL.revokeObjectURL(latestUrlRef.current);
      }
    };
  }, []);

  useEffect(() => {
    const fetchPreview = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_BASE}/shipments/${shipmentId}/preview-pdf/${docType}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          let errorDetail = response.statusText;
          try {
            const errorData = await response.json();
            if (errorData.detail) {
              errorDetail = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
            }
          } catch (e) { }
          throw new Error(errorDetail);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // Revoke the old URL to prevent memory leaks
        if (latestUrlRef.current) {
          URL.revokeObjectURL(latestUrlRef.current);
        }

        latestUrlRef.current = url;
        setPdfUrl(url);
      } catch (err: any) {
        setError(err.message || 'An error occurred while generating the preview.');
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(() => {
      fetchPreview();
    }, 2000); // 2-second debounce

    return () => clearTimeout(timer);
  }, [shipmentId, docType, JSON.stringify(data)]);

  return (
    /* pdf-preview-scroll hides scrollbars via injected CSS while keeping scroll functional */
    <div className="pdf-preview-scroll flex flex-col h-full bg-gray-50 border border-gray-200 rounded-xl overflow-hidden w-full max-w-full">
      <div className="bg-white p-4 flex justify-between items-center border-b border-gray-200 shadow-sm">
        <h3 className="font-semibold text-gray-800">Live PDF Preview</h3>
        {loading ? (
          <span className="text-sm font-medium text-blue-600 flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            Updating...
          </span>
        ) : (
          <span className="text-sm font-medium text-green-600">Up to date</span>
        )}
      </div>

      <div className="pdf-preview-scroll flex-1 min-h-[800px] relative overflow-auto">
        {loading && !pdfUrl && (
          <div className="absolute inset-0 bg-white/60 flex flex-col items-center justify-center z-10 backdrop-blur-sm">
            <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-gray-700 font-medium">Generating PDF using templates...</p>
          </div>
        )}

        {error && (
          <div className="p-8 text-center text-red-600">
            <p className="font-medium bg-red-50 p-4 rounded-lg inline-block border border-red-100">{error}</p>
          </div>
        )}

        {!loading && !error && !pdfUrl && (
          <div className="p-12 text-center text-gray-500 flex flex-col items-center">
            <svg className="w-16 h-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
            </svg>
            <p className="font-medium mb-1">Waiting for data...</p>
          </div>
        )}

        {pdfUrl && (
          <iframe
            src={`${pdfUrl}#view=FitH&scrollbar=0&toolbar=0`}
            className={`w-full h-full absolute inset-0 border-none transition-opacity duration-300 ${loading ? 'opacity-50' : 'opacity-100'}`}
            style={{ width: '100%', height: '100%', border: 'none', overflow: 'hidden' }}
            title="PDF Preview"
          />
        )}
      </div>
    </div>
  );
}
