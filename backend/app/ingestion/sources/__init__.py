from typing import Protocol, Iterable, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RecordRef:
    record_id: str
    source_uri: str
    metadata: Dict[str, Any]

@dataclass
class RawRecord:
    ref: RecordRef
    raw_content: str
    retrieved_at: datetime
    sha256: str

@dataclass
class CanonicalRecord:
    record_id: str
    title: str
    source_uri: str
    publisher: str
    published_date: str
    retrieved_at: datetime
    sha256: str
    jurisdiction: str
    language: str
    instrument_type: str
    legal_domain: str
    provision_ref: str
    content: str
    chunks: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class SourceAdapter(Protocol):
    source_id: str
    def discover(self) -> Iterable[RecordRef]: ...
    def fetch(self, ref: RecordRef) -> RawRecord: ...
    def parse(self, raw: RawRecord) -> List[CanonicalRecord]: ...
