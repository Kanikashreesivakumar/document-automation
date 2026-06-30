"use client";

/**
 * ProformaInvoicePreview — high-fidelity HTML replica of the uploaded Proforma Invoice DOCX template.
 * Merges shipment data (already collected) with proforma-specific fields.
 */
import React from 'react';
import { EXPORTER } from './InvoicePreview';

export interface ProformaPreviewData {
  // From Shipment data — auto-reused
  consigneeName?: string;
  buyerName?: string;
  buyerAddress?: string;
  buyerCountry?: string;
  preCarriageBy?: string;
  vesselFlightNo?: string;
  portOfLoading?: string;
  portOfDischarge?: string;
  finalDestination?: string;
  countryOfOrigin?: string;
  termsOfDelivery?: string;
  brandName?: string;
  productName?: string;
  containerType?: string;
  containerNo?: string;
  cartons?: number;
  eggsPerCarton?: number;
  totalEggs?: number;
  ratePerEggUsd?: number;
  amountUsd?: number;
  amountInWords?: string;
  netWeight?: number;
  grossWeight?: number;
  invoiceNo?: string;
  invoiceDate?: string;
  // Proforma-specific fields
  proformaInvoiceNumber?: string;
  poNumber?: string;
  poDate?: string;
  buyerTrn?: string;
  consigneeTrn?: string;
  notifyParty?: string;
  notifyPartyAddress?: string;
  paymentTerms?: string;
  expiryDate?: string;
  noAndKindOfPackages?: string;
  intermediateBankName?: string;
  intermediateBankAccountNumber?: string;
  intermediateBankSwift?: string;
  intermediateBankRoutingNumber?: string;
  correspondentBank?: string;
}

interface ProformaInvoicePreviewProps {
  data: ProformaPreviewData;
}

const ph = (val: any, fallback = '...') =>
  val && String(val).trim() ? String(val).trim() : <span style={{ color: '#ccc' }}>{fallback}</span>;

