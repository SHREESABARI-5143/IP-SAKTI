import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    finished_at = Column(DateTime(timezone=True), nullable=True)
    corpus_version = Column(String(50), nullable=False)
    records_attempted = Column(Integer, default=0)
    records_ingested = Column(Integer, default=0)
    records_skipped_duplicate = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    chunks_created = Column(Integer, default=0)
    embedding_model = Column(String(100), default="BAAI/bge-m3")
    notes = Column(Text, nullable=True)

class CorpusVersion(Base):
    __tablename__ = "corpus_versions"

    version = Column(String(50), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    record_count = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
