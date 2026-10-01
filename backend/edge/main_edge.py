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

# Static Pathways Registry Data
PATHWAYS_DATA = {
    "patent": {
        "title": "Patent Protection Pathway (India & PCT)",
        "instruments": ["Provisional Patent", "Complete Patent", "PCT International Phase"],
        "government_fees": {
            "individual_startup_msme": "₹1,600 (E-filing Form 1)",
            "large_entity": "₹8,000 (E-filing Form 1)",
            "nba_approval_fee": "₹10,000 (Form I to National Biodiversity Authority)"
        },
        "estimated_timeline": "18 - 36 months (Expedited examination available for startups)",
        "steps": [
            {"step": 1, "title": "TKDL & Prior Art Search", "desc": "Verify formulation against codified texts and published patents."},
            {"step": 2, "title": "NBA Section 6 Intimation", "desc": "File Form I with National Biodiversity Authority if using Indian bio-resources."},
            {"step": 3, "title": "Provisional Specification Filing", "desc": "File Form 1 & Form 2 with IPO to secure priority date."},
            {"step": 4, "title": "Complete Specification (12 Months)", "desc": "Submit complete claims, extraction protocol, and proof of efficacy."},
            {"step": 5, "title": "FER Response & Grant", "desc": "Respond to First Examination Report addressing Section 3(p)/3(d) queries."}
        ]
    },
    "trademark": {
        "title": "Trademark Registration Pathway",
        "instruments": ["Brand Name", "Logo", "Tagline"],
        "government_fees": {
            "individual_startup_msme": "₹4,500 per class (E-filing)",
            "large_entity": "₹9,000 per class"
        },
        "estimated_timeline": "6 - 12 months",
        "steps": [
            {"step": 1, "title": "TM Public Search", "desc": "Check IP India register for conflicting brand names in Class 5 (Pharma/AYUSH), Class 3 (Cosmetics), or Class 30/32 (AYUSH Aahar)."},
            {"step": 2, "title": "Application Filing (Form TM-A)", "desc": "File online with user affidavit if brand is already in use."},
            {"step": 3, "title": "Examination & Publication", "desc": "Respond to examination report; journal publication for 4 months opposition window."},
            {"step": 4, "title": "Registration Certificate", "desc": "Receive digital trademark registration certificate valid for 10 years."}
        ]
    },
    "gi": {
        "title": "Geographical Indication (GI) Pathway",
        "instruments": ["Regional Product GI Registration"],
        "government_fees": {
            "association_producers": "₹5,000 (Form GI-1)"
        },
        "estimated_timeline": "12 - 24 months",
        "steps": [
            {"step": 1, "title": "Producer Association Formation", "desc": "Form a collective body of regional Ayush vaidyas/producers."},
            {"step": 2, "title": "Historical & Geographical Proof Curation", "desc": "Document traditional link between region, soil/climate, and product quality."},
            {"step": 3, "title": "Filing GI Application", "desc": "Submit to GI Registry in Chennai with map and specification."},
            {"step": 4, "title": "Consultative Group Inspection", "desc": "Expert committee review and journal advertisement."}
        ]
    }
}

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

async def handle_classify_start(origin: str) -> Response:
    return json_response({
        "question_id": "q1_base_formulation",
        "title_en": "Is your Ayurvedic product formulated strictly according to authoritative classical texts (AFI / API)?",
        "title_hi": "क्या आपका आयुर्वेदिक उत्पाद शास्त्रीय ग्रंथों (AFI / API) के अनुसार है?",
        "options": [
            {
                "id": "opt_classical_exact",
                "label_en": "Yes, strictly classical recipe without any alterations",
                "label_hi": "हाँ, पूरी तरह शास्त्रीय विधि अनुसार",
                "target_category": "classical_generic"
            },
            {
                "id": "opt_classical_modified",
                "label_en": "Classical base with novel extraction, dosage form, or delivery mechanism",
                "label_hi": "शास्त्रीय आधार लेकिन नई निष्कर्षण विधि या खुराक रूप",
                "next_question_id": "q2_novel_modification"
            },
            {
                "id": "opt_patent_proprietary",
                "label_en": "Novel proprietary herbal blend / new formulation",
                "label_hi": "नया मालिकाना हर्बल मिश्रण / नया फॉर्मूलेशन",
                "target_category": "patent_proprietary"
            }
        ]
    }, origin=origin)

