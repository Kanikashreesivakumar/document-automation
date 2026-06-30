from core.database import engine
from sqlalchemy import text

with engine.begin() as conn:
    try:
        conn.execute(text("DROP TABLE IF EXISTS vet_certificates CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS vet_annexures CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS insurance_letters CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS examination_reports CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS export_declarations CASCADE"))
        print("Legacy tables dropped.")
    except Exception as e:
        print(f"Error: {e}")
