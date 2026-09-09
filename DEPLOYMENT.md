# DEPLOYMENT GUIDE — IP-SAKTI SAHAYAK

## 1. Local Development (Zero-Dependency SQLite)

```bash
# Terminal 1: Backend
$env:PYTHONPATH="."
python -m uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Visit:
- Frontend: `http://localhost:3000`
- Backend API Docs: `http://localhost:8000/docs`

---

## 2. Docker Compose Production Setup

```bash
# Configure environment variables
cp .env.example .env

# Build and start all services
docker-compose up --build -d
```

---

## 3. Production Environment Checklist

1. Set `SECRET_KEY` to a strong random 256-bit string.
2. Set `DATABASE_URL` to your production PostgreSQL connection string (`postgresql+asyncpg://...`).
3. Set `GEMINI_API_KEY` or `OPENAI_API_KEY` for live generative LLM synthesis.
4. Set up reverse proxy (NGINX / Caddy) with SSL certificates (Let's Encrypt).
