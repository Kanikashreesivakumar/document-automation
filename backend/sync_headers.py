import zipfile
import os
import shutil
import xml.etree.ElementTree as ET

templates_dir = 'templates'
source_docx = os.path.join(templates_dir, 'export_insurance.docx')
targets = ['invoice.docx', 'proforma_invoice.docx', 'packing_list.docx']

def sync_header(source_path, target_path):
    print(f"Syncing header from {source_path} to {target_path}")
    
    shutil.rmtree('tmp_src', ignore_errors=True)
    shutil.rmtree('tmp_tgt', ignore_errors=True)
    
    with zipfile.ZipFile(source_path, 'r') as z_src:
        z_src.extractall('tmp_src')
        
    with zipfile.ZipFile(target_path, 'r') as z_tgt:
        z_tgt.extractall('tmp_tgt')
        
    rels_path = 'tmp_src/word/_rels/header1.xml.rels'
    if not os.path.exists(rels_path):
        return
        
    tree = ET.parse(rels_path)
    root = tree.getroot()
    namespaces = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
    
    img_target = None
    img_id = None
    for rel in root.findall('rel:Relationship', namespaces):
        if 'image' in rel.attrib.get('Type', ''):
            img_target = rel.attrib.get('Target')
            img_id = rel.attrib.get('Id')
            break
            
    if not img_target:
        return
        
    img_src_path = os.path.join('tmp_src', 'word', img_target)
    shutil.copy('tmp_src/word/header1.xml', 'tmp_tgt/word/header1.xml')
    os.makedirs('tmp_tgt/word/media', exist_ok=True)
    img_tgt_path = 'tmp_tgt/word/media/image99.jpeg'
    shutil.copy(img_src_path, img_tgt_path)
    
    tgt_rels_path = 'tmp_tgt/word/_rels/header1.xml.rels'
    os.makedirs(os.path.dirname(tgt_rels_path), exist_ok=True)
    
    if os.path.exists(tgt_rels_path):
        tgt_tree = ET.parse(tgt_rels_path)
        tgt_root = tgt_tree.getroot()
        for rel in tgt_root.findall('rel:Relationship', namespaces):
            if rel.attrib.get('Id') == img_id:
                tgt_root.remove(rel)
        ET.SubElement(tgt_root, '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship', {
            'Id': img_id,
            'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image',
            'Target': 'media/image99.jpeg'
        })
        tgt_tree.write(tgt_rels_path, xml_declaration=True, encoding='UTF-8')
    else:
        root = ET.Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationships')
        ET.SubElement(root, '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship', {
            'Id': img_id,
            'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image',
            'Target': 'media/image99.jpeg'
        })
        tree = ET.ElementTree(root)
        tree.write(tgt_rels_path, xml_declaration=True, encoding='UTF-8')
        
        doc_rels = 'tmp_tgt/word/_rels/document.xml.rels'
        if os.path.exists(doc_rels):
            doc_tree = ET.parse(doc_rels)
            doc_root = doc_tree.getroot()
            header_rel_id = 'rIdHeader99'
            ET.SubElement(doc_root, '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship', {
                'Id': header_rel_id,
                'Type': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/header',
                'Target': 'header1.xml'
            })
            doc_tree.write(doc_rels, xml_declaration=True, encoding='UTF-8')
            
        doc_xml = 'tmp_tgt/word/document.xml'
        w_ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        r_ns = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        ET.register_namespace('w', w_ns)
        ET.register_namespace('r', r_ns)
        
        dx_tree = ET.parse(doc_xml)
        dx_root = dx_tree.getroot()
        body = dx_root.find(f'{{{w_ns}}}body')
        sectPr = body.find(f'{{{w_ns}}}sectPr')
        if sectPr is None:
            sectPr = ET.SubElement(body, f'{{{w_ns}}}sectPr')
            
        headerReference = ET.SubElement(sectPr, f'{{{w_ns}}}headerReference')
        headerReference.set(f'{{{w_ns}}}type', 'default')
        headerReference.set(f'{{{r_ns}}}id', header_rel_id)
        dx_tree.write(doc_xml, xml_declaration=True, encoding='UTF-8')

    ct_path = 'tmp_tgt/[Content_Types].xml'
    ct_tree = ET.parse(ct_path)
    ct_root = ct_tree.getroot()
    ct_ns = 'http://schemas.openxmlformats.org/package/2006/content-types'
    ET.register_namespace('', ct_ns)
    
    has_jpeg = False
    for default in ct_root.findall(f'{{{ct_ns}}}Default'):
        if default.attrib.get('Extension').lower() in ['jpeg', 'jpg']:
            has_jpeg = True
            
    if not has_jpeg:
        ET.SubElement(ct_root, f'{{{ct_ns}}}Default', {
            'Extension': 'jpeg',
            'ContentType': 'image/jpeg'
        })
        
    has_header = False
    for override in ct_root.findall(f'{{{ct_ns}}}Override'):
        if override.attrib.get('PartName') == '/word/header1.xml':
            has_header = True
            
    if not has_header:
        ET.SubElement(ct_root, f'{{{ct_ns}}}Override', {
            'PartName': '/word/header1.xml',
            'ContentType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml'
        })
        
    ct_tree.write(ct_path, xml_declaration=True, encoding='UTF-8')
    
    doc_xml = 'tmp_tgt/word/document.xml'
    w_ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    dx_tree = ET.parse(doc_xml)
    dx_root = dx_tree.getroot()
    body = dx_root.find(f'{{{w_ns}}}body')
    
    paragraphs_to_remove = []
    for i, p in enumerate(body.findall(f'{{{w_ns}}}p')):
        text = "".join(t.text for t in p.findall(f'.//{{{w_ns}}}t') if t.text)
        if "RASI FOODS" in text or "MUDALAIPATTI" in text or "NAMAKKAL" in text or "rasieggs" in text or "Email" in text or "mob" in text:
            paragraphs_to_remove.append(p)
        elif i < 5 and not text.strip():
            paragraphs_to_remove.append(p)
            
    for p in paragraphs_to_remove:
        try:
            body.remove(p)
        except ValueError:
            pass
            
    dx_tree.write(doc_xml, xml_declaration=True, encoding='UTF-8')

    new_target_path = target_path + '.new'
    with zipfile.ZipFile(new_target_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for root_dir, dirs, files in os.walk('tmp_tgt'):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, 'tmp_tgt')
                z_out.write(file_path, arcname)
                
    shutil.move(new_target_path, target_path)
    shutil.rmtree('tmp_src', ignore_errors=True)
    shutil.rmtree('tmp_tgt', ignore_errors=True)
    print(f"Successfully synced to {target_path}")

for target in targets:
    tgt = os.path.join(templates_dir, target)
    if os.path.exists(tgt):
        sync_header(source_docx, tgt)
    else:
        print(f"Target {tgt} not found")
