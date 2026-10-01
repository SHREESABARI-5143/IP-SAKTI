# IP-SAKTI Edge Deployment Runbook
## Serverless Cloudflare Architecture: Workers AI + Vectorize + D1

Edge-native architecture for Ayurvedic Intellectual Property protection with zero cold starts, zero external database costs, and grounded statutory citations.

---

### 🏛️ Architectural Data Split
1. **Cloudflare Vectorize (`VECTORIZE_INDEX`)**: Stores 768-dimensional dense vector embeddings (`@cf/baai/bge-base-en-v1.5`) of legal & patent documents for semantic similarity search.
2. **Cloudflare D1 (`DB`)**: Serverless edge SQL database storing structured statutory text (The Patents Act 1970, Biological Diversity Act 2002), canonical URLs, knowledge graph topology, and query audit logs.
3. **Cloudflare Workers AI (`AI`)**: Generates embeddings and orchestrates `@cf/qwen/qwen2.5-7b-instruct` to synthesize authoritative legal opinions with verified markdown links.

---

### 🛠️ Step-by-Step Provisioning & Deployment

All commands should be executed from the `backend/` directory:

```bash
cd backend
```

#### Step 1: Create the Cloudflare D1 Database
```bash
npx wrangler d1 create ip-sakti-db
```
*Note: Copy the `database_id` output by Wrangler and paste it into `wrangler.edge.toml` under `[[d1_databases]]`.*

#### Step 2: Initialize D1 Database Schema & Baseline Seeds
```bash
npx wrangler d1 execute ip-sakti-db --file=schema_d1.sql --remote
```

#### Step 3: Create the Cloudflare Vectorize Index
```bash
npx wrangler vectorize create ip-sakti-legal-embeddings --dimensions=768 --metric=cosine
```

#### Step 4: Deploy the Serverless Edge Backend
```bash
npx wrangler deploy --config wrangler.edge.toml
```

---

### 🔄 Ingest & Populate Live Vector Graph
Trigger the initial dynamic embedding and ingestion cycle into Vectorize + D1:
```bash
curl -X POST https://ip-sakti-backend-edge.<your-subdomain>.workers.dev/api/ingest/cycle \
  -H "Content-Type: application/json"
```

---

### 🔍 Verification & Health Check

#### 1. Check Health & Active Bindings
```bash
curl -X GET https://ip-sakti-backend-edge.<your-subdomain>.workers.dev/
```
Expected response:
```json
{
  "status": "active",
  "service": "IP-SAKTI Edge Legal Engine",
  "runtime": "Cloudflare Serverless Python Edge Node",
  "architecture": {
    "workers_ai": true,
    "cloudflare_d1": true,
    "cloudflare_vectorize": true,
    "zero_cost_edge_mode": true
  }
}
```

#### 2. Query Edge RAG Chat with Verified Statutory Citations
```bash
curl -X POST https://ip-sakti-backend-edge.<your-subdomain>.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Is traditional neem formulation patentable under Indian law?", "jurisdiction": "India"}'
```
