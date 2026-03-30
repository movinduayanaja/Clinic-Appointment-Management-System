from fastapi import FastAPI
from app.routes.doctor import router as doctor_router
from app.routes.schedule import router as schedule_router
from app.routes.patient import router as patient_router
from app.routes.appointment import router as appointment_router
from app.routes.medical_record import router as medical_record_router

app = FastAPI(
    title="Clinic API Gateway",
    redirect_slashes=False   
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

app.include_router(doctor_router)
app.include_router(schedule_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(medical_record_router)