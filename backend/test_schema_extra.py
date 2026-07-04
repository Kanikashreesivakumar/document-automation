"""
Test: does TradeFacilityCreate(**payload) raise when extra fields are passed?
This simulates what the preview route does.
"""
import sys
sys.path.insert(0, 'd:/Form Automation/backend')
from schemas.shipment import TradeFacilityCreate

# Simulate the full frontend payload (includes inherited fields from TradeFacilityForm)
payload = {
    # TF fields
    'date_of_examination': '15-06-2026',
    'stuffing_start_time': '10:00 AM',
    'stuffing_completion_time': '11:30 AM',
    'stuffing_duration': '1 Hours 30 Minutes',
    'authorized_signatory_name': 'John Doe',
    'authorized_signatory_designation': 'Export Manager',
    'seal_number': 'SEAL001',
    'truck_number': 'TN-99-AB-1234',
    'container_to_cfs_start_time': '12:00 PM',
    'e_seal_number': 'ESEAL001',
    'goods_description_verified': 'Yes',
    'branch_code': 'BRN001',
    'bin_number': 'BIN001',
    # Inherited fields (NOT in TradeFacilityCreate)
    'exporter_name': 'RASI FOODS',
    'exporter_gstin': '33AASFR2685Q1Z8',
    'invoice_no': 'INV-001',
    'cartons': '100',
    'total_eggs': '3600',
}

print('Testing TradeFacilityCreate(**payload)...')
try:
    obj = TradeFacilityCreate(**payload)
    print('SUCCESS: Object created without error.')
    print('  Values saved:')
    print(f'    stuffing_start_time: {obj.stuffing_start_time}')
    print(f'    stuffing_completion_time: {obj.stuffing_completion_time}')
    print(f'    stuffing_duration: {obj.stuffing_duration}')
    print(f'    authorized_signatory_name: {obj.authorized_signatory_name}')
    print(f'    authorized_signatory_designation: {obj.authorized_signatory_designation}')
    print(f'    branch_code: {obj.branch_code}')
    print(f'    bin_number: {obj.bin_number}')
except Exception as e:
    print(f'FAILED WITH ERROR: {type(e).__name__}: {e}')
    print()
    print('This is the root cause — the preview auto-save is silently skipped.')
