import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "IP-SAKTI Sahayak Backend API"
    VERSION: str = "2.0.0"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # AI / LLM Configuration
    # LLM_PROVIDER can be 'groq' (Serverless Llama 3.3), 'gemini', or 'ollama'
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")
    
    # Serverless Groq LLM Configuration (Llama 3.3 70B - High speed, 100% Free tier)
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Local Ollama LLM Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")
    
    # Cloud Gemini Configuration (Optional / Fallback)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    
    # Defaults
    DEFAULT_JURISDICTION: str = "india"
    DEFAULT_LANGUAGE: str = "en"

    # Vector DB
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")

    # Relational DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./ipsakti.db")

    # Corpus Paths
    CORPUS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "corpus")

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
        extra = "ignore"

settings = Settings()
