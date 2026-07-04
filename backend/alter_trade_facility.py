import sys
sys.path.insert(0, 'd:/Form Automation/backend')
from sqlalchemy import create_engine, text
from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

commands = [
    "ALTER TABLE trade_facilities ADD COLUMN branch_code VARCHAR(100);",
    "ALTER TABLE trade_facilities ADD COLUMN bin_number VARCHAR(100);",
]

with engine.connect() as conn:
    for cmd in commands:
        try:
            conn.execute(text(cmd))
            conn.commit()
            print(f"OK: {cmd}")
        except Exception as e:
            print(f"Skipped (already exists?): {e}")
            conn.rollback()

print("Done.")
