# M11 Hardcode Inventory

Comprehensive audit of all literals across backend and frontend codebases as mandated by Milestone M11.

## Inventory Summary

- **Total Backend Findings**: 101
- **Total Frontend Findings**: 131
- **Total Inspected**: 232

## Detailed Findings Table

| file:line | current literal | classification | replacement source | owner milestone |
| :--- | :--- | :--- | :--- | :--- |
| `backend/app/main.py:42` | `allow_methods=["*"],` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/main.py:43` | `allow_headers=["*"],` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:34` | `conf_score = 0.92` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/classification_agent.py:37` | `licensing = ["Form 32 (State Licensing Authority)", "Schedul` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:38` | `routes = ["Trademark (Class 3 - Cosmetics)", "Design Patent ` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:46` | `conf_score = 0.94` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/classification_agent.py:49` | `licensing = ["FSSAI Central / State License under Ayurveda A` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:50` | `routes = ["Trademark (Class 30 - Foods / Class 32 - Beverage` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:58` | `conf_score = 0.88` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/classification_agent.py:61` | `licensing = ["CDSCO Form 44 / New Drug Approval", "Phase I-I` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:62` | `routes = ["Process Patent (Extraction/Purification method)",` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:65` | `labels = ["Schedule H / Prescription warnings", "Standardize` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:70` | `conf_score = 0.96` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/classification_agent.py:73` | `licensing = ["Manufacturing License on Form 25-D from State ` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:74` | `routes = ["Trademark for proprietary brand name (Class 5 - P` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:77` | `labels = ["Ayurvedic Proprietary / Classical Medicine statem` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:82` | `conf_score = 0.90` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/classification_agent.py:85` | `licensing = ["Manufacturing License (Form 25-D) with Rule 15` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/classification_agent.py:86` | `routes = ["Trademark (Class 5 - Pharmaceuticals)", "Process/` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/agents/orchestrator.py:77` | `score=0.1,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:78` | `source_authority_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:79` | `retrieval_relevance_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:80` | `jurisdiction_match_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:81` | `source_freshness_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:82` | `citation_grounding_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:269` | `score=0.10,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:270` | `source_authority_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:271` | `retrieval_relevance_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:272` | `jurisdiction_match_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:273` | `source_freshness_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:274` | `citation_grounding_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:315` | `score=0.15,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:316` | `source_authority_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:317` | `retrieval_relevance_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:318` | `jurisdiction_match_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:319` | `source_freshness_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/agents/orchestrator.py:320` | `citation_grounding_score=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/api/v1/abs.py:5` | `router = APIRouter(prefix="/abs", tags=["Access and Benefit ` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/admin.py:13` | `router = APIRouter(prefix="/admin", tags=["Admin Console & T` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/auth.py:9` | `router = APIRouter(prefix="/auth", tags=["Authentication"])` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/chat.py:12` | `router = APIRouter(prefix="/chat", tags=["Conversational Int` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/classify.py:5` | `router = APIRouter(prefix="/classify", tags=["Formulation Cl` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/documents.py:12` | `router = APIRouter(prefix="/documents", tags=["Private Docum` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/documents.py:14` | `ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".csv", ".tsv` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/documents.py:93` | `return {"status": "deleted", "document_id": doc_id}` | **CONSTANT-OK** | API Response structure | M11 |
| `backend/app/api/v1/escalations.py:10` | `router = APIRouter(prefix="/escalations", tags=["Human IP Fa` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/evaluation.py:7` | `router = APIRouter(prefix="/evaluation", tags=["AI Quality E` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/ip_strategy.py:5` | `router = APIRouter(prefix="/ip", tags=["IP Protection Strate` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/products.py:11` | `router = APIRouter(prefix="/products", tags=["Product Worksp` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/api/v1/products.py:78` | `return {"message": "Product deleted successfully."}` | **CONSTANT-OK** | API Response structure | M11 |
| `backend/app/api/v1/sources.py:16` | `router = APIRouter(prefix="/sources", tags=["Authoritative S` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/core/config.py:25` | `OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://` | **CONFIG** | Central Pydantic Settings | M11 |
| `backend/app/core/config.py:28` | `VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://loca` | **CONFIG** | Central Pydantic Settings | M11 |
| `backend/app/core/config.py:34` | `"http://localhost:3000",` | **CONFIG** | Central Pydantic Settings | M11 |
| `backend/app/core/config.py:35` | `"http://localhost:3001",` | **CONFIG** | Central Pydantic Settings | M11 |
| `backend/app/core/config.py:36` | `"http://127.0.0.1:3000",` | **CONFIG** | Central Pydantic Settings | M11 |
| `backend/app/core/config.py:37` | `"http://127.0.0.1:3001",` | **CONFIG** | Central Pydantic Settings | M11 |
| `backend/app/core/config.py:43` | `ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".` | **CONFIG** | Central Pydantic Settings | M11 |
| `backend/app/evaluation/run_eval.py:35` | `citation_precision_sum = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/evaluation/run_eval.py:36` | `total_confidence_sum = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/ingestion/live_ingest.py:525` | `authority_score=0.85` | **DATA** | Database / data/corpus/*.jsonl | M11 |
| `backend/app/ingestion/seed_corpus.py:362` | `f"acid-insoluble ash (NMT 1.5%), alcohol-soluble extractive ` | **DATA** | Database / data/corpus/*.jsonl | M11 |
| `backend/app/ingestion/seed_corpus.py:500` | `"content": "All Ayurveda Aahar products must comply with mic` | **DATA** | Database / data/corpus/*.jsonl | M11 |
| `backend/app/models/conversation.py:35` | `confidence_score = Column(Float, default=0.9)` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/multilingual/dictionary.py:6` | `LEGAL_AYUSH_DICTIONARY = {` | **DATA** | Database tables / domain registry | M11 |
| `backend/app/multilingual/normalizer.py:26` | `HERB_MAP = {` | **DATA** | Database tables / domain registry | M11 |
| `backend/app/multilingual/normalizer.py:63` | `COLLOQUIAL_INTENT_MAP = {` | **DATA** | Database tables / domain registry | M11 |
| `backend/app/rag/citation_verifier.py:112` | `citation_entailment=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/citation_verifier.py:113` | `citation_completeness=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/citation_verifier.py:114` | `grounded_claim_rate=0.0,` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/citation_verifier.py:221` | `if overlap_ratio >= 0.12 or not claim_tokens:` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/citation_verifier.py:234` | `if overlap_ratio >= 0.15 or not claim_tokens:` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/confidence.py:26` | `score=0.1,` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:27` | `source_authority_score=0.0,` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:28` | `retrieval_relevance_score=0.0,` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:29` | `jurisdiction_match_score=0.0,` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:30` | `source_freshness_score=0.0,` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:31` | `citation_grounding_score=0.0,` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:53` | `freshness_score = 0.95` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:66` | `if final_score >= 0.80:` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:69` | `elif final_score >= 0.55:` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/confidence.py:72` | `elif final_score >= 0.35:` | **CONFIG** | settings.CONFIDENCE_ABSTAIN_THRESHOLD / settings.CONFIDENCE_ESCALATE_THRESHOLD | M11 |
| `backend/app/rag/intent_classifier.py:279` | `if not is_direct and chunk.get("retrieval_score", 0.0) >= 0.` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/retriever.py:10` | `STOPWORDS = {` | **CONSTANT-OK** | Internal lookup tables | M11 |
| `backend/app/rag/retriever.py:332` | `jurisdiction_match_score = 0.6` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/retriever.py:334` | `jurisdiction_match_score = 0.01` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/retriever.py:345` | `jurisdiction_match_score = 0.8` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/retriever.py:349` | `jurisdiction_match_score = 0.01` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/retriever.py:381` | `if weighted_lexical >= 0.06 or is_exact_match:` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/rag/providers/vllm_provider.py:12` | `self.base_url = (base_url or getattr(settings, "VLLM_BASE_UR` | **CONFIG** | settings.DATABASE_URL / settings.OLLAMA_BASE_URL | M11 |
| `backend/app/schemas/chat.py:19` | `score: float = 0.92` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:20` | `source_authority_score: float = 0.95` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:21` | `retrieval_relevance_score: float = 0.90` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:23` | `source_freshness_score: float = 0.95` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:24` | `citation_grounding_score: float = 0.94` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:52` | `query_parsing_ms: float = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:53` | `retrieval_ms: float = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:54` | `evidence_filtering_ms: float = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:55` | `generation_ms: float = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:56` | `verification_ms: float = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `backend/app/schemas/chat.py:57` | `total_ms: float = 0.0` | **CONSTANT-OK** | Algorithm parameter | M11 |
| `frontend/src/app/layout.tsx:34` | `<link rel="preconnect" href="https://fonts.googleapis.com" /` | **CONFIG** | process.env.NEXT_PUBLIC_API_URL | M11 |
| `frontend/src/app/layout.tsx:35` | `<link rel="preconnect" href="https://fonts.gstatic.com" cros` | **CONFIG** | process.env.NEXT_PUBLIC_API_URL | M11 |
| `frontend/src/app/layout.tsx:37` | `href="https://fonts.googleapis.com/css2?family=Noto+Sans+Dev` | **CONFIG** | process.env.NEXT_PUBLIC_API_URL | M11 |
| `frontend/src/app/page.tsx:48` | `const samplePrompts = [` | **COPY** | messages/{en,hi,ta}.json | M11 |
| `frontend/src/app/page.tsx:237` | `<span>Citation-Grounded AI • Evidence Validation & Safe Abst` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/page.tsx:254` | `<span className="text-slate-400">Target Framework:</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/page.tsx:365` | `<span>Export Report</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/page.tsx:375` | `<span className="text-emerald-700">Copied!</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/page.tsx:390` | `<span>Consult IP Facilitator</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/page.tsx:407` | `<span>Searching statutory registries, verifying TKDL exclusi` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/page.tsx:445` | `<span>Ask Sahayak</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:63` | `<h2 className="text-sm font-bold text-slate-900 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:83` | `placeholder="e.g. Ashwagandha root, Guggulu resin, Tulsi lea` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:107` | `<option value="Indian Individual/Entity">Indian Citizen / 10` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:108` | `<option value="Foreign Entity / NRI / Entity with Foreign Pa` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:191` | `<h3 className="text-xs font-bold text-slate-600 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:204` | `<h3 className="text-xs font-bold text-slate-600 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:216` | `<h3 className="text-xs font-bold text-slate-600 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/abs-helper/page.tsx:242` | `<h3 className="text-base font-bold text-slate-700">Awaiting ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:96` | `<span>Refresh Telemetry</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:104` | `<span>Grounding Score</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:115` | `<span>Abstention Rate</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:121` | `<p className="text-[11px] text-slate-500 font-medium">Safe G` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:126` | `<span>Authoritative Records</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:132` | `<p className="text-[11px] text-slate-500 font-medium">Indexe` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:137` | `<span>Escalation Queue</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:143` | `<p className="text-[11px] text-amber-700 font-medium">Pendin` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:151` | `<h2 className="text-base font-bold text-slate-900">Golden Da` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:171` | `<span className="text-emerald-800 font-medium">Pass Rate:</s` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:178` | `<span className="text-teal-800 font-medium">Groundedness Sco` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:185` | `<span className="text-blue-800 font-medium">Citation Complet` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:192` | `<span className="text-slate-600 font-medium">Retrieval Recal` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:204` | `<th className="p-2.5">Case ID</th>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:205` | `<th className="p-2.5">Test Query</th>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:206` | `<th className="p-2.5">Detected Domain</th>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:207` | `<th className="p-2.5">Confidence</th>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:208` | `<th className="p-2.5">Status</th>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:257` | `<strong>Inquiry:</strong> {esc.question}` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/admin/page.tsx:261` | `<span>Contact: <strong>{esc.contact_email}</strong> • {esc.c` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:64` | `<h2 className="text-sm font-bold text-slate-900 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:68` | `<label className="block font-semibold text-slate-700 mb-1">P` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:79` | `<label className="block font-semibold text-slate-700 mb-1">I` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:97` | `<span>Reference text in First Schedule (Samhita / AFI)?</spa` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:102` | `<label className="block font-medium text-slate-600 mb-0.5">A` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:121` | `<span>Modified / Novel Extract</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:131` | `<span>Novel Process</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:136` | `<label className="block font-semibold text-slate-700 mb-1">I` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:141` | `placeholder="Describe if intended for disease therapy, food ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:148` | `<label className="block font-semibold text-slate-700 mb-1">D` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:154` | `<option value="Vati / Tablet">Vati / Tablet</option>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:155` | `<option value="Asava / Arishta">Asava / Arishta (Fermented)<` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:156` | `<option value="Churna / Powder">Churna / Powder</option>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:157` | `<option value="Taila / Ghrita (Medicated Oil/Ghee)">Taila / ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:158` | `<option value="Standardized Botanical Extract Capsule">Stand` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:159` | `<option value="Ayurveda Aahar Health Drink / Food Bar">Ayurv` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:160` | `<option value="Topical Cream / Hair Oil (Cosmetic)">Topical ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:182` | `<span className="text-xs font-bold text-teal-800 uppercase t` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:197` | `<h3 className="text-xs font-bold text-slate-600 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:205` | `<h3 className="text-xs font-bold text-slate-600 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:237` | `<h3 className="text-xs font-bold text-slate-600 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/classify/page.tsx:263` | `<h3 className="text-base font-bold text-slate-700">Awaiting ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/documents/page.tsx:72` | `<h2 className="text-sm font-bold text-slate-900 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/documents/page.tsx:115` | `<div className="p-8 text-center text-xs text-slate-500">Load` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:75` | `<h2 className="text-sm font-bold text-slate-900 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:79` | `<label className="block font-semibold text-slate-700 mb-1">P` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:90` | `<label className="block font-semibold text-slate-700 mb-1">B` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:101` | `<label className="block font-semibold text-slate-700 mb-1">I` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:119` | `<span>Demonstrable Synergistic Efficacy</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:129` | `<span>Novel Process / Extraction Method</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:139` | `<span>Exact Classical Ayurvedic Recipe</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:160` | `<span className="text-[10px] font-bold text-teal-400 upperca` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:168` | `<h3 className="text-xs font-bold text-slate-600 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:188` | `<span className="font-semibold text-slate-800">Action Plan:<` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:213` | `<span>Timeline: {item.timeline}</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/ip-strategy/page.tsx:237` | `<h3 className="text-base font-bold text-slate-700">Awaiting ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:99` | `<span>New Product Formulation</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:105` | `<div className="p-12 text-center text-xs text-slate-500">Loa` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:143` | `<span>Dosage Form: <strong>{prod.dosage_form}</strong></span` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:156` | `<span>Created {new Date(prod.created_at).toLocaleDateString(` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:157` | `<span className="font-semibold text-teal-700">Ready for Doss` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:168` | `<h2 className="text-lg font-bold text-slate-900">Create New ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:172` | `<label className="block font-semibold text-slate-700 mb-1">P` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:177` | `placeholder="e.g. Saptamrit Loha Extract Capsule"` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:185` | `<label className="block font-semibold text-slate-700 mb-1">C` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:191` | `<option value="classical_ayurvedic">Classical Ayurvedic (Fir` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:192` | `<option value="proprietary_ayurvedic">Patent or Proprietary ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:193` | `<option value="ayurveda_aahar">Ayurveda Aahar (FSSAI 2022)</` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:194` | `<option value="phytopharmaceutical">Phytopharmaceutical Drug` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:195` | `<option value="cosmetic">Herbal / Ayurvedic Cosmetic</option` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:200` | `<label className="block font-semibold text-slate-700 mb-1">D` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:211` | `<label className="block font-semibold text-slate-700 mb-1">B` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:222` | `<label className="block font-semibold text-slate-700 mb-1">T` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/products/page.tsx:227` | `placeholder="Intended physiological indications..."` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:147` | `<span>Sync & Verify All Sources</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:188` | `<div className="p-16 text-center text-xs text-slate-500">Loa` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:214` | `<span>Authority: <strong>{src.authority}</strong></span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:218` | `<span>Type: <strong>{src.document_type \|\| src.source_type}</` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:235` | `<span>Inspect Records</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:242` | `<span>Versions</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:271` | `<span>Official Gazette</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:305` | `<div className="py-12 text-center text-xs text-slate-500">Lo` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/app/sources/page.tsx:379` | `<div className="py-8 text-center text-xs text-slate-500">Loa` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/ConfidenceBadge.tsx:36` | `<span>Confidence: <strong>{confidence.level}</strong> ({Math` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/ConfidenceBadge.tsx:45` | `<span className="text-slate-500">Source Authority Hierarchy:` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/ConfidenceBadge.tsx:49` | `<span className="text-slate-500">Semantic Relevance:</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/ConfidenceBadge.tsx:53` | `<span className="text-slate-500">Jurisdictional Precision:</` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/ConfidenceBadge.tsx:57` | `<span className="text-slate-500">Citation Grounding:</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:48` | `<h3 className="font-semibold text-sm">Escalate to Certified ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:66` | `<h3 className="text-lg font-bold text-slate-900">Escalation ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:87` | `<label className="block text-xs font-semibold text-slate-700` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:99` | `<label className="block text-xs font-semibold text-slate-700` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:109` | `<label className="block text-xs font-semibold text-slate-700` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:120` | `<label className="block text-xs font-semibold text-slate-700` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:125` | `placeholder="Mention specific concerns regarding traditional` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/EscalationModal.tsx:132` | `<span>Prior AI analysis and retrieved statutory provisions w` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/Footer.tsx:21` | `<span className="ml-1 text-[10px] text-teal-400 font-bold up` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/Footer.tsx:72` | `<span>Facilitator Escalation Portal →</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/LegalDisclaimerBanner.tsx:13` | `<aside aria-label="Statutory Notice" className="bg-gradient-` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/LegalDisclaimerBanner.tsx:26` | `<span>Primary Statutory Grounding Active</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/Navbar.tsx:39` | `const navLinks = [` | **COPY** | messages/{en,hi,ta}.json | M11 |
| `frontend/src/components/Navbar.tsx:149` | `<span className="hidden sm:inline">International</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/Navbar.tsx:176` | `title="English"` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/Navbar.tsx:185` | `title="हिन्दी"` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/Navbar.tsx:194` | `title="தமிழ்"` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/SourceDrawer.tsx:18` | `<h3 className="font-semibold text-sm">Authoritative Source I` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/SourceDrawer.tsx:46` | `<span className="text-xs font-bold text-slate-500 uppercase ` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/SourceDrawer.tsx:52` | `<h4 className="text-xs font-bold text-slate-500 uppercase tr` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/SourceDrawer.tsx:60` | `<span className="text-xs text-slate-500">Version:</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/SourceDrawer.tsx:64` | `<span className="text-xs text-slate-500">Effective Date:</sp` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/components/SourceDrawer.tsx:77` | `<span>View Official Government Registry</span>` | **COPY** | messages/{en,hi,ta}.json via useTranslations() | M11 |
| `frontend/src/lib/api.ts:3` | `const API_BASE = process.env.NEXT_PUBLIC_API_URL \|\| 'http://` | **CONFIG** | process.env.NEXT_PUBLIC_API_URL | M11 |