export function ProformaInvoicePreview({ data }: ProformaInvoicePreviewProps) {
  const {
    consigneeName, buyerName, buyerAddress, buyerCountry,
    preCarriageBy, vesselFlightNo, portOfLoading, portOfDischarge,
    finalDestination, countryOfOrigin, termsOfDelivery,
    brandName, productName, containerType, containerNo,
    cartons, eggsPerCarton, totalEggs,
    ratePerEggUsd, amountUsd, amountInWords,
    netWeight, grossWeight, invoiceNo, invoiceDate,
    proformaInvoiceNumber, poNumber, poDate,
    buyerTrn, consigneeTrn,
    notifyParty, notifyPartyAddress,
    paymentTerms, expiryDate, noAndKindOfPackages,
    intermediateBankName, intermediateBankAccountNumber, intermediateBankSwift,
    intermediateBankRoutingNumber, correspondentBank,
  } = data;

  const fmtUsd = (v?: number) => v ? `USD ${v.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : '—';
  const fmtNum = (v?: number) => v ? v.toLocaleString() : '—';

  return (
    <div style={{
      fontFamily: 'Arial, sans-serif',
      fontSize: '9px',
      color: '#111',
      background: '#fff',
      padding: '12px',
      minWidth: '600px',
    }}>
      {/* Document Title */}
      <div style={{ textAlign: 'center', fontWeight: 'bold', fontSize: '13px', letterSpacing: '2px', marginBottom: '6px' }}>
        PROFORMA INVOICE
      </div>

      {/* Top header */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }} rowSpan={4}>
              <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Exporter / Seller</div>
              <div style={{ fontWeight: 'bold' }}>{EXPORTER.name}</div>
              <div>{EXPORTER.address}</div>
              <div>Email: {EXPORTER.email}</div>
              <div>GSTIN: {EXPORTER.gstin}</div>
              <div>PAN: {EXPORTER.pan}</div>
              <div>IEC No: {EXPORTER.iec}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <span style={{ fontWeight: 'bold' }}>Proforma Invoice No.</span><br />
              {ph(proformaInvoiceNumber, 'PI-XXXX')}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <span style={{ fontWeight: 'bold' }}>Date</span><br />
              {ph(invoiceDate, 'DD.MM.YYYY')}
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <span style={{ fontWeight: 'bold' }}>PO Number:</span>&nbsp;{ph(poNumber, '—')}&nbsp;&nbsp;
              <span style={{ fontWeight: 'bold' }}>PO Date:</span>&nbsp;{ph(poDate, '—')}
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <span style={{ fontWeight: 'bold' }}>Payment Terms:</span><br />
              {ph(paymentTerms, '—')}
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <span style={{ fontWeight: 'bold' }}>Validity / Expiry Date:</span><br />
              {ph(expiryDate, '—')}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Consignee / Notify Party */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }}>
              <div style={{ fontWeight: 'bold' }}>Consignee / Buyer</div>
              <div>{ph(consigneeName, 'CONSIGNEE NAME')}</div>
              {buyerAddress && <div style={{ whiteSpace: 'pre-line' }}>{buyerAddress}</div>}
              {buyerCountry && <div>{buyerCountry}</div>}
              {consigneeTrn && <div>TRN: {consigneeTrn}</div>}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }}>
              <div style={{ fontWeight: 'bold' }}>Notify Party</div>
              <div>{ph(notifyParty, '—')}</div>
              {notifyPartyAddress && <div style={{ whiteSpace: 'pre-line' }}>{notifyPartyAddress}</div>}
              {buyerTrn && <div style={{ marginTop: '4px' }}>Buyer TRN: {buyerTrn}</div>}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Shipment Details */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Pre-Carriage By</div>
              <div>{ph(preCarriageBy, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Vessel/Flight No.</div>
              <div>{ph(vesselFlightNo, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Port of Loading</div>
              <div>{ph(portOfLoading, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Port of Discharge</div>
              <div>{ph(portOfDischarge, '...')}</div>
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Final Destination</div>
              <div>{ph(finalDestination, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Terms of Delivery</div>
              <div>{ph(termsOfDelivery, '...')}</div>
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>No. &amp; Kind of Packages</div>
              <div>{ph(noAndKindOfPackages, '—')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Country of Origin</div>
              <div>{ph(countryOfOrigin, 'INDIA')}</div>
            </td>
          </tr>
        </tbody>
      </table>

      {/* Goods Table */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <thead>
          <tr style={{ background: '#f0f0f0' }}>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'left', width: '20%' }}>Marks &amp; Nos / Container No.</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'center', width: '10%' }}>Cartons</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'left', width: '33%' }}>Description of Goods</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', width: '12%' }}>Quantity</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', width: '12%' }}>Rate (USD)</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', width: '13%' }}>Amount (USD)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top' }}>
              <div style={{ fontWeight: 'bold' }}>{ph(brandName, 'RASI')}</div>
              <div style={{ fontSize: '8px', marginTop: '4px' }}>
                {ph(containerNo, 'CONT-XXXX')}
              </div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'center' }}>
              <div style={{ fontWeight: 'bold' }}>{fmtNum(cartons)}</div>
              <div>CTNS</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', fontSize: '8px' }}>
              <div style={{ fontWeight: 'bold', fontSize: '9px' }}>{ph(productName, 'FRESH WHITE SHELL TABLE EGGS (CHICKEN).')}</div>
              <div style={{ marginTop: '3px' }}>
                {fmtNum(cartons)} CARTONS × {eggsPerCarton || '?'} EGGS/CARTON
              </div>
              <div>Total: {fmtNum(totalEggs)} EGGS</div>
              <div style={{ marginTop: '3px' }}>Container: {ph(containerType, '1 X 40 FEET')}</div>
              <div>HSN: {EXPORTER.hsn}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>{fmtNum(totalEggs)}</div>
              <div>Nos</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>USD</div>
              <div>{ratePerEggUsd ? ratePerEggUsd.toFixed(6) : '—'}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>{fmtUsd(amountUsd)}</div>
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={3}>
              <span style={{ fontWeight: 'bold' }}>Amount in Words: </span>
              {amountInWords || '—'}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', fontWeight: 'bold' }} colSpan={3}>
              Total: {fmtUsd(amountUsd)}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Weight */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '50%' }}>
              <span style={{ fontWeight: 'bold' }}>Total Net Weight: </span>
              {netWeight ? `${netWeight.toFixed(3)} KGS` : '—'}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '50%' }}>
              <span style={{ fontWeight: 'bold' }}>Total Gross Weight: </span>
              {grossWeight ? `${grossWeight.toFixed(3)} KGS` : '—'}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Banking Details */}
      {(intermediateBankName || correspondentBank) && (
        <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
          <tbody>
            <tr>
              <td style={{ border: '1px solid #444', padding: '4px 6px', width: '50%', fontSize: '8px' }}>
                <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Intermediate Bank</div>
                {intermediateBankName && <div>Bank: {intermediateBankName}</div>}
                {intermediateBankAccountNumber && <div>A/c: {intermediateBankAccountNumber}</div>}
                {intermediateBankSwift && <div>SWIFT: {intermediateBankSwift}</div>}
                {intermediateBankRoutingNumber && <div>Routing: {intermediateBankRoutingNumber}</div>}
              </td>
              <td style={{ border: '1px solid #444', padding: '4px 6px', width: '50%', fontSize: '8px' }}>
                <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Correspondent Bank</div>
                {correspondentBank && <div>{correspondentBank}</div>}
              </td>
            </tr>
          </tbody>
        </table>
      )}

      {/* Declaration & Signature */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '6px', verticalAlign: 'top', width: '60%', fontSize: '8px' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Declaration</div>
              <div>We declare that this proforma invoice shows the actual price of the goods described and that all particulars are true and correct.</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '6px', verticalAlign: 'top', width: '40%', fontSize: '8px', textAlign: 'center' }}>
              <div style={{ fontWeight: 'bold' }}>For {EXPORTER.name}</div>
              <div style={{ marginTop: '20px' }}>Authorised Signatory</div>
            </td>
          </tr>
        </tbody>
      </table>

      <div style={{ textAlign: 'center', color: '#aaa', fontSize: '7px', marginTop: '6px', fontStyle: 'italic' }}>
        Live preview — download the generated DOCX for the exact format
      </div>
    </div>
  );
}
