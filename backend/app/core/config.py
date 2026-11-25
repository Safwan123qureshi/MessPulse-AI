from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "MessPulse AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MessPulse AI"

    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production-please-make-it-long-and-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite:///./messpulse.db"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # OCR
    TESSERACT_CMD: str = "tesseract"
    OCR_ENABLED: bool = True

    # Currency
    DEFAULT_CURRENCY: str = "PKR"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()