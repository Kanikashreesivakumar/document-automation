from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from controllers.shipment_controller import get_recent_documents_ctrl

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.get("/recent")
def get_recent_documents(db: Session = Depends(get_db)):
    return get_recent_documents_ctrl(db)
