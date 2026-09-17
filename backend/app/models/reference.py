import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Jurisdiction(Base):
    __tablename__ = "jurisdictions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, index=True, nullable=False) # e.g. IN, US, EU, WIPO
    name = Column(String(100), nullable=False) # India, United States, European Union, International
    region = Column(String(100), nullable=True) # Domestic, North America, Europe, Global
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class LegalInstrument(Base):
    __tablename__ = "legal_instruments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(100), unique=True, index=True, nullable=False) # e.g. PATENTS_ACT_1970
    name = Column(String(255), nullable=False)
    jurisdiction_code = Column(String(50), nullable=False)
    instrument_type = Column(String(100), nullable=False) # Act, Rule, Regulation, Treaty, Pharmacopoeia
    official_publisher = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
