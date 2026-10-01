import os
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

# Import D1 + Vectorize edge service
try:
    from app.services.edge_d1_vectorize import (
        generate_embedding,
        search_vectorize,
        get_d1_chunks_by_ids,
        get_d1_graph_edges,
        log_query_to_d1,
        sync_d1_and_vectorize
    )
except ImportError:
    try:
        from services.edge_d1_vectorize import (  # type: ignore[import-not-found]
            generate_embedding,
            search_vectorize,
            get_d1_chunks_by_ids,
            get_d1_graph_edges,
            log_query_to_d1,
            sync_d1_and_vectorize
        )
    except ImportError:
        generate_embedding = None
        search_vectorize = None
        get_d1_chunks_by_ids = None
        get_d1_graph_edges = None
        log_query_to_d1 = None
        sync_d1_and_vectorize = None

# Import legacy self-ingest service for Postgres fallback
try:
    from app.services.edge_ingest import execute_vector_graph_self_ingest
except ImportError:
    try:
        from services.edge_ingest import execute_vector_graph_self_ingest  # type: ignore[import-not-found]
    except ImportError:
        execute_vector_graph_self_ingest = None

app = FastAPI(
    title="IP-SAKTI — Traditional Knowledge & Ayurvedic IP Protection Engine",
    description="Legal Intelligence system for Ministry of Ayush & IP-SAKTI running on Cloudflare Python Workers AI, Vectorize & D1"
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
def health_status(request: Request):
    env = getattr(request.state, "env", None) or getattr(request.scope, "env", None)
    has_d1 = bool(getattr(env, "DB", None) or getattr(env, "ip_sakti_db", None)) if env else False
    has_vectorize = bool(getattr(env, "VECTORIZE_INDEX", None) or getattr(env, "VECTORIZE", None)) if env else False
    has_ai = bool(getattr(env, "AI", None)) if env else False

    return {
        "status": "active",
        "service": "IP-SAKTI Edge Legal Engine",
        "runtime": "Cloudflare Serverless Python Edge Node",
        "llm_engine": os.environ.get("AI_MODEL", "@cf/qwen/qwen2.5-7b-instruct"),
        "architecture": {
            "workers_ai": has_ai,
            "cloudflare_d1": has_d1,
            "cloudflare_vectorize": has_vectorize,
            "zero_cost_edge_mode": has_d1 and has_vectorize
        },
        "vector_graph_sync": "cron_periodic_cycle_enabled"
    }

@app.post("/api/ingest/cycle")
def trigger_ingest_cycle(request: Request, payload: Optional[IngestSyncRequest] = Body(None)):
    """
    Dynamic sync endpoint: Syncs statutory documents into Cloudflare D1 + Vectorize (or Postgres fallback).
    """
    env = getattr(request.state, "env", None) or getattr(request.scope, "env", None)
    db_binding = (getattr(env, "DB", None) or getattr(env, "ip_sakti_db", None)) if env else None
    ai_binding = getattr(env, "AI", None) if env else None
    vec_binding = (getattr(env, "VECTORIZE_INDEX", None) or getattr(env, "VECTORIZE", None)) if env else None

    custom_sources = payload.sources if payload and payload.sources else [
        {
            "statute": "The Patents Act, 1970",
            "section": "Section 3(p)",
            "title": "Traditional Knowledge Patent Exclusions",
            "jurisdiction": "India",
            "doc_type": "statute",
            "url": "https://www.indiacode.nic.in/show-data?actid=AC_CEN_3_44_00007_197039_1517807323983&sectionId=15154&sectionno=3&orderno=3",
            "content": "An invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not patentable."
        },
        {
            "statute": "Biological Diversity Act, 2002",
            "section": "Section 6",
            "title": "Mandatory NBA Approval for IP Filing",
            "jurisdiction": "India",
            "doc_type": "statute",
            "url": "http://nbaindia.org/content/26/59/1/rules.html",
            "content": "No person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the previous approval of the National Biodiversity Authority."
        }
    ]

    # 1. Native Cloudflare D1 + Vectorize Ingestion Path
    if db_binding and sync_d1_and_vectorize:
        try:
            res = sync_d1_and_vectorize(ai_binding, vec_binding, db_binding, custom_sources)
            return {"status": "success", "engine": "Cloudflare D1 + Vectorize", "result": res}
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"D1/Vectorize ingestion failed: {str(err)}")

    # 2. PostgreSQL / Neon Fallback Path
    db_url = os.environ.get("DATABASE_URL")
    if db_url and execute_vector_graph_self_ingest:
        try:
            result = execute_vector_graph_self_ingest(db_url, custom_sources)
            return {"status": "success", "engine": "PostgreSQL fallback", "result": result}
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"PostgreSQL ingestion failed: {str(err)}")

    return {"status": "warning", "message": "No active D1 binding or DATABASE_URL found to ingest."}

