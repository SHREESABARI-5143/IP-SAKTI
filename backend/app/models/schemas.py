from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class SourceReference(BaseModel):
    doc_id: str
    doc_title: str
    section_id: str
    section_title: str
    jurisdiction: str
    citation_key: str
    excerpt: str
    relevance_score: float
    url: Optional[str] = None
    effective_date: Optional[str] = None

class QueryRequest(BaseModel):
    query: str = Field(..., description="User query in Hindi or English")
    jurisdiction: Literal["india", "international", "both"] = "india"
    language: Optional[str] = "en"
    product_category: Optional[str] = None
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    language: str
    jurisdiction: str
    confidence: Literal["HIGH", "MEDIUM", "LOW"]
    sources: List[SourceReference]
    product_category: Optional[str] = None
    disclaimer: Optional[str] = None

class ClassificationQuestionOption(BaseModel):
    id: str
    label_en: str
    label_hi: str
    next_question_id: Optional[str] = None
    target_category: Optional[str] = None

class ClassificationQuestion(BaseModel):
    question_id: str
    title_en: str
    title_hi: str
    description_en: Optional[str] = None
    description_hi: Optional[str] = None
    options: List[ClassificationQuestionOption]

class ClassificationAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    option_id: str
    answers_history: Dict[str, str] = {}

class ClassificationResult(BaseModel):
    category: str
    category_name_en: str
    category_name_hi: str
    confidence: Literal["HIGH", "MEDIUM", "LOW"]
    reasoning: str
    cited_rules: List[str]
    regulatory_implications: List[str]
    applicable_ip_instruments: List[str]
    next_steps: List[str]

class PriorArtSearchRequest(BaseModel):
    ingredients: List[str]
    preparation_method: Optional[str] = None
    indication: Optional[str] = None
    free_text: Optional[str] = None

class PriorArtMatch(BaseModel):
    id: str
    name: str
    sanskrit_name: str
    source_text: str
    afi_reference: str
    category: str
    ingredients: List[str]
    indication: str
    patentability_status: str
    match_score: float
    matched_ingredients: List[str]

class PriorArtSearchResponse(BaseModel):
    matches: List[PriorArtMatch]
    summary_verdict: str
    recommendation: str

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    rating: Literal["positive", "negative"]
    comment: Optional[str] = None
