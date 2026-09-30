import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "IP-SAKTI Sahayak Backend API"
    VERSION: str = "2.0.0"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # 100% Local LLM Configuration (Private & Offline via Ollama)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")
    VECTOR_DIMENSION: int = int(os.getenv("VECTOR_DIMENSION", "768"))
    
    # Defaults
    DEFAULT_JURISDICTION: str = "india"
    DEFAULT_LANGUAGE: str = "en"

    # PostgreSQL + pgvector Database URL (Consolidated Single DB)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://ipsakti:ipsakti_secure_2026@localhost:5432/ipsakti"
    )

    # Corpus Paths
    CORPUS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "corpus")

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
        extra = "ignore"

settings = Settings()


