import docx

def prepare_template():
    doc = docx.Document('trade facility.docx')
    
    # Simple mapping of static strings to find and replace with placeholders
    # Note: python-docx paragraph.text assignment loses inline formatting.
    # We will do a simple run-level replace where possible, or just accept formatting loss 
    # since it's a basic text template.
    
    replacements = {
        "Shipping Bill No.                                                            :      ": "Shipping Bill No.                                                            : {{ shipping_bill_no }}",
        "NAME OF THE EXPORTER                                    :  RASI FOODS": "NAME OF THE EXPORTER                                    :  {{ exporter_name }}",
        "a. IEC NO.                                                                :  3215008319": "a. IEC NO.                                                                :  {{ iec_no }}",
        "GSTIN                                                                  : 33AASFR2685Q1Z8": "GSTIN                                                                  : {{ exporter_gstin }}",
        "Branch code                                                       : ": "Branch code                                                       : {{ branch_code }}",
        "BIN (PAN Based Business identification\n Number of the Exporter)                               : ": "BIN (PAN Based Business identification\n Number of the Exporter)                               : {{ bin_number }}",
        "4. Date of Examination                                               :  ": "4. Date of Examination                                               :  {{ date_of_examination }}",
        "       Starting Time                                                 : ": "       Starting Time                                                 : {{ starting_time }}",
        "       Completion Time                                          : ": "       Completion Time                                          : {{ completion_time }}",
        "       Time Taken for Stuffing                                : ": "       Time Taken for Stuffing                                : {{ time_taken }}",
        "Description of Cargo with quatity                     :  FRESH WHITE SHELL EGG  /1312 CARTONS": "Description of Cargo with quatity                     :  {{ description_of_cargo }}",
        "Country of final destination                               : ": "Country of final destination                               : {{ country_of_destination }}",
        "Signatory                                                               :  ": "Signatory                                                               :  {{ signatory_name }}\n{{ signatory_designation }}",
        "Export Invoice No.                                      :                               DT : ": "Export Invoice No.                                      : {{ invoice_no }}                              DT : {{ invoice_date }}",
        "Total No of Packages                                  :  1312  CARTONS": "Total No of Packages                                  :  {{ total_packages }} CARTONS",
        "Name & Address of the Consignee          : ": "Name & Address of the Consignee          : {{ consignee_name }}\n{{ consignee_address }}",
        "2.Starting Time (moving the container to CFS ): ": "2.Starting Time (moving the container to CFS ): {{ container_to_cfs_time }}",
        "The e-seal number is                                     , and the colour of the seal is White.": "The e-seal number is {{ e_seal_number }}, and the colour of the seal is {{ e_seal_colour }}.",
        "Yes / No": "{{ goods_description_verified }}",
    }

    for p in doc.paragraphs:
        for old_text, new_text in replacements.items():
            if old_text in p.text:
                p.text = p.text.replace(old_text, new_text)

    # For the table
    for table in doc.tables:
        for row in table.rows:
            if "CONTAINER NO" in row.cells[0].text:
                # Add a new row below for placeholders
                cells = table.add_row().cells
                cells[0].text = "{{ container_no }}"
                cells[1].text = "{{ seal_no }}"
                cells[2].text = "{{ truck_no }}"
                cells[3].text = "{{ container_size }}"
                cells[4].text = "{{ packages_in_container }}"
                break
                
    doc.save('backend/templates/trade_facility.docx')
    print("Saved to backend/templates/trade_facility.docx")

if __name__ == "__main__":
    prepare_template()
