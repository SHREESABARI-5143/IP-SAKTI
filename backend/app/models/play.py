import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class PlayScenario(Base):
    __tablename__ = "play_scenarios"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    scenario_id = Column(String(100), unique=True, index=True, nullable=False)
    locale = Column(String(10), default="en")
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    choices_json = Column(Text, nullable=False) # JSON array of options
    outcomes_json = Column(Text, nullable=False) # JSON object mapping choices to legal consequences
    citation_ids_json = Column(Text, nullable=True) # JSON array of chunk/record IDs grounding this scenario
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
