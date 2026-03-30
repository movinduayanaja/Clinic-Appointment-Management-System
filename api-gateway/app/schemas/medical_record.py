from pydantic import BaseModel

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
