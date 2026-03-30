import httpx
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.doctor import DoctorCreate

router = APIRouter(prefix="/api/doctor", tags=["Doctor"])

@router.get("/doctors")
async def get_doctors():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{settings.DOCTOR_SERVICE_URL}/doctors")
    return r.json()

@router.get("/doctors/{doctor_id}")
async def get_doctor_by_id(doctor_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{settings.DOCTOR_SERVICE_URL}/doctors/{doctor_id}")
    return r.json()

@router.post("/doctors")
async def create_doctor(doctor: DoctorCreate):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{settings.DOCTOR_SERVICE_URL}/doctors",
            json=doctor.model_dump()
        )
    return r.json()

@router.put("/doctors/{doctor_id}")
async def update_doctor(doctor_id: int, doctor: DoctorCreate):
    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"{settings.DOCTOR_SERVICE_URL}/doctors/{doctor_id}",
            json=doctor.model_dump()
        )
    return r.json()

@router.delete("/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{settings.DOCTOR_SERVICE_URL}/doctors/{doctor_id}")
    return r.json()
