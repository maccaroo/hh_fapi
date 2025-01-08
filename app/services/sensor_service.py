from sqlalchemy.orm import Session
from app.db.models import Sensor
from app.schemas.sensor import SensorCreate

def create_sensor(db: Session, sensor: SensorCreate) -> Sensor:
    db_sensor = Sensor(name=sensor.name, description=sensor.description)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

def get_all_sensors(db: Session) -> list[Sensor]:
    return db.query(Sensor).all()

def get_sensor_by_id(db: Session, sensor_id: int) -> Sensor | None:
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()
