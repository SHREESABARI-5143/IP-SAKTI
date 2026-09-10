# ADR-001: PostgreSQL with pgvector Extension for Statutory Vector Storage

## Status
Accepted

## Context
The initial prototype stored embeddings in an unindexed SQLite JSON text column and relied on an in-memory BM25 dictionary. As the statutory and regulatory corpus scales across multiple jurisdictions (India, WIPO, US FDA, EU EMA) and multi-tenant user formulation vaults, a production-grade relational database with high-dimensional vector search capability is required.

## Decision
We adopt **PostgreSQL 16 with the `pgvector` extension** using HNSW (Hierarchical Navigable Small World) cosine indexing over 1024-dimensional vectors (BAAI/bge-m3). 

## Consequences
- **Positive**: Native ACID transactions, schema consistency via Alembic migrations, unified metadata filtering (jurisdiction, domain, tenant namespace) in single SQL queries.
- **Positive**: Eliminates standalone vector database operational overhead (e.g. separate ChromaDB/Pinecone clusters).
- **Negative**: Requires PostgreSQL instance with pgvector extension compiled in container. SQLite retained for local lightweight testing.
