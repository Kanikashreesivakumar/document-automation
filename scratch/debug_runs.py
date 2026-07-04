import zipfile
from lxml import etree

with zipfile.ZipFile(r'd:\Form Automation\invoice packing list.docx', 'r') as z:
    xml = z.read('word/document.xml')

root = etree.fromstring(xml)
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

for para in root.iter(f'{W}p'):
    texts = [t.text or '' for t in para.iter(f'{W}t')]
    full = ''.join(texts)
    if 'SHIPPING BILL NO' in full:
        for child in para:
            tag = child.tag.split('}')[-1]
            if tag == 'r':
                run_texts = ''.join(t.text or '' for t in child.iter(f'{W}t'))
                tabs = len(list(child.iter(f'{W}tab')))
                print(f'Run text={repr(run_texts)!r} tabs={tabs}')
        break
