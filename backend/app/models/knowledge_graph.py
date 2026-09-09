import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class KnowledgeEntity(Base):
    __tablename__ = "knowledge_entities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_id = Column(String(100), unique=True, index=True, nullable=False) # e.g. ENT_HERB_ASHWAGANDHA, ENT_ACT_BD2023, ENT_SEC_3P
    name = Column(String(255), nullable=False)
    entity_type = Column(String(100), nullable=False) # Law, Rule, Section, Authority, Treaty, Article, BiologicalResource, TraditionalKnowledge, Regulation
    jurisdiction = Column(String(50), default="India")
    description = Column(Text, nullable=True)
    properties_json = Column(Text, nullable=True) # JSON dictionary of metadata
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    outgoing_relationships = relationship("KnowledgeRelationship", foreign_keys="KnowledgeRelationship.source_entity_id", back_populates="source_entity", cascade="all, delete-orphan")
    incoming_relationships = relationship("KnowledgeRelationship", foreign_keys="KnowledgeRelationship.target_entity_id", back_populates="target_entity", cascade="all, delete-orphan")

class KnowledgeRelationship(Base):
    __tablename__ = "knowledge_relationships"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_entity_id = Column(String(36), ForeignKey("knowledge_entities.id"), nullable=False)
    target_entity_id = Column(String(36), ForeignKey("knowledge_entities.id"), nullable=False)
    relationship_type = Column(String(100), nullable=False) 
    # LAW_HAS_SECTION, RULE_RELATES_TO, TREATY_HAS_ARTICLE, INGREDIENT_IS_BIOLOGICAL_RESOURCE, REQUIRES_NBA_APPROVAL, EXCLUDED_UNDER_3P, REGULATED_BY
    weight = Column(Float, default=1.0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    source_entity = relationship("KnowledgeEntity", foreign_keys=[source_entity_id], back_populates="outgoing_relationships")
    target_entity = relationship("KnowledgeEntity", foreign_keys=[target_entity_id], back_populates="incoming_relationships")
