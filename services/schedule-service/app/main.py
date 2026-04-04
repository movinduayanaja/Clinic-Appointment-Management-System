from fastapi import FastAPI
from app.db.session import Base, engine
from app.utils.health import router as health_router
from app.api.v1.routes.schedules import router as schedule_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Schedule Service")

# Health endpoint (not versioned)
app.include_router(health_router)

# Versioned APIs
app.include_router(schedule_router, prefix="/api/v1")