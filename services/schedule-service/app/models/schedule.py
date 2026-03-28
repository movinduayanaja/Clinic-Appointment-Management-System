from sqlalchemy import Column, Integer, String, Date, Time, Enum
from app.db.session import Base
import enum

class ScheduleStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"

class Schedule(Base):
    __tablename__ = "schedules"

    schedule_id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, nullable=False)
    available_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.AVAILABLE)