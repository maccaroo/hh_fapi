from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import models
from app.schemas import metadata_schema
from app.schemas.pagination_schema import PaginatedResponse
from app.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def create_metadata(db: Session, metadata_create: metadata_schema.MetadataCreate) -> models.Metadata:
    """
    Create a metadata.
    """
    db_metadata = models.Metadata(**metadata_create.model_dump())

    try:
        db.add(db_metadata)
        db.commit()
        db.refresh(db_metadata)
    except IntegrityError as ex:
        db.rollback()
        if "UNIQUE constraint failed:" in str(ex):
            raise IntegrityConstraintViolationException("Metadata already exists")
        elif "check_metadata_type" in str(ex):
            raise IntegrityConstraintViolationException(f"Invalid value for 'data_type': {metadata_create.data_type}")
        else:
            raise IntegrityConstraintViolationException("Cannot create metadata")
    
    return db_metadata


def get_all_metadatas(context: PaginationContext) -> PaginatedResponse[metadata_schema.MetadataResponse]:
    """
    Get all metadatas.
    """
    query = context.db.query(models.Metadata)

    if context.search:
        query = query.filter(models.Metadata.name.contains(context.search))

    results = paginate_query(query, context.limit, context.offset)

    return results


def get_metadata_by_id(db: Session, metadata_id: int) -> models.Metadata | None:
    """
    Get a metadata by id.
    """
    return db.query(models.Metadata).filter(models.Metadata.id == metadata_id).first()


def update_metadata_by_id(db: Session, metadata_id: int, metadata_update: metadata_schema.MetadataUpdate) -> models.Metadata | None:
    """
    Update a metadata by id.
    """
    db_metadata = get_metadata_by_id(db, metadata_id)
    if not db_metadata:
        return None
    
    try:
        db.query(models.Metadata).filter(models.Metadata.id == metadata_id).update(metadata_update.model_dump())
        db.commit()
        db.refresh(db_metadata)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot update metadata")

    return db_metadata


def delete_metadata_by_id(db: Session, metadata_id: int) -> bool:
    """
    Delete a metadata by id.
    """
    metadata = get_metadata_by_id(db, metadata_id)
    if not metadata:
        return False
    
    try:
        db.delete(metadata)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot delete metadata")
    
    return True
