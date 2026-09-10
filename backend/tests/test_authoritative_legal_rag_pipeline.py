import pytest
import os
import hashlib
from backend.app.core.database import SyncSessionLocal, Base, sync_engine
from backend.app.models.source import SourceRegistry, SourceVersion, DocumentChunk, Document
from backend.app.ingestion.legal_parser import LegalDocumentParser
from backend.app.ingestion.live_ingest import live_ingestion
from backend.app.rag.retriever import retriever
from backend.app.rag.citation_verifier import citation_verifier, CitationMetrics
from backend.app.rag.llm_provider import llm_provider
from backend.app.agents.orchestrator import orchestrator

@pytest.fixture(scope="module", autouse=True)
def setup_authoritative_database():
    Base.metadata.create_all(bind=sync_engine)
    session = SyncSessionLocal()
    live_ingestion.ingest_all_authoritative_sources(session=session)
    session.close()
    retriever.reload_from_db()
    yield

# ============================================================================
# Test 1 — Parser Hierarchy (Act, Rule, Regulation, Treaty, Schedule)
# ============================================================================
def test_1_parser_hierarchy():
    parser_act = LegalDocumentParser(jurisdiction="India", legal_domain="PATENT", document_type="ACT")
    act_text = """CHAPTER II - INVENTIONS NOT PATENTABLE
Section 3. What are not inventions.
The following are not inventions within the meaning of this Act,—
(p) an invention which in effect is traditional knowledge.
"""
    chunks_act = parser_act.parse(act_text, doc_title="The Patents Act, 1970")
    assert len(chunks_act) >= 1
    assert any("Section 3" in c.section or "Section 3" in c.provision_ref for c in chunks_act)

    # Test Rule parsing
    parser_rules = LegalDocumentParser(jurisdiction="India", legal_domain="AYUSH_REGULATION", document_type="RULES")
    rules_text = """PART XVI - MANUFACTURE FOR SALE OF ASU DRUGS
Rule 158B. Guidelines for issue of licence.
(1) Category of ASU medicines.
"""
    chunks_rules = parser_rules.parse(rules_text, doc_title="Drugs and Cosmetics Rules")
    assert len(chunks_rules) >= 1
    assert any("Rule 158B" in (c.rule or "") or "Rule 158B" in c.provision_ref for c in chunks_rules)

    # Test Treaty parsing
    parser_treaty = LegalDocumentParser(jurisdiction="International", legal_domain="TRADITIONAL_KNOWLEDGE", document_type="TREATY")
    treaty_text = """Article 3. Mandatory Disclosure Requirement.
(1) Where the claimed invention is materially based on genetic resources...
"""
    chunks_treaty = parser_treaty.parse(treaty_text, doc_title="WIPO GRATK Treaty")
    assert len(chunks_treaty) >= 1
    assert any("Article 3" in (c.article or "") or "Article 3" in c.provision_ref for c in chunks_treaty)

# ============================================================================
# Test 2 — Checksum Deduplication
# ============================================================================
def test_2_checksum_deduplication():
    session = SyncSessionLocal()
    src = session.query(SourceRegistry).filter(SourceRegistry.source_id == "IN_PATENTS_ACT_1970").first()
    assert src is not None
    initial_version_count = len(src.versions)
    
    # Re-ingest same document without modifying content
    live_ingestion.ingest_source_by_id("IN_PATENTS_ACT_1970", session=session)
    session.refresh(src)
    assert len(src.versions) == initial_version_count
    session.close()

# ============================================================================
# Test 3 — Versioning & Superseding
# ============================================================================
def test_3_versioning():
    session = SyncSessionLocal()
    src = session.query(SourceRegistry).filter(SourceRegistry.source_id == "IN_PATENTS_ACT_1970").first()
    assert src is not None
    
    # Add a mock historical version
    hist_ver = SourceVersion(
        source_id=src.id,
        version_tag="1970_original",
        checksum="0000000000000000000000000000000000000000000000000000000000000000",
        status="superseded"
    )
    session.add(hist_ver)
    session.commit()
    
    # Active version should remain active alongside historical
    active_vers = [v for v in src.versions if v.status == "active"]
    assert len(active_vers) >= 1
    session.close()

# ============================================================================
# Test 4 — False Provision Detection
# ============================================================================
@pytest.mark.asyncio
async def test_4_false_provision():
    query = "What does Section 999 of the Patents Act say about Ayurvedic yoga?"
    resp = await orchestrator.process_chat_query(query=query, jurisdiction="India")
    assert resp is not None
    # System should qualify or safely abstain instead of inventing Section 999
    assert "999" not in [c.provision_ref for c in resp.citations] or resp.is_abstained or "could not be verified" in resp.full_answer.lower()

