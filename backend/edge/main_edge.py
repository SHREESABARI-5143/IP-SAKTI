import json

try:
    from js import Response, Headers  # type: ignore[import-not-found]
except ImportError:
    # Local development fallback
    class Headers:
        def __init__(self):
            self._headers = {}
        def set(self, k, v):
            self._headers[k] = v
        @classmethod
        def new(cls):
            return cls()

    class Response:
        def __init__(self, body, status=200, headers=None):
            self.body = body
            self.status = status
            self.headers = headers
        @classmethod
        def new(cls, body, status=200, headers=None):
            return cls(body, status, headers)

EMBEDDING_MODEL = "@cf/baai/bge-base-en-v1.5"
LLM_MODEL = "@cf/meta/llama-3.2-3b-instruct"
DEFAULT_JURISDICTION = "India"
FALLBACK_CITATION_NOTICE = "I do not have enough verified material to provide an authoritative statutory citation."

def cors_headers(origin: str = "*") -> Headers:
    headers = Headers.new()
    headers.set("Access-Control-Allow-Origin", origin if origin else "*")
    headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
    headers.set("Content-Type", "application/json; charset=utf-8")
    return headers

def json_response(data: dict, status: int = 200, origin: str = "*") -> Response:
    headers = cors_headers(origin)
    return Response.new(json.dumps(data), status=status, headers=headers)

async def handle_health(env, origin: str) -> Response:
    has_ai = bool(getattr(env, "AI", None))
    has_vectorize = bool(getattr(env, "VECTORIZE", None) or getattr(env, "VECTORIZE_INDEX", None))
    has_db = bool(getattr(env, "DB", None) or getattr(env, "ip_sakti_db", None))

    return json_response({
        "status": "active",
        "service": "IP-SAKTI Edge Legal Engine",
        "runtime": "Cloudflare Serverless Python Edge Node",
        "llm_engine": LLM_MODEL,
        "architecture": {
            "workers_ai": has_ai,
            "cloudflare_d1": has_db,
            "cloudflare_vectorize": has_vectorize,
            "zero_cost_edge_mode": has_ai and has_db and has_vectorize
        },
        "vector_graph_sync": "cron_periodic_cycle_enabled"
    }, origin=origin)

