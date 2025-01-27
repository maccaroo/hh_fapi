from fastapi import Depends

from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import data_schema
from app.persistence.repositories.data_repo import DataRepository, get_data_repo
from app.utils.pagination import PaginationContext


class DataService:
    """
    Data service.
    """

    def __init__(
            self,
            data_repo: DataRepository = Depends(get_data_repo)
            ):
        self.data_repo = data_repo


    def add_data(
            self, 
            data_create: data_schema.DataCreate,
            user_id: int
            ) -> data_schema.DataResponse:
        """
        Add a data.
        """
        return self.data_repo.add_data(data_create, user_id)


    def get_datas(
            self, 
            context: PaginationContext
            ) -> PaginatedResponse[data_schema.DataResponse]:
        """
        Get all datas.
        """
        return self.data_repo.get_datas(context)


    def get_data_by_id(
            self, 
            data_id: int
            ) -> data_schema.DataResponse | None:
        """
        Get a data by id.
        """
        return self.data_repo.get_data_by_id(data_id)


    def update_data_by_id(
            self, 
            data_id: int, 
            data_update: data_schema.DataUpdate
            ) -> data_schema.DataResponse | None:
        """
        Update a data by id.
        """
        return self.data_repo.update_data_by_id(data_id, data_update)


    def delete_data_by_id(
            self, 
            data_id: int
            ) -> bool:
        """
        Delete a data by id.
        """
        return self.data_repo.delete_data_by_id(data_id)
    

def get_data_service(data_repo: DataRepository = Depends(get_data_repo)) -> DataService:
    return DataService(data_repo)
