from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class IPRoutesMatrix(BaseModel):
    route_name: str # Patent, Trademark, Geographical Indication (GI), Trade Secret, Industrial Design, Copyright, Plant Variety Protection (PPV&FRA)
    relevance_level: str # Potentially Relevant, Highly Relevant, Possibly Relevant, Generally Not Applicable, Requires Professional Assessment
    analysis_details: str
    statutory_basis: str # e.g. Patents Act Sec 3(p), Trade Marks Act Class 5/30, GI Act 1999, PPV&FR Act 2001
    action_items: List[str]

class IPStrategyInput(BaseModel):
    product_name: str
    product_description: str
    ingredients: List[str]
    is_classical_formulation: bool = False
    novel_extraction_or_synergy: bool = False
    has_unique_brand_name: bool = True
    brand_name: Optional[str] = None
    has_distinct_packaging_or_bottle: bool = False
    uses_indigenous_crop_variety: bool = False
    is_proprietary_process: bool = False
    target_jurisdiction: str = "India" # India, International, USA, EU

class IPStrategyResult(BaseModel):
    product_name: str
    overall_executive_summary: str
    routes: List[IPRoutesMatrix]
    patent_analysis: Dict[str, Any] # Eligibility vs Patentability vs Freedom-to-Operate vs Section 3(p)/3(d)
    trademark_strategy: Dict[str, Any]
    gi_opportunities: Dict[str, Any]
    trade_secret_recommendations: List[str]
    timeline_and_cost_guidelines: List[Dict[str, str]]
    risk_warnings: List[str]
    disclaimer: str = "Informational IP landscape analysis. Not a legal opinion or patentability certification."
