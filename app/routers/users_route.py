from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.user_schema as user_schema
from app.services import user_service
from app.utils.database import get_db


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


@router.get("/{user_id}", response_model=user_schema.UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
