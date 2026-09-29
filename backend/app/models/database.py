"""
Database models and connection session handling using SQLAlchemy async ORM.

Production stack:
  - PostgreSQL 16 with pgvector extension for vector similarity search
  - tsvector for full-text search over statutory corpus
  - Async sessions via asyncpg
  - Falls back to SQLite (aiosqlite) for local development if DATABASE_URL not set

Tables (12):
  Domain 1 — Users:          users
  Domain 2 — Chat:           user_sessions, chat_messages, message_sources
  Domain 3 — Corpus & Graph: corpus_chunks, graph_edges
  Domain 4 — Classification: classification_sessions, classification_steps
  Domain 5 — Prior Art:      prior_art_searches, prior_art_matches
  Domain 6 — Misc:           translation_history, audit_logs, message_feedbacks
"""

import os
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy import (
    Column, String, Text, Integer, Float, DateTime, Boolean,
    ForeignKey, Index, UniqueConstraint, CheckConstraint, event, text
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Detect PostgreSQL vs SQLite
IS_POSTGRES = DATABASE_URL.startswith("postgresql")

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


# ═══════════════════════════════════════════════════════
# DOMAIN 1: USERS
# ═══════════════════════════════════════════════════════

class DBUser(Base):
    """Registered users of IP-SAKTI Sahayak."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, index=True)
    display_name = Column(String(128), nullable=False, default="Anonymous")
    email = Column(String(256), unique=True, nullable=True, index=True)
    preferred_language = Column(String(8), default="en")
    preferred_jurisdiction = Column(String(16), default="india")
    role = Column(String(16), default="user")  # user | admin | researcher
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    sessions = relationship("DBSession", back_populates="user", cascade="all, delete-orphan")
    classification_sessions = relationship("DBClassificationSession", back_populates="user")
    prior_art_searches = relationship("DBPriorArtSearch", back_populates="user")
    translations = relationship("DBTranslationHistory", back_populates="user")


# ═══════════════════════════════════════════════════════
# DOMAIN 2: CHAT SESSIONS & MESSAGES
# ═══════════════════════════════════════════════════════

class DBSession(Base):
    """Chat session tracking with jurisdiction and language context."""
    __tablename__ = "user_sessions"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    jurisdiction = Column(String(16), default="india")
    language = Column(String(8), default="en")
    session_type = Column(String(20), default="chat")  # chat | classification | search
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)

    # Relationships
    user = relationship("DBUser", back_populates="sessions")
    messages = relationship("DBMessage", back_populates="session", cascade="all, delete-orphan")


class DBMessage(Base):
    """Individual chat messages (user queries and assistant responses)."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), ForeignKey("user_sessions.id"), index=True)
    role = Column(String(16), nullable=False)  # user | assistant | system
    content = Column(Text, nullable=False)
    jurisdiction = Column(String(16), default="india")
    language = Column(String(8), default="en")
    confidence = Column(String(16), nullable=True)  # HIGH | MEDIUM | LOW
    llm_provider = Column(String(20), nullable=True)  # ollama | gemini | deterministic
    latency_ms = Column(Float, nullable=True)
    graph_nodes_consulted = Column(Integer, default=0)
    related_provisions_found = Column(Integer, default=0)
    disclaimer = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    session = relationship("DBSession", back_populates="messages")
    sources = relationship("DBMessageSource", back_populates="message", cascade="all, delete-orphan")
    feedbacks = relationship("DBFeedback", back_populates="message", cascade="all, delete-orphan")


class DBMessageSource(Base):
    """
    Normalized source citations for each assistant message.
    Replaces the old sources_json TEXT blob with proper relational structure.
    Each row links a message to a corpus chunk that was cited.
    """
    __tablename__ = "message_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"), index=True)
    chunk_id = Column(String(64), ForeignKey("corpus_chunks.chunk_id"), nullable=True, index=True)
    doc_title = Column(String(256), nullable=False)
    section_id = Column(String(64), nullable=False)
    section_title = Column(String(256), nullable=False)
    jurisdiction = Column(String(16), nullable=False)
    citation_key = Column(String(512), nullable=False)
    excerpt = Column(Text, nullable=False)
    relevance_score = Column(Float, nullable=False, default=0.0)
    is_cited_in_answer = Column(Boolean, default=False)
    validity_status = Column(String(16), default="CURRENT")  # CURRENT | AMENDED | REPEALED
    display_order = Column(Integer, default=1)

    # Relationships
    message = relationship("DBMessage", back_populates="sources")
    corpus_chunk = relationship("DBCorpusChunk", back_populates="cited_in_messages")


