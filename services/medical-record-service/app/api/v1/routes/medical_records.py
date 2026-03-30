from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse
from app.crud import medical_record as crud_mr
from app.services_communication.doctor_service import fetch_doctor_name
from app.services_communication.patient_service import fetch_patient_name

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])

@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_medical_record(record: MedicalRecordCreate, db: Session = Depends(get_db)):
    # Optionally: Validate patient and doctor exist
    doctor_name = await fetch_doctor_name(record.doctor_id)
    patient_name = await fetch_patient_name(record.patient_id)

    new_record = crud_mr.create_medical_record(db, record)

    return MedicalRecordResponse(
        record_id=new_record.record_id,
        appointment_id=new_record.appointment_id,
        patient_id=new_record.patient_id,
        doctor_id=new_record.doctor_id,
        diagnosis=new_record.diagnosis,
        treatment_notes=new_record.treatment_notes,
        created_at=new_record.created_at,
        doctor_name=doctor_name,
        patient_name=patient_name
    )

@router.get("/patient/{patient_id}", response_model=List[MedicalRecordResponse])
async def get_patient_records(patient_id: int, db: Session = Depends(get_db)):
    records = crud_mr.get_medical_records_by_patient(db, patient_id)
    result = []
    
    patient_name = await fetch_patient_name(patient_id)

    for r in records:
        doctor_name = await fetch_doctor_name(r.doctor_id)
        result.append(
            MedicalRecordResponse(
                record_id=r.record_id,
                appointment_id=r.appointment_id,
                patient_id=r.patient_id,
                doctor_id=r.doctor_id,
                diagnosis=r.diagnosis,
                treatment_notes=r.treatment_notes,
                created_at=r.created_at,
                doctor_name=doctor_name,
                patient_name=patient_name
            )
        )
    return result

@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_record(record_id: int, db: Session = Depends(get_db)):
    record = crud_mr.get_medical_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")

    doctor_name = await fetch_doctor_name(record.doctor_id)
    patient_name = await fetch_patient_name(record.patient_id)

    return MedicalRecordResponse(
        record_id=record.record_id,
        appointment_id=record.appointment_id,
        patient_id=record.patient_id,
        doctor_id=record.doctor_id,
        diagnosis=record.diagnosis,
        treatment_notes=record.treatment_notes,
        created_at=record.created_at,
        doctor_name=doctor_name,
        patient_name=patient_name
    )

@router.put("/{record_id}", response_model=MedicalRecordResponse)
async def update_record(record_id: int, updated: MedicalRecordUpdate, db: Session = Depends(get_db)):
    record = crud_mr.update_medical_record(db, record_id, updated)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")

    doctor_name = await fetch_doctor_name(record.doctor_id)
    patient_name = await fetch_patient_name(record.patient_id)

    return MedicalRecordResponse(
        record_id=record.record_id,
        appointment_id=record.appointment_id,
        patient_id=record.patient_id,
        doctor_id=record.doctor_id,
        diagnosis=record.diagnosis,
        treatment_notes=record.treatment_notes,
        created_at=record.created_at,
        doctor_name=doctor_name,
        patient_name=patient_name
    )

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(record_id: int, db: Session = Depends(get_db)):
    if not crud_mr.delete_medical_record(db, record_id):
        raise HTTPException(status_code=404, detail="Medical record not found")
    return None
