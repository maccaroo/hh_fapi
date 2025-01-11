from sqlalchemy.orm import Session
from app.db.models import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate


def create_sensor(db: Session, sensor: SensorCreate) -> Sensor:
    """
    Create a sensor.
    """
    db_sensor = Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_all_sensors(db: Session) -> list[Sensor]:
    """
    Get all sensors.
    """
    return db.query(Sensor).all()


def get_sensor_by_id(db: Session, sensor_id: int) -> Sensor | None:
    """
    Get a sensor by id.
    """
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def update_sensor_by_id(db: Session, sensor_id: int, sensor: SensorUpdate) -> Sensor | None:
    """
    Update a sensor by id.
    """
    db_sensor = get_sensor_by_id(db, sensor_id)
    if not sensor:
        return None
    
    db_sensor.name = sensor.name
    db_sensor.description = sensor.description
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