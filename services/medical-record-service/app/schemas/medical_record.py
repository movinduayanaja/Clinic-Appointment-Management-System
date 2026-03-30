from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MedicalRecordBase(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    treatment_notes: str | None = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    diagnosis: str | None = None
    treatment_notes: str | None = None

class MedicalRecordResponse(MedicalRecordBase):
    record_id: int
    created_at: datetime
    patient_name: str | None = None
    doctor_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
