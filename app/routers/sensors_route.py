from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.reading import Reading
from app.schemas.sensor import Sensor, SensorCreate, SensorUpdate
from app.services.reading_service import get_readings
from app.services.sensor_service import create_sensor, delete_sensor_by_id, get_all_sensors, get_sensor_by_id, update_sensor_by_id
from app.utils.dependencies import get_db

router = APIRouter()


### Sensors endpoints

@router.post("/", response_model=Sensor, status_code=status.HTTP_201_CREATED)
def create_sensor_endpoint(sensor: SensorCreate, db: Session = Depends(get_db)):
    """
    Create a sensor.
    """
    return create_sensor(db, sensor)


@router.get("/", response_model=list[Sensor])
def list_sensors_endpoint(db: Session = Depends(get_db)):
    """
    Get all sensors.
    """
    return get_all_sensors(db)


@router.get("/{sensor_id}", response_model=Sensor)
def get_sensor_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    """
    Get a sensor.
    """
    sensor = get_sensor_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.put("/{sensor_id}", response_model=Sensor, status_code=status.HTTP_202_ACCEPTED)
def update_sensor_endpoint(sensor_id: int, sensor: SensorUpdate, db: Session = Depends(get_db)):
    """
    Update a sensor.
    """
    updated_sensor = update_sensor_by_id(db, sensor_id, sensor)
    if not updated_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return updated_sensor


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    """
    Delete a sensor.
    """
    success = delete_sensor_by_id(db, sensor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return


### Readings endpoints

@router.get("/{sensor_id}/readings", response_model=list[Reading])
def list_readings_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    """
    Get all readings for a sensor.
    """
    readings = get_readings(db, sensor_id)
    return readings