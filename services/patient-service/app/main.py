from fastapi import FastAPI
from app.api.v1.routes.patients import router as patient_router
from app.utils.health import router as health_router
from app.db.base import Base
from app.db.session import engine
from app.models.patient import Patient

app = FastAPI(title="Patient Service")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Patient Service is running"}


app.include_router(health_router)
app.include_router(patient_router)