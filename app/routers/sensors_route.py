from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.schemas.sensor_schema as sensor_schema
import app.schemas.reading_schema as reading_schema
import app.services.sensor_service as sensor_service
import app.services.reading_service as reading_service
from app.utils.dependencies import get_db

router = APIRouter()


### Sensors endpoints

@router.post("/", response_model=sensor_schema.SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor_endpoint(sensor_create: sensor_schema.SensorCreate, db: Session = Depends(get_db)):
    """
    Create a sensor.
    """
    sensor = sensor_service.create_sensor(db, sensor_create)
    return sensor


@router.get("/", response_model=list[sensor_schema.SensorResponse])
def list_sensors_endpoint(db: Session = Depends(get_db)):
    """
    Get all sensors.
    """
    sensors = sensor_service.get_all_sensors(db)
    return sensors


@router.get("/{sensor_id}", response_model=sensor_schema.SensorResponse)
def get_sensor_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    """
    Get a sensor.
    """
    sensor = sensor_service.get_sensor_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.put("/{sensor_id}", response_model=sensor_schema.SensorResponse)
def update_sensor_endpoint(sensor_id: int, sensor_update: sensor_schema.SensorUpdate, db: Session = Depends(get_db)):
    """
    Update a sensor.
    """
    updated_sensor = sensor_service.update_sensor_by_id(db, sensor_id, sensor_update)
    if not updated_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return updated_sensor


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    """
    Delete a sensor.
    """
    success = sensor_service.delete_sensor_by_id(db, sensor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return


### Readings endpoints

@router.get("/{sensor_id}/readings", response_model=list[reading_schema.ReadingResponse])
def list_readings_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    """
    Get all readings for a sensor.
    """
    readings = reading_service.get_readings(db, sensor_id)
    return readings