from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # Authentication settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Load environment variables from .env
    class Config:
        env_file = ".env"

settings = Settings()
