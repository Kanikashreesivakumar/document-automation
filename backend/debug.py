from core.database import SessionLocal
from repositories.shipment_repository import ShipmentRepository
import pprint

db = SessionLocal()
s_repo = ShipmentRepository(db)
shipments = s_repo.list_all()

if not shipments:
    print("No shipments found.")
else:
    # Get the most recently created or updated shipment
    shipment = max(shipments, key=lambda s: s.updated_at)
    print(f"Debugging Shipment: {shipment.id} ({shipment.shipment_number})")
    
    print("\n--- PACKAGE ---")
    if shipment.package:
        print(f"cartons: {shipment.package.cartons}")
        print(f"trays_per_carton: {shipment.package.trays_per_carton}")
        print(f"eggs_per_tray: {shipment.package.eggs_per_tray}")
    else:
        print("package is None")
        
    print("\n--- INVOICE INFO ---")
    if shipment.invoice_info:
        print(f"invoice_no: {shipment.invoice_info.invoice_no}")
        print(f"invoice_date: {shipment.invoice_info.invoice_date}")
    else:
        print("invoice_info is None")
        
    print("\n--- MISSING FIELDS LOGIC ---")
    missing_fields = []
    
    if not shipment.invoice_info or not shipment.invoice_info.invoice_no:
        missing_fields.append("Invoice No")
    if not shipment.invoice_info or not shipment.invoice_info.invoice_date:
        missing_fields.append("Invoice Date")
    if not shipment.buyer or not shipment.buyer.consignee_name:
        missing_fields.append("Consignee Name")
    if not shipment.buyer or not shipment.buyer.buyer_country:
        missing_fields.append("Buyer Country")
    if not shipment.shipment_details or not shipment.shipment_details.port_of_loading:
        missing_fields.append("Port of Loading")
    if not shipment.product or not shipment.product.container_no:
        missing_fields.append("Container No")
    if not shipment.package or not shipment.package.cartons:
        missing_fields.append("Cartons")
    if not shipment.pricing or not shipment.pricing.rate_per_egg_usd:
        missing_fields.append("Rate per Egg")
        
    print(f"Missing fields: {missing_fields}")
