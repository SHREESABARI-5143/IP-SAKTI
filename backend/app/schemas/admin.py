from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr

class EscalationCreate(BaseModel):
    conversation_id: Optional[str] = None
    product_id: Optional[str] = None
    subject: str
    question: str
    jurisdiction: str = "India"
    product_category: Optional[str] = None
    ai_analysis_summary: Optional[str] = None
    sources_summary: Optional[str] = None
    user_notes: Optional[str] = None
    contact_email: EmailStr
    contact_phone: Optional[str] = None

class EscalationUpdate(BaseModel):
    status: str # Submitted, Under Review, Assigned, Resolved
    assigned_facilitator_name: Optional[str] = None
    facilitator_notes: Optional[str] = None

class EscalationOut(BaseModel):
    id: str
    user_id: str
    conversation_id: Optional[str] = None
    product_id: Optional[str] = None
    subject: str
    question: str
    jurisdiction: str
    product_category: Optional[str] = None
    ai_analysis_summary: Optional[str] = None
    sources_summary: Optional[str] = None
    user_notes: Optional[str] = None
    contact_email: str
    contact_phone: Optional[str] = None
    status: str
    assigned_facilitator_name: Optional[str] = None
    facilitator_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AdminStatsOut(BaseModel):
    total_users: int
    total_conversations: int
    total_queries: int
    total_sources: int
    total_records: int
    total_chunks: int = 0
    total_escalations: int
    pending_escalations: int
    avg_confidence_score: Optional[float] = None
    abstention_rate: Optional[float] = None
    jurisdiction_breakdown: Dict[str, int]
    domain_breakdown: Dict[str, int]

class SystemHealthOut(BaseModel):
    status: str
    database_connected: bool
    rag_retriever_status: str
    llm_provider: str
    active_sources_count: int
    uptime_seconds: float
