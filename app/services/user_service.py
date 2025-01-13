from sqlalchemy.orm import Session
import app.db.models as models
import app.schemas.user_schema as user_schema
from app.utils.dependencies import hash_password


def create_user(db: Session, user_create: user_schema.UserCreate) -> models.User:
    """
    Create a user.
    """
    hashed_password = hash_password(user_create.password)
    user_create.password = hashed_password

    db_user = models.User(**user_create.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    """
    Get a user by id.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()
