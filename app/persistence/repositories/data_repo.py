from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.schemas import data_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.persistence import models
from app.persistence.database import get_db
from app.utils.pagination import PaginationContext, paginate_query

class DataRepository:
    """
    Data repository.
    """

    def __init__(
            self, 
            db: Session
            ):
        self.db = db

    
    def add_data(
            self, 
            data_create: data_schema.DataCreate,
            user_id: int
            ) -> data_schema.DataResponse:
        """
        Add a data.
        """
        db_data = models.Data(**data_create.model_dump())
        db_data.created_by_user_id = user_id

        try:
            self.db.add(db_data)
            self.db.commit()
            self.db.refresh(db_data)
        except IntegrityError as ex:
            self.db.rollback()
            if "UNIQUE constraint failed:" in str(ex):
                raise IntegrityConstraintViolationException("Data already exists")
            elif "check_data_type_value" in str(ex):
                raise IntegrityConstraintViolationException(f"Invalid value for 'data_type': {data_create.data_type}")
            else:
                # TODO: Log the error 
                raise IntegrityConstraintViolationException(f"Cannot create data")
        
        return db_data
    

    def get_datas(self, context: PaginationContext) -> PaginatedResponse[data_schema.DataResponse]:
        """
        Get datas.
        """
        query = self.db.query(models.Data)

        if context.search:
            query = query.filter(models.Data.name.contains(context.search))

        return paginate_query(query, context.limit, context.offset)


    def get_data_by_id(self, data_id: int) -> data_schema.DataResponse | None:
        """
        Get a data by id.
        """
        db_data = self.db.query(models.Data).filter(models.Data.id == data_id).first()
        if not db_data:
            return None

        return db_data
    

    def update_data_by_id(self, data_id: int, data_update: data_schema.DataUpdate) -> data_schema.DataResponse | None:
        """
        Update a data by id.
        """
        db_data = self.db.query(models.Data).filter(models.Data.id == data_id).first()
        if not db_data:
            return None
        
        try:
            self.db.query(models.Data).filter(models.Data.id == data_id).update(data_update.model_dump())
            self.db.commit()
            self.db.refresh(db_data)
        except IntegrityError:
            self.db.rollback()
            raise IntegrityConstraintViolationException("Cannot update data")

        return db_data
    

    def delete_data_by_id(self, data_id: int) -> bool:
        """
        Delete a data by id.
        """
        db_data = self.db.query(models.Data).filter(models.Data.id == data_id).first()
        if not db_data:
            return False
        
        try:
            self.db.delete(db_data)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise IntegrityConstraintViolationException("Cannot delete data")
        
        return True


def get_data_repo(db: Session = Depends(get_db)) -> DataRepository:
    return DataRepository(db)
