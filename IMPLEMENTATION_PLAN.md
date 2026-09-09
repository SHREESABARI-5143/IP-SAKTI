# IMPLEMENTATION PLAN — IP-SAKTI SAHAYAK

**Multilingual RAG-Based Intellectual Property & Regulatory AI Assistant for Ayurveda**

---

## 1. Current Architecture
- Fresh empty workspace (`d:\Downloads\sih2026`).
- Available toolchain: Python 3.10.0, Node.js v22.17.0, npm 11.4.2, Git 2.50.1.

---

## 2. Problems & Challenges Addressed
1. **Hallucination Risk in Legal/Regulatory Domains**: LLMs hallucinating patent clauses, sections, or regulatory rules can lead to invalid patent filings or statutory violations.
2. **Jurisdiction Confusion**: Mixing Indian statutory exclusions (e.g., Section 3(p) of the Patents Act) with US/EU patentability standards or FDA/EMA classifications.
3. **Complex AYUSH Regulatory Landscape**: Navigating distinctions between Classical Ayurvedic Medicines (Rule 158B), Patent/Proprietary ASU medicines, Phytopharmaceuticals, Ayurveda Aahar (FSSAI 2022), and cosmetics.
4. **Access and Benefit Sharing (ABS) Non-Compliance**: Lack of awareness regarding mandatory National Biodiversity Authority (NBA) & State Biodiversity Board (SBB) approvals under the Biological Diversity Act, 2002 & 2023 Amendment.
5. **Multilingual Barrier**: Lack of specialized legal/regulatory AI in Indian regional languages (Hindi, Tamil) with accurate terminology translation.

---

## 3. Target Architecture
- **Frontend**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide Icons, Radix UI components, Zustand state management, TanStack React Query.
- **Backend API**: Python FastAPI, Pydantic v2, SQLAlchemy ORM (SQLite for zero-config local run with full PostgreSQL/pgvector compatibility), JWT Authentication, RBAC, Structured Logging.
- **RAG & Agent Orchestration**:
  - Multi-stage Hybrid Retriever (BM25 keyword search + Vector embeddings + Metadata filters).
  - Cross-encoder / Authority-based Reranking.
  - Relational Knowledge Graph Engine for multi-hop statutory linkages.
  - Post-generation Citation Verifier & Claim Grounding Validator.
  - Algorithmic Confidence Scorer & Graceful Abstention Engine.
  - Controlled Specialist Agents (QueryRouter, JurisdictionAgent, ClassificationAgent, IPAnalysisAgent, RegulatoryAgent, ABSAgent, SafetyAgent).
- **Multilingual Support**: Controlled legal dictionary for English, Hindi, and Tamil with semantic normalization.
- **Private RAG**: User-isolated document vault with separate namespace indexing (`PUBLIC_KNOWLEDGE`, `PRIVATE_USER_DOCUMENTS`).

---

## 4. Files to Create

### Backend (`/backend`)
1. `backend/requirements.txt`: FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic, PyJWT, passlib, python-multipart, numpy, scikit-learn, rank-bm25, pytest, httpx.
2. `backend/app/main.py`: FastAPI server setup, CORS, lifespan handlers, API routers.
3. `backend/app/core/config.py`: Environment configuration and settings.
4. `backend/app/core/database.py`: SQLAlchemy session and async/sync engine.
5. `backend/app/core/security.py`: JWT, password hashing, prompt-injection defense, sanitizers.
6. `backend/app/models/`: Database models (`user.py`, `conversation.py`, `product.py`, `source.py`, `document.py`, `knowledge_graph.py`, `escalation.py`, `audit.py`).
7. `backend/app/schemas/`: Pydantic validation schemas (`auth.py`, `chat.py`, `classification.py`, `abs.py`, `ip_strategy.py`, `sources.py`, `products.py`, `admin.py`).
8. `backend/app/rag/`:
   - `retriever.py`: Hybrid BM25 + Vector + Metadata filter retriever.
   - `reranker.py`: Weighted composite scorer.
   - `citation_verifier.py`: Grounding & verification validator.
   - `confidence.py`: Algorithmic confidence score engine.
   - `llm_provider.py`: Pluggable LLM interface (Gemini / OpenAI / Anthropic / Local).
9. `backend/app/knowledge_graph/engine.py`: Knowledge graph entity and relation traversal.
10. `backend/app/multilingual/`: Controlled vocabulary dictionary & concept normalizer for EN/HI/TA.
11. `backend/app/agents/`: Modular specialist agents (`orchestrator.py`, `classification_agent.py`, `ip_agent.py`, `abs_agent.py`, `regulatory_agent.py`, `international_agent.py`, `safety_agent.py`).
12. `backend/app/ingestion/`: Authoritative legal corpus seeder, versioned document chunker, and source registry manager.
13. `backend/app/api/v1/`: API endpoints (`auth.py`, `chat.py`, `classify.py`, `abs.py`, `ip_strategy.py`, `products.py`, `documents.py`, `sources.py`, `escalations.py`, `admin.py`, `evaluation.py`).

