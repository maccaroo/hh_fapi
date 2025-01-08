from sqlalchemy.orm import Session
from app.db.models import Reading
from app.schemas.reading import ReadingCreate

def add_reading(db: Session, value: ReadingCreate) -> Reading:
    db_value = Reading(
        sensor_id=value.sensor_id,
        recorded_at=value.recorded_at,
        value=value.value,
        extra_metadata=value.extra_metadata
    )
    db.add(db_value)
    db.commit()
    db.refresh(db_value)
    return db_value

def get_readings(db: Session, sensor_id: int) -> list[Reading]:
    return db.query(Reading).filter(Reading.sensor_id == sensor_id).all()
