# IP-SAKTI Sahayak
### Multilingual RAG-Based Intellectual Property & Regulatory AI Assistant for Ayurveda

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Frontend-Next.js%2014-black.svg)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**IP-SAKTI Sahayak** is an enterprise-grade, source-grounded AI copilot and regulatory intelligence platform designed specifically for the **Ayurveda and AYUSH ecosystem** (practitioners, researchers, startups, MSMEs, exporters, and technology transfer offices).

It delivers verifiable legal and regulatory guidance grounded in primary Indian statutes, official pharmacopoeias, and international trade treaties—with **zero hallucinated citations**, strict jurisdictional separation, and instant escalation to certified human IP facilitators.

---

## 🌟 Key Features

1. **Zero Hallucination & Source Grounding**: Every legal claim is verified and cross-referenced with official statutes (The Patents Act 1970 Sec 3(p)/3(d)/10(4), Biological Diversity Act 2002 & 2023, Drugs & Cosmetics Act 1940 Chapter IV-A / Rule 158B, FSSAI Ayurveda Aahar Regulations 2022).
2. **Explicit Jurisdiction Switching**: Toggle seamlessly between `[ India ]` and `[ International ]` (USA, EU, UK, Japan, Australia, UAE, Singapore).
3. **Formulation Classification Engine**: Guided decision tree identifying Classical Ayurvedic Medicines, Patent/Proprietary (Rule 158B), Phytopharmaceuticals, Ayurveda Aahar, and Cosmetics.
4. **ABS Compliance Helper**: 9-step assessment identifying National Biodiversity Authority (NBA) vs State Biodiversity Board (SBB) obligations, Form I/III/IV filings, and benefit-sharing rates.
5. **Multi-Route IP Strategy Matrix**: Evaluates Patents, Trademarks (Nice Class 5/30), GI tags, Trade Secrets, and Plant Variety Protection (PPV&FRA).
6. **Product Innovation Workspace**: Manage formulation profiles, botanical origins, and export dossiers.
7. **Private Document Vault (Private RAG)**: Upload proprietary PDF/DOCX formulation dossiers into isolated `PRIVATE_USER_DOCUMENTS` namespaces with zero data leakage.
8. **Trilingual Language Engine**: Native multilingual support for English, हिन्दी (Hindi), and தமிழ் (Tamil) with controlled legal concept normalization.
9. **Algorithmic Confidence Meter**: Real-time confidence breakdown based on authority hierarchy, semantic distance, recency, and citation grounding.
10. **Human IP Facilitator Escalation**: Package complex FTO and patent drafting queries for review by authorized IP facilitators.
11. **Admin Console & Telemetry**: Live telemetry dashboard, audit log inspection, and automated Golden Dataset benchmarking.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ / 20+
- npm or yarn

### 1. Backend Setup

```bash
# Clone repository and navigate to root
cd sih2026

# Install Python dependencies
pip install -r backend/requirements.txt

# Run backend test suite
$env:PYTHONPATH="." # Windows PowerShell (or export PYTHONPATH="." on Linux/Mac)
python backend/tests/smoke_test.py

# Start FastAPI server on port 8000
python -m uvicorn backend.app.main:app --reload --port 8000
```

FastAPI OpenAPI Interactive Documentation will be live at: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
# Navigate to frontend folder
cd frontend

# Install npm dependencies
npm install

# Start Next.js development server
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 🐳 Docker Deployment

Run the entire full-stack platform using Docker Compose:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## 📚 Documentation Index

- [Architecture Overview](ARCHITECTURE.md)
- [REST API Reference](API.md)
- [Database Schema & Migrations](DATABASE.md)
- [Hybrid RAG & Retrieval Engine](RAG.md)
- [Knowledge Ingestion & Corpus](KNOWLEDGE_INGESTION.md)
- [Security & Prompt-Injection Defense](SECURITY.md)
- [Production Deployment Guide](DEPLOYMENT.md)
- [AI Evaluation & Golden Benchmark](EVALUATION.md)
- [Contributing Guidelines](CONTRIBUTING.md)
