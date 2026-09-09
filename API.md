# REST API REFERENCE — IP-SAKTI SAHAYAK

Base URL: `/api/v1`

## 1. Authentication & Users
- `POST /api/v1/auth/register` — Register a new innovator or organization account.
- `POST /api/v1/auth/login` — Login and receive JWT access token.
- `GET /api/v1/auth/demo-token?role=user` — Get instantaneous demo session token.

## 2. Conversational Intelligence & Copilot
- `POST /api/v1/chat` — Core RAG Copilot endpoint.
  - **Body**:
    ```json
    {
      "message": "Can I patent my new Ayurvedic formulation with turmeric?",
      "jurisdiction": "India",
      "selected_country": null,
      "language": "en"
    }
    ```
  - **Response**: Returns grounded short answer, full markdown analysis, confidence metrics, and verified citations list.
- `GET /api/v1/chat/conversations/{id}/messages` — Retrieve conversational history and citation cards.

## 3. Formulation Classification
- `POST /api/v1/classify` — Classify Ayurvedic formulation across Rule 158B, Ayurveda Aahar, Phytopharmaceuticals, and Cosmetics.

## 4. Access and Benefit Sharing (ABS)
- `POST /api/v1/abs/assessment` — Evaluate Biological Diversity Act 2023 compliance, NBA Form III requirements, and benefit-sharing rates.

## 5. IP Protection Strategy Matrix
- `POST /api/v1/ip/assessment` — Multi-route IP evaluation (Patents, Trademarks, GI, Trade Secrets, PPV&FRA).

## 6. Product Portfolio & Workspaces
- `GET /api/v1/products` — List user products.
- `POST /api/v1/products` — Create new formulation workspace with botanical ingredients.
- `DELETE /api/v1/products/{id}` — Delete formulation workspace.

## 7. Private Document Vault (Private RAG)
- `POST /api/v1/documents/upload` — Upload PDF/DOCX/TXT file for secure text extraction and namespace-isolated indexing.
- `GET /api/v1/documents` — List user private documents.

## 8. Authoritative Sources & Registry
- `GET /api/v1/sources` — Query authoritative source registry by jurisdiction and domain.
- `GET /api/v1/sources/chunks` — Browse individual statutory provisions and citations.

## 9. Human IP Facilitator Escalation
- `POST /api/v1/escalations` — Package inquiry and AI analysis into formal facilitator ticket.
- `GET /api/v1/escalations` — List escalation tickets.
- `PATCH /api/v1/escalations/{id}` — Update ticket assignment and advisory notes.

## 10. Admin & AI Benchmark Evaluation
- `GET /api/v1/admin/stats` — Platform telemetry metrics and grounding analytics.
- `GET /api/v1/admin/health` — System health and active components status.
- `POST /api/v1/evaluation/run-benchmark` — Execute automated 25+ Golden Dataset test suite.
