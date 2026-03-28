from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate

def create_schedule(db: Session, schedule: ScheduleCreate) -> Schedule:
    new_schedule = Schedule(**schedule.model_dump())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

def get_schedules(db: Session):
    return db.query(Schedule).all()

def get_schedule_by_id(db: Session, schedule_id: int):
    return db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()

def update_schedule(db: Session, schedule_id: int, updated: ScheduleCreate):
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return None

    for key, value in updated.model_dump().items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule

def delete_schedule(db: Session, schedule_id: int) -> bool:
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return False

    db.delete(schedule)
    db.commit()
    return True