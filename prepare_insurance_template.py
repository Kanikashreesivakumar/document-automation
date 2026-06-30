import docx

doc = docx.Document('export insurance.docx')

replacements = {
    'DATE:  ': 'DATE: {{ date }}',
    'Date of loading                   :          ': 'Date of loading                   : {{ invoice_date }}',
    'Container no                     :          ': 'Container no                     : {{ container_no }}',
    'Truck                                  :        ': 'Truck                                  : {{ truck_no }}',
    'Sum Assured                     :': 'Sum Assured                     : {{ sum_assured }}',
    'Dollar                                 :         ': 'Dollar                                 : {{ dollar_value }}',
    'Quantity of goods            :         ': 'Quantity of goods            : {{ quantity_of_goods }} ',
    'Port of Delivery               :         ': 'Port of Delivery               : {{ port_of_delivery }} ',
    'Risk Cover  \t \t: \tICCA ': 'Risk Cover  \t \t: \t{{ risk_cover }} ',
    'Place of Loading   \t:          Rasi Foods, ': 'Place of Loading   \t: {{ place_of_loading }} ',
    'Name of goods                  :         Fresh white shell table eggs(chicken). ': 'Name of goods                  : {{ name_of_goods }} ',
    '(SF. No: 311/5B,Minnampalli Village, Near Puthanchandai ,namakkal   pin code 637019) ': '',
}

for p in doc.paragraphs:
    for old, new in replacements.items():
        if old in p.text:
            p.text = p.text.replace(old, new)

    # invoice no/date line
    if 'Invoice no/Date' in p.text and 'DT :' in p.text:
        p.text = 'Invoice no/Date                  : {{ invoice_no }}                                   DT : {{ invoice_date }}'

    # Seal nos line
    if 'Seal No' in p.text and 'nos' not in p.text.lower() and ':          ' in p.text:
        p.text = "Seal No's                            : {{ seal_nos }}"

    # Importer block
    if 'Name  and Address' in p.text and 'Importer' in p.text:
        p.text = 'Name  and Address \t\nOf Importer: {{ importer_name }}\n{{ importer_address }}'

    # Date line with respected
    if 'Respected Sir' in p.text:
        p.text = 'Respected Sir {{ respected_sir }},'

doc.save('backend/templates/export_insurance.docx')
print('Saved to backend/templates/export_insurance.docx')
