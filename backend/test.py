import sys
from core.database import SessionLocal
from controllers.shipment_controller import get_shipment_ctrl
import traceback

db = SessionLocal()
try:
    res = get_shipment_ctrl('3398b4f2-98ac-4bb1-aa2f-d306d9fa1fd5', db)
    print(res)
except Exception as e:
    traceback.print_exc()
