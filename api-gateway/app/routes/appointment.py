import httpx
from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate

router = APIRouter(
    prefix="/api/appointment",
    tags=["Appointment"],
    redirect_slashes=False
)

# Match backend EXACTLY
APPOINTMENT_BASE_URL = f"{settings.APPOINTMENT_SERVICE_URL}/appointments/"


# GET ALL
@router.get("/appointments")
async def get_appointments():
    async with httpx.AsyncClient() as client:
        r = await client.get(APPOINTMENT_BASE_URL)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# GET BY ID (NO trailing slash!)
@router.get("/appointments/{appointment_id}")
async def get_appointment_by_id(appointment_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{APPOINTMENT_BASE_URL}{appointment_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# CREATE
@router.post("/appointments")
async def create_appointment(payload: AppointmentCreate):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            APPOINTMENT_BASE_URL,
            json=payload.model_dump(mode="json")  # ✅ REQUIRED
        )

    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# UPDATE
@router.put("/appointments/{appointment_id}")
async def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate
):
    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"{APPOINTMENT_BASE_URL}{appointment_id}",
            json=payload.model_dump(mode="json")
        )

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# DELETE
@router.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{APPOINTMENT_BASE_URL}{appointment_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()