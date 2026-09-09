import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float, Integer
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    product_type = Column(String(100), default="classical_ayurvedic") 
    # classical_ayurvedic, proprietary_ayurvedic, phytopharmaceutical, ayurveda_aahar, nutraceutical, cosmetic, new_formulation
    dosage_form = Column(String(100), default="Syrup/Vati/Churna") # Vati, Taila, Churna, Capsule, Extract, Cream
    description = Column(Text, nullable=True)
    classical_reference_text = Column(String(255), nullable=True) # e.g. Charaka Samhita, Sharangadhara Samhita
    is_modified_formulation = Column(Boolean, default=False)
    novelty_aspect = Column(Text, nullable=True)
    intended_therapeutic_claims = Column(Text, nullable=True)
    target_jurisdictions = Column(String(255), default="India") # e.g. "India, USA, EU"
    manufacturing_process_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="products")
    ingredients = relationship("Ingredient", back_populates="product", cascade="all, delete-orphan")
    ip_assessments = relationship("IPAssessment", back_populates="product", cascade="all, delete-orphan")
    abs_assessments = relationship("ABSAssessment", back_populates="product", cascade="all, delete-orphan")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    common_name = Column(String(255), nullable=False) # e.g. Ashwagandha, Turmeric
    botanical_name = Column(String(255), nullable=True) # e.g. Withania somnifera, Curcuma longa
    sanskrit_name = Column(String(255), nullable=True) # e.g. Ashwagandha, Haridra
    part_used = Column(String(100), nullable=True) # Root, Rhizome, Leaf, Fruit
    is_biological_resource = Column(Boolean, default=True)
    source_origin_state = Column(String(100), default="India") # Kerala, Uttarakhand, etc.
    is_normally_traded_commodity = Column(Boolean, default=False) # Under Sec 40 of BD Act
    percentage_composition = Column(Float, nullable=True)

    product = relationship("Product", back_populates="ingredients")

class IPAssessment(Base):
    __tablename__ = "ip_assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    patent_eligibility_status = Column(String(100), default="Requires Novelty & Sec 3(p) Exemption")
    patent_risk_factors = Column(Text, nullable=True)
    trademark_classes = Column(String(100), default="Class 5 (Pharmaceuticals/Herbal), Class 30")
    gi_applicable = Column(Boolean, default=False)
    gi_details = Column(Text, nullable=True)
    trade_secret_applicable = Column(Boolean, default=True)
    design_protection = Column(Text, nullable=True)
    overall_strategy_summary = Column(Text, nullable=True)
    recommended_roadmap = Column(Text, nullable=True) # JSON Array of roadmap steps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="ip_assessments")

class ABSAssessment(Base):
    __tablename__ = "abs_assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    nba_approval_required = Column(Boolean, default=False)
    sbb_intimation_required = Column(Boolean, default=True)
    bmc_consultation_required = Column(Boolean, default=False)
    risk_level = Column(String(50), default="Moderate") # Low, Moderate, High
    exemptions_applicable = Column(Text, nullable=True) # e.g. Local vaids, Sec 40 notification
    form_requirements = Column(String(255), default="Form I (NBA) / SBB Form A")
    benefit_sharing_rate = Column(String(100), default="0.1% - 0.5% of ex-factory sale")
    action_checklist = Column(Text, nullable=True) # JSON Array
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="abs_assessments")
