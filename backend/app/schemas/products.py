from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class IngredientBase(BaseModel):
    common_name: str
    botanical_name: Optional[str] = None
    sanskrit_name: Optional[str] = None
    part_used: Optional[str] = None
    is_biological_resource: bool = True
    source_origin_state: Optional[str] = "India"
    is_normally_traded_commodity: bool = False
    percentage_composition: Optional[float] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientOut(IngredientBase):
    id: str
    product_id: str

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    product_type: str = "classical_ayurvedic"
    dosage_form: str = "Syrup/Vati/Churna"
    description: Optional[str] = None
    classical_reference_text: Optional[str] = None
    is_modified_formulation: bool = False
    novelty_aspect: Optional[str] = None
    intended_therapeutic_claims: Optional[str] = None
    target_jurisdictions: str = "India"
    manufacturing_process_notes: Optional[str] = None
    ingredients: List[IngredientCreate] = []

class ProductOut(BaseModel):
    id: str
    user_id: str
    name: str
    product_type: str
    dosage_form: str
    description: Optional[str] = None
    classical_reference_text: Optional[str] = None
    is_modified_formulation: bool
    novelty_aspect: Optional[str] = None
    intended_therapeutic_claims: Optional[str] = None
    target_jurisdictions: str
    manufacturing_process_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    ingredients: List[IngredientOut] = []

    class Config:
        from_attributes = True
