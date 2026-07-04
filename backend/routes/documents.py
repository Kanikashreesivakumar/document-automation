from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
from core.database import get_db
from controllers.shipment_controller import get_recent_documents_ctrl

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.get("/recent")
def get_recent_documents(db: Session = Depends(get_db)):
    return get_recent_documents_ctrl(db)


@router.get("/frame-header")
def get_frame_header_image():
    image_path = Path(r"D:\Form Automation\frame.jpeg")
    return FileResponse(path=str(image_path), filename=image_path.name, media_type="image/jpeg")
