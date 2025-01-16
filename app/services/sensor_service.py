from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import app.db.models as models
from app.schemas.pagination_schema import PaginatedResponse
import app.schemas.sensor_schema as sensor_schema
from app.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def create_sensor(db: Session, sensor_create: sensor_schema.SensorCreate, user_id: int) -> sensor_schema.SensorResponse:
    """
    Create a sensor.
    """
    db_sensor = models.Sensor(**sensor_create.model_dump())
    db_sensor.created_by_user_id = user_id

    try:
        db.add(db_sensor)
        db.commit()
        db.refresh(db_sensor)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Sensor already exists")
    
    return db_sensor


def get_all_sensors(context: PaginationContext) -> PaginatedResponse[sensor_schema.SensorResponse]:
    """
    Get all sensors.
    """
    query = context.db.query(models.Sensor)

    if context.search:
        query = query.filter(models.Sensor.name.contains(context.search))

    results = paginate_query(query, context.limit, context.offset)

    return results


def get_sensor_by_id(db: Session, sensor_id: int) -> sensor_schema.SensorResponse | None:
    """
    Get a sensor by id.
    """
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def update_sensor_by_id(db: Session, sensor_id: int, sensor_update: sensor_schema.SensorUpdate) -> sensor_schema.SensorResponse | None:
    """
    Update a sensor by id.
    """
    db_sensor = get_sensor_by_id(db, sensor_id)
    if not db_sensor:
        return None
    
    try:
        db.query(models.Sensor).filter(models.Sensor.id == sensor_id).update(sensor_update.model_dump())
        db.commit()
        db.refresh(db_sensor)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot update sensor")

    return db_sensor


def delete_sensor_by_id(db: Session, sensor_id: int) -> bool:
    """
    Delete a sensor by id.
    """
    sensor = get_sensor_by_id(db, sensor_id)
    if not sensor:
        return False
    
    try:
        db.delete(sensor)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot delete sensor")
    
    return True