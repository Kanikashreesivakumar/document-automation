from core.database import Base, engine
from sqlalchemy import text
from models import shipment

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS animal_annexures CASCADE"))
    print("Dropped animal_annexures")

Base.metadata.create_all(bind=engine)
print("Created tables")
