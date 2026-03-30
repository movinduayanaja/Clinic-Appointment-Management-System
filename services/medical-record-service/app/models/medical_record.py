from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base
from datetime import datetime, timezone

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    record_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, nullable=False)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    diagnosis = Column(String, nullable=False)
    treatment_notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