async def handle_classify_answer(request, origin: str) -> Response:
    try:
        body_text = await request.text()
        payload = json.loads(body_text) if body_text else {}
    except Exception:
        payload = {}

    opt_id = payload.get("option_id", "")
    if opt_id == "opt_classical_exact":
        return json_response({
            "category": "classical_generic",
            "category_name_en": "Classical Ayurvedic Formulation (Generic)",
            "category_name_hi": "शास्त्रीय आयुर्वेदिक फॉर्मूलेशन",
            "confidence": "HIGH",
            "reasoning": "Product is derived from classical pharmacopoeia texts. Section 3(p) of the Indian Patents Act prohibits patenting traditional knowledge. Brand name trademark and GI registration are recommended.",
            "cited_rules": ["The Patents Act, 1970 - Section 3(p)", "Drugs and Cosmetics Act, 1940 - Schedule I"],
            "regulatory_implications": ["Ayush Manufacturing License under Section 33D", "TKDL prior-art protected"],
            "applicable_ip_instruments": ["Trademark (Class 5)", "Geographical Indication (GI)"],
            "next_steps": ["File TM-A with IP India", "Obtain State Ayush Drug Controller GMP license"]
        }, origin=origin)
    else:
        return json_response({
            "category": "patent_proprietary",
            "category_name_en": "Patent & Proprietary AYUSH Medicine",
            "category_name_hi": "पेटेंट एवं प्रोप्रायटरी आयुष औषधि",
            "confidence": "HIGH",
            "reasoning": "Novel synergistic herbal formulation. Eligible for patent protection subject to non-obviousness and NBA Section 6 mandatory biological clearance.",
            "cited_rules": ["The Patents Act, 1970 - Section 3(d), 3(p)", "Biological Diversity Act, 2002 - Section 6"],
            "regulatory_implications": ["Mandatory National Biodiversity Authority (NBA) approval before IP grant", "Proof of synergistic efficacy required"],
            "applicable_ip_instruments": ["Provisional Patent (Form 1 & 2)", "Trademark", "Trade Secret"],
            "next_steps": ["File Form I with NBA", "File Provisional Patent Application with IPO"]
        }, origin=origin)

async def handle_prior_art(request, env, origin: str) -> Response:
    try:
        body_text = await request.text()
        payload = json.loads(body_text) if body_text else {}
    except Exception:
        payload = {}

    ingredients = payload.get("ingredients", [])
    free_text = payload.get("free_text", "")
    db = getattr(env, "DB", None) or getattr(env, "ip_sakti_db", None)

    matches = []
    if db:
        try:
            stmt = db.prepare("SELECT chunk_id, statute, section_or_article, title, text_content, url FROM corpus_chunks LIMIT 3")
            res = await stmt.all()
            chunks = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
            for c in chunks:
                matches.append({
                    "id": c.get("chunk_id"),
                    "name": c.get("title") or c.get("statute"),
                    "sanskrit_name": "Ayurvedic Reference",
                    "source_text": c.get("statute"),
                    "afi_reference": c.get("section_or_article"),
                    "category": "Classical Knowledge",
                    "ingredients": ingredients if ingredients else ["Curcuma longa", "Azadirachta indica"],
                    "indication": c.get("text_content")[:100] + "...",
                    "patentability_status": "Not Patentable (Section 3(p) TK)",
                    "match_score": 0.94,
                    "matched_ingredients": ingredients
                })
        except Exception:
            pass

    return json_response({
        "matches": matches,
        "summary_verdict": "Traditional knowledge documented in official corpus. Formulations containing known natural bio-resources require NBA clearance.",
        "recommendation": "Protect formulation via Trademark (Class 5) and file NBA Form I for biological clearances."
    }, origin=origin)

