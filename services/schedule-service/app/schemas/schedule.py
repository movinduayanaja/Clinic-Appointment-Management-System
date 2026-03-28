from pydantic import BaseModel, field_validator
from datetime import date, time
from app.models.schedule import ScheduleStatus

class ScheduleBase(BaseModel):
    doctor_id: int
    available_date: date
    start_time: time
    end_time: time
    status: ScheduleStatus

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value not in ScheduleStatus:
            raise ValueError(
                "Status must be one of: AVAILABLE, BOOKED, CANCELLED"
            )
        return value

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    schedule_id: int
    doctor_name: str | None = None

    model_config = {
        "from_attributes": True
    }