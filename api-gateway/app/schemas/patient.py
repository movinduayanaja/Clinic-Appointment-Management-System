from pydantic import BaseModel, EmailStr
from typing import Optional

class PatientCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    age: Optional[int] = None
    gender: Optional[str] = None