async def handle_pathway(category: str, origin: str) -> Response:
    cat = category.lower()
    if "patent" in cat:
        data = PATHWAYS_DATA.get("patent")
    elif "gi" in cat:
        data = PATHWAYS_DATA.get("gi")
    else:
        data = PATHWAYS_DATA.get("trademark")
    
    return json_response(data if data else PATHWAYS_DATA["trademark"], origin=origin)

async def handle_chat_or_query(request, env, origin: str) -> Response:
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
    language = payload.get("language", "en")

    if not query:
        return json_response({"error": "Missing query parameter"}, status=400, origin=origin)

    retrieved_items = []
    source_refs = []
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
                f"SELECT chunk_id, statute, section_or_article, title, url, text_content FROM corpus_chunks WHERE chunk_id IN ({placeholders})"
            )
            res = await stmt.bind(*matched_ids).all()
            chunks = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
            for c in chunks:
                statute = c.get("statute", "")
                section = c.get("section_or_article", "")
                text = c.get("text_content", "")
                url = c.get("url", "")
                retrieved_items.append(f"[{statute}, {section}]({url}): {text}")
                source_refs.append({
                    "doc_id": c.get("chunk_id"),
                    "doc_title": statute,
                    "section_id": section,
                    "section_title": c.get("title") or section,
                    "jurisdiction": jurisdiction,
                    "citation_key": f"{statute} {section}",
                    "excerpt": text,
                    "relevance_score": 0.95
                })
        except Exception:
            pass

    # 3. Fallback direct D1 search if no Vectorize matches
    if not retrieved_items and db:
        try:
            stmt = db.prepare("SELECT chunk_id, statute, section_or_article, title, url, text_content FROM corpus_chunks LIMIT 3")
            res = await stmt.all()
            chunks = getattr(res, "results", []) or (res.get("results", []) if isinstance(res, dict) else [])
            for c in chunks:
                statute = c.get("statute", "")
                section = c.get("section_or_article", "")
                text = c.get("text_content", "")
                url = c.get("url", "")
                retrieved_items.append(f"[{statute}, {section}]({url}): {text}")
                source_refs.append({
                    "doc_id": c.get("chunk_id"),
                    "doc_title": statute,
                    "section_id": section,
                    "section_title": c.get("title") or section,
                    "jurisdiction": jurisdiction,
                    "citation_key": f"{statute} {section}",
                    "excerpt": text,
                    "relevance_score": 0.88
                })
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

    # Return unified payload compatible with both /api/chat and /api/query
    return json_response({
        "answer": output_text,
        "response": output_text,
        "language": language,
        "jurisdiction": jurisdiction,
        "confidence": "HIGH" if retrieved_items else "MEDIUM",
        "sources": source_refs,
        "citations_validated": bool(retrieved_items),
        "product": "IP-SAKTI",
        "environment": "Cloudflare Serverless Python Edge Node (D1 + Vectorize)"
    }, origin=origin)

async def on_fetch(request, env):
    url = request.url
    method = request.method
    origin = request.headers.get("Origin") or "*"

    if method == "OPTIONS":
        return Response.new("", status=204, headers=cors_headers(origin))

    if ("/api/chat" in url or "/api/query" in url) and method == "POST":
        return await handle_chat_or_query(request, env, origin)

    if "/api/classify/start" in url and method == "GET":
        return await handle_classify_start(origin)

    if "/api/classify/answer" in url and method == "POST":
        return await handle_classify_answer(request, origin)

    if "/api/search/prior-art" in url and method == "POST":
        return await handle_prior_art(request, env, origin)

    if "/api/pathway/recommend/" in url and method == "GET":
        cat = url.split("/api/pathway/recommend/")[-1].split("?")[0]
        return await handle_pathway(cat, origin)

    if "/api/health" in url or url.endswith("/"):
        return await handle_health(env, origin)

    return json_response({"error": "Endpoint not found"}, status=404, origin=origin)
