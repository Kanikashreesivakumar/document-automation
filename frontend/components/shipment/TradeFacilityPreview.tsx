import React from 'react';

export function TradeFacilityPreview({ data }: { data: any }) {
  // Helpers for text rendering
  const val = (v: any) => v || '\u00A0';

  return (
    <div className="w-[800px] bg-white text-black p-10 mx-auto shadow-sm" style={{ fontFamily: 'Times New Roman, serif', fontSize: '14px', lineHeight: '1.6' }}>
      
      {/* Header */}
      <div className="flex justify-end font-bold mb-4">
        TRADE FACILITY No. 04/2017
      </div>
      <div className="text-center font-bold mb-6 underline">
        ANNEXURE<br />
        Examination Report for Self-Sealed Container
      </div>

      {/* Basic details */}
      <div className="grid grid-cols-[300px_auto] gap-x-4 gap-y-2 mb-6">
        <div>Shipping Bill No.</div>
        <div>: {val(data?.shipping_bill_no)}</div>

        <div>NAME OF THE EXPORTER</div>
        <div className="font-bold">: {val(data?.exporter_name)}</div>

        <div>a. IEC NO.</div>
        <div>: {val(data?.iec_no)}</div>

        <div>GSTIN</div>
        <div>: {val(data?.exporter_gstin)}</div>

        <div>Branch code</div>
        <div>: {val(data?.branch_code)}</div>

        <div>BIN (PAN Based Business identification<br/>Number of the Exporter)</div>
        <div>: {val(data?.bin_number)}</div>

        <div>Factory Address</div>
        <div>
          : {val(data?.exporter_address)}
        </div>
      </div>

      {/* Examination details */}
      <div className="grid grid-cols-[300px_auto] gap-x-4 gap-y-2 mb-6">
        <div>4. Date of Examination</div>
        <div>: {val(data?.date_of_examination)}</div>

        <div>Time of Stuffing</div>
        <div>:</div>

        <div className="pl-8">Starting Time</div>
        <div>: {val(data?.stuffing_start_time)}</div>

        <div className="pl-8">Completion Time</div>
        <div>: {val(data?.stuffing_completion_time)}</div>

        <div className="pl-8">Time Taken for Stuffing</div>
        <div>: {val(data?.stuffing_duration)}</div>

        <div>Description of Cargo with quatity</div>
        <div>: {val(data?.description_of_cargo)}</div>

        <div>Country of final destination</div>
        <div>: {val(data?.country_of_destination)}</div>

        <div>Name & Designation of the Authorized<br/>Signatory</div>
        <div>
          : {val(data?.authorized_signatory_name)}<br/>
          &nbsp;&nbsp;{val(data?.authorized_signatory_designation)}
        </div>

        <div className="font-bold mt-2">Particulars of the Export Invoice</div>
        <div></div>

        <div>Export Invoice No.</div>
        <div>: {val(data?.invoice_no)} &nbsp;&nbsp;&nbsp;&nbsp; DT : {val(data?.invoice_date)}</div>

        <div>Total No of Packages</div>
        <div>: {val(data?.total_packages)}</div>

        <div>Name & Address of the Consignee</div>
        <div>
          : {val(data?.consignee_name)}<br/>
          &nbsp;&nbsp;{val(data?.consignee_address)}
        </div>

        <div>
          Is the description of the goods the<br/>
          Quantity and their value as per particulars<br/>
          furnished in Export GST Invoice
        </div>
        <div><br/>: {val(data?.goods_description_verified)}</div>
      </div>

      <div className="mb-2">11.Container Particulars:</div>
      <table className="w-full border-collapse border border-black text-center mb-6">
        <thead>
          <tr>
            <th className="border border-black p-2 font-normal">CONTAINER NO</th>
            <th className="border border-black p-2 font-normal">SEAL NO</th>
            <th className="border border-black p-2 font-normal">TRUCK NO</th>
            <th className="border border-black p-2 font-normal">SIZE</th>
            <th className="border border-black p-2 font-normal">No of Packages stuffed in the container</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border border-black p-2">{val(data?.container_no)}</td>
            <td className="border border-black p-2">{val(data?.seal_number)}</td>
            <td className="border border-black p-2">{val(data?.truck_number)}</td>
            <td className="border border-black p-2">{val(data?.container_type)}</td>
            <td className="border border-black p-2">{val(data?.number_of_cartons)}</td>
          </tr>
        </tbody>
      </table>

      <div className="mb-4">
        2.Starting Time (moving the container to CFS ): {val(data?.container_to_cfs_start_time)}
      </div>

      <p className="mb-8 text-justify leading-relaxed">
        I have examined the goods and the same are found to be as per the declaration. The goods are stuffed in the container and the container was sealed with e-seal under my supervision. The e-seal number is <strong>{val(data?.e_seal_number)}</strong>, and the colour of the seal is <strong>White</strong>. I undertake full responsibility for any difference in description, quality of the goods.
      </p>

      <div className="flex justify-end mt-12 font-bold pb-10">
        SIGNATURE OF THE EXPORTER
      </div>

    </div>
  );
}
