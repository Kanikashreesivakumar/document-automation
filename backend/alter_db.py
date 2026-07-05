import sys
from sqlalchemy import create_engine, text
from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

commands = [
    "ALTER TABLE invoice_info ADD COLUMN exporter_reference VARCHAR(200);",
    "ALTER TABLE invoice_info ADD COLUMN other_reference VARCHAR(200);",
    "ALTER TABLE products ADD COLUMN shipment_declaration TEXT;",
    "ALTER TABLE products ADD COLUMN production_date VARCHAR(50);",
    "ALTER TABLE products ADD COLUMN expiry_date VARCHAR(50);",
    "ALTER TABLE products ADD COLUMN lot_number VARCHAR(100);",
    "ALTER TABLE products ADD COLUMN epcg_licence_number VARCHAR(100);",
    "ALTER TABLE products ADD COLUMN dt VARCHAR(100);",
    "ALTER TABLE products ADD COLUMN egg_size VARCHAR(100);",
    "ALTER TABLE products ADD COLUMN pan_number VARCHAR(100);",
    "ALTER TABLE products ADD COLUMN gstin VARCHAR(100);",
    "ALTER TABLE products ADD COLUMN hsn_code VARCHAR(100);",
    "ALTER TABLE products ADD COLUMN production_duration VARCHAR(50);",
    "ALTER TABLE proforma_invoices ADD COLUMN company_account_name VARCHAR(200);",
    "ALTER TABLE proforma_invoices ADD COLUMN company_account_number VARCHAR(100);",
    "ALTER TABLE proforma_invoices ADD COLUMN company_bank_name VARCHAR(200);",
    "ALTER TABLE proforma_invoices ADD COLUMN company_branch VARCHAR(100);",
    "ALTER TABLE proforma_invoices ADD COLUMN company_swift VARCHAR(50);"
]

with engine.connect() as conn:
    for cmd in commands:
        try:
            conn.execute(text(cmd))
            conn.commit()
            print(f"Success: {cmd}")
        except Exception as e:
            print(f"Skipped/Error on {cmd}: {e}")
            conn.rollback()
