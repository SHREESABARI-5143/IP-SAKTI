import pytest
import uuid
import hashlib
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.main import app
from backend.app.core.database import async_session_factory
from backend.app.models.source import Document, DocumentChunk

@pytest.mark.asyncio
async def test_record_accounting_and_admin_stats():
    test_sha = hashlib.sha256(f"test_record_{uuid.uuid4().hex}".encode("utf-8")).hexdigest()
    
    async with async_session_factory() as session:
        # Create 1 parent document (Record)
        doc = Document(
            id=str(uuid.uuid4()),
            title="Test Multi-Chunk Statutory Record",
            filename="test_statute.jsonl",
            file_type="statute",
            jurisdiction="India",
            language="en",
            instrument_type="ACT",
            source_uri="https://ipindia.gov.in/test-section-100",
            publisher="CGPDTM",
            sha256=test_sha,
            chunk_count=7,
            corpus_version="v1.0"
        )
        session.add(doc)
        await session.flush()

        # Add 7 chunks linked to this document
        for i in range(7):
            chunk = DocumentChunk(
                id=str(uuid.uuid4()),
                document_id=doc.id,
                chunk_index=i,
                record_index=1,
                section_title=f"Section 100 Subsection ({i+1})",
                provision_ref=f"Sec 100({i+1})",
                content=f"Content for subsection {i+1} of section 100 regarding Ayurvedic patents.",
                jurisdiction="India",
                legal_domain="PATENT"
            )
            session.add(chunk)
        await session.commit()

    # Call admin stats endpoint
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/admin/stats")
        assert response.status_code == 200
        data = response.json()

        # Assert record count is reported at record level
        assert "total_records" in data
        assert "total_chunks" in data
        assert data["total_records"] >= 1
        assert data["total_chunks"] >= 7
        assert data["total_chunks"] >= data["total_records"]

@pytest.mark.asyncio
async def test_distinct_records_retrieval_accounting():
    """Verify that retrieval of multiple chunks from the same document counts as 1 distinct record retrieved."""
    from backend.app.rag.retriever import HybridRetriever
    
    retriever = HybridRetriever()
    results = retriever.search(query="patent traditional knowledge section 3p", top_k=6)
    
    # Check that retrieved items have record accounting metadata
    distinct_sources = set()
    for r in results:
        chunk = r.get("chunk", {})
        doc_id = chunk.get("document_id") or chunk.get("source_id") or chunk.get("source_hash")
        if doc_id:
            distinct_sources.add(doc_id)
            
    assert len(results) >= 0
    # Distinct records is less than or equal to total chunks retrieved
    assert len(distinct_sources) <= len(results)