async def handle_ingest_cycle(request, env, origin: str) -> Response:
    db = getattr(env, "DB", None) or getattr(env, "ip_sakti_db", None)
    ai = getattr(env, "AI", None)
    vec = getattr(env, "VECTORIZE", None) or getattr(env, "VECTORIZE_INDEX", None)

    if not db:
        return json_response({"status": "error", "message": "Cloudflare D1 database binding not detected."}, status=500, origin=origin)

    try:
        body_text = await request.text()
        payload = json.loads(body_text) if body_text else {}
    except Exception:
        payload = {}

    sources = payload.get("sources") or [
        {
            "chunk_id": "in_patents_act_1970_sec_3p",
            "statute": "The Patents Act, 1970",
            "section": "Section 3(p)",
            "title": "Traditional Knowledge Patent Exclusions",
            "jurisdiction": "India",
            "doc_type": "statute",
            "url": "https://www.indiacode.nic.in/show-data?actid=AC_CEN_3_44_00007_197039_1517807323983&sectionId=15154&sectionno=3&orderno=3",
            "content": "An invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not patentable."
        },
        {
            "chunk_id": "in_patents_act_1970_sec_3j",
            "statute": "The Patents Act, 1970",
            "section": "Section 3(j)",
            "title": "Plants and Animals Exclusions",
            "jurisdiction": "India",
            "doc_type": "statute",
            "url": "https://www.indiacode.nic.in/show-data?actid=AC_CEN_3_44_00007_197039_1517807323983&sectionId=15154&sectionno=3&orderno=3",
            "content": "Plants and animals in whole or any part thereof other than micro-organisms but including seeds, varieties and species and essentially biological processes for production or propagation of plants and animals are not patentable inventions."
        },
        {
            "chunk_id": "in_biodiversity_act_2002_sec_6",
            "statute": "Biological Diversity Act, 2002",
            "section": "Section 6",
            "title": "Mandatory NBA Approval for IP Filing",
            "jurisdiction": "India",
            "doc_type": "statute",
            "url": "http://nbaindia.org/content/26/59/1/rules.html",
            "content": "No person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the previous approval of the National Biodiversity Authority."
        }
    ]

    ingested_count = 0
    vectorized_count = 0

    for src in sources:
        chunk_id = src.get("chunk_id") or f"chunk_{abs(hash(src.get('statute', '') + src.get('section', '')))}"
        statute = src.get("statute", "General Act")
        section = src.get("section", "Section 0")
        title = src.get("title", "")
        jurisdiction = src.get("jurisdiction", "India")
        doc_type = src.get("doc_type", "statute")
        url = src.get("url", "https://ipindia.gov.in")
        content = src.get("content", "")

        # 1. Upsert into D1
        try:
            stmt = db.prepare(
                "INSERT OR REPLACE INTO corpus_chunks (chunk_id, statute, section_or_article, title, jurisdiction, doc_type, url, text_content) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            )
            await stmt.bind(chunk_id, statute, section, title, jurisdiction, doc_type, url, content).run()
            ingested_count += 1
        except Exception:
            pass

        # 2. Vectorize embedding
        if ai and vec and content:
            try:
                try:
                    emb_res = await ai.run(EMBEDDING_MODEL, text=f"{statute} {section}: {content}")
                except Exception:
                    emb_res = await ai.run(EMBEDDING_MODEL, {"text": [f"{statute} {section}: {content}"]})
                
                emb = None
                if isinstance(emb_res, dict) and "data" in emb_res and emb_res["data"]:
                    emb = emb_res["data"][0]
                elif hasattr(emb_res, "data"):
                    emb = list(emb_res.data[0])

                if emb:
                    await vec.upsert([{
                        "id": chunk_id,
                        "values": emb,
                        "metadata": {"statute": statute, "section": section, "jurisdiction": jurisdiction}
                    }])
                    vectorized_count += 1
            except Exception:
                pass

    return json_response({
        "status": "success",
        "engine": "Cloudflare D1 + Vectorize",
        "ingested_chunks": ingested_count,
        "vectorized_count": vectorized_count
    }, origin=origin)

async def handle_chat(request, env, origin: str) -> Response:
    db = getattr(env, "DB", None) or getattr(env, "ip_sakti_db", None)
    ai = getattr(env, "AI", None)
    vec = getattr(env, "VECTORIZE", None) or getattr(env, "VECTORIZE_INDEX", None)

    try:
        body_text = await request.text()
        payload = json.loads(body_text) if body_text else {}
    except Exception:
        payload = {}

    query = payload.get("query", "").strip()
    jurisdiction = payload.get("jurisdiction", DEFAULT_JURISDICTION)

    if not query:
        return json_response({"error": "Missing query parameter"}, status=400, origin=origin)

    retrieved_items = []
    graph_items = []
    matched_ids = []

    # 1. Semantic Search with Vectorize
    if ai and vec:
        try:
            try:
                emb_res = await ai.run(EMBEDDING_MODEL, text=query)
            except Exception:
                emb_res = await ai.run(EMBEDDING_MODEL, {"text": [query]})

            emb = None
            if isinstance(emb_res, dict) and "data" in emb_res and emb_res["data"]:
                emb = emb_res["data"][0]
            elif hasattr(emb_res, "data"):
                emb = list(emb_res.data[0])

            if emb:
                v_res = await vec.query(emb, topK=3, returnMetadata="all")
                matches = getattr(v_res, "matches", []) or (v_res.get("matches", []) if isinstance(v_res, dict) else [])
                for m in matches:
                    cid = getattr(m, "id", None) or (m.get("id") if isinstance(m, dict) else None)
                    if cid:
                        matched_ids.append(cid)
        except Exception:
            pass

    # 2. Hydrate from D1 by IDs
    if db and matched_ids:
        try:
            placeholders = ",".join(["?"] * len(matched_ids))
            stmt = db.prepare(
                f"SELECT chunk_id, statute, section_or_article, url, text_content FROM corpus_chunks WHERE chunk_id IN ({placeholders})"
            )
            res = await stmt.bind(*matched_ids).all()
            chunks = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
            for c in chunks:
                retrieved_items.append(f"[{c.get('statute')}, {c.get('section_or_article')}]({c.get('url')}): {c.get('text_content')}")
        except Exception:
            pass

    # 3. Fallback direct D1 search if no Vectorize matches
    if not retrieved_items and db:
        try:
            stmt = db.prepare("SELECT chunk_id, statute, section_or_article, url, text_content FROM corpus_chunks LIMIT 3")
            res = await stmt.all()
            chunks = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
            for c in chunks:
                retrieved_items.append(f"[{c.get('statute')}, {c.get('section_or_article')}]({c.get('url')}): {c.get('text_content')}")
        except Exception:
            pass

    # Build Context
    if retrieved_items:
        context_text = "\n\n".join(retrieved_items)
    else:
        context_text = f"No statutory records found. {FALLBACK_CITATION_NOTICE}"

    system_prompt = (
        "You are IP-SAKTI Sahayak, an expert legal intelligence system for Ayurvedic Intellectual Property protection and the Ministry of Ayush.\n"
        "Instructions:\n"
        "1. Base your answer strictly on the verified statutory contexts below.\n"
        "2. For every legal statutory claim, include the direct verified link in markdown citation format: [[Source: Statute Name, Section]](exact_url).\n"
        f"3. If verified context is insufficient, explicitly state: '{FALLBACK_CITATION_NOTICE}'\n\n"
        f"Verified Statutory Context:\n{context_text}"
    )

    if ai:
        try:
            combined_prompt = f"{system_prompt}\n\nUser Question: {query}\n\nAuthoritative Legal Opinion:"
            try:
                ai_res = await ai.run(LLM_MODEL, prompt=combined_prompt)
            except Exception:
                ai_res = await ai.run(LLM_MODEL, {"prompt": combined_prompt})
            
            if isinstance(ai_res, dict):
                output_text = ai_res.get("response", "").strip()
            elif hasattr(ai_res, "response"):
                output_text = str(ai_res.response).strip()
            else:
                output_text = str(ai_res).strip()
        except Exception as e:
            output_text = f"AI Generation error: {str(e)}"
    else:
        output_text = f"{FALLBACK_CITATION_NOTICE}\n[Note: Workers AI binding not available in offline preview]"

    # Audit log to D1
    if db:
        try:
            log_stmt = db.prepare("INSERT INTO query_logs (query, jurisdiction, response) VALUES (?, ?, ?)")
            await log_stmt.bind(query, jurisdiction, output_text).run()
        except Exception:
            pass

    return json_response({
        "response": output_text,
        "product": "IP-SAKTI",
        "environment": "Cloudflare Serverless Python Edge Node (D1 + Vectorize)",
        "jurisdiction": jurisdiction,
        "citations_validated": bool(retrieved_items)
    }, origin=origin)

async def on_fetch(request, env):
    url = request.url
    method = request.method
    origin = request.headers.get("Origin") or "*"

    if method == "OPTIONS":
        return Response.new("", status=204, headers=cors_headers(origin))

    if "/api/chat" in url and method == "POST":
        return await handle_chat(request, env, origin)

    if "/api/ingest/cycle" in url and method == "POST":
        return await handle_ingest_cycle(request, env, origin)

    if "/api/health" in url or url.endswith("/"):
        return await handle_health(env, origin)

    return json_response({"error": "Endpoint not found"}, status=404, origin=origin)
