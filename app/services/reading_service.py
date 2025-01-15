from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import app.db.models as models
import app.schemas.reading_schema as reading_schema
from app.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def add_reading(db: Session, reading_create: reading_schema.ReadingCreate) -> models.Reading:
    """
    Add a reading.
    """
    db_value = models.Reading(**reading_create.model_dump())

    try:
        db.add(db_value)
        db.commit()
        db.refresh(db_value)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot add reading")
    
    return db_value


def get_readings(context: PaginationContext, sensor_id: int) -> list[models.Reading]:
    """
    Get readings for a sensor.
    """
    query = context.db.query(models.Reading).filter(models.Reading.sensor_id == sensor_id)
    results = paginate_query(query, context.limit, context.offset)

    return results


def get_reading_by_id(db: Session, reading_id: int) -> models.Reading | None:
    """
    Get a reading by id.
    """
    return db.query(models.Reading).filter(models.Reading.id == reading_id).first()


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