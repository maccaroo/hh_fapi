from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import data_meta_schema, data_point_schema, data_schema
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.core.services import data_meta_service, data_point_service, data_service
from app.persistence.database import get_db
from app.utils.auth import get_current_user
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/datas", tags=["Datas"])


### Datas endpoints

@router.post("/", response_model=data_schema.DataResponse, status_code=status.HTTP_201_CREATED)
def create_data_endpoint(data_create: data_schema.DataCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a data.
    """
    try:
        data = data_service.create_data(db, data_create, current_user.id)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return data


@router.get("/", response_model=PaginatedResponse[data_schema.DataResponse])
def list_datas_endpoint(
    search: str = Query(None, description="Search"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
    ):
    """
    Get all datas.
    """
    context = PaginationContext(limit=limit, offset=offset, search=search, db=db)
    
    paged_response = data_service.get_all_datas(context)
    return paged_response


@router.get("/{data_id}", response_model=data_schema.DataResponse)
def get_data_endpoint(data_id: int, db: Session = Depends(get_db)):
    """
    Get a data.
    """
    data = data_service.get_data_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


@router.put("/{data_id}", response_model=data_schema.DataResponse)
def update_data_endpoint(data_id: int, data_update: data_schema.DataUpdate, db: Session = Depends(get_db)):
    """
    Update a data.
    """
    try:
        updated_data = data_service.update_data_by_id(db, data_id, data_update)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    if not updated_data:
        raise HTTPException(status_code=404, detail="Data not found")
    return updated_data


@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_endpoint(data_id: int, db: Session = Depends(get_db)):
    """
    Delete a data.
    """
    try:
        success = data_service.delete_data_by_id(db, data_id)
        if not success:
            raise HTTPException(status_code=404, detail="Data not found")
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return


### Data points endpoints

@router.get("/{data_id}/data_points/", response_model=PaginatedResponse[data_point_schema.DataPointResponse])
def list_data_points_endpoint(
    data_id: int, 
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)):
    """
    Get all data points for a data.
    """
    context = PaginationContext(limit=limit, offset=offset, db=db)

    data = data_service.get_data_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    paged_response = data_point_service.get_data_points(context, data_id)
    return paged_response


### Meta endpoints

@router.post("/{data_id}/metas/", response_model=data_meta_schema.DataMetaResponse, status_code=status.HTTP_201_CREATED)
def create_data_meta_endpoint(data_id: int, data_meta_create: data_meta_schema.DataMetaCreate, db: Session = Depends(get_db)):
    """
    Create a data meta.
    """
    if not data_id == data_meta_create.data_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data id mismatch")

    try:
        data_meta_res = data_meta_service.create_data_meta(db, data_meta_create)
    except data_meta_service.IntegrityConstraintViolationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex))
    
    return data_meta_res


@router.get("/{data_id}/metas/", response_model=PaginatedResponse[data_meta_schema.DataMetaResponse])
def list_data_metas_endpoint(
    data_id: int, 
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)):
    """
    Get all data metas for a data.
    """
    context = PaginationContext(limit=limit, offset=offset, db=db)

    data = data_service.get_data_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    paged_response = data_meta_service.get_data_meta_by_data_id(context, data_id)
    return paged_response


@router.get("/{data_id}/metas/{meta_id}", response_model=data_meta_schema.DataMetaResponse)
def get_data_meta_endpoint(data_id: int, meta_id: int, db: Session = Depends(get_db)):
    """
    Get a data meta.
    """
    data_meta = data_meta_service.get_data_meta_by_data_id_and_meta_id(db, data_id, meta_id)
    if not data_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data meta not found")
    return data_meta


@router.put("/{data_id}/metas/{meta_id}", response_model=data_meta_schema.DataMetaResponse)
def update_data_meta_endpoint(data_id: int, meta_id: int, data_meta_update: data_meta_schema.DataMetaUpdate, db: Session = Depends(get_db)):
    """
    Update a data meta.
    """
    if not data_id == data_meta_update.data_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data id mismatch")
    elif not meta_id == data_meta_update.meta_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Meta id mismatch")

    try:
        data_meta = data_meta_service.update_data_meta(db, data_meta_update)
    except data_meta_service.IntegrityConstraintViolationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    if not data_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data meta not found")
    return data_meta


@router.delete("/{data_id}/metas/{meta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_meta_endpoint(data_id: int, meta_id: int, db: Session = Depends(get_db)):
    """
    Delete a data meta.
    """
    success = data_meta_service.delete_data_meta(db, data_id, meta_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data meta not found")
    return