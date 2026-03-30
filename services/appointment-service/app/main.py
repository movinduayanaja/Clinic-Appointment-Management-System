from fastapi import FastAPI
from app.api.v1.routes.appointments import router as appointment_router
from app.utils.health import router as health_router
from app.db.session import Base, engine
from app.models.appointment import Appointment

app = FastAPI(title="Appointment Service")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Appointment Service is running"}


app.include_router(health_router)
app.include_router(appointment_router)