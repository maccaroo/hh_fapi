from fastapi import Depends

from app.persistence import models
from app.api.schemas import meta_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.persistence.repositories.meta_repo import MetaRepository, get_meta_repo
from app.utils.pagination import PaginationContext


class MetaService:
    """
    Meta service.
    """

    def __init__(
            self,
            meta_repo: MetaRepository = Depends(get_meta_repo)):
        self.meta_repo = meta_repo


    def create_meta(
            self, 
            meta_create: meta_schema.MetaCreate
            ) -> models.Meta:
        """
        Create a meta.
        """
        return self.meta_repo.create_meta(meta_create)


    def get_metas(
            self, 
            context: PaginationContext
            ) -> PaginatedResponse[meta_schema.MetaResponse]:
        """
        Get metas.
        """
        return self.meta_repo.get_metas(context)


    def get_meta_by_id(
            self, 
            meta_id: int
            ) -> meta_schema.MetaResponse | None:
        """
        Get a meta by id.
        """
        return self.meta_repo.get_meta_by_id(meta_id)


    def update_meta_by_id(
            self, 
            meta_id: int, 
            meta_update: meta_schema.MetaUpdate
            ) -> meta_schema.MetaResponse | None:
        """
        Update a meta by id.
        """
        return self.meta_repo.update_meta_by_id(meta_id, meta_update)


    def delete_meta_by_id(
            self, 
            meta_id: int
            ) -> bool:
        """
        Delete a meta by id.
        """
        return self.meta_repo.delete_meta_by_id(meta_id)


def get_meta_service(meta_repo: MetaRepository = Depends(get_meta_repo)):
    return MetaService(meta_repo)
