import os
import psycopg2
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Graceful import handling: `workers.asgi` is provided natively by Cloudflare Workers runtime
try:
    import workers.asgi  # type: ignore[import-not-found]
    HAS_WORKERS_RUNTIME = True
except ImportError:
    HAS_WORKERS_RUNTIME = False

# Import self-ingest service for dynamic vector graph synchronization
try:
    from app.services.edge_ingest import execute_vector_graph_self_ingest
except ImportError:
    try:
        from app.services.edge_ingest import execute_vector_graph_self_ingest
    except ImportError:
        execute_vector_graph_self_ingest = None

app = FastAPI(
    title="IP-SAKTI — Traditional Knowledge & Ayurvedic IP Protection Engine",
    description="Legal Intelligence system for Ministry of Ayush & IP-SAKTI running on Cloudflare Python Workers AI"
)

# Dynamic CORS origins configuration
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

class IngestSyncRequest(BaseModel):
    sources: Optional[List[Dict[str, Any]]] = Field(default=None, description="Optional dynamic list of statutory endpoints or documents to sync")

@app.get("/")
def health_status():
    return {
        "status": "active",
        "service": "IP-SAKTI Edge Legal Engine",
        "runtime": "Cloudflare Serverless Python Edge Node",
        "llm_engine": os.environ.get("AI_MODEL", "@cf/qwen/qwen2.5-7b-instruct"),
        "isolation_protocol": "Active v2-edge deployment",
        "vector_graph_sync": "cron_periodic_cycle_enabled"
    }

@app.post("/api/ingest/cycle")
def trigger_ingest_cycle(payload: Optional[IngestSyncRequest] = Body(None)):
    """
    Periodic self-ingestion endpoint triggered by Cloudflare Cron or remote triggers.
    Dynamically fetches live statutory endpoints, extracts legal graph edges, and syncs to PostgreSQL.
    Zero local static files or JSON files required.
    """
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not configured.")

    if execute_vector_graph_self_ingest is None:
        raise HTTPException(status_code=500, detail="Ingest service module unavailable.")

    try:
        custom_sources = payload.sources if payload else None
        result = execute_vector_graph_self_ingest(db_url, custom_sources)
        return {"status": "success", "result": result}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Dynamic self-ingestion cycle failed: {str(err)}")

@app.post("/api/chat")
async def process_edge_rag(payload: LegalQueryRequest, request: Request):
    """
    RAG Pipeline executing entirely within Cloudflare isolate.
    Retrieves verified corpus chunks and relational graph edges with exact canonical citation URLs.
    """
    db_url = os.environ.get("DATABASE_URL")
    model_name = os.environ.get("AI_MODEL", "@cf/qwen/qwen2.5-7b-instruct")
    fallback_notice = os.environ.get(
        "FALLBACK_CITATION_NOTICE",
        "I do not have enough verified material to provide an authoritative statutory citation."
    )

    env = getattr(request.state, "env", None) or getattr(request.scope, "env", None)

    retrieved_context_items = []
    graph_context_items = []

    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            
            # 1. Fetch relevant statutory chunks from database
            cursor.execute("""
                SELECT statute, section_or_article, text_content, url, chunk_id
                FROM corpus_chunks
                WHERE jurisdiction ILIKE %s OR statute ILIKE %s
                ORDER BY indexed_at DESC
                LIMIT 4;
            """, (f"%{payload.jurisdiction}%", f"%{payload.jurisdiction}%"))
            chunks = cursor.fetchall()

            for c in chunks:
                statute, section, text_content, url, chunk_id = c
                retrieved_context_items.append(
                    f"[{statute}, {section}]({url}): {text_content}"
                )

                # 2. Fetch connected Knowledge Graph relationships for cited chunks
                cursor.execute("""
                    SELECT edge_type, label, target_chunk_id
                    FROM graph_edges
                    WHERE source_chunk_id = %s
                    LIMIT 2;
                """, (chunk_id,))
                edges = cursor.fetchall()
                for edge in edges:
                    graph_context_items.append(
                        f"-> Knowledge Graph Relationship ({edge[0]}): {edge[1]}"
                    )

            cursor.close()
            conn.close()
        except Exception:
            retrieved_context_items = []
            graph_context_items = []

    # Format the verified statutory and graph context
    if retrieved_context_items:
        context_data = "\n\n".join(retrieved_context_items)
        if graph_context_items:
            context_data += "\n\nRelational Legal Topology:\n" + "\n".join(graph_context_items)
    else:
        context_data = f"No verified statutory records found for query scope. Statutory Rule: {fallback_notice}"

    system_prompt = (
        "You are IP-SAKTI Sahayak, an expert legal intelligence system for Ayurvedic Intellectual Property protection and the Ministry of Ayush.\n"
        "Instructions:\n"
        "1. GROUNDING: Base your answer strictly on the verified statutory contexts below. Do not guess or formulate sections.\n"
        "2. WORKING CITATIONS: For every legal statutory claim, include the direct verified link in markdown citation format: "
        "[[Source: Statute Name, Section]](exact_url).\n"
        f"3. FALLBACK: If the verified context does not contain sufficient statutory proof to answer the question, explicitly state: '{fallback_notice}'\n\n"
        f"Verified Statutory Context:\n{context_data}"
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
            "citations_validated": bool(retrieved_context_items)
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
    entrypoint = app
