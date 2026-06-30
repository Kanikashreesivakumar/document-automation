import React from 'react';

interface AnimalCertificatePreviewProps {
  data: {
    // Static government heading
    issuing_dept?: string;
    issuing_govt?: string;
    issuing_district?: string;

    // Document-specific (user inputs)
    serial_no?: string;
    issue_date?: string;
    date_of_inspection?: string;
    vet_officer_name?: string;
    vet_officer_designation?: string;

    // Auto-populated: Exporter
    exporter_name?: string;
    exporter_address?: string;

    // Auto-populated: Importer
    importer_name?: string;
    importer_address?: string;
    addressee?: string;

    // Auto-populated: Product & Package
    number_of_cartons?: string | number;
    description_of_goods?: string;
    type_of_packing?: string;
    gross_weight?: string;
    production_date?: string;
    expiry_date?: string;

    // Auto-populated: Shipment
    port_of_shipment?: string;
    container_no?: string;
    truck_no?: string;
    invoice_no?: string;
    invoice_date?: string;
    means_of_transport?: string;
  };
}

export function AnimalCertificatePreview({ data }: AnimalCertificatePreviewProps) {
  const val = (v: any) => v || '\u00A0';

  return (
    <div
      className="w-[800px] bg-white text-black mx-auto shadow-sm"
      style={{ fontFamily: 'Times New Roman, serif', fontSize: '13px', lineHeight: '1.55' }}
    >
      {/* Government Header */}
      <div className="text-center py-4 px-8 border-b-2 border-black">
        <div className="font-bold text-base">{val(data.issuing_dept || 'Animal Husbandry Department')}</div>
        <div className="font-bold">{val(data.issuing_govt || 'Government of Tamil Nadu')}</div>
        <div className="font-bold">{val(data.issuing_district || 'Namakkal District')}</div>
      </div>

      {/* Certificate Title */}
      <div className="text-center font-bold text-[15px] underline py-3 border-b border-black">
        VETERINARY HEALTH CERTIFICATE
      </div>

      {/* S.No and Date row */}
      <div className="flex border-b border-black">
        <div className="flex-1 border-r border-black px-4 py-2">
          <span className="font-bold">S.NO:</span>&nbsp;{val(data.serial_no)}
        </div>
        <div className="flex-1 px-4 py-2">
          <span className="font-bold">TO DATE:</span>&nbsp;{val(data.issue_date)}
        </div>
      </div>

      {/* Addressee */}
      <div className="px-6 py-3 border-b border-black">
        <div className="font-bold">To,</div>
        <div className="pl-4">{val(data.importer_name)}</div>
        <div className="pl-4">{val(data.importer_address)}</div>
      </div>

      {/* Body paragraph */}
      <div className="px-6 py-3 border-b border-black text-justify leading-relaxed">
        This is to Certify that I have this day examined{' '}
        <strong>{val(data.number_of_cartons)}</strong> Cartons of Indian Fresh Eggs belonging{' '}
        <strong>{val(data.exporter_name)}</strong>{' '}
        {val(data.exporter_address)} being exported{' '}
        <strong>{val(data.importer_name)}</strong>,{' '}
        {val(data.importer_address)},{' '}
        Eggs were found to be clean fresh, well packed and fit for human consumption.
      </div>

      {/* Details Table */}
      <table className="w-full border-collapse border-b border-black">
        <tbody>
          {[
            ['Type of Packing',    val(data.type_of_packing  || 'Eggs laid in Trays & Packed in Carton')],
            ['Description',        val(data.description_of_goods || 'Farm Fresh White Shell Eggs')],
            ['Gross weight',       val(data.gross_weight)],
            ['Production Date',    val(data.production_date)],
            ['Expiry Date',        val(data.expiry_date)],
            ['Port of Shipment',   val(data.port_of_shipment)],
            ['Date of Inspection', val(data.date_of_inspection)],
            ['Container No',       val(data.container_no)],
            ['Means of Transport', val(data.means_of_transport || 'Reefer Container')],
          ].map(([label, value]) => (
            <tr key={label} className="border-b border-black">
              <td className="border-r border-black px-4 py-1.5 font-bold w-[220px]">{label}</td>
              <td className="px-4 py-1.5">{value}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Truck & Invoice row */}
      <table className="w-full border-collapse border-b border-black">
        <tbody>
          <tr className="border-b border-black">
            <td className="border-r border-black px-4 py-1.5 font-bold w-[220px]">TRUCK No</td>
            <td className="px-4 py-1.5">{val(data.truck_no)}</td>
          </tr>
          <tr>
            <td className="border-r border-black px-4 py-1.5 font-bold">INVOICE NO./DT</td>
            <td className="px-4 py-1.5">{val(data.invoice_no)}&nbsp;&nbsp;DT: {val(data.invoice_date)}</td>
          </tr>
        </tbody>
      </table>

      {/* Certification paragraphs (static) */}
      <div className="px-6 py-3 text-justify leading-relaxed border-b border-black text-[12.5px]">
        <p className="mb-2">
          These Consignment Of Eggs Are Sourced From HPAI Free Namakkal, Tamilnadu and South India.
          On the basis of the above regional status I certify as here under. It is certify that the
          flocks where from the Poultry Eggs derived are free from any Contagious and infectious diseases
          and originate from poultry farm in Namakkal district, Tamilnadu, India. None of the birds in
          the farms were exhibiting signs or symptoms of any contagious or infectious diseases at the
          time of collection of these eggs.
        </p>
        <p className="mb-2">
          The Eggs are free from extraneous contamination and are transported to the place of export
          without coming in contact with any infected birds. It is certified that highly pathogenic avian
          influenza (HPAI) has not been reported in the flocks and the eggs derived is free from avian
          influenza &amp; avian flu (H5N1) and are originated from farms were New Castle Disease,
          Pullorium disease &amp; Avian Bird Flu were not reported for the last 40 days before the date
          of departure of the consignment based on random samples tested.
        </p>
        <p>
          It is certified that Notifiable Avian influenza Virus infection in farms of Namakkal District
          is absent at the time of issue of this certificate.
        </p>
      </div>

      {/* Signature block */}
      <table className="w-full border-collapse">
        <tbody>
          <tr>
            <td className="border-r border-black px-4 py-6 w-1/2 align-bottom">
              <div>Signature of Applicant /</div>
              <div>Representative of exporting firm</div>
            </td>
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
