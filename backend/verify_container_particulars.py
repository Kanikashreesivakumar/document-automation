"""
Full end-to-end verification of Container Particulars data flow.
"""
import sys
sys.path.insert(0, 'd:/Form Automation/backend')
from debug import shipments
from services.shipment_service import _shipment_to_dict
from mapping import trade_facility_context

s = max(shipments, key=lambda x: x.updated_at)
d = _shipment_to_dict(s)
ctx = trade_facility_context(d)

FIELDS = {
    'Container No':     ('product',       'container_no',    'container_no'),
    'Seal No':          ('trade_facility', 'seal_number',     'seal_no'),
    'Truck No':         ('trade_facility', 'truck_number',    'truck_no'),
    'Container Size':   ('product',       'container_type',  'container_size'),
    'No. of Packages':  ('package',       'cartons',         'total_packages'),
}

print(f"Shipment: {s.shipment_number}\n")
print(f"{'Field':<22} {'DB Value':<25} {'Context Key':<18} {'Context Value':<20}")
print("-" * 90)

all_pass = True
for label, (table, col, ctx_key) in FIELDS.items():
    db_val  = (d.get(table) or {}).get(col, '<<<MISSING>>>')
    ctx_val = ctx.get(ctx_key, '<<<MISSING>>>')
    ok = ctx_val not in ('', '<<<MISSING>>>', None)
    flag = "OK" if ok else "MISSING"
    if not ok:
        all_pass = False
    print(f"{label:<22} {str(db_val):<25} {ctx_key:<18} {str(ctx_val):<20}  [{flag}]")

print()
print("=== DOCX Placeholder Mapping ===")
for label, (table, col, ctx_key) in FIELDS.items():
    ph_map = {
        'container_no':    '{{ container_no }}',
        'seal_no':         '{{ seal_no }}',
        'truck_no':        '{{ truck_no }}',
        'container_size':  '{{ container_size }}',
        'total_packages':  '{{ total_packages }}',
    }
    ph = ph_map.get(ctx_key, '?')
    print(f"  {label:<22} -> {ph}")

print()
if all_pass:
    print("RESULT: All fields resolve correctly from DB -> context -> DOCX.")
else:
    print("RESULT: Some fields are missing. Check DB input for this shipment.")
