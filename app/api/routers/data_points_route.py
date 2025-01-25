from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas import data_point_schema
from app.logic.services import data_point_service
from app.persistence.db.database import get_db


router = APIRouter(prefix="/data_points", tags=["Data Points"])


### Data points endpoints

@router.post("/", response_model=data_point_schema.DataPointResponse, status_code=status.HTTP_201_CREATED)
def add_data_point_endpoint(data_point_create: data_point_schema.DataPointCreate, db: Session = Depends(get_db)):
    """
    Create a data point.
    """
    try:
        data_point = data_point_service.add_data_point(db, data_point_create)
    except data_point_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return data_point


@router.get("/{data_point_id}", response_model=data_point_schema.DataPointResponse)
def get_data_point_endpoint(data_point_id: int, db: Session = Depends(get_db)):
    """
    Get a data point.
    """
    data_point = data_point_service.get_data_point_by_id(db, data_point_id)
    if not data_point:
        raise HTTPException(status_code=404, detail="Data point not found")
    return data_point


@router.delete("/{data_point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_point_endpoint(data_point_id: int, db: Session = Depends(get_db)):
    """
    Delete a data point.
    """
    success = data_point_service.delete_data_point_by_id(db, data_point_id)
    if not success:
        raise HTTPException(status_code=404, detail="Data point not found")
    return
