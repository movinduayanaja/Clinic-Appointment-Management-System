from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def get_all_patients(db: Session):
    return db.query(Patient).order_by(Patient.id.asc()).all()


def get_patient_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patient_by_email(db: Session, email: str):
    return db.query(Patient).filter(Patient.email == email).first()


def create_patient(db: Session, payload: PatientCreate):
    patient = Patient(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        age=payload.age,
        gender=payload.gender
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update_patient(db: Session, patient: Patient, payload: PatientUpdate):
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(db: Session, patient: Patient):
    db.delete(patient)
    db.commit()
    return patient