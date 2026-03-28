from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import Base, engine, get_db
from app.models.schedule import Schedule, ScheduleStatus
from app.schemas.schedule import ScheduleCreate, ScheduleResponse
from app.services_communication.doctor_service import fetch_doctor_name

import asyncio

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Schedule Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "schedule-service"}


#  CREATE Schedule
@app.post("/schedules", response_model=ScheduleResponse)
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    doctor_name = await fetch_doctor_name(schedule.doctor_id)
    if doctor_name is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_schedule = Schedule(**schedule.model_dump())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    return ScheduleResponse(
        schedule_id=new_schedule.schedule_id,
        doctor_id=new_schedule.doctor_id,
        available_date=new_schedule.available_date,
        start_time=new_schedule.start_time,
        end_time=new_schedule.end_time,
        status=new_schedule.status,
        doctor_name=doctor_name
    )


# Schedule GET ALL
@app.get("/schedules", response_model=List[ScheduleResponse])
async def get_schedules(db: Session = Depends(get_db)):
    schedules = db.query(Schedule).all()
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
                doctor_name=doctor_name
            )
        )
    return result


# Schedule GET BY ID
@app.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()
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
        doctor_name=doctor_name
    )


# Schedule UPDATE
@app.put("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(schedule_id: int, updated: ScheduleCreate, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    for key, value in updated.model_dump().items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)

    doctor_name = await fetch_doctor_name(schedule.doctor_id)

    return ScheduleResponse(
        schedule_id=schedule.schedule_id,
        doctor_id=schedule.doctor_id,
        available_date=schedule.available_date,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        status=schedule.status,
        doctor_name=doctor_name
    )


# DELETE
@app.delete("/schedules/{schedule_id}")
async def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted successfully"}