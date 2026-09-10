import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "IP-SAKTI Sahayak"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ipsakti-sahayak-super-secret-production-key-change-in-prod-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database (PostgreSQL 16 with pgvector in Production/Docker; SQLite for zero-dependency local testing)
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "sqlite+aiosqlite:///./ipsakti.db"
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL") or (
        DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", "") if "sqlite" not in DATABASE_URL else "sqlite:///./ipsakti.db"
    )
    VECTOR_BACKEND: str = os.getenv("VECTOR_BACKEND", "pgvector")
    
    # LLM Settings (Local Open Source & Offline Zero-API Fallback)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")  # ollama, deterministic, vllm
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
    OLLAMA_TIMEOUT_SECONDS: float = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60.0"))
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama3.1:latest")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*"
    ]
    
    # Upload limits
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".csv"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
