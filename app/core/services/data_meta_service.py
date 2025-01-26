from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.persistence import models
from app.api.schemas import data_meta_schema
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def create_data_meta(db: Session, data_meta_create: data_meta_schema.DataMetaCreate) -> data_meta_schema.DataMetaResponse:
    """
    Create a data meta.
    """
    # Validate the value is compatible with the meta type
    db_meta = db.query(models.Meta).filter(models.Meta.id == data_meta_create.meta_id).first()
    if not db_meta:
        raise IntegrityConstraintViolationException("Meta not found")
    
    # TODO: Validate the value is compatible with the meta type

    db_data_meta = models.DataMeta(**data_meta_create.model_dump())

    try:
        db.add(db_data_meta)
        db.commit()
        db.refresh(db_data_meta)
    except IntegrityError as ex:
        db.rollback()
        if "UNIQUE constraint failed:" in str(ex):
            raise IntegrityConstraintViolationException("Data meta already exists")
        else:
            raise IntegrityConstraintViolationException(f"Cannot create data meta")
    
    return db_data_meta


def get_data_meta_by_data_id(context: PaginationContext, data_id: int) -> data_meta_schema.DataMetaResponse | None:
    """
    Get a data meta by data id.
    """
    query = context.db.query(models.DataMeta).filter(models.DataMeta.data_id == data_id)

    if context.search:
        query = query.filter(models.DataMeta.value.contains(context.search))

    results = paginate_query(query, context.limit, context.offset)

    return results


def get_data_meta_by_data_id_and_meta_id(db: Session, data_id: int, meta_id: int) -> data_meta_schema.DataMetaResponse | None:
    """
    Get a data meta by data id and meta id.
    """
    return db.query(models.DataMeta).filter(models.DataMeta.data_id == data_id, models.DataMeta.meta_id == meta_id).first()


def update_data_meta(db: Session, data_meta_update: data_meta_schema.DataMetaUpdate) -> data_meta_schema.DataMetaResponse | None:
    """
    Update a data meta by id.
    """
    db_data_meta = get_data_meta_by_data_id_and_meta_id(db, data_meta_update.data_id, data_meta_update.meta_id)
    if not db_data_meta:
        return None
    
    try:
        db.query(models.DataMeta).filter(models.DataMeta.data_id == data_meta_update.data_id, models.DataMeta.meta_id == data_meta_update.meta_id).update(data_meta_update.model_dump())
        db.commit()
        db.refresh(db_data_meta)
    except IntegrityError as ex:
        db.rollback()
        if "UNIQUE constraint failed:" in str(ex):
            raise IntegrityConstraintViolationException("Data meta already exists")
        else:
            raise IntegrityConstraintViolationException(f"Cannot update data meta")

    return db_data_meta


def delete_data_meta(db: Session, data_id:int, meta_id: int) -> bool:
    """
    Delete a data meta by data id and meta id.
    """
    db_data_meta = get_data_meta_by_data_id_and_meta_id(db, data_id, meta_id)
    if not db_data_meta:
        return False
    
    try:
        db.delete(db_data_meta)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot delete data meta")
    
    return True