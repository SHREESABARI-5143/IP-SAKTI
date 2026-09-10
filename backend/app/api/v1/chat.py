import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from backend.app.core.database import get_db
from backend.app.agents.orchestrator import orchestrator
from backend.app.models.conversation import Conversation, Message, Citation
from backend.app.schemas.chat import ChatRequest, ChatResponse, ChatMessageOut

router = APIRouter(prefix="/chat", tags=["Conversational Intelligence Copilot"])

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    conv_id = request.conversation_id
    if not conv_id:
        # Create new conversation
        conv = Conversation(
            id=str(uuid.uuid4()),
            title=request.message[:45] + "...",
            jurisdiction=request.jurisdiction,
            selected_country=request.selected_country,
            language=request.language
        )
        db.add(conv)
        await db.flush()
        conv_id = conv.id
    else:
        # Verify conversation exists
        res = await db.execute(select(Conversation).where(Conversation.id == conv_id))
        conv = res.scalars().first()
        if not conv:
            conv = Conversation(
                id=conv_id,
                title=request.message[:45] + "...",
                jurisdiction=request.jurisdiction,
                selected_country=request.selected_country,
                language=request.language
            )
            db.add(conv)
            await db.flush()

    user_msg = Message(
        id=str(uuid.uuid4()),
        conversation_id=conv_id,
        role="user",
        content=request.message,
        jurisdiction=request.jurisdiction
    )
    db.add(user_msg)

    # Execute multi-agent orchestration pipeline
    response_msg_id = str(uuid.uuid4())
    ai_response = await orchestrator.process_chat_query(
        query=request.message,
        jurisdiction=request.jurisdiction,
        selected_country=request.selected_country,
        language_preference=request.language,
        product_context=request.product_context,
        conversation_id=conv_id,
        message_id=response_msg_id
    )

    # Persist assistant message and citations
    assistant_msg = Message(
        id=response_msg_id,
        conversation_id=conv_id,
        role="assistant",
        content=ai_response.full_answer,
        jurisdiction=request.jurisdiction,
        domain=ai_response.detected_domain,
        confidence_level=ai_response.confidence.level,
        confidence_score=ai_response.confidence.score,
        reasoning_summary=ai_response.confidence.explanation,
        is_abstained=ai_response.is_abstained,
        abstention_reason=ai_response.abstention_reason
    )
    db.add(assistant_msg)

    for cit in ai_response.citations:
        db_cit = Citation(
            id=str(uuid.uuid4()),
            message_id=response_msg_id,
            chunk_id=cit.id,
            citation_number=cit.citation_number,
            source_title=cit.source_title,
            authority=cit.authority,
            provision_ref=cit.provision_ref,
            quote_text=cit.quote_text,
            source_url=cit.source_url,
            version=cit.version,
            effective_date=cit.effective_date,
            verification_status=cit.verification_status
        )
        db.add(db_cit)

    await db.commit()
    return ai_response

@router.get("/conversations/{conv_id}/messages")
async def get_conversation_history(conv_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(Message)
        .options(selectinload(Message.citations))
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at.asc())
    )
    messages = res.scalars().all()
    return messages
