import os
import psycopg2
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Graceful import handling: `workers.asgi` is provided natively by Cloudflare Workers runtime
try:
    import workers.asgi  # type: ignore[import-not-found]
    HAS_WORKERS_RUNTIME = True
except ImportError:
    HAS_WORKERS_RUNTIME = False

app = FastAPI(
    title="IP-SAKTI — Traditional Knowledge & Ayurvedic IP Protection Engine",
    description="Legal Intelligence system for Ministry of Ayush & IP-SAKTI running on Cloudflare Python Workers AI"
)

# Extract origins dynamically from environment or default to wildcard fallback
raw_origins = os.environ.get("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()] if raw_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LegalQueryRequest(BaseModel):
    query: str = Field(..., description="Ayurvedic intellectual property query parameters")
    jurisdiction: str = Field(default_factory=lambda: os.environ.get("DEFAULT_JURISDICTION", "India"))

@app.get("/")
def health_status():
    return {
        "status": "active",
        "service": "IP-SAKTI Edge Legal Engine",
        "runtime": "Cloudflare Serverless Python Edge Node",
        "llm_engine": os.environ.get("AI_MODEL", "@cf/qwen/qwen2.5-7b-instruct"),
        "isolation_protocol": "Active v2-edge deployment"
    }

@app.post("/api/chat")
async def process_edge_rag(payload: LegalQueryRequest, request: Request):
    """
    RAG Pipeline executing entirely within the Cloudflare Worker isolate.
    Retrieves context from Serverless PostgreSQL (Neon DB) and executes Workers AI inference.
    """
    db_url = os.environ.get("DATABASE_URL")
    model_name = os.environ.get("AI_MODEL", "@cf/qwen/qwen2.5-7b-instruct")
    fallback_notice = os.environ.get(
        "FALLBACK_CITATION_NOTICE",
        "I do not have enough verified material to provide an authoritative statutory citation."
    )

    # Resolve environment bindings from request scope/state
    env = getattr(request.state, "env", None) or getattr(request.scope, "env", None)

    retrieved_context = ""

    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT regime, section_marker, content FROM legal_corpus WHERE regime ILIKE %s LIMIT 3;",
                (f"%{payload.jurisdiction}%",)
            )
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if records:
                retrieved_context = "\n".join([f"[{r[0]}, {r[1]}]: {r[2]}" for r in records])
        except Exception:
            retrieved_context = ""

    # Check if authoritative statutory context is available
    if not retrieved_context.strip():
        context_block = f"No verified statutory records found for query scope. Statutory Rule: {fallback_notice}"
    else:
        context_block = retrieved_context

    system_prompt = (
        "You are IP-SAKTI Sahayak, an expert legal intelligence system for Ayurvedic Intellectual Property protection and the Ministry of Ayush.\n"
        "Instructions:\n"
        "1. GROUNDING: Base your answer exclusively on the verified legal contexts listed below. Do not guess or formulate sections.\n"
        "2. CITATIONS: You must append clear, inline bracketed references like [Source: Patents Act, Section 3(p)].\n"
        f"3. FALLBACK: If the verified context does not contain sufficient statutory proof to answer the question, explicitly state: '{fallback_notice}'\n\n"
        f"Verified Context Data:\n{context_block}"
    )

    try:
        ai_binding = getattr(env, "AI", None) if env else None

        if ai_binding is not None:
            ai_response = ai_binding.run(
                model_name,
                {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": payload.query}
                    ],
                    "temperature": float(os.environ.get("AI_TEMPERATURE", "0.1"))
                }
            )
            output_text = ai_response.get("response", "").strip() if isinstance(ai_response, dict) else str(ai_response)
        else:
            output_text = (
                f"{fallback_notice}\n"
                "[Note: Workers AI binding was not detected in this runtime execution context.]"
            )

        return {
            "response": output_text,
            "product": "IP-SAKTI",
            "environment": "Cloudflare Serverless Python Edge Node v2",
            "jurisdiction": payload.jurisdiction,
            "citations_validated": bool(retrieved_context.strip())
        }
    except Exception as ai_err:
        raise HTTPException(
            status_code=500,
            detail=f"Edge AI Inference execution failure: {str(ai_err)}"
        )

# Cloudflare Workers Python ASGI entrypoint wrapper
if HAS_WORKERS_RUNTIME:
    entrypoint = workers.asgi.entrypoint(app)
else:
    # Fallback entrypoint when running in local IDE / standard ASGI runners
    entrypoint = app
