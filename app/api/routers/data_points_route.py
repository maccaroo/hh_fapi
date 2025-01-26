from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import data_point_schema
from app.core.services.data_point_service import DataPointService, get_data_point_service


router = APIRouter(prefix="/data_points", tags=["Data Points"])


@router.post("/", response_model=data_point_schema.DataPointResponse, status_code=status.HTTP_201_CREATED)
def add_data_point_endpoint(
    data_point_create: data_point_schema.DataPointCreate, 
    data_point_service: DataPointService = Depends(get_data_point_service),
    ):
    """
    Create a data point.
    """
    try:
        data_point = data_point_service.add_data_point(data_point_create)
    except data_point_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return data_point


@router.get("/{data_point_id}", response_model=data_point_schema.DataPointResponse)
def get_data_point_endpoint(
    data_point_id: int, 
    data_point_service: DataPointService = Depends(get_data_point_service),
    ):
    """
    Get a data point.
    """
    data_point = data_point_service.get_data_point_by_id(data_point_id)
    if not data_point:
        raise HTTPException(status_code=404, detail="Data point not found")
    return data_point


@router.delete("/{data_point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_point_endpoint(
    data_point_id: int, 
    data_point_service: DataPointService = Depends(get_data_point_service),
    ):
    """
    Delete a data point.
    """
    success = data_point_service.delete_data_point_by_id(data_point_id)
    if not success:
        raise HTTPException(status_code=404, detail="Data point not found")
    return
