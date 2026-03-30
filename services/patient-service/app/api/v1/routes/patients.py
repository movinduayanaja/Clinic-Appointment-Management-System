from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.patient import (
    get_all_patients,
    get_patient_by_id,
    get_patient_by_email,
    create_patient as create_patient_crud,
    update_patient as update_patient_crud,
    delete_patient as delete_patient_crud,
)
from app.db.session import get_db
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return get_all_patients(db)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_single_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient_by_id(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return patient


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    existing_patient = get_patient_by_email(db, payload.email)

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A patient with this email already exists"
        )

    return create_patient_crud(db, payload)


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    patient = get_patient_by_id(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    if payload.email and payload.email != patient.email:
        existing_patient = get_patient_by_email(db, payload.email)
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A patient with this email already exists"
            )

    return update_patient_crud(db, patient, payload)


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient_by_id(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    delete_patient_crud(db, patient)
    return {"message": "Patient deleted successfully"}