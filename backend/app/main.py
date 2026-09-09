from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import async_engine, Base
from backend.app.ingestion.seeder import seed_database
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.classify import router as classify_router
from backend.app.api.v1.abs import router as abs_router
from backend.app.api.v1.ip_strategy import router as ip_router
from backend.app.api.v1.products import router as products_router
from backend.app.api.v1.documents import router as documents_router
from backend.app.api.v1.sources import router as sources_router
from backend.app.api.v1.escalations import router as escalations_router
from backend.app.api.v1.admin import router as admin_router
from backend.app.api.v1.evaluation import router as evaluation_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed authoritative corpus
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Seed statutory knowledge
    seed_database()
    yield
    # Shutdown
    await async_engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Multilingual RAG-Based Intellectual Property & Regulatory AI Assistant for Ayurveda",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 Routers
api_v1_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(chat_router, prefix=api_v1_prefix)
app.include_router(classify_router, prefix=api_v1_prefix)
app.include_router(abs_router, prefix=api_v1_prefix)
app.include_router(ip_router, prefix=api_v1_prefix)
app.include_router(products_router, prefix=api_v1_prefix)
app.include_router(documents_router, prefix=api_v1_prefix)
app.include_router(sources_router, prefix=api_v1_prefix)
app.include_router(escalations_router, prefix=api_v1_prefix)
app.include_router(admin_router, prefix=api_v1_prefix)
app.include_router(evaluation_router, prefix=api_v1_prefix)

@app.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "status": "online",
        "version": settings.PROJECT_VERSION,
        "docs_url": "/docs",
        "jurisdictions_supported": ["India", "International (USA, EU, UK, Japan, Australia, UAE, Singapore)"],
        "languages_supported": ["English (en)", "Hindi (hi)", "Tamil (ta)"]
    }
