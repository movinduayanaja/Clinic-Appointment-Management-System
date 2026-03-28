from pydantic import BaseModel, EmailStr
from typing import Optional


class PatientCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    age: Optional[int] = None
    gender: Optional[str] = None


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    age: Optional[int] = None
    gender: Optional[str] = None

    model_config = {
        "from_attributes": True
    }