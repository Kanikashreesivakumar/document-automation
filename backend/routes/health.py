from fastapi import APIRouter
from controllers.health_controller import check_health, check_root

router = APIRouter()

@router.get("/")
def read_root():
    return check_root()

@router.get("/api/health")
def read_health():
    return check_health()
