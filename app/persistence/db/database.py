from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.persistence.db.base import Base
from app.config.settings import settings


# Build the DATABASE_URL
DATABASE_URL = f"postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the schema exists
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS hh"))
    conn.commit()

def init_db():
    """
    Initialize the database.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
