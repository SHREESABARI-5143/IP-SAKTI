import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "IP-SAKTI Sahayak Backend API"
    VERSION: str = "2.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # AI / LLM Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    
    # Defaults
    DEFAULT_JURISDICTION: str = "india"
    DEFAULT_LANGUAGE: str = "en"

    # Vector DB
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_URL: str = "http://localhost:6333"

    # Relational DB
    DATABASE_URL: str = "sqlite+aiosqlite:///./ipsakti.db"

    # Corpus Paths
    CORPUS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "corpus")

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
        extra = "ignore"

settings = Settings()
