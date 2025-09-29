import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    # Add more settings as needed

settings = Settings() 