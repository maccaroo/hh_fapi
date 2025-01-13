from app.db.database import SessionLocal
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    """
    Get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    """
    Hash a password.
    """
    return pwd_context.hash(password)