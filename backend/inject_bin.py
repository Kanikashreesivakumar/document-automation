import zipfile
import re

doc_path = r'd:\Form Automation\backend\templates\trade_facility.docx'

with zipfile.ZipFile(doc_path, 'r') as z:
    xml = z.read('word/document.xml').decode('utf-8')

match = re.search(r'(<w:p\b[^>]*>.*?branch_code.*?</w:p>)', xml)
if not match:
    print("branch_code paragraph not found")
    exit(1)

branch_p = match.group(1)

# create the new paragraph
bin_p = branch_p.replace('Branch code', 'BIN (PAN Based Business Identification Number)')
bin_p = bin_p.replace('branch_code', 'bin_number')
# change the padding to match visually (remove some spaces since the label is longer)
# original label length: len("Branch code                                                       ") ~ 66 chars
# new label length: len("BIN (PAN Based Business Identification Number)") ~ 46 chars
# so we need about 20 spaces
bin_p = bin_p.replace('BIN (PAN Based Business Identification Number)                                                       ', 'BIN (PAN Based Business Identification Number)                    ')

# replace IDs to avoid duplicate ID errors (though Word is usually forgiving, safer to remove them)
bin_p = re.sub(r' w14:paraId="[^"]*"', '', bin_p)
bin_p = re.sub(r' w14:textId="[^"]*"', '', bin_p)

# insert right after
new_xml = xml[:match.end()] + bin_p + xml[match.end():]

# write back to docx
with zipfile.ZipFile(doc_path, 'a') as z:
    z.writestr('word/document.xml', new_xml)

print("Injected bin_number paragraph successfully.")
