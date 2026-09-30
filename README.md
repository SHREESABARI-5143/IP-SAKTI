<div align="center">

# 🌿 AYURA — IP-SAKTI Sahayak
### AI-Powered Statutory IP Law, Prior-Art Search & ASU Product Classification Engine
**Smart India Hackathon (SIH) | Problem Statement: Ministry of Ayush**

[![CI Build](https://github.com/SHREESABARI-5143/IP-SAKTI/actions/workflows/ci.yml/badge.svg)](https://github.com/SHREESABARI-5143/IP-SAKTI/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Next.js 16](https://img.shields.io/badge/Frontend-Next.js_16_Turbopack-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_v2.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![AWS Serverless](https://img.shields.io/badge/Cloud-AWS_Lambda_Function_URL-FF9900?logo=amazon-aws)](https://aws.amazon.com/lambda/)
[![Cloudflare Pages](https://img.shields.io/badge/Edge-Cloudflare_Pages-F38020?logo=cloudflare)](https://pages.cloudflare.com/)
[![Groq Llama 3.3](https://img.shields.io/badge/LLM-Llama_3.3_70B_Versatile-f55036?logo=groq)](https://groq.com/)

[**Live Demo (Cloudflare)**](https://ayura.pages.dev) • [**API Docs**](https://ayura.pages.dev/docs) • [**Report Bug**](https://github.com/SHREESABARI-5143/IP-SAKTI/issues) • [**Request Feature**](https://github.com/SHREESABARI-5143/IP-SAKTI/issues)

</div>

---

## 📌 Problem Statement & Overview

Ayurveda and Indian Systems of Medicine (ASU) encompass thousands of years of classical traditional knowledge documented in ancient texts. However, modern researchers, pharmaceutical MSMEs, vaidyas, and startups face severe legal complexity:

1. **Biopiracy & Patent Eligibility (Section 3(p))**: Distinguishing patentable technological extractions from non-patentable traditional formulations.
2. **Statutory Classification Under Rule 158-B**: Navigating the Drugs & Cosmetics Rules, 1945 across 6 discrete licensing categories (Classical, Proprietary, Phytopharmaceutical, etc.).
3. **Biodiversity Approvals (NBA Section 6)**: Ensuring compliance with the Biological Diversity Act, 2002 before filing domestic or international patent claims.
4. **Multilingual Barrier**: Lack of authentic, source-cited legal guidance accessible in native Indic languages.

**AYURA (IP-SAKTI Sahayak)** is an enterprise-grade, source-cited, jurisdiction-aware AI system designed to resolve these regulatory bottlenecks with **100% statutory grounding** and zero hallucination.

---

## ✨ Key Capabilities

| Feature | Description |
| :--- | :--- |
| **🌐 Dual Jurisdiction Engine** | Switch seamlessly between **India Jurisdiction** (Classical Ayurvedic Emerald Mandala) and **International Jurisdiction** (3D Interactive Rotating World Globe for WIPO, TRIPS, PCT, and CBD treaties). |
| **⚖️ 6-Category ASU Classifier** | Step-by-step statutory wizard mapping products to Form 25-D, Rule 158-B, FSSAI Ayush Aahar, or CDSCO Phytopharmaceutical pathways with exact licensing checklists. |
| **📜 Graph-Hybrid RAG Engine** | Traverses 57 statutory provisions across 29 directed graph edges to verify temporal validity (AMENDS, REPEALS, CROSS-REFERENCES) before synthesis. |
| **🔬 Pharmacopoeial Prior-Art Search** | Ingests formulations from the Ayurvedic Formulary of India (AFI) and Ayurvedic Pharmacopoeia of India (API) for instant vector novelty screening. |
| **🗣️ 7 Indic Languages** | Native, full-context support in English, Hindi (हिन्दी), Sanskrit (संस्कृतम्), Tamil (தமிழ்), Telugu (తెలుగు), Marathi (मराठी), and Bengali (বাংলা). |
| **⚡ 100% Free Serverless Cloud** | Operates with zero hosting costs using Cloudflare Pages, AWS Lambda Function URLs, and Groq Serverless Llama 3.3 inference. |

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Client ["Client Layer (Cloudflare Pages)"]
        UI["React 19 / Next.js 16 SPA\nTailwind CSS v4 + 3D Three.js Globe\nClient-side Indic I18n Engine"]
    end

    subgraph Serverless ["Compute Layer (AWS Lambda)"]
        FURL["Lambda Function URL (HTTPS / CORS)"]
        ASGI["Mangum Adapter"]
        API["FastAPI 2.0 Core Service"]
        FURL --> ASGI --> API
    end

    subgraph Engine ["RAG & Reasoning Engine"]
        QP["Agent 1: Query Planner\n(Intent & Language Decomposition)"]
        VS["Agent 2: Hybrid Retrieval\n(Dense Vector + BM25 Lexical)"]
        KG["Agent 3: Validity Checker\n(Temporal Knowledge Graph)"]
        LLM["Agent 4: Citation Synthesis\n(Groq Llama 3.3 70B Versatile)"]
        
        API --> QP --> VS --> KG --> LLM
    end

    subgraph DataStore ["External Managed Data Tier"]
        QD[("Qdrant Cloud\nVector Corpus")]
        GROQ[("Groq Cloud\nInference Acceleration")]
        VS <--> QD
        LLM <--> GROQ
    end

    UI -->|REST / JSON| FURL
```

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 16 (Turbopack, Static HTML Export), React 19, Tailwind CSS v4, Lucide Icons, Three.js / Canvas.
- **Backend**: Python 3.11, FastAPI, Mangum ASGI Adapter, Uvicorn, SQLAlchemy.
- **AI & NLP**: Serverless Llama 3.3 70B via Groq API, Google Gemini Flash (fallback), Qwen 2.5 (offline local).
- **Vector Database**: Qdrant Vector Cloud (Cosine similarity on 768-dim embeddings).
- **Deployment**: Cloudflare Pages (Frontend CDN), AWS Lambda (Serverless Compute), Docker (Container images).

---

## 🚀 Quickstart: Local Development

### Prerequisites
- Node.js 20+ and npm
- Python 3.11+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/SHREESABARI-5143/IP-SAKTI.git
cd IP-SAKTI
```

### 2. Run the Backend API
```bash
cd backend
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The interactive Swagger API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 3. Run the Frontend Application
```bash
cd ../frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## ☁️ 100% Free-Tier Cloud Deployment

| Service | Component | Free Tier Quota | Cost |
| :--- | :--- | :--- | :--- |
| **Cloudflare Pages** | Frontend Static Export | Unlimited requests, unlimited bandwidth | **$0.00** |
| **AWS Lambda** | Backend ASGI Container | 1M requests/mo + 3.2M compute seconds | **$0.00** |
| **Groq Cloud** | Llama 3.3 70B Serverless | ~250-300 tokens/sec, generous free tier | **$0.00** |
| **Qdrant Cloud** | Vector Monograph DB | 1GB persistent cluster forever | **$0.00** |

Refer to our complete [Deployment Playbook](https://github.com/SHREESABARI-5143/IP-SAKTI/blob/main/backend/README.md) for step-by-step guides.

---

## 🤝 Contributing

We welcome contributions from researchers, software developers, and legal scholars! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting pull requests.

---

## 🛡️ Security

For vulnerability disclosures and reporting procedures, please review our [Security Policy](SECURITY.md).

---

## 📄 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Developed with 💚 for the Smart India Hackathon | Ministry of Ayush</sub>
</div>
