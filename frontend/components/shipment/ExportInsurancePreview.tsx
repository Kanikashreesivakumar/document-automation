import React from 'react';

export function ExportInsurancePreview({ data }: { data: any }) {
  const val = (v: any) => v || '\u00A0';

  return (
    <div className="w-[800px] bg-white text-black p-10 mx-auto shadow-sm" style={{ fontFamily: 'Times New Roman, serif', fontSize: '15px', lineHeight: '1.6' }}>
      
      {/* Exporter Header */}
      <div className="mb-8">
        <div className="font-bold text-lg mb-1">{val(data?.exporter_name)}</div>
        <div>{val(data?.exporter_address)}</div>
        <div>Email: {val(data?.exporter_email)}</div>
      </div>

      <div className="flex justify-between items-start mb-6">
        <div>
          <div>To</div>
          <div className="pl-6">The Divisional Manager,</div>
          <div className="pl-6">The New India Assurance Co Ltd.,</div>
          <div className="pl-6">Namakkal.</div>
        </div>
        <div>
          <div>DATE: {val(data?.date)}</div>
        </div>
      </div>

      <div className="mb-4">
        Respected Sir {val(data?.respected_sir)},
      </div>

      <div className="flex justify-center mb-6 text-center font-bold underline px-12 leading-relaxed">
        Sub: MARINE POLICY: SINGLE VOYAGE POLICY,<br/>
        CIF POLICY <br/>
        Covering all risk from NAMAKKAL WARE HOUSE TO {val(data?.coverage_route)}
      </div>

      <div className="mb-6 indent-8 text-justify">
        With reference to above-mentioned matter, we hereby request you to issue to the policy for the following container.
      </div>

      <div className="grid grid-cols-[200px_auto] gap-y-2 mb-6 ml-8">
        <div>Date of loading</div>
        <div>: {val(data?.invoice_date)}</div>

        <div>Invoice no/Date</div>
        <div>: {val(data?.invoice_no)} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DT : {val(data?.invoice_date)}</div>

        <div>Container no</div>
        <div>: {val(data?.container_no)}</div>

        <div>Seal No's</div>
        <div>: {val(data?.seal_nos)}</div>

        <div>Truck</div>
        <div>: {val(data?.truck_no)}</div>

        <div>Risk Cover</div>
        <div>: {val(data?.risk_cover)}</div>

        <div>Place of Loading</div>
        <div>: {val(data?.place_of_loading)}</div>
      </div>

      <div className="grid grid-cols-[200px_auto] gap-y-2 mb-6 ml-8">
        <div>Name and Address<br/>Of Importer</div>
        <div>
          {val(data?.importer_name)}<br/>
          {val(data?.importer_address)}
        </div>
      </div>

      <div className="grid grid-cols-[200px_auto] gap-y-2 mb-8 ml-8">
        <div>Sum Assured</div>
        <div>: {val(data?.sum_assured)}</div>

        <div>Dollar</div>
        <div>: {val(data?.dollar_value)}</div>

        <div>Name of goods</div>
        <div>: {val(data?.name_of_goods)}</div>

        <div>Quantity of goods</div>
        <div>: {val(data?.quantity_of_goods)}</div>

        <div>Port of Delivery</div>
        <div>: {val(data?.port_of_delivery)}</div>
      </div>

      {data?.insurance_remarks && (
        <div className="mb-8 ml-8">
          <strong>Remarks:</strong> {data.insurance_remarks}
        </div>
      )}

      <div className="text-center italic mb-12">
        Kindly do the needful at your earliest and oblige
      </div>

      <div className="flex justify-end pr-12">
        <div className="text-center">
          <div className="mb-12">For Rasi Foods</div>
          <div className="font-bold">Authorised Signatory</div>
        </div>
      </div>

    </div>
  );
}
