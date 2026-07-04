import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repositories.shipment_repository import ShipmentRepository
from mapping import get_context
from services.docx_template_engine import fill_docx_template
from docx import Document

def main():
    engine = create_engine('sqlite:///shipments.db')
    Session = sessionmaker(bind=engine)
    db = Session()
    shipments = ShipmentRepository(db).list_all()
    if not shipments:
        print("No shipments found in DB")
        return
    
    shipment_orm = shipments[0]
    
    # We need dict shipment data for get_context!
    # Wait, in document_generator, how is it done? Let's just mock a shipment dict
    # Or call a service to get it
    from services.shipment_service import get_shipment
    shipment_dict = get_shipment(str(shipment_orm.id), db)
    
    context = get_context('export_insurance', shipment_dict)
    
    output_path = 'test_corruption_insurance.docx'
    
    try:
        fill_docx_template('templates/export_insurance.docx', output_path, context)
        print("Generated export_insurance.docx successfully")
    except Exception as e:
        print(f"Exception during generation: {e}")
        return

    try:
        doc = Document(output_path)
        print("Validation SUCCESS: DOCX reopened properly.")
    except Exception as e:
        print(f"Validation FAILED: DOCX is corrupted! Error: {e}")

if __name__ == '__main__':
    main()
