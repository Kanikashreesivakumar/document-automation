from services.health_service import get_health_status, get_root_status

def check_root():
    return get_root_status()

def check_health():
    return get_health_status()