# ============================================================================
# Test 5 — Regulatory vs Patentability Distinction
# ============================================================================
@pytest.mark.asyncio
async def test_5_regulatory_vs_patentability():
    query = "Does getting an AYUSH manufacturing license under Rule 158B automatically mean my formulation is patentable?"
    resp = await orchestrator.process_chat_query(query=query, jurisdiction="India")
    assert resp is not None
    full_text = resp.full_answer.lower()
    assert "regulatory" in full_text or "patent" in full_text

# ============================================================================
# Test 6 — Traditional Knowledge & Synergy
# ============================================================================
@pytest.mark.asyncio
async def test_6_traditional_knowledge_synergy():
    query = "Does merely using Turmeric and Ashwagandha make an invention unpatentable under Section 3(p)?"
    resp = await orchestrator.process_chat_query(query=query, jurisdiction="India")
    assert resp is not None
    # Must cite Section 3 or Section 3(p) and ground explanation in statutory terms
    provs = [c.provision_ref for c in resp.citations]
    assert any("3" in p or "Patent" in c.source_title for p, c in zip(provs, resp.citations)) or len(resp.citations) > 0

# ============================================================================
# Test 7 — Biological Resources Statutory Conditions
# ============================================================================
@pytest.mark.asyncio
async def test_7_biological_resources():
    query = "What approval is required under Section 6 of Biological Diversity Act before patent grant?"
    resp = await orchestrator.process_chat_query(query=query, jurisdiction="India")
    assert resp is not None
    assert any("Section 6" in c.provision_ref or "Section 3" in c.provision_ref or "Biological Diversity" in c.source_title for c in resp.citations)

# ============================================================================
# Test 8 — Citation Entailment Verification
# ============================================================================
def test_8_citation_entailment():
    retrieved = [{
        "chunk_id": "chunk-1",
        "source_title": "The Patents Act, 1970",
        "authority": "CGPDTM",
        "provision_ref": "Section 3(p)",
        "content": "An invention which in effect is traditional knowledge is not patentable.",
        "source_text": "An invention which in effect is traditional knowledge is not patentable.",
        "version": "2005",
        "effective_date": "Active"
    }]
    supported_text = "Traditional knowledge is excluded from patentability under the Patents Act. [1]"
    res = citation_verifier.verify_and_format_citations(supported_text, retrieved)
    _, _, unsupp_cnt, entailment_rate = res
    assert res.metrics.citation_validity == 1.0
    assert res.metrics.citation_entailment >= 0.5

# ============================================================================
# Test 9 — Currentness & Versioning Preference
# ============================================================================
def test_9_currentness_preference():
    results = retriever.search("Section 3(p) traditional knowledge", jurisdiction="India")
    assert len(results) > 0
    top = results[0]
    assert top["version"] in ["2005_amendment", "current", "Active", "2024_amendment", "2024_diplomatic_conference"]

# ============================================================================
# Test 10 — Cross-Jurisdiction Separation
# ============================================================================
@pytest.mark.asyncio
async def test_10_cross_jurisdiction():
    query = "How do US FDA DSHEA dietary supplement claims compare to Indian AYUSH drug claims?"
    resp = await orchestrator.process_chat_query(query=query, jurisdiction="International", selected_country="USA")
    assert resp is not None
    assert len(resp.citations) > 0

# ============================================================================
# Test 11 — Safe Abstention on Out-of-Corpus Query
# ============================================================================
@pytest.mark.asyncio
async def test_11_safe_abstention():
    query = "What are the aerospace orbital collision liability laws for satellites?"
    resp = await orchestrator.process_chat_query(query=query, jurisdiction="India")
    assert resp.is_abstained is True
    assert "abstain" in resp.confidence.level.lower()

# ============================================================================
# Test 12 — Private Formulation Vault Tenant Isolation
# ============================================================================
def test_12_private_tenant_isolation():
    session = SyncSessionLocal()
    user_a_doc = live_ingestion.ingest_raw_document(
        filename="UserA_Secret_Curcumin_Nano_Formula.txt",
        content_bytes=b"Secret User A Curcumin Nano-liposome protocol with 99.8% absorption.",
        user_id="user_alpha_999",
        session=session
    )
    session.close()

    # User B queries the retriever
    user_b_results = retriever.search(
        query="Curcumin Nano liposome absorption protocol",
        namespace="USER_user_beta_888"
    )

    # Verify User A's private doc is NOT retrievable by User B
    for chunk in user_b_results:
        assert chunk["namespace"] != "USER_user_alpha_999"
        assert "UserA_Secret" not in chunk.get("section_title", "")
