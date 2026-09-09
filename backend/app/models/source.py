import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class SourceRegistry(Base):
    __tablename__ = "source_registry"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(100), unique=True, index=True, nullable=False) # e.g. PATENTS_ACT_1970, BD_ACT_2023
    name = Column(String(255), nullable=False)
    authority = Column(String(255), nullable=False) # e.g. CGPDTM, NBA, Ministry of AYUSH, WIPO, US FDA
    authority_rank = Column(Integer, default=1) # 1 (Highest: Primary Legislation) to 10 (Commentary)
    jurisdiction = Column(String(50), nullable=False) # India, International, USA, EU, etc.
    domain = Column(String(100), nullable=False) # Patent, ABS, Regulatory, TM, GI, Export
    source_type = Column(String(100), nullable=False) # Act, Rule, Notification, Treaty, Regulation, Pharmacopoeia
    source_url = Column(String(500), nullable=True)
    update_frequency = Column(String(50), default="monthly")
    last_checked = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_success = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    is_demo = Column(Boolean, default=False)

    versions = relationship("SourceVersion", back_populates="source", cascade="all, delete-orphan")
    chunks = relationship("DocumentChunk", back_populates="source", cascade="all, delete-orphan")

class SourceVersion(Base):
    __tablename__ = "source_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(36), ForeignKey("source_registry.id"), nullable=False)
    version_tag = Column(String(50), nullable=False) # e.g. 2023_amendment, 1970_base
    effective_from = Column(String(50), nullable=True)
    effective_until = Column(String(50), nullable=True)
    checksum = Column(String(64), nullable=False) # SHA-256
    status = Column(String(50), default="active") # active, superseded, repealed
    changelog = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source = relationship("SourceRegistry", back_populates="versions")

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True) # Null for system public documents
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False) # pdf, docx, txt
    namespace = Column(String(50), default="PUBLIC_KNOWLEDGE") # PUBLIC_KNOWLEDGE, PRIVATE_USER_DOCUMENTS, ORGANIZATION_DOCUMENTS
    jurisdiction = Column(String(50), default="India")
    domain = Column(String(100), default="General")
    file_size_bytes = Column(Integer, default=0)
    status = Column(String(50), default="indexed") # uploaded, processing, indexed, error
    checksum = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(36), ForeignKey("source_registry.id"), nullable=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True)
    chunk_index = Column(Integer, default=0)
    section_title = Column(String(255), nullable=True) # e.g. "Section 3(p) - Traditional Knowledge"
    provision_ref = Column(String(100), nullable=True) # "Sec 3(p)", "Rule 158B"
    content = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    embedding_json = Column(Text, nullable=True) # JSON array of float vector embeddings
    namespace = Column(String(50), default="PUBLIC_KNOWLEDGE")
    jurisdiction = Column(String(50), default="India")
    domain = Column(String(100), default="General")
    authority = Column(String(255), default="Government of India")
    authority_score = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source = relationship("SourceRegistry", back_populates="chunks")
    document = relationship("Document", back_populates="chunks")
    citations = relationship("Citation", back_populates="chunk")
