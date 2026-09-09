# IP-SAKTI Sahayak — Comprehensive System Audit

**Audit Date:** September 8, 2026  
**Auditor Roles:** Principal AI Engineer, Senior Full-Stack Engineer, RAG Architect, Cybersecurity Engineer, DevOps Engineer, Product Engineer  
**Repository:** `d:/Downloads/sih2026`  

---

## 1. Executive Summary

This audit evaluates the current architectural maturity, security posture, citation grounding, multilingual pipeline, RAG fidelity, database persistence, and user experience of **IP-SAKTI Sahayak** (Multilingual RAG-Based Intellectual Property & Regulatory Assistant for Ayurveda).

---

## 2. Component-by-Component Assessment Matrix

| Component | Status | Classification | Key Observations |
| :--- | :--- | :--- | :--- |
| **Frontend Architecture** | Working | `WORKING` | Next.js 14 App Router, Tailwind CSS, Plus Jakarta Sans font, Zustand state, Lucide icons. Responsive layout with 8 dedicated sub-routes (`/`, `/classify`, `/abs-helper`, `/ip-strategy`, `/products`, `/documents`, `/sources`, `/admin`). |
| **Zero-Hallucination Messaging** | Partially Working | `AI/RAG RISK` | Previous copy contained "Zero Hallucination Guarantee" which violates engineering rigor. Must be replaced with "Citation-grounded AI with evidence validation and safe abstention." |
| **Backend Architecture** | Working | `WORKING` | FastAPI framework with modular router organization under `/api/v1` (`chat`, `classify`, `abs`, `ip_strategy`, `products`, `documents`, `sources`, `admin`, `escalations`, `evaluation`, `auth`). |
| **Database & Persistence** | Working | `WORKING` | SQLAlchemy async ORM with SQLite default (with PostgreSQL connection string readiness). Models for Users, Sources, Versions, Chunks, Conversations, Messages, Citations, Products, Knowledge Entities, Escalations. |
| **Authentication & RBAC** | Partially Working | `SECURITY RISK` | Model supports password hashing and roles (`User`, `Researcher`, `Entrepreneur`, `IP Facilitator`, `Admin`), but frontend requests currently default to demo credentials if unauthenticated. Real JWT tokens and server-side RBAC guards needed. |
| **RAG Retrieval Engine** | Partially Working | `AI/RAG RISK` | Hybrid BM25 + Vector ranking with authority weighting. Needs semantic reranking, strict claim-level extraction, cross-source conflict detection, and deeper similarity thresholding. |
| **LLM Provider Abstraction** | Working | `WORKING` | Pluggable architecture supporting Google Gemini (`gemini-2.5-flash`), OpenAI, and a deterministic structured grounded fallback when API keys are absent. |
| **Citation Verification** | Partially Working | `AI/RAG RISK` | Regex citation scanner verifies provisions against retrieved chunks. Needs full claim-level validation to verify semantic support and reject hallucinated claims before final rendering. |
| **Statutory Knowledge Corpus** | Working | `WORKING` | High-fidelity seed corpus with ~30 authoritative provisions across Patents Act 1970 (Sec 3(p), 3(d), 10(4)), Biological Diversity Act 2002/2023, Drugs & Cosmetics Act Ch. IV-A / Rule 158B, FSSAI Ayurveda Aahar 2022, WIPO GRATK 2024, US FDA DSHEA, EU THMPD. Needs dynamic ingestion APIs without requiring code modification. |
| **Source Freshness & Versioning**| Working | `WORKING` | Schema tracks `version_tag`, `effective_from`, `checksum`, `status`. Needs active staleness background monitoring and admin freshness flags. |
| **Multilingual Pipeline** | Partially Working | `MULTILINGUAL RISK` | Language detection (EN/HI/TA) and terminology normalization with canonical concept IDs in place. Needs support for Hinglish, Tanglish mixed-code queries, and expanded Dravidian/Indo-Aryan languages. |
| **Document Processing & OCR** | Partially Working | `AI/RAG RISK` | Text file chunking and checksum hashing supported. Real PDF/DOCX/image extraction with numeric preservation (HPLC assays, herb ratios) and sandboxed prompt-injection defense required. |
| **Private Document Isolation** | Partially Working | `SECURITY RISK` | Database models link documents to `user_id`, but multi-tenant vector/retrieval isolation must be enforced strictly at the database/retrieval query layer. |
| **Human IP Facilitator Escalation** | Working | `WORKING` | Escalation modal and DB schema support packaging question, AI analysis, sources, and status workflows (`Submitted`, `Assigned`, `Under Review`, `Resolved`). |
| **Evaluation Framework** | Partially Working | `AI/RAG RISK` | Golden test dataset exists (`golden_dataset.json`), but automated scoring metrics (Recall@K, Groundedness, Citation Precision/Recall, Abstention Accuracy) need complete benchmark runners. |
| **Observability & Logging** | Partially Working | `SCALABILITY RISK` | Basic logging present. Needs structured JSON logs, request IDs, latency tracking (p50/p95/p99), and rate limiting. |

---

## 3. High-Priority Risk Categorization

1. **AI/RAG Risks**:
   - Absence of explicit claim-level decomposition and semantic verification before final response generation.
   - Ambiguous queries risking forced citations if retrieval confidence score is below threshold.
2. **Security Risks**:
   - Unauthenticated direct access allowed in local dev endpoints.
   - Untrusted file uploads in Private Vault requiring strict magic byte validation, size caps, and prompt-injection scrubbing.
3. **Multilingual Risks**:
   - Code-switched sentences (e.g. *"En product-ku Section 3(p) apply aaguma?"*) must be normalized to canonical legal concepts without losing intent.
