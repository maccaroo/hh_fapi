from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.persistence.db import models
from app.api.schemas import sensor_metadata_schema
from app.logic.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def create_sensor_metadata(db: Session, sensor_metadata_create: sensor_metadata_schema.SensorMetadataCreate) -> sensor_metadata_schema.SensorMetadataResponse:
    """
    Create a sensor metadata.
    """
    # Validate the value is compatible with the metadata data type
    metadata = db.query(models.Metadata).filter(models.Metadata.id == sensor_metadata_create.metadata_id).first()
    if not metadata:
        raise IntegrityConstraintViolationException("Metadata not found")
    
    # TODO: Validate the value is compatible with the metadata data type

    db_sensor_metadata = models.SensorMetadata(**sensor_metadata_create.model_dump())

    try:
        db.add(db_sensor_metadata)
        db.commit()
        db.refresh(db_sensor_metadata)
    except IntegrityError as ex:
        db.rollback()
        if "UNIQUE constraint failed:" in str(ex):
            raise IntegrityConstraintViolationException("Sensor metadata already exists")
        else:
            raise IntegrityConstraintViolationException(f"Cannot create sensor metadata")
    
    return db_sensor_metadata


def get_sensor_metadata_by_sensor_id(context: PaginationContext, sensor_id: int) -> sensor_metadata_schema.SensorMetadataResponse | None:
    """
    Get a sensor metadata by sensor id.
    """
    query = context.db.query(models.SensorMetadata).filter(models.SensorMetadata.sensor_id == sensor_id)

    if context.search:
        query = query.filter(models.SensorMetadata.value.contains(context.search))

    results = paginate_query(query, context.limit, context.offset)

    return results


def get_sensor_metadata_by_sensor_id_and_metadata_id(db: Session, sensor_id: int, metadata_id: int) -> sensor_metadata_schema.SensorMetadataResponse | None:
    """
    Get a sensor metadata by id.
    """
    return db.query(models.SensorMetadata).filter(models.SensorMetadata.sensor_id == sensor_id, models.SensorMetadata.metadata_id == metadata_id).first()


def update_sensor_metadata(db: Session, sensor_metadata_update: sensor_metadata_schema.SensorMetadataUpdate) -> sensor_metadata_schema.SensorMetadataResponse | None:
    """
    Update a sensor metadata by id.
    """
    db_sensor_metadata = get_sensor_metadata_by_sensor_id_and_metadata_id(db, sensor_metadata_update.sensor_id, sensor_metadata_update.metadata_id)
    if not db_sensor_metadata:
        return None
    
    try:
        db.query(models.SensorMetadata).filter(models.SensorMetadata.sensor_id == sensor_metadata_update.sensor_id, models.SensorMetadata.metadata_id == sensor_metadata_update.metadata_id).update(sensor_metadata_update.model_dump())
        db.commit()
        db.refresh(db_sensor_metadata)
    except IntegrityError as ex:
        db.rollback()
        if "UNIQUE constraint failed:" in str(ex):
            raise IntegrityConstraintViolationException("Sensor metadata already exists")
        else:
            raise IntegrityConstraintViolationException(f"Cannot update sensor metadata")

    return db_sensor_metadata


def delete_sensor_metadata(db: Session, sensor_id:int, metadata_id: int) -> bool:
    """
    Delete a sensor metadata by id.
    """
    sensor_metadata = get_sensor_metadata_by_sensor_id_and_metadata_id(db, sensor_id, metadata_id)
    if not sensor_metadata:
        return False
    
    try:
        db.delete(sensor_metadata)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot delete sensor metadata")
    
    return True