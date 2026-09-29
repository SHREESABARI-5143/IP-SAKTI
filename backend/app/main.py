from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.database import init_db
from app.api.routers import health, classify, query, prior_art, pathway

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    try:
        await init_db()
    except Exception as e:
        print(f"[Lifespan] Error initializing DB: {e}")
    yield
    # Shutdown logic if any

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multilingual, Source-Cited, Jurisdiction-Aware AI Assistant & Product Classification Engine for Ayurveda IP & Regulations.",
    lifespan=lifespan
)

# Enable CORS for local and web frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health.router)
app.include_router(classify.router)
app.include_router(query.router)
app.include_router(prior_art.router)
app.include_router(pathway.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
