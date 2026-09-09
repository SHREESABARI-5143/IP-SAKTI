import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from backend.app.core.database import get_db
from backend.app.models.product import Product, Ingredient, IPAssessment, ABSAssessment
from backend.app.schemas.products import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["Product Workspace"])

@router.post("", response_model=ProductOut)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    # Demo/Fallback User ID for instant exploration
    user_id = "demo-user-ipsakti"
    
    prod_id = str(uuid.uuid4())
    new_prod = Product(
        id=prod_id,
        user_id=user_id,
        name=product_in.name,
        product_type=product_in.product_type,
        dosage_form=product_in.dosage_form,
        description=product_in.description,
        classical_reference_text=product_in.classical_reference_text,
        is_modified_formulation=product_in.is_modified_formulation,
        novelty_aspect=product_in.novelty_aspect,
        intended_therapeutic_claims=product_in.intended_therapeutic_claims,
        target_jurisdictions=product_in.target_jurisdictions,
        manufacturing_process_notes=product_in.manufacturing_process_notes
    )
    db.add(new_prod)

    for ing in product_in.ingredients:
        new_ing = Ingredient(
            id=str(uuid.uuid4()),
            product_id=prod_id,
            common_name=ing.common_name,
            botanical_name=ing.botanical_name,
            sanskrit_name=ing.sanskrit_name,
            part_used=ing.part_used,
            is_biological_resource=ing.is_biological_resource,
            source_origin_state=ing.source_origin_state,
            is_normally_traded_commodity=ing.is_normally_traded_commodity,
            percentage_composition=ing.percentage_composition
        )
        db.add(new_ing)

    await db.commit()
    
    # Reload with ingredients
    res = await db.execute(select(Product).where(Product.id == prod_id).options(selectinload(Product.ingredients)))
    saved_product = res.scalars().first()
    return saved_product

@router.get("", response_model=List[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Product).options(selectinload(Product.ingredients)).order_by(Product.created_at.desc()))
    return res.scalars().all()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Product).where(Product.id == product_id).options(selectinload(Product.ingredients)))
    prod = res.scalars().first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found.")
    return prod

@router.delete("/{product_id}")
async def delete_product(product_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Product).where(Product.id == product_id))
    prod = res.scalars().first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found.")
    await db.delete(prod)
    await db.commit()
    return {"message": "Product deleted successfully."}
