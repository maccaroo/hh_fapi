from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.sensor_value import SensorValue, SensorValueCreate
from app.services.sensor_value_service import add_sensor_value, get_sensor_values
from app.utils.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=SensorValue)
def add_sensor_value_endpoint(value: SensorValueCreate, db: Session = Depends(get_db)):
    return add_sensor_value(db, value)

@router.get("/{sensor_id}/values", response_model=list[SensorValue])
def list_sensor_values_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    return get_sensor_values(db, sensor_id)
