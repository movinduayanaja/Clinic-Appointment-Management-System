from fastapi import FastAPI
from app.db.session import Base, engine
from app.utils.health import router as health_router
from app.api.v1.routes.medical_records import router as medical_records_router
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Record Service")

# Health endpoint
app.include_router(health_router)

# Versioned APIs
app.include_router(medical_records_router, prefix="/api/v1")
