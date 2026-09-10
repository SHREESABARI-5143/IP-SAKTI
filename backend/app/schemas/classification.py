from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ClassificationInput(BaseModel):
    product_name: str
    product_type_hint: Optional[str] = None # Classical, Proprietary, Phytopharmaceutical, Ayurveda-Aahar, Cosmetic, etc.
    ingredients: List[str]
    has_classical_text_reference: bool = False
    classical_text_name: Optional[str] = None # Charaka Samhita, Sushruta Samhita, AFI, etc.
    is_modified_or_extract: bool = False
    novel_processing_method: bool = False
    intended_use_or_claims: str # Therapeutic, Dietary wellness, External cosmetic, etc.
    dosage_form: str # Vati, Asava, Arishta, Capsule, Tablet, Powder, Oil, Cream
    biological_sources_origin: str = "India" # India, Imported, Mixed
    target_market: str = "India" # India, USA, EU, Global
    language: str = "en" # en, hi, ta
    clarification_answers: Optional[Dict[str, str]] = None

class ClassificationResult(BaseModel):
    likely_category: str # Classical Ayurvedic Medicine, Patent/Proprietary Ayurvedic Medicine, Phytopharmaceutical Drug, Ayurveda-Aahar, Nutraceutical/Dietary Supplement, Cosmetic
    confidence: str # High, Medium, Low
    confidence_score: float
    regulatory_classification: str
    statutory_governance: str # e.g. Drugs and Cosmetics Act 1940 Chapter IV-A / Rule 158B or FSSAI Ayurveda Aahar Regulations 2022
    why_explanation: str
    licensing_requirements: List[str]
    potential_ip_routes: List[str]
    traditional_knowledge_concerns: str
    abs_considerations: str
    mandatory_labeling_rules: List[str]
    export_implications: Optional[str] = None
    clarifying_questions: List[Dict[str, Any]] = []
    important_caveat: str = "This classification is for preliminary regulatory and IP assessment only and does not constitute a statutory approval from the State Licensing Authority (SLA) or CDSCO."
