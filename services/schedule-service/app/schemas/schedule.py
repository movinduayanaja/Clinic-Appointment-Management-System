from pydantic import BaseModel
from datetime import date, time
from app.models.schedule import ScheduleStatus

class ScheduleBase(BaseModel):
    doctor_id: int
    available_date: date
    start_time: time
    end_time: time
    status: ScheduleStatus

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    schedule_id: int
    doctor_name: str | None = None  #  added doctor name

    class Config:
        from_attributes = True  #  updated from orm_mode