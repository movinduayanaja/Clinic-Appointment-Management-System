from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from app.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    schedule_id: int
    appointment_date: date
    start_time: time
    end_time: time
    reason: str


class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    schedule_id: Optional[int] = None
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    reason: Optional[str] = None
    status: Optional[AppointmentStatus] = None


class AppointmentResponse(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    schedule_id: int
    appointment_date: date
    start_time: time
    end_time: time
    reason: str
    status: AppointmentStatus

    model_config = {
        "from_attributes": True
    }