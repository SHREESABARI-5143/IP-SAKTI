import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from app.models.schemas import QueryRequest
from app.services.qa_service import qa_service

def test_rag_english():
    print("\n--- Testing Real English RAG ---")
    req = QueryRequest(
        query="Can I patent a classical Ayurvedic formulation like Chyawanprash in India?",
        jurisdiction="india",
        language="en"
    )
    resp = qa_service.answer_query(req)
    print(f"Confidence: {resp.confidence}")
    print(f"Jurisdiction: {resp.jurisdiction}")
    print(f"Sources found: {len(resp.sources)}")
    for s in resp.sources:
        print(f" - [{s.relevance_score}] {s.citation_key}: {s.section_title}")
    print("\nGenerated Answer Preview:")
    print(resp.answer[:400] + "...")

def test_rag_hindi():
    print("\n--- Testing Real Hindi RAG ---")
    req = QueryRequest(
        query="क्या मैं भारत में पारंपरिक आयुर्वेदिक औषधि का पेटेंट करा सकता हूँ?",
        jurisdiction="india",
        language="hi"
    )
    resp = qa_service.answer_query(req)
    print(f"Confidence: {resp.confidence}")
    print("\nHindi Generated Answer Preview:")
    print(resp.answer[:400] + "...")

if __name__ == "__main__":
    test_rag_english()
    test_rag_hindi()
