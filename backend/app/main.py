from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import DataError, StatementError
import time

app = FastAPI(
    title="Document Template Automation API",
    description="API for document template automation, dynamic mapping, and generation",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Response status: {response.status_code} in {process_time:.4f}s")
    return response

@app.exception_handler(DataError)
async def data_error_handler(request: Request, exc: DataError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid data format provided (e.g., invalid UUID)."},
    )

@app.exception_handler(StatementError)
async def statement_error_handler(request: Request, exc: StatementError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

# Import models so SQLAlchemy registers them before create_all
from models import shipment as _shipment_models  # noqa: F401
from core.database import Base, engine

# Auto-create all tables on startup
try:
    print("Attempting to connect to PostgreSQL and initialize tables...")
    Base.metadata.create_all(bind=engine)
    print("Database connection and table initialization successful.")
except Exception as e:
    print("Failed to connect to PostgreSQL or initialize tables.")
    print(f"Exact error: {e}")
    # We don't raise here to avoid crashing FastAPI completely,
    # as per user request: "Do not crash FastAPI. Explain the problem clearly."
    print("FastAPI will start, but database operations will fail.")

from routes.health import router as health_router
from routes.shipments import router as shipments_router
from routes.documents import router as documents_router

app.include_router(health_router)
app.include_router(shipments_router)
app.include_router(documents_router)
