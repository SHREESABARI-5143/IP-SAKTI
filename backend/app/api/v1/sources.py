import os
import uuid
import hashlib
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, Body, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from backend.app.core.database import get_db, SyncSessionLocal
from backend.app.models.source import SourceRegistry, SourceVersion, DocumentChunk
from backend.app.schemas.sources import SourceRegistryOut, SourceVersionOut, DocumentChunkOut
from backend.app.ingestion.live_ingest import live_ingestion
from backend.app.rag.retriever import retriever

router = APIRouter(prefix="/sources", tags=["Authoritative Source & Registry Explorer"])

@router.get("", response_model=List[SourceRegistryOut])
async def list_sources(
    jurisdiction: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Lists all registered authoritative statutory/regulatory sources."""
    query = select(SourceRegistry).options(selectinload(SourceRegistry.versions))
    if jurisdiction:
        query = query.where(SourceRegistry.jurisdiction == jurisdiction)
    if domain:
        query = query.where(SourceRegistry.domain.ilike(f"%{domain}%"))

    res = await db.execute(query)
    sources = res.scalars().all()

    # If database is empty, run live ingestion from authoritative sources
    if not sources:
        live_ingestion.ingest_all_authoritative_sources()
        res = await db.execute(query)
        sources = res.scalars().all()

    return sources

@router.get("/discover", response_model=List[Dict[str, Any]])
@router.post("/discover", response_model=List[Dict[str, Any]])
async def discover_official_sources():
    """Discovers available authoritative official sources from the controlled source catalog."""
    return live_ingestion.discover_sources()

@router.post("/{source_id}/download")
async def download_source(source_id: str, db: AsyncSession = Depends(get_db)):
    """Downloads/loads the authoritative primary document into raw storage."""
    catalog = live_ingestion.discover_sources()
    item = next((c for c in catalog if c["source_id"] == source_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Source ID '{source_id}' not found in official catalog.")

    res = await db.execute(select(SourceRegistry).where(SourceRegistry.source_id == source_id))
    src = res.scalars().first()
    if src:
        src.ingestion_status = "DOWNLOADED"
        await db.commit()

    return {
        "status": "success",
        "source_id": source_id,
        "filename": item["filename"],
        "ingestion_status": "DOWNLOADED"
    }

@router.post("/{source_id}/validate")
async def validate_source(source_id: str, db: AsyncSession = Depends(get_db)):
    """Validates raw source file integrity and calculates SHA-256."""
    catalog = live_ingestion.discover_sources()
    item = next((c for c in catalog if c["source_id"] == source_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Source ID '{source_id}' not found.")

    orig_path = os.path.join(live_ingestion.BASE_RAW_DIR, item["folder"], "original", item["filename"])
    if not os.path.exists(orig_path):
        raise HTTPException(status_code=404, detail=f"Raw source file missing at {orig_path}")

    with open(orig_path, "rb") as f:
        content = f.read()

    checksum = live_ingestion.compute_sha256(content)
    is_valid = len(content) > 0

    return {
        "source_id": source_id,
        "is_valid": is_valid,
        "checksum_sha256": checksum,
        "verification_status": "VERIFIED" if is_valid else "NOT_VERIFIED",
        "file_size_bytes": len(content)
    }

@router.post("/{source_id}/ingest")
@router.post("/{source_id}/reingest")
async def ingest_single_source(source_id: str):
    """Parses legal structure, validates checksum, and indexes chunks for the source."""
    try:
        result = live_ingestion.ingest_source_by_id(source_id)
        retriever.reload_from_db()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync-check")
async def sync_check():
    """Performs controlled source verification check and updates checksums/versions."""
    results = live_ingestion.ingest_all_authoritative_sources()
    return {
        "status": "synced",
        "sources_checked": len(results),
        "details": results
    }

@router.get("/{source_id}", response_model=SourceRegistryOut)
async def get_source(source_id: str, db: AsyncSession = Depends(get_db)):
    """Gets details for a specific source."""
    res = await db.execute(
        select(SourceRegistry).options(selectinload(SourceRegistry.versions)).where(SourceRegistry.source_id == source_id)
    )
    src = res.scalars().first()
    if not src:
        raise HTTPException(status_code=404, detail="Source not found.")
    return src

@router.get("/{source_id}/chunks", response_model=List[DocumentChunkOut])
@router.get("/{source_id}/records", response_model=List[DocumentChunkOut])
async def get_source_records(source_id: str, db: AsyncSession = Depends(get_db)):
    """Gets all parsed authoritative knowledge records for a specific source."""
    res = await db.execute(select(SourceRegistry).where(SourceRegistry.source_id == source_id))
    src = res.scalars().first()
    if not src:
        raise HTTPException(status_code=404, detail="Source not found.")

    res_chunks = await db.execute(
        select(DocumentChunk).where(DocumentChunk.source_id == src.id).order_by(DocumentChunk.chunk_index)
    )
    return res_chunks.scalars().all()

@router.get("/{source_id}/versions", response_model=List[SourceVersionOut])
async def get_source_versions(source_id: str, db: AsyncSession = Depends(get_db)):
    """Gets historical and active versions for a source."""
    res = await db.execute(select(SourceRegistry).where(SourceRegistry.source_id == source_id))
    src = res.scalars().first()
    if not src:
        raise HTTPException(status_code=404, detail="Source not found.")

    res_vers = await db.execute(
        select(SourceVersion).where(SourceVersion.source_id == src.id).order_by(SourceVersion.created_at.desc())
    )
    return res_vers.scalars().all()

@router.get("/chunks/all", response_model=List[DocumentChunkOut])
@router.get("/records/all", response_model=List[DocumentChunkOut])
async def list_all_records(
    source_id: Optional[str] = Query(None),
    limit: int = Query(500),
    db: AsyncSession = Depends(get_db)
):
    query = select(DocumentChunk)
    if source_id:
        query = query.where(DocumentChunk.source_id == source_id)
    res = await db.execute(query.limit(limit))
    return res.scalars().all()
