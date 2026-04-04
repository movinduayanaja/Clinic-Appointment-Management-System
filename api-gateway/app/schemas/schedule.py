from pydantic import BaseModel
from datetime import date, time
from typing import Literal

class ScheduleCreate(BaseModel):
    doctor_id: int
    available_date: date
    start_time: time
    end_time: time
    status: Literal["AVAILABLE", "BOOKED", "CANCELLED"]