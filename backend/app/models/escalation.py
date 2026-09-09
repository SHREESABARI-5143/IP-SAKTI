import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class EscalationRequest(Base):
    __tablename__ = "escalations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String(36), nullable=True)
    product_id = Column(String(36), nullable=True)
    subject = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    jurisdiction = Column(String(50), default="India")
    product_category = Column(String(100), nullable=True)
    ai_analysis_summary = Column(Text, nullable=True)
    sources_summary = Column(Text, nullable=True)
    user_notes = Column(Text, nullable=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=True)
    status = Column(String(50), default="Submitted") # Submitted, Under Review, Assigned, Resolved
    assigned_facilitator_name = Column(String(255), nullable=True)
    facilitator_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="escalations")
