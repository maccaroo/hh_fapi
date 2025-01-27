from fastapi import Depends

from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import data_point_schema
from app.persistence.repositories.data_point_repo import DataPointRepository, get_data_point_repo
from app.utils.pagination import PaginationContext


class DataPointService:
    """
    Data point service.
    """

    def __init__(
            self, 
            data_point_repo: DataPointRepository = Depends(get_data_point_repo)
            ):
        self.data_point_repo = data_point_repo


    def add_data_point(
            self, 
            data_point_create: data_point_schema.DataPointCreate
            ) -> data_point_schema.DataPointResponse:
        """
        Add a data point.
        """
        created_data_point = self.data_point_repo.add_data_point(data_point_create)

        return created_data_point


    def get_data_points(
            self, 
            context: PaginationContext, 
            data_id: int
            ) -> PaginatedResponse[data_point_schema.DataPointResponse]:
        """
        Get data points for a data.
        """
        return self.data_point_repo.get_data_points(context, data_id)


    def get_data_point_by_id(
            self, 
            data_point_id: int
            ) -> data_point_schema.DataPointResponse | None:
        """
        Get a data point by id.
        """
        return self.data_point_repo.get_data_point_by_id(data_point_id)


    def delete_data_point_by_id(
            self, 
            data_point_id: int
            ) -> bool:
        """
        Delete a data point by id.
        """
        return self.data_point_repo.delete_data_point_by_id(data_point_id)


def get_data_point_service(data_point_repo: DataPointRepository = Depends(get_data_point_repo)) -> DataPointService:
    return DataPointService(data_point_repo)