# ═══════════════════════════════════════════════════════
# DOMAIN 3: CORPUS & KNOWLEDGE GRAPH
# ═══════════════════════════════════════════════════════

class DBCorpusChunk(Base):
    """
    Database mirror of the JSON statutory corpus.
    On PostgreSQL: uses tsvector for full-text search and pgvector for embeddings.
    On SQLite: text-only storage (BM25 search handled in Python).
    """
    __tablename__ = "corpus_chunks"

    chunk_id = Column(String(64), primary_key=True)
    title = Column(String(256), nullable=False)
    section_or_article = Column(String(64), nullable=False)
    statute = Column(String(256), nullable=False, index=True)
    jurisdiction = Column(String(16), nullable=False, index=True)
    doc_type = Column(String(32), nullable=False, index=True)  # statute | rule | treaty | pharmacopoeia
    effective_date = Column(String(128), nullable=True)
    url = Column(String(512), nullable=True)
    text_content = Column(Text, nullable=False)
    tags_json = Column(Text, nullable=True)  # JSON array of tags
    metadata_json = Column(Text, nullable=True)  # Extra fields (ingredients, etc.)
    source_file = Column(String(128), nullable=True)
    is_active = Column(Boolean, default=True)
    indexed_at = Column(DateTime, default=datetime.utcnow)

    # Note: tsvector column 'search_vector' and pgvector column 'embedding'
    # are created via raw SQL in init_db() for PostgreSQL only.

    # Relationships
    outbound_edges = relationship(
        "DBGraphEdge",
        foreign_keys="DBGraphEdge.source_chunk_id",
        back_populates="source_node",
        cascade="all, delete-orphan"
    )
    inbound_edges = relationship(
        "DBGraphEdge",
        foreign_keys="DBGraphEdge.target_chunk_id",
        back_populates="target_node",
        cascade="all, delete-orphan"
    )
    cited_in_messages = relationship("DBMessageSource", back_populates="corpus_chunk")


class DBGraphEdge(Base):
    """
    Knowledge graph edges representing legal relationships between provisions.
    Edge types: AMENDS, REPEALED_BY, CROSS_REFERENCES, IMPLEMENTS
    """
    __tablename__ = "graph_edges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_chunk_id = Column(String(64), ForeignKey("corpus_chunks.chunk_id"), index=True)
    target_chunk_id = Column(String(64), ForeignKey("corpus_chunks.chunk_id"), index=True)
    edge_type = Column(String(32), nullable=False, index=True)
    label = Column(Text, nullable=False)
    effective_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("source_chunk_id", "target_chunk_id", "edge_type", name="uq_edge_src_tgt_type"),
    )

    # Relationships
    source_node = relationship(
        "DBCorpusChunk",
        foreign_keys=[source_chunk_id],
        back_populates="outbound_edges"
    )
    target_node = relationship(
        "DBCorpusChunk",
        foreign_keys=[target_chunk_id],
        back_populates="inbound_edges"
    )


# ═══════════════════════════════════════════════════════
# DOMAIN 4: CLASSIFICATION
# ═══════════════════════════════════════════════════════

