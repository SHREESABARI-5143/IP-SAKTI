import uuid
import hashlib
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.core.database import get_db, SyncSessionLocal
from backend.app.models.source import Document, DocumentChunk
from backend.app.ingestion.live_ingest import live_ingestion, LiveIngestionPipeline
from backend.app.rag.retriever import retriever

router = APIRouter(prefix="/documents", tags=["Private Document Vault & Multi-Tenant RAG"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".csv", ".tsv", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB

def sanitize_document_text(text: str) -> str:
    """
    Scrubs potential prompt-injection payloads from uploaded files,
    treating the document strictly as passive data.
    """
    return LiveIngestionPipeline.sanitize_text(text)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    jurisdiction: str = Form("India"),
    domain: str = Form("Proprietary Formulation"),
    user_id: Optional[str] = Form("demo-user-ipsakti"),
    db: AsyncSession = Depends(get_db)
):
    filename = file.filename or "uploaded_document.txt"
    ext = "." + filename.split(".")[-1].lower() if "." in filename else ".txt"

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    content_bytes = await file.read()
    file_size = len(content_bytes)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed limit of 15MB (Received {round(file_size/(1024*1024), 2)}MB)."
        )

    # Perform live document parsing, chunking, DB persistence, and retriever re-indexing
    sync_session = SyncSessionLocal()
    try:
        result = live_ingestion.ingest_raw_document(
            filename=filename,
            content_bytes=content_bytes,
            user_id=user_id or "demo-user-ipsakti",
            jurisdiction=jurisdiction,
            domain=domain,
            session=sync_session
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process and index document: {str(e)}")
    finally:
        sync_session.close()

@router.get("")
async def list_documents(
    user_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Document).order_by(Document.created_at.desc())
    if user_id:
        query = query.where(Document.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()

@router.delete("/{doc_id}")
async def delete_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Document).where(Document.id == doc_id))
    doc = res.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    
    # Delete associated chunks
    await db.execute(
        select(DocumentChunk).where(DocumentChunk.document_id == doc_id)
    )
    await db.delete(doc)
    await db.commit()

    retriever.reload_from_db()
    return {"status": "deleted", "document_id": doc_id}
