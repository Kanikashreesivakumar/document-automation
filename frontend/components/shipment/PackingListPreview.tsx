"use client";

/**
 * PackingListPreview — high-fidelity HTML replica of the uploaded Packing List DOCX template.
 * Automatically uses shipment data — no additional user input required.
 */
import React from 'react';
import { EXPORTER } from './InvoicePreview';

export interface PackingListPreviewData {
  invoiceNo?: string;
  invoiceDate?: string;
  shippingBillNo?: string;
  shippingBillDate?: string;
  consigneeName?: string;
  buyerName?: string;
  buyerAddress?: string;
  buyerCountry?: string;
  preCarriageBy?: string;
  vesselFlightNo?: string;
  placeOfReceipt?: string;
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
  traysPerCarton?: number;
  eggsPerTray?: number;
  eggsPerCarton?: number;
  totalEggs?: number;
  netWeightPerCarton?: number;
  grossWeightPerCarton?: number;
  netWeight?: number;
  grossWeight?: number;
}

interface PackingListPreviewProps {
  data: PackingListPreviewData;
}

const ph = (val: any, fallback = '...') =>
  val && String(val).trim() ? String(val).trim() : <span style={{ color: '#ccc' }}>{fallback}</span>;

export function PackingListPreview({ data }: PackingListPreviewProps) {
  const {
    invoiceNo, invoiceDate, shippingBillNo, shippingBillDate,
    consigneeName, buyerName, buyerAddress, buyerCountry,
    preCarriageBy, vesselFlightNo, placeOfReceipt, portOfLoading, portOfDischarge,
    finalDestination, countryOfOrigin, termsOfDelivery,
    brandName, productName, containerType, containerNo,
    cartons, traysPerCarton, eggsPerTray, eggsPerCarton, totalEggs,
    netWeightPerCarton, grossWeightPerCarton, netWeight, grossWeight,
  } = data;

  const fmtNum = (v?: number) => v ? v.toLocaleString() : '—';
  const totalTrays = cartons && traysPerCarton ? cartons * traysPerCarton : undefined;

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
        PACKING LIST
      </div>

      {/* Top header */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }} rowSpan={3}>
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
            <td style={{ border: '1px solid #444', padding: '4px 6px' }}>
              <span style={{ fontWeight: 'bold' }}>Exporter&apos;s Ref:</span><br />
              {EXPORTER.iec}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }}>
              <span style={{ fontWeight: 'bold' }}>S.B. No. &amp; Date:</span><br />
              {ph(shippingBillNo, '—')} {shippingBillDate ? `DT: ${shippingBillDate}` : ''}
            </td>
          </tr>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px' }} colSpan={2}>
              <span style={{ fontWeight: 'bold' }}>Buyer&apos;s Order No. &amp; Date:</span><br />—
            </td>
          </tr>
        </tbody>
      </table>

      {/* Consignee / Buyer */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }}>
              <div style={{ fontWeight: 'bold' }}>Consignee</div>
              <div>{ph(consigneeName, 'CONSIGNEE NAME')}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', width: '50%' }}>
              <div style={{ fontWeight: 'bold' }}>Buyer (if other than Consignee)</div>
              <div>{ph(buyerName, '—')}</div>
              {buyerAddress && <div style={{ whiteSpace: 'pre-line' }}>{buyerAddress}</div>}
              {buyerCountry && <div>{buyerCountry}</div>}
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
        </tbody>
      </table>

      {/* Packing Details Table */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <thead>
          <tr style={{ background: '#f0f0f0' }}>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'left', width: '20%' }}>Marks &amp; Nos / Container No.</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'center', width: '10%' }}>No. of Cartons</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'left', width: '30%' }}>Description of Goods</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', width: '13%' }}>Quantity (Eggs)</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', width: '13%' }}>Net Wt. (KGS)</th>
            <th style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', width: '14%' }}>Gross Wt. (KGS)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top' }}>
              <div style={{ fontWeight: 'bold' }}>{ph(brandName, 'BRAND')}</div>
              <div style={{ fontSize: '8px', marginTop: '4px' }}>
                Cont. Type: {ph(containerType, '1 X 40 FEET')}<br />
                Cont. No.: {ph(containerNo, 'CONT-XXXX')}
              </div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'center' }}>
              <div style={{ fontWeight: 'bold' }}>{fmtNum(cartons)}</div>
              <div>CARTONS</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', fontSize: '8px' }}>
              <div style={{ fontWeight: 'bold', fontSize: '9px' }}>{ph(productName, 'FRESH WHITE SHELL TABLE EGGS (CHICKEN).')}</div>
              <div style={{ marginTop: '3px' }}>
                {fmtNum(cartons)} CARTONS × {traysPerCarton || '?'} TRAYS × {eggsPerTray || '?'} EGGS/TRAY
              </div>
              <div>{fmtNum(eggsPerCarton)} EGGS PER CARTON</div>
              <div>Total: {fmtNum(totalTrays)} TRAYS</div>
              <div>HSN Code: {EXPORTER.hsn}</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>{fmtNum(totalEggs)}</div>
              <div>Nos</div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>{netWeight ? netWeight.toFixed(3) : '—'}</div>
              <div style={{ fontSize: '8px', color: '#666' }}>
                {netWeightPerCarton ? `${netWeightPerCarton} per ctn` : ''}
              </div>
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', verticalAlign: 'top', textAlign: 'right' }}>
              <div style={{ fontWeight: 'bold' }}>{grossWeight ? grossWeight.toFixed(3) : '—'}</div>
              <div style={{ fontSize: '8px', color: '#666' }}>
                {grossWeightPerCarton ? `${grossWeightPerCarton} per ctn` : ''}
              </div>
            </td>
          </tr>
          {/* Totals row */}
          <tr style={{ background: '#f9f9f9' }}>
            <td style={{ border: '1px solid #444', padding: '4px 6px', fontWeight: 'bold' }} colSpan={2}>
              TOTAL
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', fontWeight: 'bold' }}>
              {fmtNum(cartons)} CARTONS
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', fontWeight: 'bold' }}>
              {fmtNum(totalEggs)} Nos
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', fontWeight: 'bold' }}>
              {netWeight ? `${netWeight.toFixed(3)} KGS` : '—'}
            </td>
            <td style={{ border: '1px solid #444', padding: '4px 6px', textAlign: 'right', fontWeight: 'bold' }}>
              {grossWeight ? `${grossWeight.toFixed(3)} KGS` : '—'}
            </td>
          </tr>
        </tbody>
      </table>

      {/* Declaration */}
      <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #444', borderTop: 'none' }}>
        <tbody>
          <tr>
            <td style={{ border: '1px solid #444', padding: '6px', verticalAlign: 'top', width: '60%', fontSize: '8px' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>Declaration</div>
              <div>We declare that this packing list shows the actual details of the goods described and that all particulars are true and correct.</div>
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
