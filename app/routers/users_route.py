from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.schemas.user_schema as user_schema
from app.services import user_service
from app.utils.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Create a user.
    """
    user = user_service.create_user(db, user_create)
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
