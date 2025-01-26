from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.schemas import data_point_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.persistence import models
from app.persistence.database import get_db
from app.utils.pagination import PaginationContext, paginate_query


def get_data_point_repo(db: Session = Depends(get_db)):
    return DataPointRepository(db)

class DataPointRepository:
    """
    Data point repository.
    """

    def __init__(
            self, db: Session
            ):
        self.db = db

        

    def add_data_point(
            self, 
            data_point_create: data_point_schema.DataPointCreate
            ) -> models.DataPoint:
        """
        Add a data point.
        """
        db_data_point = models.DataPoint(**data_point_create.model_dump())

        try:
            self.db.add(db_data_point)
            self.db.commit()
            self.db.refresh(db_data_point)
        except IntegrityError:
            self.db.rollback()
            if "UNIQUE constraint failed:" in str(IntegrityError):
                raise IntegrityConstraintViolationException("Data point already exists")
            raise IntegrityConstraintViolationException("Cannot add data point")
        
        return db_data_point


    def get_data_points(
            self, 
            context: PaginationContext, 
            data_id: int
            ) -> PaginatedResponse[data_point_schema.DataPointResponse]:
        """
        Get data points for a data.
        """
        query = self.db.query(models.DataPoint).filter(models.DataPoint.data_id == data_id)

        if context.search:
            query = query.filter(models.DataPoint.value.contains(context.search))

        results = paginate_query(query, context.limit, context.offset)

        return results


    def get_data_point_by_id(
            self, 
            data_point_id: int
            ) -> models.DataPoint | None:
        """
        Get a data point by id.
        """
        return self.db.query(models.DataPoint).filter(models.DataPoint.id == data_point_id).first()


    def delete_data_point_by_id(
            self, 
            data_point_id: int
            ) -> bool:
        """
        Delete a data point by id.
        """
        db_data_point = self.db.query(models.DataPoint).filter(models.DataPoint.id == data_point_id).first()
        if not db_data_point:
            return False
        
        self.db.delete(db_data_point)
        self.db.commit()

        return True
        