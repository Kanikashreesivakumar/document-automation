import sys
sys.path.insert(0, 'd:/Form Automation/backend')
from debug import shipments
from services.shipment_service import _shipment_to_dict
from mapping import trade_facility_context

s = max(shipments, key=lambda x: x.updated_at)
d = _shipment_to_dict(s)
ctx = trade_facility_context(d)

FIELDS = ['branch_code', 'bin_number', 'starting_time', 'completion_time', 'time_taken', 'signatory_name', 'signatory_designation']

print('=== DB trade_facility record ===')
tf = d.get('trade_facility') or {}
for k, v in tf.items():
    print(f'  {k}: {repr(v)}')

print()
print('=== MAPPING CONTEXT for 7 fields ===')
for f in FIELDS:
    val = ctx.get(f, 'NOT_IN_CONTEXT')
    print(f'  {f}: {repr(val)}')
