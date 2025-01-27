from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.schemas import meta_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.persistence import models
from app.persistence.database import get_db
from app.utils.pagination import PaginationContext, paginate_query


class MetaRepository:
    """
    Meta repository.
    """

    def __init__(
            self, 
            db: Session
            ):
        self.db = db
    

    def create_meta(
            self,
            meta_create: meta_schema.MetaCreate
            ) -> models.Meta:
        """
        Create a meta.
        """
        db_meta = models.Meta(**meta_create.model_dump())

        try:
            self.db.add(db_meta)
            self.db.commit()
            self.db.refresh(db_meta)
        except IntegrityError as ex:
            self.db.rollback()
            if "UNIQUE constraint failed:" in str(ex):
                raise IntegrityConstraintViolationException("Meta already exists")
            elif "check_meta_type_value" in str(ex):
                raise IntegrityConstraintViolationException(f"Invalid value for 'meta_type': {meta_create.meta_type}")
            else:
                raise IntegrityConstraintViolationException(f"Cannot create meta: {ex}")
        
        return db_meta
    

    def get_metas(self, context: PaginationContext) -> PaginatedResponse[meta_schema.MetaResponse]:
        """
        Get metas.
        """
        query = self.db.query(models.Meta)

        if context.search:
            query = query.filter(models.Meta.name.contains(context.search))

        results = paginate_query(query, context.limit, context.offset)

        return results
    

    def get_meta_by_id(self, meta_id: int) -> models.Meta | None:
        """
        Get a meta by id.
        """
        return self.db.query(models.Meta).filter(models.Meta.id == meta_id).first()
    

    def update_meta_by_id(self, meta_id: int, meta_update: meta_schema.MetaUpdate) -> models.Meta | None:
        """
        Update a meta by id.
        """
        db_meta = self.db.query(models.Meta).filter(models.Meta.id == meta_id).first()
        if not db_meta:
            return None
        
        try:
            self.db.query(models.Meta).filter(models.Meta.id == meta_id).update(meta_update.model_dump())
            self.db.commit()
            self.db.refresh(db_meta)
        except IntegrityError:
            self.db.rollback()
            raise IntegrityConstraintViolationException("Cannot update meta")

        return db_meta
    

    def delete_meta_by_id(self, meta_id: int) -> bool:
        """
        Delete a meta by id.
        """
        meta = self.db.query(models.Meta).filter(models.Meta.id == meta_id).first()
        if not meta:
            return False
        
        try:
            self.db.delete(meta)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise IntegrityConstraintViolationException("Cannot delete meta")
        
        return True


def get_meta_repo(db: Session = Depends(get_db)) -> MetaRepository:
    return MetaRepository(db)
