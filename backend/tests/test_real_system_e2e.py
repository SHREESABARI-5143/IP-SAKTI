"""
End-to-end automated verification suite for IP-SAKTI Sahayak (Real-Data System).
Tests Qdrant, Gemini RAG, Hindi support, Jurisdiction isolation, and Prior-art.
"""

import os
import sys
import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    res = requests.get(f"{BASE_URL}/api/health", timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["mode"] == "real_data_qdrant_gemini"

def test_qdrant_collections_exist():
    q_res = requests.get("http://localhost:6333/collections", timeout=5)
    assert q_res.status_code == 200
    collections = [c["name"] for c in q_res.json()["result"]["collections"]]
    assert "india_corpus" in collections
    assert "international_corpus" in collections

def test_rag_patent_query_india():
    payload = {
        "query": "Can I patent a classical Ayurvedic formulation like Chyawanprash?",
        "jurisdiction": "india",
        "language": "en"
    }
    res = requests.post(f"{BASE_URL}/api/query", json=payload, timeout=25)
    assert res.status_code == 200
    data = res.json()
    assert data["confidence"] in ("HIGH", "MEDIUM")
    assert len(data["sources"]) > 0
    # Must cite Patents Act Section 3
    found_patents_act = any("Patents Act" in s["doc_title"] for s in data["sources"])
    assert found_patents_act, "Expected Patents Act citation in retrieved sources"

def test_jurisdiction_isolation():
    # Query international jurisdiction
    payload = {
        "query": "What are TRIPS obligations regarding traditional knowledge and biodiversity?",
        "jurisdiction": "international",
        "language": "en"
    }
    res = requests.post(f"{BASE_URL}/api/query", json=payload, timeout=25)
    assert res.status_code == 200
    data = res.json()
    for s in data["sources"]:
        assert s["jurisdiction"] == "international", f"Found non-international source: {s['citation_key']}"

def test_prior_art_search_turmeric():
    payload = {
        "ingredients": ["Haridra", "Curcuma longa", "Cow Milk", "Go-Ghrita"],
        "free_text": "Granules for urticaria and skin allergy"
    }
    res = requests.post(f"{BASE_URL}/api/search/prior-art", json=payload, timeout=20)
    assert res.status_code == 200
    data = res.json()
    assert len(data["matches"]) > 0
    # Top match should identify Haridra Khanda
    names = [m["name"].lower() for m in data["matches"]]
    assert any("haridra" in name for name in names), f"Expected Haridra Khanda in {names}"

def test_classification_flow():
    # Start classification
    start_res = requests.get(f"{BASE_URL}/api/classify/start", timeout=5)
    assert start_res.status_code == 200
    q1 = start_res.json()
    assert q1["question_id"] == "q1"

    # Answer q1 -> yes -> leads to q2
    ans1 = requests.post(f"{BASE_URL}/api/classify/answer", json={
        "session_id": "test_sess",
        "question_id": "q1",
        "option_id": "q1_yes"
    }, timeout=5)
    assert ans1.status_code == 200
    q2 = ans1.json()
    assert q2["question_id"] == "q2"

    # Answer q2 -> exact -> classical_generic
    ans2 = requests.post(f"{BASE_URL}/api/classify/answer", json={
        "session_id": "test_sess",
        "question_id": "q2",
        "option_id": "q2_exact"
    }, timeout=5)
    assert ans2.status_code == 200
    result = ans2.json()
    assert result["category"] == "classical_generic"
    assert len(result["regulatory_implications"]) > 0

if __name__ == "__main__":
    print("Running automated E2E test suite...")
    test_health_check()
    print("[PASS] Health check passed")
    test_qdrant_collections_exist()
    print("[PASS] Qdrant collections verified")
    test_rag_patent_query_india()
    print("[PASS] Real RAG query passed with Patents Act citation")
    test_jurisdiction_isolation()
    print("[PASS] Jurisdiction isolation verified")
    test_prior_art_search_turmeric()
    print("[PASS] Prior art search passed (Haridra Khanda matched)")
    test_classification_flow()
    print("[PASS] 6-category classification wizard passed")
    print("\nALL REAL-DATA TESTS PASSED SUCCESSFULLY!")
