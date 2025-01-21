from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import sensor_schema, reading_schema, sensor_metadata_schema
from app.logic.services.exceptions import IntegrityConstraintViolationException
from app.logic.services import sensor_service, reading_service, sensor_metadata_service
from app.persistence.db.database import get_db
from app.utils.auth import get_current_user
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/sensors", tags=["Sensors"])


### Sensors endpoints

@router.post("/", response_model=sensor_schema.SensorResponse, status_code=status.HTTP_201_CREATED)
def create_sensor_endpoint(sensor_create: sensor_schema.SensorCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a sensor.
    """
    try:
        sensor = sensor_service.create_sensor(db, sensor_create, current_user.id)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return sensor


@router.get("/", response_model=PaginatedResponse[sensor_schema.SensorResponse])
def list_sensors_endpoint(
    search: str = Query(None, description="Search by name"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
    ):
    """
    Get all sensors.
    """
    context = PaginationContext(limit=limit, offset=offset, search=search, db=db)
    
    paged_response = sensor_service.get_all_sensors(context)
    return paged_response


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
    try:
        updated_sensor = sensor_service.update_sensor_by_id(db, sensor_id, sensor_update)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    if not updated_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return updated_sensor


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    """
    Delete a sensor.
    """
    try:
        success = sensor_service.delete_sensor_by_id(db, sensor_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sensor not found")
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return


### Readings endpoints

@router.get("/{sensor_id}/readings", response_model=PaginatedResponse[reading_schema.ReadingResponse])
def list_readings_endpoint(
    sensor_id: int, 
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)):
    """
    Get all readings for a sensor.
    """
    context = PaginationContext(limit=limit, offset=offset, db=db)

    sensor = sensor_service.get_sensor_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    
    paged_response = reading_service.get_readings(context, sensor_id)
    return paged_response


### Metadata endpoints

@router.post("/{sensor_id}/metadatas", response_model=sensor_metadata_schema.SensorMetadataResponse, status_code=status.HTTP_201_CREATED)
def create_sensor_metadata_endpoint(sensor_id: int, sensor_metadata_create: sensor_metadata_schema.SensorMetadataCreate, db: Session = Depends(get_db)):
    """
    Create a sensor metadata.
    """
    if not sensor_id == sensor_metadata_create.sensor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sensor id mismatch")

    try:
        sensor_metadata_res = sensor_metadata_service.create_sensor_metadata(db, sensor_metadata_create)
    except sensor_metadata_service.IntegrityConstraintViolationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex))
    
    return sensor_metadata_res


@router.get("/{sensor_id}/metadatas", response_model=PaginatedResponse[sensor_metadata_schema.SensorMetadataResponse])
def list_sensor_metadatas_endpoint(
    sensor_id: int, 
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)):
    """
    Get all sensor metadatas for a sensor.
    """
    context = PaginationContext(limit=limit, offset=offset, db=db)

    sensor = sensor_service.get_sensor_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    
    paged_response = sensor_metadata_service.get_sensor_metadata_by_sensor_id(context, sensor_id)
    return paged_response


@router.get("/{sensor_id}/metadatas/{metadata_id}", response_model=sensor_metadata_schema.SensorMetadataResponse)
def get_sensor_metadata_endpoint(sensor_id: int, metadata_id: int, db: Session = Depends(get_db)):
    """
    Get a sensor metadata.
    """
    sensor_metadata = sensor_metadata_service.get_sensor_metadata_by_sensor_id_and_metadata_id(db, sensor_id, metadata_id)
    if not sensor_metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor metadata not found")
    return sensor_metadata


@router.put("/{sensor_id}/metadatas/{metadata_id}", response_model=sensor_metadata_schema.SensorMetadataResponse)
def update_sensor_metadata_endpoint(sensor_id: int, metadata_id: int, sensor_metadata_update: sensor_metadata_schema.SensorMetadataUpdate, db: Session = Depends(get_db)):
    """
    Update a sensor metadata.
    """
    if not sensor_id == sensor_metadata_update.sensor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sensor id mismatch")
    elif not metadata_id == sensor_metadata_update.metadata_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Metadata id mismatch")

    try:
        sensor_metadata = sensor_metadata_service.update_sensor_metadata(db, sensor_metadata_update)
    except sensor_metadata_service.IntegrityConstraintViolationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    if not sensor_metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor metadata not found")
    return sensor_metadata


@router.delete("/{sensor_id}/metadatas/{metadata_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_metadata_endpoint(sensor_id: int, metadata_id: int, db: Session = Depends(get_db)):
    """
    Delete a sensor metadata.
    """
    success = sensor_metadata_service.delete_sensor_metadata(db, sensor_id, metadata_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor metadata not found")
    return