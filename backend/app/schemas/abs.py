from typing import List, Optional
from pydantic import BaseModel

class ABSAssessmentInput(BaseModel):
    product_name: str
    biological_resources: List[str] # e.g. Ashwagandha root, Turmeric rhizome, Red Sandalwood
    sourcing_location: str = "India" # India (State name), Cultivated, Wild collection, Imported
    user_entity_type: str = "Indian Individual/Entity" # Indian Individual/Entity, Foreign Entity / NRI / Indian Entity with Foreign Participation (Sec 3(2))
    activity_type: str = "Commercial Utilization" # Commercial Utilization, Research, Bio-survey, Applying for IPR, Third-party transfer
    associated_traditional_knowledge: bool = False
    is_normally_traded_commodity: bool = False # Section 40 NTC notification
    is_local_vaid_or_hakim: bool = False # Section 7 exemption
    is_seeking_ipr: bool = False # Section 6 patent approval
    is_export_involved: bool = False

class ABSAssessmentResult(BaseModel):
    biological_resource_status: str
    jurisdiction_authority: str # National Biodiversity Authority (NBA) vs State Biodiversity Board (SBB) vs Biodiversity Management Committee (BMC)
    risk_level: str # Low, Moderate, High, Critical
    nba_approval_required: bool
    sbb_intimation_required: bool
    benefit_sharing_obligation: str
    applicable_forms: List[str] # Form I (Sec 3/19), Form III (Sec 6 IPR), Form IV (Third-party transfer), SBB Form A
    applicable_statutory_sections: List[str] # Sec 3, 4, 6, 7, 19, 20, 21, 23, 24, 40 of Biological Diversity Act 2002 & 2023 Amendment
    exemptions_identified: List[str]
    documents_to_verify: List[str]
    step_by_step_compliance_roadmap: List[str]
    informational_note: str = "Informational guidance pursuant to Biological Diversity Act 2002, 2023 Amendment and ABS Guidelines. Consult the National Biodiversity Authority or legal counsel prior to filing or commercial roll-out."
