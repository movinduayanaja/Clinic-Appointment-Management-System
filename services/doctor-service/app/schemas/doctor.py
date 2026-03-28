from pydantic import BaseModel

class DoctorBase(BaseModel):
    full_name: str
    specialization: str
    phone: str
    email: str
    room_number: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    doctor_id: int

    class Config:
        orm_mode = True