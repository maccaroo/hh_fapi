from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.schemas import user_schema
from app.api.schemas.pagination_schema import PaginatedResponse
from app.core.services.exceptions import IntegrityConstraintViolationException
from app.persistence import models
from app.persistence.database import get_db
from app.utils.pagination import PaginationContext, paginate_query


class UserRepository:
    """
    User repository.
    """

    def __init__(
            self, db: Session
            ):
        self.db = db


    def add_user(
            self, 
            user_create: user_schema.UserCreate
            ):
        """
        Add a user.
        """
        user = models.User(**user_create.model_dump())

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError:
            self.db.rollback()
            if "UNIQUE constraint failed:" in str(IntegrityError):
                raise IntegrityConstraintViolationException("User already exists")
            raise IntegrityConstraintViolationException("Cannot add user")

        return user


    def get_users(
            self, 
            context: PaginationContext
            ) -> PaginatedResponse[user_schema.UserResponse]:
        """
        Get users.
        """
        query = self.db.query(models.User)

        if context.search:
            query = query.filter(models.User.username.contains(context.search))

        results = paginate_query(query, context.limit, context.offset)

        return results
    
    def get_user_by_id(
            self, 
            user_id: int
            ) -> user_schema.UserResponse | None:
        """
        Get a user by id.
        """
        return self.db.query(models.User).filter(models.User.id == user_id).first()


    def get_user_by_email(
            self, 
            db: Session, 
            email: EmailStr
            ) -> user_schema.UserResponse | None:
        """
        Get a user by email.
        """
        return self.db.query(models.User).filter(models.User.email == email).first()


    def delete_user_by_id(
            self, 
            user_id: int
            ) -> bool:
        """
        Delete a user by id.
        """
        db_user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()

        return True


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
