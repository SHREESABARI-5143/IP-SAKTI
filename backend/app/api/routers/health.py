from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "mode": "real_data_qdrant_gemini"
    }

@router.get("/")
def root_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}
