import sys
import traceback
from core.database import SessionLocal
from models.shipment import Shipment, AnimalAnnexure

def test():
    db = SessionLocal()
    try:
        shipment = db.query(Shipment).filter(Shipment.id == '3398b4f2-98ac-4bb1-aa2f-d306d9fa1fd5').first()
        print("Shipment loaded:", shipment.id if shipment else None)
        
        from schemas.shipment import ShipmentFull
        full = ShipmentFull.model_validate(shipment)
        print("ShipmentFull validation successful!")
        print("Animal Annexure:", full.animal_annexure)
    except Exception as e:
        print("Error occurred:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test()
