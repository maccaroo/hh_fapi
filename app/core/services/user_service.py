from fastapi import Depends
from pydantic import EmailStr

from app.api.schemas.pagination_schema import PaginatedResponse
from app.api.schemas import user_schema
from app.persistence.repositories.user_repo import UserRepository, get_user_repo
from app.utils.auth import hash_password
from app.utils.pagination import PaginationContext


def get_user_service(user_repo = Depends(get_user_repo)):
    return UserService(user_repo)


class UserService:
    """
    User service.
    """

    def __init__(
            self, 
            user_repo: UserRepository = Depends(get_user_repo)
            ):
        self.user_repo = user_repo


    def add_user(
            self, 
            user_create: user_schema.UserCreate
            ) -> user_schema.UserResponse:
        """
        Add a user.
        """
        hashed_password = hash_password(user_create.password)
        user_create.password = hashed_password

        created_user = self.user_repo.add_user(user_create)

        return created_user


    def get_users(
            self, 
            context: PaginationContext
            ) -> PaginatedResponse[user_schema.UserResponse]:
        """
        Get users.
        """
        return self.user_repo.get_users(context)


    def get_user_by_id(
            self, 
            user_id: int
            ) -> user_schema.UserResponse | None:
        """
        Get a user by id.
        """
        return self.user_repo.get_user_by_id(user_id)


    def get_user_by_email(
            self, 
            email: EmailStr
            ) -> user_schema.UserResponse | None:
        """
        Get a user by email.
        """
        return self.user_repo.get_user_by_email(email)
