import requests

API = "http://localhost:8000/api/shipments"

# Create
s = requests.post(API).json()
if "id" not in s:
    print("Could not create shipment. Backend might not be running.", s)
    exit(1)

id = s["id"]
print("Created shipment:", id)

# Step 1: Save data
data = {
    "cartons": 1500,
    "invoice_no": "INV-123",
    "invoice_date": "2026-07-04",
    "consignee_name": "John Doe",
    "buyer_country": "US",
    "port_of_loading": "Mundra",
    "container_no": "CONT123",
    "rate_per_egg_usd": 0.1,
    "trays_per_carton": 12,
    "eggs_per_tray": 30
}
res = requests.post(f"{API}/{id}/data", json=data)
print("Saved Data:", res.status_code)

# Step 2: Live preview proforma (bug simulation)
res = requests.post(f"{API}/{id}/preview-pdf/proforma_invoice", json={"po_number": "PO-999"})
print("Preview Proforma:", res.status_code)

# Generate
res = requests.post(f"{API}/{id}/generate")
print("Generate:", res.status_code, res.json())
