import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

import google.generativeai as genai
from qdrant_client import QdrantClient

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

client = QdrantClient(url="http://localhost:6333")

def test_search():
    query = "Can I patent classical Ayurvedic formulation?"
    print(f"Query: '{query}'")
    emb = genai.embed_content(
        model="models/gemini-embedding-001",
        content=query,
        task_type="retrieval_query"
    )["embedding"]

    results = client.query_points(
        collection_name="india_corpus",
        query=emb,
        limit=3
    )
    for p in results.points:
        print(f"Score: {p.score:.4f} | ID: {p.payload['chunk_id']} | Title: {p.payload['title']}")

if __name__ == "__main__":
    test_search()
