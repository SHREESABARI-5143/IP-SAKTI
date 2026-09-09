from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class SourceVersionOut(BaseModel):
    id: str
    version_tag: str
    effective_from: Optional[str] = None
    effective_until: Optional[str] = None
    checksum: str
    status: str
    changelog: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SourceRegistryCreate(BaseModel):
    source_id: str
    name: str
    authority: str
    authority_rank: int = 1
    jurisdiction: str = "India"
    domain: str = "Patent"
    source_type: str = "Act"
    source_url: Optional[str] = None
    update_frequency: str = "monthly"

class SourceRegistryOut(BaseModel):
    id: str
    source_id: str
    name: str
    authority: str
    authority_rank: int
    jurisdiction: str
    domain: str
    source_type: str
    source_url: Optional[str] = None
    update_frequency: str
    last_checked: datetime
    last_success: datetime
    is_active: bool
    is_demo: bool
    versions: List[SourceVersionOut] = []

    class Config:
        from_attributes = True

class DocumentChunkOut(BaseModel):
    id: str
    source_id: Optional[str] = None
    document_id: Optional[str] = None
    chunk_index: int
    section_title: Optional[str] = None
    provision_ref: Optional[str] = None
    content: str
    token_count: int
    namespace: str
    jurisdiction: str
    domain: str
    authority: str
    authority_score: float

    class Config:
        from_attributes = True
