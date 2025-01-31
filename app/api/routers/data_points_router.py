from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.schemas import data_point_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.data_point_service import DataPointService, get_data_point_service
from app.core.services.data_service import DataService, get_data_service
from app.core.services.exceptions import IntegrityConstraintViolationException, NotFoundException, ValidationException
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/datas/{data_id}/data_points", tags=["Data Points"])


@router.post("/", response_model=data_point_schema.DataPointResponse, status_code=status.HTTP_201_CREATED)
def add_data_point_endpoint(
    data_id: int,
    data_point_create: data_point_schema.DataPointCreate, 
    data_point_service: DataPointService = Depends(get_data_point_service),
    ):
    """
    Create a data point.
    """
    if not data_id == data_point_create.data_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data id mismatch")
    
    try:
        data_point = data_point_service.add_data_point(data_point_create)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return data_point


@router.get("/", response_model=PaginatedResponse[data_point_schema.DataPointResponse])
def list_data_points_endpoint(
    data_id: int, 
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    data_point_service: DataPointService = Depends(get_data_point_service),
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Get all data points for a data.
    """
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    context = PaginationContext(limit=limit, offset=offset)
    
    paged_response = data_point_service.get_data_points(context, data_id)
    return paged_response


@router.get("/{data_point_id}", response_model=data_point_schema.DataPointResponse)
def get_data_point_endpoint(
    data_id: int,
    data_point_id: int, 
    data_point_service: DataPointService = Depends(get_data_point_service),
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Get a data point.
    """
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    data_point = data_point_service.get_data_point_by_id(data_point_id)
    if not data_point:
        raise HTTPException(status_code=404, detail="Data point not found")
    return data_point


@router.delete("/{data_point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_point_endpoint(
    data_id: int,
    data_point_id: int, 
    data_point_service: DataPointService = Depends(get_data_point_service),
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Delete a data point.
    """
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    success = data_point_service.delete_data_point_by_id(data_point_id)
    if not success:
        raise HTTPException(status_code=404, detail="Data point not found")
    return
