from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.persistence.db import models
from app.api.schemas import data_point_schema
from app.logic.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext, paginate_query


def add_data_point(db: Session, data_point_create: data_point_schema.DataPointCreate) -> models.DataPoint:
    """
    Add a data point.
    """
    db_data_point = models.DataPoint(**data_point_create.model_dump())

    try:
        db.add(db_data_point)
        db.commit()
        db.refresh(db_data_point)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("Cannot add data point")
    
    return db_data_point


def get_data_points(context: PaginationContext, data_id: int) -> list[models.DataPoint]:
    """
    Get data points for a data.
    """
    query = context.db.query(models.DataPoint).filter(models.DataPoint.data_id == data_id)
    results = paginate_query(query, context.limit, context.offset)

    return results


def get_data_point_by_id(db: Session, data_point_id: int) -> models.DataPoint | None:
    """
    Get a data point by id.
    """
    return db.query(models.DataPoint).filter(models.DataPoint.id == data_point_id).first()


def delete_data_point_by_id(db: Session, data_point_id: int) -> bool:
    """
    Delete a data point by id.
    """
    db_data_point = get_data_point_by_id(db, data_point_id)
    if not db_data_point:
        return False
    
    db.delete(db_data_point)
    db.commit()
    return True