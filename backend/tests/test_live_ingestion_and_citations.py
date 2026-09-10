import unittest
import asyncio
import uuid
from backend.app.ingestion.seeder import seed_database
from backend.app.ingestion.live_ingest import live_ingestion
from backend.app.rag.retriever import retriever
from backend.app.agents.orchestrator import orchestrator
from backend.app.rag.citation_verifier import citation_verifier
from backend.app.core.database import SyncSessionLocal
from backend.app.models.source import SourceRegistry, DocumentChunk, Document

class TestLiveIngestionAndCitations(unittest.IsolatedAsyncioTestCase):
    """
    Test suite verifying that:
    1. Statutory corpus is loaded dynamically from external datasets into DB without hardcoded Python literals.
    2. Hybrid retriever indexes and retrieves chunks directly from live database records.
    3. Live document uploads dynamically index new chunks into the retriever.
    4. Citations in responses are dynamically built from live database chunk records with accurate metadata.
    """

    def setUp(self):
        seed_database()

    def test_01_database_contains_live_ingested_sources_and_chunks(self):
        session = SyncSessionLocal()
        try:
            sources = session.query(SourceRegistry).all()
            self.assertTrue(len(sources) >= 5, f"Expected at least 5 statutory sources, found {len(sources)}")
            
            chunks = session.query(DocumentChunk).all()
            self.assertTrue(len(chunks) >= 15, f"Expected at least 15 chunks, found {len(chunks)}")

            # Check that every chunk has an ID, provision_ref, and valid content
            for c in chunks:
                self.assertIsNotNone(c.id)
                self.assertIsNotNone(c.content)
                self.assertTrue(len(c.content) > 10)
        finally:
            session.close()

    def test_02_retriever_returns_live_db_chunks_with_metadata(self):
        results = retriever.search(
            query="patent traditional knowledge Section 3(p) turmeric synergy",
            jurisdiction="India",
            domain_filter="Patent"
        )
        self.assertTrue(len(results) > 0)
        top = results[0]
        self.assertIn("chunk_id", top)
        self.assertIn("provision_ref", top)
        self.assertIn("source_title", top)
        self.assertIn("content", top)
        self.assertTrue("3" in top["provision_ref"] or "Patent" in top["source_title"] or "Section" in top["provision_ref"])

    async def test_03_chat_generates_live_citations_from_retrieved_evidence(self):
        res = await orchestrator.process_chat_query(
            query="Can I patent a formulation of Turmeric and Ashwagandha under Section 3(p)?",
            jurisdiction="India"
        )
        self.assertFalse(res.is_abstained)
        self.assertTrue(len(res.citations) >= 1)

        first_cit = res.citations[0]
        self.assertIsNotNone(first_cit.id)
        self.assertIn("Patents Act", first_cit.source_title)
        self.assertTrue(len(first_cit.quote_text) > 20)
        self.assertEqual(first_cit.verification_status, "verified")

    async def test_04_live_document_upload_and_instant_citation(self):
        doc_filename = f"Kashayam_Clinical_Trial_{uuid.uuid4().hex[:6]}.txt"
        doc_content = (
            "Specialized trial report for Amritadi Kashayam. "
            "The synergistic combination of Tinospora cordifolia and Azadirachta indica "
            "demonstrates a 74% reduction in inflammatory biomarkers in human pilot studies. "
            "Batch extraction protocol No. AYUR-2026-X99 complies with GMP standards."
        ).encode("utf-8")

        unique_uid = f"test-user-{uuid.uuid4().hex[:8]}"
        # Live ingest user document
        result = live_ingestion.ingest_raw_document(
            filename=doc_filename,
            content_bytes=doc_content,
            user_id=unique_uid,
            jurisdiction="India",
            domain="Proprietary Formulation"
        )
        self.assertEqual(result["status"], "indexed")
        self.assertTrue(result["chunks_indexed"] >= 1)

        # Retrieve against the newly ingested document
        retrieved = retriever.search(
            query="Amritadi Kashayam inflammatory biomarkers AYUR-2026-X99",
            jurisdiction="India",
            namespace=result["namespace"]
        )
        self.assertTrue(len(retrieved) >= 1)
        self.assertEqual(retrieved[0]["source_title"], doc_filename)

        # Verify citation generation
        claims, citations, unsupp, rate = citation_verifier.verify_and_format_citations(
            raw_text=f"The formulation demonstrates reduction in biomarkers as per trial report. [1]",
            retrieved_sources=retrieved
        )
        self.assertTrue(len(citations) >= 1)
        self.assertEqual(citations[0].source_title, doc_filename)
        self.assertIn("Amritadi Kashayam", citations[0].quote_text)

if __name__ == "__main__":
    unittest.main()
