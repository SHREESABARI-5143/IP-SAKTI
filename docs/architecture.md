# IP-SAKTI Sahayak — Architecture & C4 System Model

## 1. System Context Diagram (C4 Level 1)

```mermaid
graph TD
    User["Ayurvedic Innovator / MSME / Researcher"]
    Facilitator["Certified Human IP Facilitator"]
    Admin["National IP Officer / Admin"]

    IPSAKTI["IP-SAKTI Sahayak Platform\n(Multilingual Legal RAG Engine)"]
    
    DB[("PostgreSQL 16 + pgvector\n(Statutory Chunks & Tenant Vaults)")]
    OLLAMA["Local LLM Service\n(Ollama / vLLM / Synthesis)"]
    GovReg["Official Gazette Registries\n(CGPDTM, NBA, AYUSH, CDSCO, WIPO)"]

    User -->|Queries, Uploads, Formulations| IPSAKTI
    Facilitator -->|Reviews Escalated Tickets| IPSAKTI
    Admin -->|Monitors Telemetry & Benchmarks| IPSAKTI

    IPSAKTI <-->|Embeddings & Chunks| DB
    IPSAKTI <-->|Grounded Synthesis| OLLAMA
    IPSAKTI -.->|Live Verified Citations| GovReg
```

## 2. Container Diagram (C4 Level 2)

```mermaid
graph TD
    Client["Next.js 14 Web App\n(TypeScript, Tailwind, PWA)"]
    Nginx["Nginx Reverse Proxy & TLS\n(Port 80/443, Security Headers)"]
    API["FastAPI Application\n(Python 3.11, Uvicorn)"]
    
    subgraph Core Engine
        Orchestrator["Agent Orchestrator"]
        Classifier["Formulation Classifier"]
        ABS["ABS Assessment Agent"]
        Retriever["Dynamic Hybrid Retriever"]
        Verifier["Claim-Level Citation Verifier"]
        Scorer["Algorithmic Confidence Calculator"]
        Ingest["Live Ingestion Pipeline"]
    end

    DB[("PostgreSQL 16\n(pgvector + Full Text)")]

    Client -->|HTTPS| Nginx
    Nginx -->|Proxy /api/v1| API
    API --> Orchestrator
    Orchestrator --> Classifier
    Orchestrator --> ABS
    Orchestrator --> Ingest
    Orchestrator --> Retriever
    Retriever <--> DB
    Orchestrator --> Verifier
    Orchestrator --> Scorer
```

## 3. End-to-End Grounded Chat Execution Flow

1. **Input Sanitization**: Query is scrubbed of prompt-injection attempts and classified for intent (Greeting vs Legal Inquiry vs Out-of-Scope).
2. **Concept Normalization**: Multi-script Indic concepts (Hindi / Tamil / Tanglish) are normalized to canonical statutory terminology.
3. **Dynamic Retrieval**: Hybrid BM25 and vector similarity search queries live database chunks filtered strictly by Jurisdiction and Namespace.
4. **Answer Synthesis**: Pluggable LLM generates a structured legal assessment citing primary provisions `[1]`, `[2]`.
5. **Claim-Level Grounding**: `CitationVerifier` validates token overlap between claims and retrieved statutory evidence, removing ungrounded claims.
6. **Algorithmic Confidence**: Computes composite confidence based on authority hierarchy, retrieval relevance, and citation grounding. Low confidence triggers automatic safe abstention or human facilitator escalation.
