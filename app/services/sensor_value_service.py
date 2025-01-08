from sqlalchemy.orm import Session
from app.db.models import SensorValue
from app.schemas.sensor_value import SensorValueCreate

def add_sensor_value(db: Session, value: SensorValueCreate) -> SensorValue:
    db_value = SensorValue(
        sensor_id=value.sensor_id,
        recorded_at=value.recorded_at,
        value=value.value,
        metadata=value.metadata
    )
    db.add(db_value)
    db.commit()
    db.refresh(db_value)
    return db_value

def get_sensor_values(db: Session, sensor_id: int) -> list[SensorValue]:
    return db.query(SensorValue).filter(SensorValue.sensor_id == sensor_id).all()
