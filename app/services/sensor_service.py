from sqlalchemy.orm import Session

import app.db.models as models
import app.schemas.sensor_schema as sensor_schema


def create_sensor(db: Session, sensor_create: sensor_schema.SensorCreate, user_id: int) -> models.Sensor:
    """
    Create a sensor.
    """
    db_sensor = models.Sensor(**sensor_create.model_dump())
    db_sensor.created_by_user_id = user_id

    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_all_sensors(db: Session) -> list[models.Sensor]:
    """
    Get all sensors.
    """
    return db.query(models.Sensor).all()


def get_sensor_by_id(db: Session, sensor_id: int) -> models.Sensor | None:
    """
    Get a sensor by id.
    """
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def update_sensor_by_id(db: Session, sensor_id: int, sensor_update: sensor_schema.SensorUpdate) -> models.Sensor | None:
    """
    Update a sensor by id.
    """
    db_sensor = get_sensor_by_id(db, sensor_id)
    if not db_sensor:
        return None
    
    db.query(models.Sensor).filter(models.Sensor.id == sensor_id).update(sensor_update.model_dump())
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def delete_sensor_by_id(db: Session, sensor_id: int) -> bool:
    """
    Delete a sensor by id.
    """
    sensor = get_sensor_by_id(db, sensor_id)
    if not sensor:
        return False
    
    db.delete(sensor)
    db.commit()
    return True