# IP-SAKTI Cloudflare Deployment Runbook

Complete isolated deployment guide for launching the serverless Python edge backend on Cloudflare Workers AI with automated periodic vector graph self-ingestion and zero hardcoded static files.

---

### 📋 Prerequisites & Dynamic Environment Variables
1. **Cloudflare Account**: Workers AI and Python Workers enabled.
2. **PostgreSQL / Neon DB**: Serverless database for live vector and graph storage.
3. **Dynamic Variables** (configured in `wrangler.edge.toml` or as Secrets):
   - `DATABASE_URL`: Serverless PostgreSQL pooling URI (Encrypted Secret).
   - `DYNAMIC_REGISTRY_FEEDS`: Optional JSON string of dynamic open statutory registry feeds.
   - `ALLOWED_ORIGINS`: Comma-delimited CORS list.
   - `AI_MODEL`: Workers AI model identifier (`@cf/qwen/qwen2.5-7b-instruct`).

---

### 🛠️ Execution Pipeline

#### 1. Authenticate with Cloudflare Wrangler CLI
```bash
npx wrangler login
```

#### 2. Provision Encrypted Database Secret
```bash
npx wrangler secret put DATABASE_URL --config wrangler.edge.toml
```

#### 3. Deploy Isolated Edge Backend
```bash
npx wrangler deploy --config wrangler.edge.toml
```

---

### 🔄 Dynamic Periodic Vector Graph Self-Ingestion

Cloudflare Workers will automatically trigger the periodic self-ingestion cycle based on the configured cron trigger:
```toml
[triggers]
crons = [ "0 2 * * *" ] # Daily at 02:00 UTC
```

You can also trigger an on-demand self-ingestion cycle dynamically via HTTP POST without storing any files locally:
```bash
curl -X POST https://<your-worker-subdomain>.workers.dev/api/ingest/cycle \
  -H "Content-Type: application/json" \
  -d '{
    "sources": [
      {
        "statute": "The Patents Act, 1970",
        "section": "Section 3(p)",
        "title": "Traditional Knowledge Patent Exclusions",
        "jurisdiction": "India",
        "doc_type": "statute",
        "url": "https://www.indiacode.nic.in/show-data?actid=AC_CEN_3_44_00007_197039_1517807323983&sectionId=15154&sectionno=3&orderno=3",
        "content": "An invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not patentable."
      },
      {
        "statute": "Biological Diversity Act, 2002",
        "section": "Section 6",
        "title": "Mandatory NBA Approval for IP Filing",
        "jurisdiction": "India",
        "doc_type": "statute",
        "url": "http://nbaindia.org/content/26/59/1/rules.html",
        "content": "No person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the previous approval of the National Biodiversity Authority."
      }
    ]
  }'
```

---

### 🔍 Verification & Health Check
Verify active edge deployment health:
```bash
curl -X GET https://<your-worker-subdomain>.workers.dev/
```

Query edge RAG chat endpoint:
```bash
curl -X POST https://<your-worker-subdomain>.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Is traditional neem formulation patentable under Indian law?", "jurisdiction": "India"}'
```
```
