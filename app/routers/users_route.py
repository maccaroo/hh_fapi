from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.schemas.pagination_schema import PaginatedResponse
import app.schemas.user_schema as user_schema
from app.services import user_service
from app.db.database import get_db
from app.utils.pagination import PaginationContext


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Create a user.
    """
    try:
        user = user_service.create_user(db, user_create)
    except user_service.IntegrityConstraintViolationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    return user


@router.get("/", response_model=PaginatedResponse[user_schema.UserResponse])
def get_user_endpoint(
    search: str = Query(None, description="Search by name"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
    ):
    """
    Get all users.
    """
    context = PaginationContext(limit=limit, offset=offset, search=search, db=db)

    paged_response = user_service.get_all_users(context)
    return paged_response


@router.get("/{user_id}", response_model=user_schema.UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
