from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.sensor import Sensor, SensorCreate
from app.services.sensor_service import create_sensor, get_all_sensors, get_sensor_by_id
from app.utils.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=Sensor, status_code=status.HTTP_201_CREATED)
def create_sensor_endpoint(sensor: SensorCreate, db: Session = Depends(get_db)):
    return create_sensor(db, sensor)


@router.get("/", response_model=list[Sensor])
def list_sensors_endpoint(db: Session = Depends(get_db)):
    return get_all_sensors(db)


@router.get("/{sensor_id}", response_model=Sensor)
def get_sensor_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    sensor = get_sensor_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor
