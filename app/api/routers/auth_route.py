from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.persistence.db.database import get_db
from app.api.schemas import auth_schema
from app.logic.services import user_service
import app.utils.auth as auth_utils


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login a user.
    """
    user = user_service.get_user_by_email(db, user_credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not auth_utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth_utils.create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
        }