### Frontend (`/frontend`)
1. `frontend/package.json`: Next.js 14, React, TypeScript, TailwindCSS, Lucide, Radix UI, Zustand, TanStack Query, Axios.
2. `frontend/src/app/`:
   - `layout.tsx`: Root layout with Navbar, Footer, Language/Jurisdiction provider, Legal Disclaimer banner.
   - `page.tsx`: Landing page with hero, quick-start prompts, feature highlights, and authority stats.
   - `chat/page.tsx`: Full legal research AI copilot with streaming, source drawer, confidence badge, and facilitator escalation.
   - `classify/page.tsx`: Step-by-step Ayurvedic Formulation Classification Wizard.
   - `abs-helper/page.tsx`: 9-step Biological Diversity & ABS Compliance Assessment tool.
   - `ip-strategy/page.tsx`: Interactive IP Protection Route Matrix (Patent, TM, GI, Copyright, Design, Plant Variety, Trade Secret).
   - `products/page.tsx`: Product Workspace for managing formulations, ingredients, export targets, and generating full landscape reports.
   - `documents/page.tsx`: Private Document Vault for uploading PDFs/DOCXs with isolated private RAG.
   - `sources/page.tsx`: Authoritative Source & Registry Explorer with version history and freshness flags.
   - `admin/page.tsx`: Admin Console for sources, crawlers, evaluations, abstention telemetry, and escalation management.
3. `frontend/src/components/`: Reusable UI components (Navbar, JurisdictionSwitch, LanguageSelector, SourcePanel, ConfidenceMeter, DisclaimerModal, EscalationModal, ExportButton).
4. `frontend/src/lib/`: API client, Zustand stores, language dictionaries, types.

### Testing, Data & DevOps
1. `backend/tests/`: Comprehensive test suite (`test_auth.py`, `test_rag.py`, `test_classification.py`, `test_abs.py`, `test_citation_verification.py`, `test_security.py`).
2. `backend/app/evaluation/golden_dataset.json`: 25+ benchmark evaluation test cases.
3. `backend/app/evaluation/evaluate.py`: Automated evaluation script for Groundedness, Citation Accuracy, and Recall.
4. `Dockerfile.backend`, `Dockerfile.frontend`, `docker-compose.yml`.
5. Documentation: `README.md`, `ARCHITECTURE.md`, `API.md`, `DATABASE.md`, `RAG.md`, `KNOWLEDGE_INGESTION.md`, `SECURITY.md`, `DEPLOYMENT.md`, `EVALUATION.md`, `CONTRIBUTING.md`.

---

## 5. Database Schema
- `users`: User identity, roles (user, facilitator, admin), organization ID.
- `conversations` & `messages`: Threaded legal research sessions with detected jurisdiction, domain, confidence, and feedback.
- `sources` & `source_versions`: Authoritative legal acts, rules, treaties, and notifications with checksums, validity dates, and URLs.
- `document_chunks`: Processed text embeddings, token lengths, metadata tags, and namespace partitions.
- `citations`: Relational link between generated messages, specific claims, and authoritative source chunks.
- `products` & `ingredients`: User-defined formulations, biological origins, classical text references, and target markets.
- `abs_assessments`: SBB/NBA evaluation records and risk ratings.
- `ip_assessments`: IP strategy matrices and patent eligibility reviews.
- `escalations`: Human IP facilitator review requests and status workflows.
- `knowledge_entities` & `knowledge_relationships`: Graph nodes (Law, Rule, Section, Authority, Herb, Formulation, Treaty) and edges.
- `audit_logs`: Query, latency, retrieval telemetry, policy decisions, and security events.

---

## 6. Implementation Phases
- **Phase 1**: Foundation & Architecture Setup (FastAPI structure, DB models, Next.js framework, styling tokens, security).
- **Phase 2**: Authoritative Knowledge Corpus & Hybrid RAG Engine (Statutory ingestion, BM25 + Vector retrieval, citation verifier, confidence scorer).
- **Phase 3**: Domain Intelligence Engines (Formulation Classifier, ABS Compliance Helper, IP Strategy Matrix, International/Export framework).
- **Phase 4**: Relational Knowledge Graph Engine & Specialist Agent Orchestrator.
- **Phase 5**: Multilingual Normalization & Terminology Translation (EN / HI / TA).
- **Phase 6**: Enterprise UI & Interactive Workspaces (Research Copilot, Formulation Wizard, ABS Flow, Product Workspace, Document Vault).
- **Phase 7**: Admin Console, Facilitator Escalations, Audit Telemetry, and Golden Dataset Evaluation.
- **Phase 8**: Verification, Testing, Docker/Deployment configs, and Complete Documentation.
