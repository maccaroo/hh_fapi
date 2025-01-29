from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import data_schema
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.core.services.data_service import DataService, get_data_service
from app.utils.auth import get_current_user_id
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/datas", tags=["Datas"])


@router.post("/", response_model=data_schema.DataResponse, status_code=status.HTTP_201_CREATED)
def create_data_endpoint(
    data_create: data_schema.DataCreate, 
    data_service: DataService = Depends(get_data_service),
    current_user_id: dict = Depends(get_current_user_id)
    ):
    """
    Create a data.
    """
    try:
        data = data_service.add_data(data_create, current_user_id)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return data


@router.get("/", response_model=PaginatedResponse[data_schema.DataResponse])
def list_datas_endpoint(
    search: str = Query(None, description="Search"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Get all datas.
    """
    context = PaginationContext(limit=limit, offset=offset, search=search)
    
    paged_response = data_service.get_datas(context)
    return paged_response


@router.get("/{data_id}", response_model=data_schema.DataResponse)
def get_data_endpoint(
    data_id: int, 
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Get a data.
    """
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


@router.put("/{data_id}", response_model=data_schema.DataResponse)
def update_data_endpoint(
    data_id: int, 
    data_update: data_schema.DataUpdate, 
    data_service: DataService = Depends(get_data_service),
    ):
    """
    Update a data.
    """
    try:
        updated_data = data_service.update_data_by_id(data_id, data_update)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    if not updated_data:
        raise HTTPException(status_code=404, detail="Data not found")
    return updated_data


@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_endpoint(
    data_id: int, 
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Delete a data.
    """
    try:
        success = data_service.delete_data_by_id(data_id)
        if not success:
            raise HTTPException(status_code=404, detail="Data not found")
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return
