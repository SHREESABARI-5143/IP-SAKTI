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
    title = Column(String(255), nullable=True)
    authority = Column(String(255), nullable=False) # e.g. CGPDTM, NBA, Ministry of AYUSH, WIPO, US FDA
    authority_rank = Column(Integer, default=1) # 1 (Highest: Primary Legislation) to 10 (Commentary)
    jurisdiction = Column(String(50), nullable=False) # India, International, USA, EU, etc.
    domain = Column(String(100), nullable=False) # Patent, ABS, Regulatory, TM, GI, Export
    legal_domain = Column(String(100), nullable=True)
    source_type = Column(String(100), nullable=False) # Act, Rule, Notification, Treaty, Regulation, Pharmacopoeia
    document_type = Column(String(100), nullable=True)
    source_url = Column(String(500), nullable=True)
    official_url = Column(String(500), nullable=True)
    publication_date = Column(String(50), nullable=True)
    effective_date = Column(String(50), nullable=True)
    version = Column(String(50), default="1.0")
    verification_status = Column(String(50), default="NOT_VERIFIED") # VERIFIED, NOT_VERIFIED
    ingestion_status = Column(String(50), default="DISCOVERED") # DISCOVERED, DOWNLOADING, DOWNLOADED, VALIDATED, EXTRACTING, STRUCTURING, CHUNKING, EMBEDDING, INDEXED, FAILED, SUPERSEDED
    retrieved_at = Column(DateTime(timezone=True), nullable=True)
    checksum_sha256 = Column(String(64), nullable=True)
    original_file_path = Column(String(500), nullable=True)
    extracted_file_path = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
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
    version_id = Column(String(36), nullable=True)
    chunk_index = Column(Integer, default=0)
    section_title = Column(String(255), nullable=True) # e.g. "Section 3(p) - Traditional Knowledge"
    provision_ref = Column(String(100), nullable=True) # "Sec 3(p)", "Rule 158B"
    content = Column(Text, nullable=False)
    source_text = Column(Text, nullable=True)
    token_count = Column(Integer, default=0)
    embedding_json = Column(Text, nullable=True) # JSON array of float vector embeddings
    namespace = Column(String(50), default="PUBLIC_KNOWLEDGE")
    jurisdiction = Column(String(50), default="India")
    domain = Column(String(100), default="General")
    legal_domain = Column(String(100), default="PATENT")
    document_type = Column(String(100), default="ACT")
    
    # Hierarchical fields
    part = Column(String(100), nullable=True)
    chapter = Column(String(100), nullable=True)
    section = Column(String(100), nullable=True)
    subsection = Column(String(100), nullable=True)
    clause = Column(String(100), nullable=True)
    subclause = Column(String(100), nullable=True)
    rule = Column(String(100), nullable=True)
    subrule = Column(String(100), nullable=True)
    regulation = Column(String(100), nullable=True)
    subregulation = Column(String(100), nullable=True)
    article = Column(String(100), nullable=True)
    paragraph = Column(String(100), nullable=True)
    schedule = Column(String(100), nullable=True)
    entry = Column(String(100), nullable=True)
    page = Column(Integer, nullable=True)
    source_location = Column(String(255), nullable=True)
    parent_chunk_id = Column(String(36), nullable=True)

    authority = Column(String(255), default="Government of India")
    authority_score = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source = relationship("SourceRegistry", back_populates="chunks")
    document = relationship("Document", back_populates="chunks")
    citations = relationship("Citation", back_populates="chunk")
