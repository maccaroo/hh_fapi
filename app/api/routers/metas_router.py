from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.services.exceptions import IntegrityConstraintViolationException
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.meta_service import MetaService, get_meta_service
from app.api.schemas import meta_schema
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/metas", tags=["Metas"])


@router.post("/", response_model=meta_schema.MetaResponse, status_code=status.HTTP_201_CREATED)
def create_meta_endpoint(
    meta_create: meta_schema.MetaCreate, 
    meta_service: MetaService = Depends(get_meta_service)
    ):
    """
    Create a meta.
    """
    try:
        meta = meta_service.create_meta(meta_create)
    except IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return meta


@router.get("/", response_model=PaginatedResponse[meta_schema.MetaResponse])
def list_metas_endpoint(
    search: str = Query(None, description="Search"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    meta_service: MetaService = Depends(get_meta_service)
    ):
    """
    Get metas.
    """
    context = PaginationContext(limit=limit, offset=offset, search=search)
    
    paged_response = meta_service.get_metas(context)
    return paged_response


@router.get("/{meta_id}", response_model=meta_schema.MetaResponse)
def get_meta_endpoint(
    meta_id: int, 
    meta_service: MetaService = Depends(get_meta_service)
    ):
    """ 
    Get a meta.
    """
    meta = meta_service.get_meta_by_id(meta_id)
    if not meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta not found")
    return meta


@router.put("/{meta_id}", response_model=meta_schema.MetaResponse)
def update_meta_endpoint(
    meta_id: int, 
    meta_update: meta_schema.MetaUpdate, 
    meta_service: MetaService = Depends(get_meta_service)
    ):
    """
    Update a meta.
    """
    try:
        updated_meta = meta_service.update_meta_by_id(meta_id, meta_update)
    except meta_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    if not updated_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta not found")
    return updated_meta


@router.delete("/{meta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meta_endpoint(
    meta_id: int, 
    meta_service: MetaService = Depends(get_meta_service)
    ):
    """
    Delete a meta.
    """
    try:
        success = meta_service.delete_meta_by_id(meta_id)
        if not success: 
            raise HTTPException(status_code=404, detail="Meta not found")
    except meta_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return
