from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.schedule import ScheduleCreate, ScheduleResponse
from app.crud import schedule as crud_schedule
from app.services_communication.doctor_service import fetch_doctor_name

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.post("/", response_model=ScheduleResponse)
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    doctor_name = await fetch_doctor_name(schedule.doctor_id)
    if doctor_name is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_schedule = crud_schedule.create_schedule(db, schedule)

    return ScheduleResponse(
        schedule_id=new_schedule.schedule_id,
        doctor_id=new_schedule.doctor_id,
        available_date=new_schedule.available_date,
        start_time=new_schedule.start_time,
        end_time=new_schedule.end_time,
        status=new_schedule.status,
        doctor_name=doctor_name,
    )

@router.get("/", response_model=List[ScheduleResponse])
async def get_schedules(db: Session = Depends(get_db)):
    schedules = crud_schedule.get_schedules(db)
    result = []

    for s in schedules:
        doctor_name = await fetch_doctor_name(s.doctor_id)
        result.append(
            ScheduleResponse(
                schedule_id=s.schedule_id,
                doctor_id=s.doctor_id,
                available_date=s.available_date,
                start_time=s.start_time,
                end_time=s.end_time,
                status=s.status,
                doctor_name=doctor_name,
            )
        )
    return result

@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = crud_schedule.get_schedule_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    doctor_name = await fetch_doctor_name(schedule.doctor_id)

    return ScheduleResponse(
        schedule_id=schedule.schedule_id,
        doctor_id=schedule.doctor_id,
        available_date=schedule.available_date,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        status=schedule.status,
        doctor_name=doctor_name,
    )

@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(schedule_id: int, updated: ScheduleCreate, db: Session = Depends(get_db)):
    schedule = crud_schedule.update_schedule(db, schedule_id, updated)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    doctor_name = await fetch_doctor_name(schedule.doctor_id)

    return ScheduleResponse(
        schedule_id=schedule.schedule_id,
        doctor_id=schedule.doctor_id,
        available_date=schedule.available_date,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        status=schedule.status,
        doctor_name=doctor_name,
    )

@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    if not crud_schedule.delete_schedule(db, schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")

    return {"message": "Schedule deleted successfully"}