class DBClassificationSession(Base):
    """Tracks a complete product classification wizard session."""
    __tablename__ = "classification_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    final_category = Column(String(32), nullable=True)
    confidence = Column(String(16), nullable=True)
    reasoning = Column(Text, nullable=True)
    cited_rules_json = Column(Text, nullable=True)
    regulatory_json = Column(Text, nullable=True)
    ip_instruments_json = Column(Text, nullable=True)
    next_steps_json = Column(Text, nullable=True)
    is_complete = Column(Boolean, default=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("DBUser", back_populates="classification_sessions")
    steps = relationship("DBClassificationStep", back_populates="classification_session", cascade="all, delete-orphan")


class DBClassificationStep(Base):
    """Individual step/answer in a classification wizard session."""
    __tablename__ = "classification_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    classification_session_id = Column(Integer, ForeignKey("classification_sessions.id"), index=True)
    question_id = Column(String(16), nullable=False)
    option_id = Column(String(32), nullable=False)
    option_label = Column(String(256), nullable=False)
    step_order = Column(Integer, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    classification_session = relationship("DBClassificationSession", back_populates="steps")


# ═══════════════════════════════════════════════════════
# DOMAIN 5: PRIOR ART SEARCH
# ═══════════════════════════════════════════════════════

class DBPriorArtSearch(Base):
    """Tracks each prior art formulation search and its parameters."""
    __tablename__ = "prior_art_searches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    ingredients_json = Column(Text, nullable=False)
    preparation_method = Column(String(256), nullable=True)
    indication = Column(String(256), nullable=True)
    free_text = Column(Text, nullable=True)
    summary_verdict = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    match_count = Column(Integer, default=0)
    top_match_score = Column(Float, default=0.0)
    latency_ms = Column(Float, default=0.0)
    searched_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("DBUser", back_populates="prior_art_searches")
    matches = relationship("DBPriorArtMatch", back_populates="search", cascade="all, delete-orphan")


class DBPriorArtMatch(Base):
    """Individual formulation match from a prior art search."""
    __tablename__ = "prior_art_matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    search_id = Column(Integer, ForeignKey("prior_art_searches.id"), index=True)
    formulation_id = Column(String(64), nullable=False)
    formulation_name = Column(String(256), nullable=False)
    sanskrit_name = Column(String(256), nullable=True)
    source_text = Column(String(256), nullable=False)
    afi_reference = Column(String(128), nullable=False)
    category = Column(String(128), nullable=False)
    ingredients_json = Column(Text, nullable=False)
    dosage_form = Column(String(64), nullable=True)
    indication = Column(Text, nullable=True)
    patentability_status = Column(Text, nullable=False)
    match_score = Column(Float, nullable=False)
    matched_ingredients_json = Column(Text, nullable=True)
    display_order = Column(Integer, default=1)

    # Relationships
    search = relationship("DBPriorArtSearch", back_populates="matches")


# ═══════════════════════════════════════════════════════
# DOMAIN 6: TRANSLATION, FEEDBACK & AUDIT
# ═══════════════════════════════════════════════════════

class DBTranslationHistory(Base):
    """Tracks translation operations (client-side NLLB results logged)."""
    __tablename__ = "translation_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_language = Column(String(8), nullable=False)
    target_language = Column(String(8), nullable=False)
    model_used = Column(String(64), nullable=False, default="nllb-200-distilled-600M")
    execution_backend = Column(String(16), nullable=False, default="wasm")  # webgpu | wasm | cpu
    latency_ms = Column(Float, default=0.0)
    translated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("DBUser", back_populates="translations")


class DBFeedback(Base):
    """User feedback (thumbs-up/down) on assistant responses."""
    __tablename__ = "message_feedbacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    rating = Column(Integer, nullable=False)  # +1 (helpful) or -1 (unhelpful)
    comment = Column(Text, nullable=True)
    feedback_type = Column(String(32), default="general")  # accuracy | completeness | language | other
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    message = relationship("DBMessage", back_populates="feedbacks")


class DBAuditLog(Base):
    """API request audit trail for compliance and analytics."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    endpoint = Column(String(128), index=True)
    http_method = Column(String(8), default="POST")
    query_text = Column(Text, nullable=True)
    jurisdiction = Column(String(16), default="india")
    matched_chunk_ids = Column(Text, nullable=True)
    llm_provider = Column(String(20), nullable=True)
    latency_ms = Column(Float, default=0.0)
    status_code = Column(Integer, default=200)
    client_ip = Column(String(64), nullable=True)
    user_agent = Column(String(256), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


# ═══════════════════════════════════════════════════════
# DATABASE INITIALIZATION
# ═══════════════════════════════════════════════════════

async def init_db():
    """
    Initializes all tables on startup.
    On PostgreSQL: also creates pgvector extension, tsvector column,
    and GIN indexes for full-text search.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if IS_POSTGRES:
        async with engine.begin() as conn:
            # Enable pgvector extension
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

            # Add tsvector column for full-text search (if not exists)
            await conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'corpus_chunks' AND column_name = 'search_vector'
                    ) THEN
                        ALTER TABLE corpus_chunks ADD COLUMN search_vector tsvector;
                    END IF;
                END $$;
            """))

            # Add pgvector embedding column (1024 dimensions for multilingual-e5-large)
            await conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'corpus_chunks' AND column_name = 'embedding'
                    ) THEN
                        ALTER TABLE corpus_chunks ADD COLUMN embedding vector(1024);
                    END IF;
                END $$;
            """))

            # Create GIN index on tsvector for fast full-text search
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_corpus_search_vector
                ON corpus_chunks USING GIN (search_vector)
            """))

            # Create HNSW index on pgvector for fast similarity search
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_corpus_embedding
                ON corpus_chunks USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64)
            """))

            # Create trigger to auto-update tsvector on INSERT/UPDATE
            await conn.execute(text("""
                CREATE OR REPLACE FUNCTION corpus_search_vector_update() RETURNS trigger AS $$
                BEGIN
                    NEW.search_vector :=
                        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                        setweight(to_tsvector('english', COALESCE(NEW.section_or_article, '')), 'A') ||
                        setweight(to_tsvector('english', COALESCE(NEW.statute, '')), 'B') ||
                        setweight(to_tsvector('english', COALESCE(NEW.text_content, '')), 'C') ||
                        setweight(to_tsvector('english', COALESCE(NEW.tags_json, '')), 'D');
                    RETURN NEW;
                END
                $$ LANGUAGE plpgsql;
            """))

            await conn.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_corpus_search_vector'
                    ) THEN
                        CREATE TRIGGER trg_corpus_search_vector
                        BEFORE INSERT OR UPDATE ON corpus_chunks
                        FOR EACH ROW EXECUTE FUNCTION corpus_search_vector_update();
                    END IF;
                END $$;
            """))

    print("[Database] Initialized all 12 tables successfully.")
    if IS_POSTGRES:
        print("[Database] PostgreSQL extensions: pgvector ✓, tsvector + GIN index ✓, HNSW index ✓")

    # Seed DBCorpusChunk and DBGraphEdge from verified corpus metadata if empty
    await seed_corpus_and_graph_if_empty()


async def seed_corpus_and_graph_if_empty():
    """
    Seeds verified authentic legal provisions and knowledge graph relationships
    directly into database tables (corpus_chunks, graph_edges).
    Guarantees that database is the single authoritative source of truth.
    """
    import json
    from sqlalchemy import select, func
    from app.services.graph_service import STATUTORY_EDGES

    async with async_session() as session:
        result = await session.execute(select(func.count(DBCorpusChunk.chunk_id)))
        count = result.scalar() or 0

        if count > 0:
            print(f"[Database] Corpus already contains {count} provisions in DB.")
            return

        print("[Database] Seeding authentic corpus provisions and graph edges into database...")
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        corpus_dir = os.path.join(backend_dir, "corpus", "processed")

        inserted_chunk_ids = set()

        for juri in ["india", "international"]:
            juri_path = os.path.join(corpus_dir, juri)
            if not os.path.exists(juri_path):
                continue
            for fname in os.listdir(juri_path):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(juri_path, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        items = data if isinstance(data, list) else [data]
                        for item in items:
                            cid = item.get("chunk_id")
                            if not cid or cid in inserted_chunk_ids:
                                continue
                            
                            meta_extra = {
                                k: v for k, v in item.items()
                                if k not in {
                                    "chunk_id", "title", "section_or_article", "statute",
                                    "jurisdiction", "doc_type", "effective_date", "url",
                                    "text", "tags"
                                }
                            }

                            chunk_row = DBCorpusChunk(
                                chunk_id=cid,
                                title=item.get("title", ""),
                                section_or_article=item.get("section_or_article", ""),
                                statute=item.get("statute", ""),
                                jurisdiction=item.get("jurisdiction", juri),
                                doc_type=item.get("doc_type", "statute"),
                                effective_date=item.get("effective_date", ""),
                                url=item.get("url", ""),
                                text_content=item.get("text", ""),
                                tags_json=json.dumps(item.get("tags", [])),
                                metadata_json=json.dumps(meta_extra) if meta_extra else None,
                                source_file=fname,
                                is_active=True
                            )
                            session.add(chunk_row)
                            inserted_chunk_ids.add(cid)
                except Exception as e:
                    print(f"[Database] Error reading seed file {fpath}: {e}")

        await session.commit()
        print(f"[Database] Seeded {len(inserted_chunk_ids)} authentic provisions into 'corpus_chunks' table.")

        # Seed Graph Edges
        edge_count = 0
        for src, edge_type, tgt, label in STATUTORY_EDGES:
            if src in inserted_chunk_ids and tgt in inserted_chunk_ids:
                edge_row = DBGraphEdge(
                    source_chunk_id=src,
                    target_chunk_id=tgt,
                    edge_type=edge_type,
                    label=label,
                    is_active=True
                )
                session.add(edge_row)
                edge_count += 1

        await session.commit()
        print(f"[Database] Seeded {edge_count} knowledge graph edges into 'graph_edges' table.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provides an async database session for FastAPI dependency injection."""
    async with async_session() as session:
        yield session

