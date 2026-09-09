# SECURITY & PRIVACY CONTROLS — IP-SAKTI SAHAYAK

IP-SAKTI Sahayak is engineered with security and data privacy best practices, conforming to standard application security requirements and alignment with data protection principles.

---

## 1. Prompt-Injection & Jailbreak Defense

Untrusted user inputs and retrieved document chunks are strictly sanitized before LLM context construction:
- Regex-based filtering of prompt injection triggers (`ignore previous instructions`, `DAN mode`, `system prompt override`).
- **Data vs. Instruction Separation**: Retrieved texts are framed strictly as *read-only factual data*, preventing malicious embedded instructions inside user PDFs from hijacking system behavior.

---

## 2. Multi-Tenant Namespace Isolation

- Public statutory documents are stored in the global `PUBLIC_KNOWLEDGE` namespace.
- Private uploaded files are indexed in the `PRIVATE_USER_DOCUMENTS` namespace keyed by user/organization ID.
- Cross-tenant queries are blocked at the retrieval pre-filtering layer.

---

## 3. Authentication & RBAC

- Password hashing using salted cryptographic SHA-256 / PBKDF2.
- JWT Access tokens with configurable expiration.
- Role-based permissions (`user`, `facilitator`, `admin`).

---

## 4. Audit & Telemetry Logging

- Every query is logged with timestamp, user ID, latency ms, policy checks, retrieved source IDs, and computed confidence score in the `audit_logs` table.
