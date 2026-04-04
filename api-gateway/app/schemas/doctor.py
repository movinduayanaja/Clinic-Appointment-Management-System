from pydantic import BaseModel

class DoctorCreate(BaseModel):
    full_name: str
    specialization: str
    phone: str
    email: str
    room_number: str