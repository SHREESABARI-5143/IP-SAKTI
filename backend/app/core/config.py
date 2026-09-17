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
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    OLLAMA_TIMEOUT_SECONDS: float = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60.0"))
    OLLAMA_KEEP_ALIVE: str = os.getenv("OLLAMA_KEEP_ALIVE", "15m")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    LLM_NUM_CTX: int = int(os.getenv("LLM_NUM_CTX", "4096"))
    LLM_NUM_PREDICT: int = int(os.getenv("LLM_NUM_PREDICT", "512"))
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "qwen2.5:3b")
    LLM_MODEL_BY_LOCALE: dict = {
        "en": os.getenv("LLM_MODEL_EN", "qwen2.5:3b"),
        "hi": os.getenv("LLM_MODEL_HI", "qwen2.5:3b"),
        "ta": os.getenv("LLM_MODEL_TA", "qwen2.5:3b")
    }
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")

    # Retrieval & Confidence Thresholds
    RRF_K: int = int(os.getenv("RRF_K", "60"))
    RRF_DEFAULT_MIN_SCORE: float = float(os.getenv("RRF_DEFAULT_MIN_SCORE", "0.22"))
    RRF_FALLBACK_MIN_SCORE: float = float(os.getenv("RRF_FALLBACK_MIN_SCORE", "0.18"))
    INTENT_EVIDENCE_DIRECT_THRESHOLD: float = float(os.getenv("INTENT_EVIDENCE_DIRECT_THRESHOLD", "0.70"))
    INTENT_EVIDENCE_CONTEXTUAL_THRESHOLD: float = float(os.getenv("INTENT_EVIDENCE_CONTEXTUAL_THRESHOLD", "0.85"))
    CONFIDENCE_ABSTAIN_THRESHOLD: float = float(os.getenv("CONFIDENCE_ABSTAIN_THRESHOLD", "0.65"))
    CONFIDENCE_ESCALATE_THRESHOLD: float = float(os.getenv("CONFIDENCE_ESCALATE_THRESHOLD", "0.55"))
    LLM_TOP_P: float = float(os.getenv("LLM_TOP_P", "0.9"))
    
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
