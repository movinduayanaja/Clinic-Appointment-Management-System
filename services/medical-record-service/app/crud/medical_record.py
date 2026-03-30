from sqlalchemy.orm import Session
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate

def create_medical_record(db: Session, record: MedicalRecordCreate) -> MedicalRecord:
    new_record = MedicalRecord(**record.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def get_medical_records_by_patient(db: Session, patient_id: int):
    return db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()

def get_medical_record_by_id(db: Session, record_id: int):
    return db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()

def update_medical_record(db: Session, record_id: int, updated: MedicalRecordUpdate):
    record = get_medical_record_by_id(db, record_id)
    if not record:
        return None

    update_data = updated.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record

def delete_medical_record(db: Session, record_id: int) -> bool:
    record = get_medical_record_by_id(db, record_id)
    if not record:
        return False

    db.delete(record)
    db.commit()
    return True
