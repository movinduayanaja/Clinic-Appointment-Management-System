import httpx
from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate

router = APIRouter(
    prefix="/api/medical-records",
    tags=["Medical Records"],
    redirect_slashes=False
)

MEDICAL_RECORD_BASE_URL = f"{settings.MEDICAL_RECORD_SERVICE_URL}/api/v1/medical-records/"

@router.get("/patient/{patient_id}")
async def get_patient_records(patient_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{MEDICAL_RECORD_BASE_URL}patient/{patient_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()

@router.get("/{record_id}")
async def get_record_by_id(record_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{MEDICAL_RECORD_BASE_URL}{record_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()

@router.post("/")
async def create_record(record: MedicalRecordCreate):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            MEDICAL_RECORD_BASE_URL,
            json=record.model_dump(mode="json")
        )

    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()

@router.put("/{record_id}")
async def update_record(record_id: int, updated: MedicalRecordUpdate):
    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"{MEDICAL_RECORD_BASE_URL}{record_id}",
            json=updated.model_dump(exclude_unset=True, mode="json")
        )

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()

@router.delete("/{record_id}")
async def delete_record(record_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{MEDICAL_RECORD_BASE_URL}{record_id}")

    if r.status_code not in (200, 204):
        raise HTTPException(status_code=r.status_code, detail=r.text)

    # API gateway returns JSON, so we handle a 204 carefully
    try:
        return r.json()
    except:
        return {"message": "Record deleted successfully"}
