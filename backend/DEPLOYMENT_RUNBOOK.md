# IP-SAKTI Edge Deployment Runbook
## Serverless Cloudflare Architecture: Workers AI + Vectorize + D1

Edge-native architecture for Ayurvedic Intellectual Property protection with zero cold starts, zero external database costs, and grounded statutory citations.

---

### 🏛️ Architectural Data Split
1. **Cloudflare Vectorize (`VECTORIZE`)**: Stores 768-dimensional dense vector embeddings (`@cf/baai/bge-base-en-v1.5`) of legal & patent documents for semantic similarity search.
2. **Cloudflare D1 (`DB`)**: Serverless edge SQL database (`2977e86c-96a6-4a7a-babe-8d61c744952b`) storing structured statutory text, canonical URLs, and query audit logs.
3. **Cloudflare Workers AI (`AI`)**: Generates embeddings and orchestrates `@cf/qwen/qwen2.5-7b-instruct` to synthesize authoritative legal opinions with verified markdown links.

---

### 🛠️ One-Step Edge Deployment

Navigate to the isolated `backend/edge` directory:

```bash
cd backend/edge
```

Deploy directly to Cloudflare:
```bash
npx wrangler deploy
```

*(This uploads only the clean edge worker code in under **10 KiB**, without bundling `.venv` or encountering pip module errors).*

---

### 🔄 Ingest & Populate Live Vector Graph
Trigger the dynamic embedding and ingestion cycle into Vectorize + D1:
```bash
curl -X POST https://ip-sakti-backend-edge.<your-subdomain>.workers.dev/api/ingest/cycle
```

---

### 🔍 Verification & Health Check

#### 1. Check Health & Active Bindings
```bash
curl -X GET https://ip-sakti-backend-edge.<your-subdomain>.workers.dev/api/health
```

#### 2. Query Edge RAG Chat with Verified Statutory Citations
```bash
curl -X POST https://ip-sakti-backend-edge.<your-subdomain>.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Is traditional turmeric formulation patentable under Indian law?", "jurisdiction": "India"}'
```
