from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class CitationOut(BaseModel):
    id: Optional[str] = None
    citation_number: int
    source_title: str
    authority: str
    provision_ref: Optional[str] = None
    quote_text: Optional[str] = None
    source_url: Optional[str] = None
    version: Optional[str] = None
    effective_date: Optional[str] = None
    verification_status: str = "verified"

class ConfidenceBreakdown(BaseModel):
    level: str = "High" # High, Medium, Low, Abstain
    score: float = 0.92
    source_authority_score: float = 0.95
    retrieval_relevance_score: float = 0.90
    jurisdiction_match_score: float = 1.0
    source_freshness_score: float = 0.95
    citation_grounding_score: float = 0.94
    explanation: str

class ChatMessageOut(BaseModel):
    id: str
    role: str
    content: str
    jurisdiction: str
    domain: Optional[str] = None
    confidence: ConfidenceBreakdown
    citations: List[CitationOut] = []
    is_abstained: bool = False
    abstention_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    jurisdiction: str = "India" # India, International
    selected_country: Optional[str] = None # USA, EU, UK, Japan, Australia, UAE, Singapore
    language: str = "en" # en, hi, ta
    product_context: Optional[Dict[str, Any]] = None
    include_private_docs: bool = True

class TimingDiagnostics(BaseModel):
    query_parsing_ms: float = 0.0
    retrieval_ms: float = 0.0
    evidence_filtering_ms: float = 0.0
    generation_ms: float = 0.0
    verification_ms: float = 0.0
    total_ms: float = 0.0
    execution_path: str = "FAST_PATH"  # FAST_PATH, STANDARD_PATH, DEEP_PATH
    llm_calls_count: int = 0
    provider_used: str = "deterministic"

class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    short_answer: str
    full_answer: str
    jurisdiction: str
    detected_domain: str
    confidence: ConfidenceBreakdown
    citations: List[CitationOut]
    recommended_next_steps: List[str] = []
    followup_suggestions: List[str] = []
    is_abstained: bool = False
    abstention_reason: Optional[str] = None
    timing_diagnostics: Optional[TimingDiagnostics] = None
    disclaimer: str = "IP-SAKTI Sahayak provides general informational guidance and does not provide legal advice, regulatory approval, or a legal opinion. For decisions involving filing, prosecution, licensing, compliance, disputes, or commercialisation, consult a qualified IP/legal/regulatory professional."
