from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.persistence import models
from app.api.schemas import meta_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def create_meta(db: Session, meta_create: meta_schema.MetaCreate) -> models.Meta:
    """
    Create a meta.
    """
    db_meta = models.Meta(**meta_create.model_dump())

    try:
        db.add(db_meta)
        db.commit()
        db.refresh(db_meta)
    except IntegrityError as ex:
        db.rollback()
        if "UNIQUE constraint failed:" in str(ex):
            raise IntegrityConstraintViolationException("Meta already exists")
        elif "check_meta_type_value" in str(ex):
            raise IntegrityConstraintViolationException(f"Invalid value for 'meta_type': {meta_create.meta_type}")
        else:
            raise IntegrityConstraintViolationException(f"Cannot create meta: {ex}")
    
    return db_meta


def get_all_metas(context: PaginationContext) -> PaginatedResponse[meta_schema.MetaResponse]:
    """
    Get all metas.
    """
    query = context.db.query(models.Meta)

    if context.search:
        query = query.filter(models.Meta.name.contains(context.search))

    results = paginate_query(query, context.limit, context.offset)

    return results


def get_meta_by_id(db: Session, meta_id: int) -> models.Meta | None:
    """
    Get a meta by id.
    """
    return db.query(models.Meta).filter(models.Meta.id == meta_id).first()


def update_meta_by_id(db: Session, meta_id: int, meta_update: meta_schema.MetaUpdate) -> models.Meta | None:
    """
    Update a meta by id.
    """
    db_meta = get_meta_by_id(db, meta_id)
    if not db_meta:
        return None
    
    try:
        db.query(models.Meta).filter(models.Meta.id == meta_id).update(meta_update.model_dump())
        db.commit()
        db.refresh(db_meta)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot update meta")

    return db_meta


def delete_meta_by_id(db: Session, meta_id: int) -> bool:
    """
    Delete a meta by id.
    """
    meta = get_meta_by_id(db, meta_id)
    if not meta:
        return False
    
    try:
        db.delete(meta)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot delete meta")
    
    return True
