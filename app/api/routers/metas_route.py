from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.persistence.db.database import get_db
from app.api.schemas.pagination_schema import PaginatedResponse
from app.utils.auth import get_current_user
from app.logic.services import meta_service
from app.api.schemas import meta_schema
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/metas", tags=["Metas"])


@router.post("/", response_model=meta_schema.MetaResponse, status_code=status.HTTP_201_CREATED)
def create_meta_endpoint(meta_create: meta_schema.MetaCreate, db: Session = Depends(get_db)):
    """
    Create a meta.
    """
    try:
        meta = meta_service.create_meta(db, meta_create)
    except meta_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return meta


@router.get("/", response_model=PaginatedResponse[meta_schema.MetaResponse])
def list_metas_endpoint(
    search: str = Query(None, description="Search"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
    ):
    """
    Get all metas.
    """
    context = PaginationContext(limit=limit, offset=offset, search=search, db=db)
    
    paged_response = meta_service.get_all_metas(context)
    return paged_response


@router.get("/{meta_id}", response_model=meta_schema.MetaResponse)
def get_meta_endpoint(meta_id: int, db: Session = Depends(get_db)):
    """ 
    Get a meta.
    """
    meta = meta_service.get_meta_by_id(db, meta_id)
    if not meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta not found")
    return meta


@router.put("/{meta_id}", response_model=meta_schema.MetaResponse)
def update_meta_endpoint(meta_id: int, meta_update: meta_schema.MetaUpdate, db: Session = Depends(get_db)):
    """
    Update a meta.
    """
    try:
        updated_meta = meta_service.update_meta_by_id(db, meta_id, meta_update)
    except meta_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    if not updated_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta not found")
    return updated_meta


@router.delete("/{meta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meta_endpoint(meta_id: int, db: Session = Depends(get_db)):
    """
    Delete a meta.
    """
    try:
        success = meta_service.delete_meta_by_id(db, meta_id)
        if not success: 
            raise HTTPException(status_code=404, detail="Meta not found")
    except meta_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return