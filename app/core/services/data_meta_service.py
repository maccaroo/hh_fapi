from fastapi import Depends

from app.api.schemas import data_meta_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.persistence.repositories.data_meta_repo import DataMetaRepository, get_data_meta_repo
from app.utils.pagination import PaginationContext


class DataMetaService:
    """
    Data meta service.
    """

    def __init__(
            self,
            data_meta_repo: DataMetaRepository = Depends(get_data_meta_repo)
            ):
        self.data_meta_repo = data_meta_repo


    def create_data_meta(
            self, 
            data_meta_create: data_meta_schema.DataMetaCreate
            ) -> data_meta_schema.DataMetaResponse:
        """
        Create a data meta.
        """
        return self.data_meta_repo.create_data_meta(data_meta_create)


    def get_data_metas_by_data_id(
            self, 
            context: PaginationContext, 
            data_id: int
            ) -> PaginatedResponse[data_meta_schema.DataMetaResponse]:
        """
        Get a data meta by data id.
        """
        return self.data_meta_repo.get_data_metas_by_data_id(context, data_id)


    def get_data_meta_by_data_id_and_meta_id(
            self, 
            data_id: int, 
            meta_id: int
            ) -> data_meta_schema.DataMetaResponse | None:
        """
        Get a data meta by data id and meta id.
        """
        return self.data_meta_repo.get_data_meta_by_data_id_and_meta_id(data_id, meta_id)
    

    def update_data_meta(
            self, 
            data_meta_update: data_meta_schema.DataMetaUpdate
            ) -> data_meta_schema.DataMetaResponse | None:
        """
        Update a data meta by id.
        """
        return self.data_meta_repo.update_data_meta_by_id(data_meta_update.data_id, data_meta_update)


    def delete_data_meta(
            self, 
            data_id:int, 
            meta_id: int
            ) -> bool:
        """
        Delete a data meta by data id and meta id.
        """
        return self.data_meta_repo.delete_data_meta(data_id, meta_id)


def get_data_meta_service(data_meta_repo: DataMetaRepository = Depends(get_data_meta_repo)):
    return DataMetaService(data_meta_repo)
