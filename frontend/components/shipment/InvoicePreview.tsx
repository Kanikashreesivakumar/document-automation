"use client";

/**
 * InvoicePreview — high-fidelity HTML replica of the uploaded Invoice DOCX template.
 * Renders a live, real-time updating preview matching the actual document layout.
 */
import React from 'react';

// Static exporter — mirrors backend STATIC_EXPORTER
export const EXPORTER = {
  name: 'RASI FOODS',
  address: 'NO. 1/219, MUDALAIPATTI, SALEM MAIN ROAD, NAMAKKAL -637003, TAMILNADU, INDIA',
  email: 'rasieggs@gmail.com',
  gstin: '33AASFR2685Q1Z8',
  pan: 'AASFR2685Q',
  hsn: '04072100',
  iec: '3215008319',
};

export interface InvoicePreviewData {
  // Invoice Info
  invoiceNo?: string;
  invoiceDate?: string;
  buyerOrderNoDate?: string;
  referenceProformaInvoiceNo?: string;
  shippingBillNo?: string;
  shippingBillDate?: string;
  // Buyer
  consigneeName?: string;
  buyerName?: string;
  buyerAddress?: string;
  buyerPostalCode?: string;
  buyerCountry?: string;
  // Shipment
  preCarriageBy?: string;
  vesselFlightNo?: string;
  placeOfReceipt?: string;
  portOfLoading?: string;
  portOfDischarge?: string;
  finalDestination?: string;
  countryOfOrigin?: string;
  countryOfFinalDestination?: string;
  termsOfDelivery?: string;
  // Product
  brandName?: string;
  productName?: string;
  containerType?: string;
  containerNo?: string;
  // Package
  cartons?: number;
  traysPerCarton?: number;
  eggsPerTray?: number;
  eggsPerCarton?: number;
  totalEggs?: number;
  // Pricing
  ratePerEggUsd?: number;
  amountUsd?: number;
  amountInWords?: string;
  // Weight
  netWeightPerCarton?: number;
  grossWeightPerCarton?: number;
  netWeight?: number;
  grossWeight?: number;
}

interface InvoicePreviewProps {
  data: InvoicePreviewData;
}

const ph = (val: any, fallback = '...') =>
  val && String(val).trim() ? String(val).trim() : <span style={{ color: '#ccc' }}>{fallback}</span>;

