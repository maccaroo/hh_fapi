from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import data_meta_schema
from app.core.services.data_meta_service import DataMetaService, get_data_meta_service
from app.core.services.data_service import DataService, get_data_service
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.utils.pagination import PaginationContext

router = APIRouter(prefix="/datas/{data_id}/metas", tags=["Data Metas"])


@router.post("/", response_model=data_meta_schema.DataMetaResponse, status_code=status.HTTP_201_CREATED)
def create_data_meta_endpoint(
    data_id: int, 
    data_meta_create: data_meta_schema.DataMetaCreate,
    data_service: DataService = Depends(get_data_service),
    data_meta_service: DataMetaService = Depends(get_data_meta_service)
    ):
    """
    Create a data meta.
    """
    if not data_id == data_meta_create.data_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data id mismatch")
    
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    try:
        data_meta_res = data_meta_service.create_data_meta(data_meta_create)
    except IntegrityConstraintViolationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex))
    
    return data_meta_res


@router.get("/", response_model=PaginatedResponse[data_meta_schema.DataMetaResponse])
def list_data_metas_endpoint(
    data_id: int, 
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    data_meta_service: DataMetaService = Depends(get_data_meta_service),
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Get all data metas for a data.
    """
    try:
        data = data_service.get_data_by_id(data_id)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

        context = PaginationContext(limit=limit, offset=offset)
        
        paged_response = data_meta_service.get_data_metas_by_data_id(context, data_id)
        return paged_response
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


@router.get("/{meta_id}", response_model=data_meta_schema.DataMetaResponse)
def get_data_meta_endpoint(
    data_id: int, 
    meta_id: int, 
    data_meta_service: DataMetaService = Depends(get_data_meta_service),
    data_service: DataService = Depends(get_data_service)
    ):
    """
    Get a data meta.
    """
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    data_meta = data_meta_service.get_data_meta_by_data_id_and_meta_id(data_id, meta_id)
    if not data_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data meta not found")
    return data_meta


@router.put("/{meta_id}", response_model=data_meta_schema.DataMetaResponse)
def update_data_meta_endpoint(
    data_id: int, 
    meta_id: int, 
    data_meta_update: data_meta_schema.DataMetaUpdate,
    data_service: DataService = Depends(get_data_service),
    data_meta_service: DataMetaService = Depends(get_data_meta_service)
    ):
    """
    Update a data meta.
    """
    if not data_id == data_meta_update.data_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data id mismatch")
    elif not meta_id == data_meta_update.meta_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Meta id mismatch")
    
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    try:
        data_meta = data_meta_service.update_data_meta(data_meta_update)
    except data_meta_service.IntegrityConstraintViolationException as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex))

    if not data_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data meta not found")
    return data_meta


@router.delete("/{meta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_meta_endpoint(
    data_id: int, 
    meta_id: int,
    data_service: DataService = Depends(get_data_service),
    data_meta_service: DataMetaService = Depends(get_data_meta_service)
    ):
    """
    Delete a data meta.
    """
    data = data_service.get_data_by_id(data_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    success = data_meta_service.delete_data_meta(data_id, meta_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data meta not found")
    return
