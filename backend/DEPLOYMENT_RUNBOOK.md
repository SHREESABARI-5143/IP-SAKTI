# IP-SAKTI Cloudflare Deployment Runbook

Complete isolated deployment guide for launching the serverless Python edge backend on Cloudflare Workers AI without altering legacy containerized scripts.

---

### 📋 Prerequisites & Environment Configuration
1. Cloudflare account with Workers & Workers AI enabled.
2. Serverless PostgreSQL connection string (Neon DB / Supabase pooler).
3. Node.js (>= 18.x) & npm.

---

### 🛠️ Execution Pipeline

#### 1. Authenticate with Cloudflare Wrangler CLI
```bash
npx wrangler login
```

#### 2. Configure Dynamic Environment Variables & Secrets
Inject your serverless database pooling URI into Cloudflare's encrypted vault for the isolated configuration:
```bash
npx wrangler secret put DATABASE_URL --config wrangler.edge.toml
```

Optional dynamic variables can be passed or updated directly in `wrangler.edge.toml` under `[vars]`:
- `ALLOWED_ORIGINS`: Comma-delimited list of allowed origins.
- `AI_MODEL`: Target model matrix (e.g., `@cf/qwen/qwen2.5-7b-instruct`).
- `DEFAULT_JURISDICTION`: Default jurisdiction scope (e.g., `India`).
- `FALLBACK_CITATION_NOTICE`: Citation threshold fallback text.

#### 3. Deploy Isolated Edge Backend
Deploy the edge bundle targeting the isolated config file:
```bash
npx wrangler deploy --config wrangler.edge.toml
```

---

### 🔍 Verification & Health Check
Verify active edge deployment health via curl or browser:
```bash
curl -X GET https://<your-worker-subdomain>.workers.dev/
```

Test edge RAG chat endpoint:
```bash
curl -X POST https://<your-worker-subdomain>.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Is traditional neem formulation patentable under Indian law?"}'
```
