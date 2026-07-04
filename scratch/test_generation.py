"""
End-to-end test of document generation.
Run from the backend directory: python test_generation.py
"""
import sys
sys.path.insert(0, r'd:\Form Automation\backend')

sample_shipment = {
    "id": "test-001",
    "shipment_number": "SHP-TEST-001",
    "status": "complete",
    "invoice_info": {
        "invoice_no": "RF/049/26-27",
        "invoice_date": "24.06.2026",
        "shipping_bill_no": "1234567",
        "shipping_bill_date": "25.06.2026",
    },
    "buyer": {
        "consignee_name": "NESTO HYPERMARKET L.L.C.",
        "buyer_name": "NESTO HYPERMARKET",
        "buyer_address": "KHOR AL FAKKAN, UNITED ARAB EMIRATES",
        "buyer_country": "UAE",
    },
    "shipment_details": {
        "pre_carriage_by": "REEFER CONTAINER",
        "vessel_flight_no": "BY SEA",
        "place_of_receipt": "NAMAKKAL",
        "port_of_loading": "COCHIN",
        "port_of_discharge": "DUBAI",
        "final_destination": "DUBAI, UAE",
        "country_of_origin": "INDIA",
        "country_of_final_destination": "UNITED ARAB EMIRATES",
        "terms_of_delivery": "CFR",
    },
    "product": {
        "brand_name": "RASI",
        "product_name": "FRESH WHITE SHELL TABLE EGGS (CHICKEN)",
        "container_type": "40' REEFER",
        "container_no": "TTNU8044030",
    },
    "package": {
        "cartons": 1312,
        "trays_per_carton": 12,
        "eggs_per_tray": 30,
        "eggs_per_carton": 360,
        "total_eggs": 472320,
    },
    "pricing": {
        "rate_per_egg_usd": 0.074,
        "amount_usd": 34951.68,
        "amount_in_words": "US DOLLARS THIRTY FOUR THOUSAND NINE HUNDRED FIFTY ONE AND SIXTY EIGHT CENTS ONLY",
    },
    "weight": {
        "net_weight_per_carton": 18.0,
        "gross_weight_per_carton": 19.5,
        "net_weight": 23616.0,
        "gross_weight": 25584.0,
    },
    "trade_facility": {
        "branch_code": "BR001",
        "bin_number": "BIN123",
        "date_of_examination": "25.06.2026",
        "starting_time": "10:00 AM",
        "completion_time": "02:00 PM",
        "time_taken": "4 Hours",
        "signatory_name": "T. SHANMUGAM",
        "signatory_designation": "DIRECTOR",
        "seal_number": "SEAL12345",
        "truck_number": "TN88M0911",
    },
    "export_insurance": {
        "date": "25.06.2026",
        "sum_assured": "USD 38000",
        "dollar_value": "38000",
        "risk_cover": "ICCA",
        "place_of_loading": "Rasi Foods, Namakkal",
    },
    "animal_certificate": {
        "serial_no": "001/2026",
        "issue_date": "25.06.2026",
        "date_of_inspection": "24.06.2026",
        "vet_officer_name": "Dr. R. MANIVEL",
        "vet_officer_designation": "B.V.Sc",
    },
    "animal_annexure": {
        "producer_name": "SRI SARA EGG FARMS",
        "producer_address": "SF NO:13, PILLUR ROAD, NAMAKKAL",
        "certificate_number": "HC/001/2026",
        "date_of_issue": "25.06.2026",
    },
    "proforma_invoice": {
        "expiry_date": "21.09.2026",
    },
}

from services.document_generator import generate_all

print("=== Testing Document Generation ===")
results = generate_all(sample_shipment)
print(f"\nGenerated {len(results)} documents:")
for r in results:
    print(f"  - {r['file_name']}")
