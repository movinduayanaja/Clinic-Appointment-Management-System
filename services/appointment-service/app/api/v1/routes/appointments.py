from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.appointment import (
    get_all_appointments,
    get_appointment_by_id,
    create_appointment as create_appointment_crud,
    update_appointment as update_appointment_crud,
    delete_appointment as delete_appointment_crud,
    get_overlapping_appointment,
)
from app.db.session import get_db
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)
from app.services_communication.patient_service import fetch_patient
from app.services_communication.doctor_service import fetch_doctor
from app.services_communication.schedule_service import fetch_schedule

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def parse_iso_time(value: str) -> time:
    return time.fromisoformat(value)


def validate_slot_within_schedule(payload, schedule_data):
    schedule_date = parse_iso_date(schedule_data["available_date"])
    schedule_start = parse_iso_time(schedule_data["start_time"])
    schedule_end = parse_iso_time(schedule_data["end_time"])

    if payload.appointment_date != schedule_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment date must match the schedule date"
        )

    if payload.start_time >= payload.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment start_time must be earlier than end_time"
        )

    if payload.start_time < schedule_start or payload.end_time > schedule_end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment time must be within the selected schedule time range"
        )


@router.get("/", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    return get_all_appointments(db)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_single_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = get_appointment_by_id(db, appointment_id)

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    return appointment


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    patient = await fetch_patient(payload.patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid patient_id"
        )

    doctor = await fetch_doctor(payload.doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid doctor_id"
        )

    schedule = await fetch_schedule(payload.schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid schedule_id"
        )

    if schedule["doctor_id"] != payload.doctor_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected schedule does not belong to the given doctor"
        )

    validate_slot_within_schedule(payload, schedule)

    overlapping = get_overlapping_appointment(
        db=db,
        doctor_id=payload.doctor_id,
        appointment_date=payload.appointment_date,
        start_time=payload.start_time,
        end_time=payload.end_time
    )

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This appointment time overlaps with another appointment"
        )

    return create_appointment_crud(db, payload)


@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = get_appointment_by_id(db, appointment_id)

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    new_patient_id = payload.patient_id if payload.patient_id is not None else appointment.patient_id
    new_doctor_id = payload.doctor_id if payload.doctor_id is not None else appointment.doctor_id
    new_schedule_id = payload.schedule_id if payload.schedule_id is not None else appointment.schedule_id
    new_appointment_date = payload.appointment_date if payload.appointment_date is not None else appointment.appointment_date
    new_start_time = payload.start_time if payload.start_time is not None else appointment.start_time
    new_end_time = payload.end_time if payload.end_time is not None else appointment.end_time

    patient = await fetch_patient(new_patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid patient_id"
        )

    doctor = await fetch_doctor(new_doctor_id)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid doctor_id"
        )

    schedule = await fetch_schedule(new_schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid schedule_id"
        )

    if schedule["doctor_id"] != new_doctor_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selected schedule does not belong to the given doctor"
        )

    class SlotPayload:
        appointment_date = new_appointment_date
        start_time = new_start_time
        end_time = new_end_time

    validate_slot_within_schedule(SlotPayload, schedule)

    overlapping = get_overlapping_appointment(
        db=db,
        doctor_id=new_doctor_id,
        appointment_date=new_appointment_date,
        start_time=new_start_time,
        end_time=new_end_time,
        exclude_appointment_id=appointment_id
    )

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This appointment time overlaps with another appointment"
        )

    return update_appointment_crud(db, appointment, payload)


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = get_appointment_by_id(db, appointment_id)

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    delete_appointment_crud(db, appointment)
    return {"message": "Appointment deleted successfully"}