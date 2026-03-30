import httpx
from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.schemas.patient import PatientCreate

router = APIRouter(
    prefix="/api/patient",
    tags=["Patient"],
    redirect_slashes=False
)


PATIENT_BASE_URL = f"{settings.PATIENT_SERVICE_URL}/patients/"


# GET ALL PATIENTS
@router.get("/patients")
async def get_patients():
    async with httpx.AsyncClient() as client:
        r = await client.get(PATIENT_BASE_URL)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# GET PATIENT BY ID (NO trailing slash!)
@router.get("/patients/{patient_id}")
async def get_patient_by_id(patient_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{PATIENT_BASE_URL}{patient_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# CREATE PATIENT
@router.post("/patients")
async def create_patient(patient: PatientCreate):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            PATIENT_BASE_URL,
            json=patient.model_dump(mode="json")  # ✅ Pydantic v2 fix
        )

    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# UPDATE PATIENT
@router.put("/patients/{patient_id}")
async def update_patient(patient_id: int, patient: PatientCreate):
    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"{PATIENT_BASE_URL}{patient_id}",
            json=patient.model_dump(mode="json")
        )

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


#  DELETE PATIENT
@router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{PATIENT_BASE_URL}{patient_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()