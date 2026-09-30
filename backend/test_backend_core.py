import sys
import os

sys.path.insert(0, os.path.abspath("."))

from app.services.vector_service import vector_service
from app.services.graph_service import graph_service
from app.services.classification_service import classification_service
from app.services.qa_service import qa_service
from app.models.schemas import QueryRequest

def test_backend():
    print("====================================================")
    print("   AYURA BACKEND AI & RAG ENGINE TEST SUITE")
    print("====================================================\n")

    # 1. Test Vector Service Retrieval
    print("--- 1. Testing Vector Service Retrieval ---")
    query = "Section 3(p) traditional knowledge patent eligibility"
    hits = vector_service.search_corpus(query=query, jurisdiction="india", top_k=3)
    assert len(hits) > 0, "Vector search returned no results!"
    print(f"[PASS] Retrieved {len(hits)} relevant statutory chunks for query: '{query}'")
    for idx, hit in enumerate(hits, 1):
        print(f"       Chunk {idx}: [{hit.citation_key}] score={hit.relevance_score:.4f} ({hit.doc_title})")

    # 2. Test Knowledge Graph Traversal
    print("\n--- 2. Testing Knowledge Graph Traversal ---")
    chunk_ids = [h.doc_id for h in hits]
    cross_refs = graph_service.traverse_cross_references(chunk_ids, max_depth=2)
    validity = graph_service.check_temporal_validity(chunk_ids)
    print(f"[PASS] Graph traversal completed:")
    print(f"       Cross-referenced provisions discovered: {len(cross_refs)}")
    print(f"       Temporal validity annotations: {len(validity)}")

    # 3. Test ASU Classification Engine
    print("\n--- 3. Testing 6-Category Classification Wizard Engine ---")
    start_q = classification_service.start_classification()
    assert start_q is not None, "Failed to load start question!"
    print(f"[PASS] Loaded Step 1 Question: {start_q.title_en[:80]}...")
    print(f"       Options available: {[opt.label_en for opt in start_q.options]}")

    # 4. Test QA Service Integration
    print("\n--- 4. Testing End-to-End QA Pipeline ---")
    req = QueryRequest(
        query="What are the patent eligibility criteria for an Ayurvedic extract under Section 3(p)?",
        jurisdiction="india",
        language="en"
    )
    ans = qa_service.answer_query(req)
    assert ans is not None, "QA service returned None!"
    assert len(ans.answer) > 0, "Answer text is empty!"
    print(f"[PASS] Generated Answer ({len(ans.answer)} characters):")
    print(f"       Confidence: {ans.confidence}")
    print(f"       Sources Cited: {len(ans.sources)}")
    print(f"       Snippet: {ans.answer[:140]}...")

    print("\n====================================================")
    print("ALL BACKEND CORE SERVICES PASSED SUCCESSFULLY (100%)")
    print("====================================================")

if __name__ == "__main__":
    test_backend()
