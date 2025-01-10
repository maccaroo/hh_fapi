from sqlalchemy.orm import Session
from app.db.models import Reading
from app.schemas.reading import ReadingCreate


def add_reading(db: Session, value: ReadingCreate) -> Reading:
    """
    Add a reading.
    """
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
    """
    Get readings for a sensor.
    """
    return db.query(Reading).filter(Reading.sensor_id == sensor_id).all()


def get_reading_by_id(db: Session, reading_id: int) -> Reading | None:
    """
    Get a reading by id.
    """
    return db.query(Reading).filter(Reading.id == reading_id).first()


def delete_reading_by_id(db: Session, reading_id: int) -> bool:
    """
    Delete a reading by id.
    """
    reading = get_reading_by_id(db, reading_id)
    if not reading:
        return False
    
    db.delete(reading)
    db.commit()
    return True