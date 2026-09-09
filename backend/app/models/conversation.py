import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float, Integer
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True) # Guest or logged-in
    title = Column(String(255), default="Ayurvedic IP Consultation")
    jurisdiction = Column(String(50), default="India") # India, International
    selected_country = Column(String(50), nullable=True) # USA, EU, UK, etc.
    language = Column(String(10), default="en") # en, hi, ta
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False) # user, assistant, system
    content = Column(Text, nullable=False)
    jurisdiction = Column(String(50), default="India")
    domain = Column(String(100), nullable=True)
    confidence_level = Column(String(20), default="High") # High, Medium, Low, Abstain
    confidence_score = Column(Float, default=0.9)
    reasoning_summary = Column(Text, nullable=True)
    is_abstained = Column(Boolean, default=False)
    abstention_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    conversation = relationship("Conversation", back_populates="messages")
    citations = relationship("Citation", back_populates="message", cascade="all, delete-orphan")
    retrieval_logs = relationship("RetrievalLog", back_populates="message", cascade="all, delete-orphan")

class Citation(Base):
    __tablename__ = "citations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    message_id = Column(String(36), ForeignKey("messages.id"), nullable=False)
    chunk_id = Column(String(36), ForeignKey("document_chunks.id"), nullable=True)
    citation_number = Column(Integer, default=1)
    source_title = Column(String(255), nullable=False)
    authority = Column(String(255), nullable=False)
    provision_ref = Column(String(100), nullable=True)
    quote_text = Column(Text, nullable=True)
    source_url = Column(String(500), nullable=True)
    version = Column(String(50), nullable=True)
    effective_date = Column(String(50), nullable=True)
    verification_status = Column(String(50), default="verified") # verified, unverified, partial

    message = relationship("Message", back_populates="citations")
    chunk = relationship("DocumentChunk", back_populates="citations")

class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    message_id = Column(String(36), ForeignKey("messages.id"), nullable=False)
    raw_query = Column(Text, nullable=False)
    rewritten_query = Column(Text, nullable=True)
    detected_language = Column(String(10), default="en")
    detected_jurisdiction = Column(String(50), default="India")
    detected_domains = Column(String(255), nullable=True)
    retrieved_chunk_ids = Column(Text, nullable=True) # JSON list
    retrieval_scores = Column(Text, nullable=True) # JSON dict of scores
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    message = relationship("Message", back_populates="retrieval_logs")
