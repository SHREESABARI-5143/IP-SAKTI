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
    title: Optional[str] = None
    authority: str
    authority_rank: int = 1
    jurisdiction: str = "India"
    domain: str = "Patent"
    legal_domain: Optional[str] = None
    source_type: str = "Act"
    document_type: Optional[str] = None
    source_url: Optional[str] = None
    official_url: Optional[str] = None
    publication_date: Optional[str] = None
    effective_date: Optional[str] = None
    version: Optional[str] = "1.0"
    update_frequency: str = "monthly"

class SourceRegistryOut(BaseModel):
    id: str
    source_id: str
    name: str
    title: Optional[str] = None
    authority: str
    authority_rank: int
    jurisdiction: str
    domain: str
    legal_domain: Optional[str] = None
    source_type: str
    document_type: Optional[str] = None
    source_url: Optional[str] = None
    official_url: Optional[str] = None
    publication_date: Optional[str] = None
    effective_date: Optional[str] = None
    version: Optional[str] = None
    verification_status: Optional[str] = "NOT_VERIFIED"
    ingestion_status: Optional[str] = "DISCOVERED"
    retrieved_at: Optional[datetime] = None
    checksum_sha256: Optional[str] = None
    original_file_path: Optional[str] = None
    extracted_file_path: Optional[str] = None
    error_message: Optional[str] = None
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
    version_id: Optional[str] = None
    chunk_index: int
    section_title: Optional[str] = None
    provision_ref: Optional[str] = None
    content: str
    source_text: Optional[str] = None
    token_count: int
    namespace: str
    jurisdiction: str
    domain: str
    legal_domain: Optional[str] = None
    document_type: Optional[str] = None
    part: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    clause: Optional[str] = None
    subclause: Optional[str] = None
    rule: Optional[str] = None
    subrule: Optional[str] = None
    regulation: Optional[str] = None
    subregulation: Optional[str] = None
    article: Optional[str] = None
    paragraph: Optional[str] = None
    schedule: Optional[str] = None
    entry: Optional[str] = None
    page: Optional[int] = None
    source_location: Optional[str] = None
    parent_chunk_id: Optional[str] = None
    authority: str
    authority_score: float

    class Config:
        from_attributes = True
