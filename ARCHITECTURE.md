# SYSTEM ARCHITECTURE — IP-SAKTI SAHAYAK

```text
                                  +---------------------------------------+
                                  |     IP-SAKTI Sahayak Web UI           |
                                  |  (Next.js 14, TailwindCSS, Lucide,   |
                                  |   Zustand, React Query, Radix UI)     |
                                  +-------------------+-------------------+
                                                      |
                                           REST API & SSE Streams
                                                      |
                                  +-------------------v-------------------+
                                  |       FastAPI Backend Gateway         |
                                  |  (Auth, RBAC, Rate Limiting, Audit)   |
                                  +-------------------+-------------------+
                                                      |
                  +-----------------------------------+-----------------------------------+
                  |                                   |                                   |
        +---------v---------+               +---------v---------+               +---------v---------+
        |   Auth & User     |               |   Orchestrator    |               |  Product & Docs   |
        |   Management      |               |  Specialist Agents|               |  Private Vault    |
        +-------------------+               +---------+---------+               +-------------------+
                                                      |
                            +-------------------------+-------------------------+
                            |                                                   |
                  +---------v---------+                               +---------v---------+
                  |  Query Router     |                               | Knowledge Graph   |
                  |  & Normalizer     |                               | (Multi-hop Entity |
                  |  (EN / HI / TA)   |                               |  Relationships)   |
                  +---------+---------+                               +---------+---------+
                            |                                                   |
                            +-------------------------+-------------------------+
                                                      |
                                            +---------v---------+
                                            | Hybrid Retriever  |
                                            | (Semantic + BM25  |
                                            |  + Metadata Filter|
                                            |  + Reranker)      |
                                            +---------+---------+
                                                      |
                                            +---------v---------+
                                            | Grounded Answer   |
                                            | Generator &       |
                                            | Citation Verifier |
                                            +---------+---------+
                                                      |
                                            +---------v---------+
                                            | Confidence &      |
                                            | Abstention Engine |
                                            +-------------------+
```

---

## Architectural Principles

1. **Strict Source Grounding**: No legal or regulatory claim is generated unless supported by an indexed primary provision.
2. **Deterministic Confidence & Abstention**: Confidence levels (High, Medium, Low, Abstain) are computed mathematically via source authority rankings, semantic distance, and citation grounding checks rather than arbitrary LLM output.
3. **Multi-Agent Specialist Modules**:
   - `QueryRouter`: Classifies user intent and assigns domain tags.
   - `MultilingualNormalizer`: Normalizes Devanagari and Tamil terms into canonical English legal concepts.
   - `ClassificationAgent`: Evaluates formulation status under Rule 158B, FSSAI Ayurveda Aahar 2022, and Phytopharmaceutical Drug guidelines.
   - `ABSComplianceAgent`: Assesses NBA Form I/III/IV and SBB Form A requirements under Biological Diversity Act 2023.
   - `IPStrategyAgent`: Synthesizes multi-route protection across Patents, Trademarks, GI, and Trade Secrets.
   - `CitationVerifier`: Validates post-generation citations against retrieved source IDs.
4. **Namespace Isolation for Private RAG**: Public statutory knowledge (`PUBLIC_KNOWLEDGE`) is strictly partitioned from confidential user dossiers (`PRIVATE_USER_DOCUMENTS`).
