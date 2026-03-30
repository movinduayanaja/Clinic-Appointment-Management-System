import httpx
from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.schemas.schedule import ScheduleCreate

router = APIRouter(
    prefix="/api/schedule",
    tags=["Schedule"],
    redirect_slashes=False
)

# MUST match schedule-service route EXACTLY (with trailing slash)
SCHEDULE_BASE_URL = f"{settings.SCHEDULE_SERVICE_URL}/api/v1/schedules/"


# GET ALL
@router.get("/schedules")
async def get_schedules():
    async with httpx.AsyncClient() as client:
        r = await client.get(SCHEDULE_BASE_URL)

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# ✅ GET BY ID
@router.get("/schedules/{schedule_id}")
async def get_schedule_by_id(schedule_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SCHEDULE_BASE_URL}{schedule_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


# CREATE (POST)  JSON SERIALIZATION
@router.post("/schedules")
async def create_schedule(schedule: ScheduleCreate):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            SCHEDULE_BASE_URL,
            json=schedule.model_dump(mode="json")  
        )

    if r.status_code not in (200, 201):
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


#  UPDATE (PUT)
@router.put("/schedules/{schedule_id}")
async def update_schedule(schedule_id: int, schedule: ScheduleCreate):
    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"{SCHEDULE_BASE_URL}{schedule_id}",
            json=schedule.model_dump(mode="json")  
        )

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()


#  DELETE
@router.delete("/schedules/{schedule_id}")
async def delete_schedule(schedule_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{SCHEDULE_BASE_URL}{schedule_id}")

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return r.json()