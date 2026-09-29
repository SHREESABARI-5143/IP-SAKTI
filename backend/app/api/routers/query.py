import json
import time
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.models.schemas import QueryRequest, QueryResponse
from app.services.qa_service import qa_service
from app.models.database import get_db, DBSession, DBMessage, DBFeedback, DBAuditLog

router = APIRouter(prefix="/api/query", tags=["Q&A RAG Engine"])

class FeedbackRequest(BaseModel):
    message_id: int
    rating: int  # 1 or -1
    comment: Optional[str] = None

@router.post("", response_model=QueryResponse)
async def handle_query(req: QueryRequest, db: AsyncSession = Depends(get_db)):
    """Main source-cited, jurisdiction-aware RAG query endpoint with database persistence."""
    start_time = time.time()
    
    # 1. Generate answer via RAG pipeline
    response = qa_service.answer_query(req)
    latency_ms = round((time.time() - start_time) * 1000, 2)

    # 2. Persist to database if session provided or create new
    try:
        session_id = req.session_id or f"sess_{int(time.time())}"
        
        # Check if session exists
        stmt = select(DBSession).where(DBSession.id == session_id)
        result = await db.execute(stmt)
        db_sess = result.scalar_one_or_none()
        if not db_sess:
            db_sess = DBSession(
                id=session_id,
                jurisdiction=req.jurisdiction or "india",
                language=req.language or "en"
            )
            db.add(db_sess)
            await db.flush()

        # Save user message
        user_msg = DBMessage(
            session_id=session_id,
            role="user",
            content=req.query,
            jurisdiction=req.jurisdiction or "india",
            language=req.language or "en"
        )
        db.add(user_msg)

        # Save assistant message
        sources_payload = [s.model_dump() for s in response.sources]
        asst_msg = DBMessage(
            session_id=session_id,
            role="assistant",
            content=response.answer,
            jurisdiction=response.jurisdiction,
            language=response.language,
            confidence=response.confidence,
            sources_json=json.dumps(sources_payload),
            disclaimer=response.disclaimer
        )
        db.add(asst_msg)

        # Save audit log
        chunk_ids = [s.doc_id for s in response.sources]
        audit = DBAuditLog(
            endpoint="/api/query",
            query_text=req.query,
            jurisdiction=req.jurisdiction or "india",
            matched_chunk_ids=",".join(chunk_ids),
            latency_ms=latency_ms,
            status_code=200
        )
        db.add(audit)
        await db.commit()
    except Exception as e:
        print(f"[QueryRouter] Warning: DB persistence failed: {e}")
        # Non-blocking: always return user response even if logging fails

    return response

@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest, db: AsyncSession = Depends(get_db)):
    """Records user thumbs-up/thumbs-down feedback on answers."""
    try:
        fb = DBFeedback(
            message_id=req.message_id,
            rating=req.rating,
            comment=req.comment
        )
        db.add(fb)
        await db.commit()
        return {"status": "ok", "message": "Feedback recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
