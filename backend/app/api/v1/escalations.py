import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.core.database import get_db
from backend.app.models.escalation import EscalationRequest
from backend.app.schemas.escalation import EscalationCreate, EscalationUpdate, EscalationOut

router = APIRouter(prefix="/escalations", tags=["Human IP Facilitator Escalation"])

@router.post("", response_model=EscalationOut)
async def create_escalation(data: EscalationCreate, db: AsyncSession = Depends(get_db)):
    esc_id = str(uuid.uuid4())
    esc = EscalationRequest(
        id=esc_id,
        user_id="demo-user-ipsakti",
        conversation_id=data.conversation_id,
        product_id=data.product_id,
        subject=data.subject,
        question=data.question,
        jurisdiction=data.jurisdiction,
        product_category=data.product_category,
        ai_analysis_summary=data.ai_analysis_summary,
        sources_summary=data.sources_summary,
        user_notes=data.user_notes,
        contact_email=data.contact_email,
        contact_phone=data.contact_phone,
        status="Submitted"
    )
    db.add(esc)
    await db.commit()
    await db.refresh(esc)
    return esc

@router.get("", response_model=List[EscalationOut])
async def list_escalations(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(EscalationRequest).order_by(EscalationRequest.created_at.desc()))
    return res.scalars().all()

@router.patch("/{esc_id}", response_model=EscalationOut)
async def update_escalation(esc_id: str, data: EscalationUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(EscalationRequest).where(EscalationRequest.id == esc_id))
    esc = res.scalars().first()
    if not esc:
        raise HTTPException(status_code=404, detail="Escalation request not found.")
    
    esc.status = data.status
    if data.assigned_facilitator_name:
        esc.assigned_facilitator_name = data.assigned_facilitator_name
    if data.facilitator_notes:
        esc.facilitator_notes = data.facilitator_notes
        
    await db.commit()
    await db.refresh(esc)
    return esc
