import sys
sys.path.insert(0, 'd:/Form Automation/backend')
from mapping import _build_base_context
ctx = _build_base_context({})
for k in ['container_no', 'seal_no', 'truck_no', 'container_size', 'total_packages']:
    val = ctx.get(k, 'MISSING')
    print(f'{k}: {repr(val)}')
