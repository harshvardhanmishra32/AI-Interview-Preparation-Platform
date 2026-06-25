"""Application configuration using pydantic-settings."""
import os
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
IS_VERCEL = os.getenv("VERCEL") == "1"

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Interview Preparation Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Auth
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database
    DATABASE_URL: str = "sqlite:////tmp/interview_assistant.db" if IS_VERCEL else "sqlite:///./interview_assistant.db"
    
    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # ChromaDB
    CHROMA_DB_PATH: str = "/tmp/chroma_db" if IS_VERCEL else str(ROOT_DIR / "chroma_db")
    
    # File Upload
    UPLOAD_DIR: str = "/tmp/uploads" if IS_VERCEL else str(ROOT_DIR / "uploads")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    FRONTEND_ORIGINS: str = "http://localhost:8501,http://127.0.0.1:8501,http://localhost:3000"
    
    # GitHub
    GITHUB_TOKEN: str = ""  # Optional, for higher rate limits

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value: Any) -> bool:
        if isinstance(value, str) and value.lower() in {"release", "prod", "production"}:
            return False
        return value
    
    class Config:
        env_file = ROOT_DIR / ".env"
        case_sensitive = True

settings = Settings()
