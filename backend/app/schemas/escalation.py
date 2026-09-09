from typing import Optional
from datetime import datetime
from pydantic import BaseModel

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
    contact_email: str
    contact_phone: Optional[str] = None

class EscalationUpdate(BaseModel):
    status: str
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
