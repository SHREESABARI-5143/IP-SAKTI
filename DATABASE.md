# DATABASE SCHEMA & MODELS — IP-SAKTI SAHAYAK

The database uses SQLAlchemy ORM with support for both SQLite (zero-config local runtime) and PostgreSQL with pgvector (production enterprise deployment).

---

## Core Relational Tables

### 1. `users` & `organizations`
- User identity, hashed passwords, roles (`user`, `facilitator`, `admin`), and tenant organization association.

### 2. `source_registry` & `source_versions`
- Verified legal and regulatory primary sources:
  - `source_id`: Unique identifier (e.g. `IN_PATENTS_ACT_1970`, `IN_BD_ACT_2002_2023`).
  - `authority`: Primary governing body (e.g. CGPDTM, NBA, Ministry of AYUSH, FSSAI, US FDA).
  - `authority_rank`: 1 (Primary Acts) to 10 (Commentaries).
  - `checksum`: SHA-256 integrity hash.
  - `status`: `active`, `superseded`, or `repealed`.

### 3. `document_chunks`
- Segmented statutory provisions and private user dossiers:
  - `provision_ref`: Provision reference (e.g. `Section 3(p)`, `Rule 158B`).
  - `namespace`: `PUBLIC_KNOWLEDGE` or `PRIVATE_USER_DOCUMENTS`.
  - `authority_score`: Hierarchy multiplier.
  - `embedding_json`: Vector representation.

### 4. `conversations`, `messages` & `citations`
- Threaded research conversations with linked verified citations and confidence scores.

### 5. `products` & `ingredients`
- Ayurvedic formulations, botanical names, classical Samhita references, dosage forms, and origin states.

### 6. `abs_assessments` & `ip_assessments`
- Saved risk rating evaluations and multi-route IP protection roadmaps.

### 7. `escalations`
- Facilitator support packages with contact details, user notes, and assigned advisor status.

### 8. `knowledge_entities` & `knowledge_relationships`
- Relational graph nodes (Laws, Rules, Sections, Authorities, Herbs, Treaties) and directed relational edges.

### 9. `audit_logs`
- Telemetry logs tracking queries, latency ms, policy checks, and retrieval provenance.
