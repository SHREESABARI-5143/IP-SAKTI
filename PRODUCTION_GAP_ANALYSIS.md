# IP-SAKTI Sahayak — Production Gap Analysis & Remediation Roadmap

**Document Version:** 1.0 (Production Target)  
**Target Architecture:** Enterprise-Grade Multilingual Legal & Regulatory AI Platform for Ayurveda  

---

## 1. Classification of Current Capabilities

### 🟢 `WORKING`
1. **FastAPI Application Skeleton**: Async DB lifecycle, CORS, route grouping under `/api/v1`.
2. **Next.js 14 Frontend**: Plus Jakarta Sans design, responsive navbar, zero text-wrapping glitches, clean modern cards, trilingual UI toggles (EN/HI/TA), jurisdiction toggle (India vs. International).
3. **Primary Statutory Baseline Corpus**: High-authority provisions from Patents Act 1970, BD Act 2023, D&C Act Rule 158B, FSSAI 2022, WIPO GRATK 2024, US FDA DSHEA, Nagoya Protocol.
4. **Intent Classification & Greeting Guard**: Filters greetings and general queries in EN/HI/TA without spurious legal citations.
5. **Formulation Classifier, ABS Helper & IP Strategy Engines**: Deterministic statutory decision trees covering ASU Classical vs Proprietary vs Ayurveda Aahar and NBA Form III mandates.
6. **Knowledge Graph Subgraph Engine**: Multi-hop entity exploration across Acts, Sections, Herbs, Regulatory Bodies, and International Treaties.
7. **Human IP Facilitator Escalation Workflow**: Ticket creation, status tracking, and notes management.

---

### 🟡 `PARTIALLY WORKING`
1. **Citation & Claim Grounding**:
   - *Current:* Post-generation regex matching against retrieved chunks.
   - *Required:* Strict claim decomposition (`Claim -> Evidence chunk -> Semantic verification -> Verified Citation | Reject Claim`).
2. **Multilingual Pipeline**:
   - *Current:* English, Hindi, Tamil dictionary normalization.
   - *Required:* Robust Tanglish / Hinglish transliteration handling, Dravidian/Indo-Aryan expansion architecture, and native-language response synthesis without translating official statutory act titles.
3. **Safe Abstention Protocol**:
   - *Current:* Abstains on empty retrieval or safety flags.
   - *Required:* Explicit multi-criteria abstention (conflicting sources, weak evidence relevance score < 0.65, unverified international country law, ambiguous legal facts).
4. **Document Ingestion & OCR**:
   - *Current:* Basic text file upload and chunking.
   - *Required:* Robust multi-format parsing (PDF, scanned documents, text) with numeric integrity preservation for formulation ratios, HPLC assays, and chromatography peaks.
5. **Evaluation Suite**:
   - *Current:* Basic smoke tests and sample golden dataset.
   - *Required:* Automated evaluation harness computing `grounded_answer_rate`, `citation_precision`, `citation_recall`, `unsupported_claim_rate`, `abstention_accuracy`, and `retrieval_recall`.

---

### 🔴 `MISSING` & `RISKS`
1. **`AI/RAG RISK` — Removal of "Zero Hallucination" claims**:
   - *Action:* Replace all instances with "Citation-grounded AI with evidence validation and safe abstention".
2. **`SECURITY RISK` — Real Authentication, JWT, and Multi-Tenant Isolation**:
   - *Action:* Implement real JWT token generation, password hashing verification, middleware route guards, and enforce tenant isolation on private documents.
3. **`SECURITY RISK` — Sandboxed Prompt-Injection Defense in Document Processing**:
   - *Action:* Sanitize uploaded documents and treat all retrieved content strictly as passive data, preventing indirect prompt injection.
4. **`SCALABILITY RISK` — Dynamic Source Ingestion Admin**:
   - *Action:* Allow admins to add, version, refresh, and inspect sources via REST API without code modification.
5. **`OBSERVABILITY RISK` — Request Tracing & Structured Logging**:
   - *Action:* Add request ID middleware, latency logging, structured JSON logs, and health readiness endpoints (`/health`, `/ready`).

---

## 2. Implementation Execution Plan

```mermaid
graph TD
    A[Phase 1: Messaging & Grounding Guardrails] --> B[Phase 2: Real JWT Auth & RBAC Security]
    B --> C[Phase 3: Production Hybrid RAG & Claim-Level Grounding]
    C --> D[Phase 4: Multilingual Engine (Hinglish/Tanglish + Native Output)]
    D --> E[Phase 5: Secure Document Processing & Numeric OCR]
    E --> F[Phase 6: Dynamic Admin Source Management & Freshness]
    F --> G[Phase 7: Automated Evaluation & Test Harness]
    G --> H[Phase 8: Frontend Alignment & Verification]
```
