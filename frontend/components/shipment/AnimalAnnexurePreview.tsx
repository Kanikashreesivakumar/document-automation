import React from 'react';

interface AnimalAnnexurePreviewProps {
  data: {
    exporter_name?: string;
    exporter_address?: string;
    producer_name?: string;
    producer_address?: string;
    destination_country?: string;
    container_no?: string;
    production_date?: string;
    expiry_date?: string;
    invoice_no?: string;
    invoice_date?: string;
    certificate_no?: string;
    date_of_issue?: string;
    vet_officer_name?: string;
    vet_officer_designation?: string;
  };
}

export function AnimalAnnexurePreview({ data }: AnimalAnnexurePreviewProps) {
  const val = (v: any) => v || '\u00A0';

  return (
    <div
      className="w-[800px] bg-white text-black mx-auto shadow-sm p-10"
      style={{ fontFamily: 'Times New Roman, serif', fontSize: '13.5px', lineHeight: '1.6' }}
    >
      <div className="text-center font-bold text-lg mb-6 underline">
        ANNEXURE – 1
      </div>

      <div className="text-justify mb-6">
        This is to certify that the flocks where from the poultry eggs derived 
        <strong> {val(data.exporter_name)}</strong>, {val(data.exporter_address)}, 
        are free from any Contagious and infectious and other bacterial diseases 
        and originate from poultry farms in southern Part of India.
      </div>

      <div className="mb-6">
        <strong>Producer:</strong> {val(data.producer_name)}, {val(data.producer_address)}
      </div>

      <ol className="list-decimal pl-6 space-y-2 mb-8">
        <li>The eggs are packed in fresh cartons free from extraneous contamination.</li>
        <li>That the eggs exported to <strong>{val(data.destination_country)}</strong> has been Disinfected.</li>
        <li>It is certified that highly pathogenic avian influenza (HPAI) has not been reported.</li>
        <li>The poultry farms are under continuous surveillance for HPAI.</li>
        <li>The birds in our farms are randomly tested.</li>
        <li>The Certificate is not valid for export purposes.</li>
        <li>The shipment is transported in new or appropriately sanitized Containers.</li>
      </ol>

      <table className="w-full border-collapse border-b border-black mb-6">
        <tbody>
          {[
            ['Container No', val(data.container_no)],
            ['Production Date', val(data.production_date)],
            ['Expiry Date', val(data.expiry_date)],
            ['Invoice No/Date', `${val(data.invoice_no)}  DT: ${val(data.invoice_date)}`],
          ].map(([label, value]) => (
            <tr key={label} className="border-t border-black">
              <td className="border-r border-black px-4 py-2 font-bold w-[250px]">{label}</td>
              <td className="px-4 py-2">{value}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <table className="w-full border-collapse mt-8">
        <tbody>
          <tr>
            <td className="border-r border-black border-t border-b px-4 py-2 font-bold w-[250px]">Certificate No</td>
            <td className="border-t border-b px-4 py-2">{val(data.certificate_no)}</td>
          </tr>
          <tr>
            <td className="border-r border-black border-b px-4 py-2 font-bold w-[250px]">Date of Issue</td>
            <td className="border-b px-4 py-2">{val(data.date_of_issue)}</td>
          </tr>
          <tr>
            <td className="border-r border-black px-4 py-6 w-[250px]"></td>
            <td className="px-4 py-6 align-bottom">
              <div className="font-bold">{val(data.vet_officer_name || 'Dr. R. MANIVEL B.V.Sc')}</div>
              <div>{val(data.vet_officer_designation)}</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
