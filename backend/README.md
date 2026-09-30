---
title: AYURA Backend API
emoji: 🌿
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: apache-2.0
---

# AYURA (IP-SAKTI Sahayak) Backend API

FastAPI backend service powering source-cited, jurisdiction-aware AI assistance, pharmacopoeial prior-art search, and statutory product classification for Ayurvedic medicine.

### Endpoints
- `GET /health` - System status and API health check
- `POST /api/query/` - Grounded RAG legal query engine
- `POST /api/classify/start` - 6-category ASU product classification wizard
- `POST /api/prior-art/search` - Classical AFI/API vector monograph search
- `GET /docs` - Interactive Swagger API documentation
