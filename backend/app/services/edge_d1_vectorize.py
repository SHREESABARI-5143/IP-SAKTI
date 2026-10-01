"""
Edge-Native Vectorize + D1 Integration Service for Cloudflare Workers.
- Vectorize: Handles raw mathematical embeddings & approximate nearest-neighbor (ANN) search.
- D1: Handles structured relational metadata, verified statutory texts, canonical URLs, and query audit logs.
"""
from typing import List, Dict, Any, Optional
import json

EMBEDDING_MODEL = "@cf/baai/bge-base-en-v1.5"

def generate_embedding(ai_binding: Any, text: str) -> Optional[List[float]]:
    """Generates dense vector embeddings using Workers AI."""
    if not ai_binding:
        return None
    try:
        res = ai_binding.run(EMBEDDING_MODEL, {"text": [text]})
        if isinstance(res, dict) and "data" in res and res["data"]:
            return res["data"][0]
        elif isinstance(res, list) and len(res) > 0:
            return res[0]
        return None
    except Exception:
        return None

def search_vectorize(vectorize_binding: Any, embedding: List[float], top_k: int = 4) -> List[str]:
    """Queries Cloudflare Vectorize for nearest matching statutory document chunk IDs."""
    if not vectorize_binding or not embedding:
        return []
    try:
        query_result = vectorize_binding.query(embedding, topK=top_k, returnMetadata="all")
        # Extract matched chunk IDs
        matches = getattr(query_result, "matches", []) or (query_result.get("matches", []) if isinstance(query_result, dict) else [])
        chunk_ids = []
        for m in matches:
            cid = getattr(m, "id", None) or (m.get("id") if isinstance(m, dict) else None)
            if cid:
                chunk_ids.append(cid)
        return chunk_ids
    except Exception:
        return []

def get_d1_chunks_by_ids(db_binding: Any, chunk_ids: List[str]) -> List[Dict[str, Any]]:
    """Hydrates full statutory texts and canonical citations from Cloudflare D1 by chunk IDs."""
    if not db_binding or not chunk_ids:
        return []
    try:
        placeholders = ",".join(["?"] * len(chunk_ids))
        stmt = db_binding.prepare(
            f"SELECT chunk_id, statute, section_or_article, title, jurisdiction, url, text_content "
            f"FROM corpus_chunks WHERE chunk_id IN ({placeholders})"
        )
        res = stmt.bind(*chunk_ids).all()
        results = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
        return results
    except Exception:
        return []

def get_d1_graph_edges(db_binding: Any, chunk_ids: List[str]) -> List[Dict[str, Any]]:
    """Retrieves relational legal topology and cross-references from Cloudflare D1."""
    if not db_binding or not chunk_ids:
        return []
    try:
        placeholders = ",".join(["?"] * len(chunk_ids))
        stmt = db_binding.prepare(
            f"SELECT source_chunk_id, edge_type, label, target_chunk_id "
            f"FROM graph_edges WHERE source_chunk_id IN ({placeholders})"
        )
        res = stmt.bind(*chunk_ids).all()
        results = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
        return results
    except Exception:
        return []

def log_query_to_d1(db_binding: Any, query: str, jurisdiction: str, response: str) -> bool:
    """Audit logs query and response into Cloudflare D1 asynchronously."""
    if not db_binding:
        return False
    try:
        stmt = db_binding.prepare(
            "INSERT INTO query_logs (query, jurisdiction, response) VALUES (?, ?, ?)"
        )
        stmt.bind(query, jurisdiction, response).run()
        return True
    except Exception:
        return False

def sync_d1_and_vectorize(ai_binding: Any, vectorize_binding: Any, db_binding: Any, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ingests dynamic sources into both D1 (metadata & text) and Vectorize (embeddings).
    """
    if not db_binding:
        return {"status": "error", "message": "D1 database binding missing"}

    indexed_count = 0
    vectors_to_upsert = []

    for src in sources:
        chunk_id = src.get("chunk_id") or f"chunk_{abs(hash(src.get('statute', '') + src.get('section', '')))}"
        statute = src.get("statute", "Unknown Statute")
        section = src.get("section", "Section 0")
        title = src.get("title", "")
        jurisdiction = src.get("jurisdiction", "India")
        doc_type = src.get("doc_type", "statute")
        url = src.get("url", "https://ipindia.gov.in")
        content = src.get("content", "")

        # 1. Upsert into D1 Database
        stmt = db_binding.prepare("""
            INSERT OR REPLACE INTO corpus_chunks 
            (chunk_id, statute, section_or_article, title, jurisdiction, doc_type, url, text_content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """)
        stmt.bind(chunk_id, statute, section, title, jurisdiction, doc_type, url, content).run()

        # 2. Compute embedding and prepare for Vectorize
        if ai_binding and vectorize_binding and content:
            emb = generate_embedding(ai_binding, f"{statute} {section}: {content}")
            if emb:
                vectors_to_upsert.append({
                    "id": chunk_id,
                    "values": emb,
                    "metadata": {"statute": statute, "section": section, "jurisdiction": jurisdiction}
                })
        
        indexed_count += 1

    # 3. Batch insert vectors into Vectorize
    if vectorize_binding and vectors_to_upsert:
        try:
            vectorize_binding.upsert(vectors_to_upsert)
        except Exception:
            pass

    return {
        "status": "success",
        "ingested_chunks": indexed_count,
        "vectorized_count": len(vectors_to_upsert)
    }
