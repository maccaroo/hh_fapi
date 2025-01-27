from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import app.utils.auth as auth_utils
from app.core.services.user_service import UserService, get_user_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    user_service: UserService = Depends(get_user_service),
    ):
    """
    Login a user.
    """
    user = user_service.get_user_by_email(user_credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not auth_utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth_utils.create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
        }