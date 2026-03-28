from datetime import date, time
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


def get_all_appointments(db: Session):
    return db.query(Appointment).order_by(Appointment.appointment_id.asc()).all()


def get_appointment_by_id(db: Session, appointment_id: int):
    return (
        db.query(Appointment)
        .filter(Appointment.appointment_id == appointment_id)
        .first()
    )


def create_appointment(db: Session, payload: AppointmentCreate):
    appointment = Appointment(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        schedule_id=payload.schedule_id,
        appointment_date=payload.appointment_date,
        start_time=payload.start_time,
        end_time=payload.end_time,
        reason=payload.reason,
        status=AppointmentStatus.BOOKED
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def update_appointment(db: Session, appointment: Appointment, payload: AppointmentUpdate):
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment: Appointment):
    db.delete(appointment)
    db.commit()
    return appointment


def get_overlapping_appointment(
    db: Session,
    doctor_id: int,
    appointment_date: date,
    start_time: time,
    end_time: time,
    exclude_appointment_id: int | None = None
):
    query = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status != AppointmentStatus.CANCELLED,
        and_(
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        )
    )

    if exclude_appointment_id is not None:
        query = query.filter(Appointment.appointment_id != exclude_appointment_id)

    return query.first()