export function InvoicePreview({ data }: InvoicePreviewProps) {
  const {
    invoiceNo, invoiceDate, buyerOrderNoDate, referenceProformaInvoiceNo,
    shippingBillNo, shippingBillDate,
    consigneeName, buyerName, buyerAddress, buyerPostalCode, buyerCountry,
    preCarriageBy, vesselFlightNo, placeOfReceipt, portOfLoading, portOfDischarge,
    finalDestination, countryOfOrigin, countryOfFinalDestination, termsOfDelivery,
    brandName, productName, containerType, containerNo,
    cartons, traysPerCarton, eggsPerCarton, totalEggs,
    ratePerEggUsd, amountUsd, amountInWords,
    netWeight, grossWeight,
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
        INVOICE
      </div>

      {/* Top header table */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', marginBottom: '0px' }}>
        <tbody>
          <tr>
            {/* Exporter cell — spans 4 rows */}
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }} rowSpan={4}>
              <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Exporter</div>
              <div style={{ fontWeight: 'bold' }}>{EXPORTER.name}</div>
              <div>{EXPORTER.address}</div>
              <div>Email: {EXPORTER.email}</div>
              <div>GSTIN: {EXPORTER.gstin}</div>
              <div>PAN: {EXPORTER.pan}</div>
              <div>IEC No: {EXPORTER.iec}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <span style={{ fontWeight: 'bold' }}>Invoice No.</span><br />
              {ph(invoiceNo, 'INV-XXXX')}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <span style={{ fontWeight: 'bold' }}>Dated</span><br />
              {ph(invoiceDate, 'DD.MM.YYYY')}
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <span style={{ fontWeight: 'bold' }}>Exporter&apos;s Ref:</span><br />
              {EXPORTER.iec}
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <span style={{ fontWeight: 'bold' }}>Buyer&apos;s Order No. &amp; Date</span><br />
              {ph(buyerOrderNoDate, '—')}
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <span style={{ fontWeight: 'bold' }}>Reference Proforma Invoice No.</span><br />
              {ph(referenceProformaInvoiceNo, '—')}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Consignee / Buyer */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', marginBottom: '0px', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Consignee</div>
              <div>{ph(consigneeName, 'CONSIGNEE NAME')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Buyer (if other than Consignee)</div>
              <div>{ph(buyerName, '—')}</div>
              {buyerAddress && <div style={{ whiteSpace: 'pre-line' }}>{buyerAddress}</div>}
              {buyerPostalCode && <div>Postal Code: {buyerPostalCode}</div>}
              {buyerCountry && <div>{buyerCountry}</div>}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Shipping Bill & other ref */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', marginBottom: '0px', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '50%' }}>
              <span style={{ fontWeight: 'bold' }}>Shipping Bill No. &amp; Date:</span>&nbsp;
              {ph(shippingBillNo, '—')} {shippingBillDate ? `DT: ${shippingBillDate}` : ''}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '50%' }}>
              <span style={{ fontWeight: 'bold' }}>Country of Origin of Goods:</span>&nbsp;
              {ph(countryOfOrigin, 'INDIA')}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Shipment Details */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', marginBottom: '0px', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Pre-Carriage By</div>
              <div>{ph(preCarriageBy, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Vessel/Fl. No.</div>
              <div>{ph(vesselFlightNo, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Place of Receipt</div>
              <div>{ph(placeOfReceipt, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', width: '25%' }}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Port of Loading</div>
              <div>{ph(portOfLoading, '...')}</div>
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Port of Discharge</div>
              <div>{ph(portOfDischarge, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Final Destination</div>
              <div>{ph(finalDestination, '...')}</div>
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Country of Final Destination</div>
              <div>{ph(countryOfFinalDestination, '...')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <div style={{ fontWeight: 'bold', fontSize: '8px' }}>Terms of Delivery &amp; Payment</div>
              <div>{ph(termsOfDelivery, '...')}</div>
            </td>
          </tr>
        </tbody>
      </table>

      {/* Goods Table */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', marginBottom: '0px', borderTop: 'none' }}>
        <thead>
          <tr style={{ background: '#f0f0f0' }}>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'left', fontWeight: 'bold', width: '16%' }}>Marks &amp; Nos / Container No.</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'left', fontWeight: 'bold', width: '10%' }}>No. &amp; Kind of Pkgs.</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'left', fontWeight: 'bold', width: '35%' }}>Description of Goods</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', fontWeight: 'bold', width: '13%' }}>Quantity</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', fontWeight: 'bold', width: '13%' }}>Rate per Egg</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', fontWeight: 'bold', width: '13%' }}>Amount (USD)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top' }}>
              <div style={{ fontWeight: 'bold' }}>{ph(brandName, 'BRAND')}</div>
              <div style={{ fontSize: '8px', marginTop: '4px' }}>
                Cont. No.:<br />{ph(containerNo, 'CONT-XXXX')}
              </div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'center' }}>
              <div style={{ fontWeight: 'bold' }}>{cartons ? cartons : '—'}</div>
              <div>CTNS</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', fontSize: '8px' }}>
              <div style={{ fontWeight: 'bold', fontSize: '9px' }}>{ph(productName, 'FRESH WHITE SHELL TABLE EGGS (CHICKEN).')}</div>
              <div style={{ marginTop: '3px' }}>
                TOTAL {cartons || '?'} CARTONS × {traysPerCarton || '?'} TRAYS/CTN × {eggsPerCarton || '?'} EGGS/TRAY
              </div>
              <div>= {fmtNum(totalEggs)} EGGS TOTAL</div>
              <div style={{ marginTop: '3px' }}>Container Type: {ph(containerType, '1 X 40 FEET')}</div>
              <div>HSN Code: {EXPORTER.hsn}</div>
              <div>Country of Origin: {ph(countryOfOrigin, 'INDIA')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>{fmtNum(totalEggs)}</div>
              <div>Nos</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>USD</div>
              <div>{ratePerEggUsd ? ratePerEggUsd.toFixed(6) : '—'}</div>
              <div>per Egg</div>
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

      {/* Weight footer */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', marginBottom: '0px', borderTop: 'none' }}>
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

      {/* Declaration & Signature */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', marginTop: '0px', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '6px', verticalAlign: 'top', width: '60%', fontSize: '8px' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Declaration</div>
              <div>We declare that this invoice shows the actual price of the goods described and that all particulars are true and correct.</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '6px', verticalAlign: 'top', width: '40%', fontSize: '8px', textAlign: 'center' }}>
              <div style={{ fontWeight: 'bold' }}>For {EXPORTER.name}</div>
              <div style={{ marginTop: '20px' }}>Signature &amp; Date</div>
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
