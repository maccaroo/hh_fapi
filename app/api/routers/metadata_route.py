from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.persistence.db.database import get_db
from app.api.schemas.pagination_schema import PaginatedResponse
from app.utils.auth import get_current_user
import app.logic.services.metadata_service as metadata_service
from app.api.schemas import metadata_schema
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/metadatas", tags=["Metadatas"])


@router.post("/", response_model=metadata_schema.MetadataResponse, status_code=status.HTTP_201_CREATED)
def create_metadata_endpoint(metadata_create: metadata_schema.MetadataCreate, db: Session = Depends(get_db)):
    """
    Create a metadata.
    """
    try:
        metadata = metadata_service.create_metadata(db, metadata_create)
    except metadata_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return metadata


@router.get("/", response_model=PaginatedResponse[metadata_schema.MetadataResponse])
def list_metadatas_endpoint(
    search: str = Query(None, description="Search by name"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
    ):
    """
    Get all metadatas.
    """
    context = PaginationContext(limit=limit, offset=offset, search=search, db=db)
    
    paged_response = metadata_service.get_all_metadatas(context)
    return paged_response


@router.get("/{metadata_id}", response_model=metadata_schema.MetadataResponse)
def get_metadata_endpoint(metadata_id: int, db: Session = Depends(get_db)):
    """ 
    Get a metadata.
    """
    metadata = metadata_service.get_metadata_by_id(db, metadata_id)
    if not metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metadata not found")
    return metadata


@router.put("/{metadata_id}", response_model=metadata_schema.MetadataResponse)
def update_metadata_endpoint(metadata_id: int, metadata_update: metadata_schema.MetadataUpdate, db: Session = Depends(get_db)):
    """
    Update a metadata.
    """
    try:
        updated_metadata = metadata_service.update_metadata_by_id(db, metadata_id, metadata_update)
    except metadata_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    if not updated_metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metadata not found")
    return updated_metadata


@router.delete("/{metadata_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_metadata_endpoint(metadata_id: int, db: Session = Depends(get_db)):
    """
    Delete a metadata.
    """
    try:
        success = metadata_service.delete_metadata_by_id(db, metadata_id)
        if not success: 
            raise HTTPException(status_code=404, detail="Metadata not found")
    except metadata_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return