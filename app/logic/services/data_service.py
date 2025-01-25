from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.persistence.db import models
from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import data_schema
from app.logic.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def create_data(db: Session, data_create: data_schema.DataCreate, user_id: int) -> data_schema.DataResponse:
    """
    Create a data.
    """
    db_data = models.Data(**data_create.model_dump())
    db_data.created_by_user_id = user_id

    try:
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
    except IntegrityError as ex:
        db.rollback()
        if "UNIQUE constraint failed:" in str(ex):
            raise IntegrityConstraintViolationException("Data already exists")
        elif "check_data_type_value" in str(ex):
            raise IntegrityConstraintViolationException(f"Invalid value for 'data_type': {data_create.data_type}")
        else:
            raise IntegrityConstraintViolationException(f"Cannot create data: {ex}")
    
    return db_data


def get_all_datas(context: PaginationContext) -> PaginatedResponse[data_schema.DataResponse]:
    """
    Get all datas.
    """
    query = context.db.query(models.Data)

    if context.search:
        query = query.filter(models.Data.name.contains(context.search))

    results = paginate_query(query, context.limit, context.offset)

    return results


def get_data_by_id(db: Session, data_id: int) -> data_schema.DataResponse | None:
    """
    Get a data by id.
    """
    db_data = db.query(models.Data).filter(models.Data.id == data_id).first()
    if not db_data:
        return None

    return db_data


def update_data_by_id(db: Session, data_id: int, data_update: data_schema.DataUpdate) -> data_schema.DataResponse | None:
    """
    Update a data by id.
    """
    db_data = db.query(models.Data).filter(models.Data.id == data_id).first()
    if not db_data:
        return None
    
    try:
        db.query(models.Data).filter(models.Data.id == data_id).update(data_update.model_dump())
        db.commit()
        db.refresh(db_data)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot update data")

    return db_data


def delete_data_by_id(db: Session, data_id: int) -> bool:
    """
    Delete a data by id.
    """
    db_data = db.query(models.Data).filter(models.Data.id == data_id).first()
    if not db_data:
        return False
    
    try:
        db.delete(db_data)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot delete data")
    
    return True