from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import app.db.models as models
from app.schemas.pagination_schema import PaginatedResponse
import app.schemas.user_schema as user_schema
from app.services.exceptions import IntegrityConstraintViolationException
from app.utils.auth import hash_password
from app.utils.pagination import PaginationContext, paginate_query


def create_user(db: Session, user_create: user_schema.UserCreate) -> models.User:
    """
    Create a user.
    """
    hashed_password = hash_password(user_create.password)
    user_create.password = hashed_password

    db_user = models.User(**user_create.model_dump())

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise IntegrityConstraintViolationException("User already exists")

    return db_user


def get_all_users(context: PaginationContext) -> PaginatedResponse[user_schema.UserResponse]:
    """
    Get all users.
    """
    query = context.db.query(models.User)

    if context.search:
        query = query.filter(models.User.username.contains(context.search))

    results = paginate_query(query, context.limit, context.offset)

    return results


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    """
    Get a user by id.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: EmailStr) -> models.User | None:
    """
    Get a user by email.
    """
    return db.query(models.User).filter(models.User.email == email).first()
