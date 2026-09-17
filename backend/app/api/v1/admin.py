import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from backend.app.core.database import get_db
from backend.app.models.user import User, AuditLog
from backend.app.models.conversation import Conversation, Message
from backend.app.models.source import SourceRegistry, Document, DocumentChunk
from backend.app.models.escalation import EscalationRequest
from backend.app.schemas.admin import AdminStatsOut, SystemHealthOut

router = APIRouter(prefix="/admin", tags=["Admin Console & Telemetry"])

APP_START_TIME = time.time()

@router.get("/stats", response_model=AdminStatsOut)
async def get_admin_stats(days: int = 30, db: AsyncSession = Depends(get_db)):
    user_count = (await db.execute(select(func.count(User.id)))).scalar() or 0
    conv_count = (await db.execute(select(func.count(Conversation.id)))).scalar() or 0
    msg_count = (await db.execute(select(func.count(Message.id)))).scalar() or 0
    source_count = (await db.execute(select(func.count(SourceRegistry.id)))).scalar() or 0
    
    # Record accounting: count distinct documents/records as headline
    doc_record_count = (await db.execute(select(func.count(Document.id)))).scalar() or 0
    chunk_count = (await db.execute(select(func.count(DocumentChunk.id)))).scalar() or 0
    record_count = doc_record_count if doc_record_count > 0 else chunk_count

    esc_count = (await db.execute(select(func.count(EscalationRequest.id)))).scalar() or 0
    pending_esc = (await db.execute(select(func.count(EscalationRequest.id)).where(EscalationRequest.status == "Submitted"))).scalar() or 0

    # Live computation of average confidence score and abstention rate over assistant messages
    avg_conf_res = (await db.execute(select(func.avg(Message.confidence_score)).where(Message.role == "assistant"))).scalar()
    avg_conf = round(float(avg_conf_res), 3) if avg_conf_res is not None else None

    total_assistant_msgs = (await db.execute(select(func.count(Message.id)).where(Message.role == "assistant"))).scalar() or 0
    if total_assistant_msgs > 0:
        abstained_msgs = (await db.execute(select(func.count(Message.id)).where(Message.role == "assistant", Message.is_abstained == True))).scalar() or 0
        abstention_rate = round(abstained_msgs / total_assistant_msgs, 3)
    else:
        abstention_rate = None

    # Live jurisdiction breakdown from knowledge records
    jur_rows = (await db.execute(
        select(DocumentChunk.jurisdiction, func.count(DocumentChunk.id)).group_by(DocumentChunk.jurisdiction)
    )).all()
    jurisdiction_breakdown = {row[0]: row[1] for row in jur_rows if row[0]}
    if not jurisdiction_breakdown:
        src_jur_rows = (await db.execute(
            select(SourceRegistry.jurisdiction, func.count(SourceRegistry.id)).group_by(SourceRegistry.jurisdiction)
        )).all()
        jurisdiction_breakdown = {row[0]: row[1] for row in src_jur_rows if row[0]}
    if not jurisdiction_breakdown:
        jurisdiction_breakdown = {}

    # Live domain breakdown from knowledge records
    domain_rows = (await db.execute(
        select(DocumentChunk.legal_domain, func.count(DocumentChunk.id)).group_by(DocumentChunk.legal_domain)
    )).all()
    domain_breakdown = {row[0]: row[1] for row in domain_rows if row[0]}
    if not domain_breakdown:
        src_domain_rows = (await db.execute(
            select(SourceRegistry.domain, func.count(SourceRegistry.id)).group_by(SourceRegistry.domain)
        )).all()
        domain_breakdown = {row[0]: row[1] for row in src_domain_rows if row[0]}
    if not domain_breakdown:
        domain_breakdown = {}

    return AdminStatsOut(
        total_users=user_count,
        total_conversations=conv_count,
        total_queries=msg_count,
        total_sources=source_count,
        total_records=record_count,
        total_chunks=chunk_count,
        total_escalations=esc_count,
        pending_escalations=pending_esc,
        avg_confidence_score=avg_conf,
        abstention_rate=abstention_rate,
        jurisdiction_breakdown=jurisdiction_breakdown,
        domain_breakdown=domain_breakdown
    )

@router.get("/health", response_model=SystemHealthOut)
async def get_system_health(db: AsyncSession = Depends(get_db)):
    uptime = time.time() - APP_START_TIME
    source_count = (await db.execute(select(func.count(SourceRegistry.id)))).scalar() or 0
    return SystemHealthOut(
        status="operational",
        database_connected=True,
        rag_retriever_status="active",
        llm_provider="Open-Source Ollama / Live Grounded Synthesis",
        active_sources_count=source_count,
        uptime_seconds=round(uptime, 2)
    )

@router.get("/audit-logs")
async def get_audit_logs(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100))
    return res.scalars().all()
