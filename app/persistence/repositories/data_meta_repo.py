from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.schemas import data_meta_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.persistence import models
from app.persistence.database import get_db
from app.utils.pagination import PaginationContext, paginate_query


class DataMetaRepository:
    """
    Data meta repository.
    """

    def __init__(
            self, 
            db: Session):
        self.db = db
    

    def create_data_meta(
            self, 
            data_meta_create: data_meta_schema.DataMetaCreate
            ) -> models.DataMeta:
        """
        Create a data meta.
        """
        # Validate the value is compatible with the meta type
        db_meta = self.db.query(models.Meta).filter(models.Meta.id == data_meta_create.meta_id).first()
        if not db_meta:
            raise IntegrityConstraintViolationException("Meta not found")
        
        # TODO: Validate the value is compatible with the meta type

        db_data_meta = models.DataMeta(**data_meta_create.model_dump())

        try:
            self.db.add(db_data_meta)
            self.db.commit()
            self.db.refresh(db_data_meta)
        except IntegrityError as ex:
            self.db.rollback()
            if "UNIQUE constraint failed:" in str(ex):
                raise IntegrityConstraintViolationException("Data meta already exists")
            else:
                raise IntegrityConstraintViolationException(f"Cannot create data meta")
        
        return db_data_meta
    

    def get_data_metas_by_data_id(
            self, 
            context: PaginationContext, 
            data_id: int
            ) -> PaginatedResponse[data_meta_schema.DataMetaResponse]:
        """
        Get a data meta by data id.
        """
        query = self.db.query(models.DataMeta).filter(models.DataMeta.data_id == data_id)

        if context.search:
            query = query.filter(models.DataMeta.value.contains(context.search))

        results = paginate_query(query, context.limit, context.offset)

        return results
    

    def get_data_meta_by_data_id_and_meta_id(
            self, 
            data_id: int, 
            meta_id: int
            ) -> models.DataMeta | None:
        """
        Get a data meta by data id and meta id.
        """
        return self.db.query(models.DataMeta).filter(models.DataMeta.data_id == data_id, models.DataMeta.meta_id == meta_id).first()


    def update_data_meta_by_id(
            self, 
            data_id: int, 
            data_meta_update: data_meta_schema.DataMetaUpdate
            ) -> models.DataMeta | None:
        """
        Update a data meta by id.
        """
        db_data_meta = self.db.query(models.DataMeta).filter(models.DataMeta.data_id == data_id, models.DataMeta.meta_id == data_meta_update.meta_id).first()
        if not db_data_meta:
            return None
        
        try:
            self.db.query(models.DataMeta).filter(models.DataMeta.data_id == data_id, models.DataMeta.meta_id == data_meta_update.meta_id).update(data_meta_update.model_dump())
            self.db.commit()
            self.db.refresh(db_data_meta)
        except IntegrityError as ex:
            self.db.rollback()
            if "UNIQUE constraint failed:" in str(ex):
                raise IntegrityConstraintViolationException("Data meta already exists")
            else:
                raise IntegrityConstraintViolationException(f"Cannot update data meta")

        return db_data_meta
    

    def delete_data_meta(
            self, 
            data_id:int, 
            meta_id: int
            ) -> bool:
        """
        Delete a data meta by data id and meta id.
        """
        db_data_meta = self.db.query(models.DataMeta).filter(models.DataMeta.data_id == data_id, models.DataMeta.meta_id == meta_id).first()
        if not db_data_meta:
            return False
        
        try:
            self.db.delete(db_data_meta)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise IntegrityConstraintViolationException("Cannot delete data meta")
        
        return True


def get_data_meta_repo(db: Session = Depends(get_db)) -> DataMetaRepository:
    return DataMetaRepository(db)