@app.post("/api/chat")
async def process_edge_rag(payload: LegalQueryRequest, request: Request):
    """
    RAG Pipeline executing entirely within Cloudflare isolate:
    1. Vectorize: Semantic similarity search returning top chunk IDs.
    2. D1: Batch hydration of verified statutory text & graph edges.
    3. Workers AI: Synthesis of grounded legal advisory with canonical markdown links.
    4. D1: Audit logging of user queries.
    """
    model_name = os.environ.get("AI_MODEL", "@cf/qwen/qwen2.5-7b-instruct")
    fallback_notice = os.environ.get(
        "FALLBACK_CITATION_NOTICE",
        "I do not have enough verified material to provide an authoritative statutory citation."
    )

    env = getattr(request.state, "env", None) or getattr(request.scope, "env", None)
    ai_binding = getattr(env, "AI", None) if env else None
    vec_binding = (getattr(env, "VECTORIZE_INDEX", None) or getattr(env, "VECTORIZE", None)) if env else None
    db_binding = (getattr(env, "DB", None) or getattr(env, "ip_sakti_db", None)) if env else None
    db_url = os.environ.get("DATABASE_URL")

    retrieved_context_items = []
    graph_context_items = []
    matched_chunk_ids = []

    # --- Strategy A: Native Cloudflare Vectorize + D1 ---
    if ai_binding and vec_binding and db_binding and generate_embedding and search_vectorize:
        try:
            query_vec = generate_embedding(ai_binding, payload.query)
            if query_vec:
                matched_chunk_ids = search_vectorize(vec_binding, query_vec, top_k=4)
            
            if matched_chunk_ids and get_d1_chunks_by_ids:
                chunks = get_d1_chunks_by_ids(db_binding, matched_chunk_ids)
                for c in chunks:
                    statute = c.get("statute", "")
                    section = c.get("section_or_article", "")
                    text_content = c.get("text_content", "")
                    url = c.get("url", "")
                    retrieved_context_items.append(f"[{statute}, {section}]({url}): {text_content}")

                if get_d1_graph_edges:
                    edges = get_d1_graph_edges(db_binding, matched_chunk_ids)
                    for edge in edges:
                        graph_context_items.append(
                            f"-> Knowledge Graph Relationship ({edge.get('edge_type')}): {edge.get('label')}"
                        )
        except Exception:
            pass

    # --- Strategy B: Fallback to Direct D1 Query if Vectorize empty ---
    if not retrieved_context_items and db_binding:
        try:
            stmt = db_binding.prepare("""
                SELECT chunk_id, statute, section_or_article, text_content, url 
                FROM corpus_chunks 
                WHERE jurisdiction LIKE ? OR statute LIKE ? OR text_content LIKE ?
                LIMIT 4
            """)
            like_term = f"%{payload.jurisdiction}%"
            res = stmt.bind(like_term, like_term, f"%{payload.query[:20]}%").all()
            chunks = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
            for c in chunks:
                retrieved_context_items.append(
                    f"[{c.get('statute')}, {c.get('section_or_article')}]({c.get('url')}): {c.get('text_content')}"
                )
        except Exception:
            pass

    # --- Strategy C: PostgreSQL Fallback ---
    if not retrieved_context_items and db_url:
        try:
            import psycopg2  # type: ignore[import-not-found]
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
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
                retrieved_context_items.append(f"[{statute}, {section}]({url}): {text_content}")
            cursor.close()
            conn.close()
        except Exception:
            pass

    # Context formatting
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

        # Asynchronously log query into D1
        if db_binding and log_query_to_d1:
            try:
                log_query_to_d1(db_binding, payload.query, payload.jurisdiction, output_text)
            except Exception:
                pass

        return {
            "response": output_text,
            "product": "IP-SAKTI",
            "environment": "Cloudflare Serverless Python Edge Node (D1 + Vectorize)",
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
