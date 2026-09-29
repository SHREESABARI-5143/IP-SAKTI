"""
Generates real embeddings using Google Gemini API (gemini-embedding-001)
and indexes all corpus chunks into Qdrant vector database.
Supports both Docker Qdrant (http://localhost:6333) and embedded persistent mode.
"""

import os
import sys
import json
import time
import uuid
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load env from backend/.env
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(backend_dir, ".env"))

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

API_KEY = os.getenv("GEMINI_API_KEY", "")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is missing. Please define it in your backend/.env file.")
genai.configure(api_key=API_KEY)
EMBEDDING_MODEL = "models/gemini-embedding-001"
VECTOR_DIM = 3072

INDIA_DIR = os.path.join(backend_dir, "corpus", "processed", "india")
INTL_DIR = os.path.join(backend_dir, "corpus", "processed", "international")
STORAGE_DIR = os.path.join(os.path.dirname(backend_dir), "data", "qdrant_storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

def get_qdrant_client() -> QdrantClient:
    """Connects to Qdrant server or falls back to local persistent store."""
    try:
        client = QdrantClient(url="http://localhost:6333", timeout=3.0)
        client.get_collections()
        print("Connected to Qdrant Docker server at http://localhost:6333")
        return client
    except Exception as e:
        print(f"Docker Qdrant not immediately responding ({e}), using persistent embedded store at: {STORAGE_DIR}")
        return QdrantClient(path=STORAGE_DIR)

def load_chunks_from_dir(directory: str) -> List[Dict[str, Any]]:
    chunks = []
    if not os.path.exists(directory):
        return chunks
    for fname in os.listdir(directory):
        if fname.endswith(".json"):
            fpath = os.path.join(directory, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        chunks.extend(data)
                    elif isinstance(data, dict):
                        chunks.append(data)
            except Exception as e:
                print(f"Error loading {fname}: {e}")
    return chunks

def embed_text(text: str) -> List[float]:
    """Generates 3072-dimensional vector embedding using Gemini API."""
    for attempt in range(3):
        try:
            res = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            return res["embedding"]
        except Exception as e:
            print(f"Attempt {attempt+1} embedding failed: {e}. Retrying in 2s...")
            time.sleep(2)
    raise RuntimeError(f"Failed to embed text: {text[:60]}...")

def setup_collection(client: QdrantClient, collection_name: str):
    collections = [c.name for c in client.get_collections().collections]
    if collection_name not in collections:
        print(f"Creating Qdrant collection: {collection_name} (dim={VECTOR_DIM}, Cosine)")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(size=VECTOR_DIM, distance=qmodels.Distance.COSINE)
        )
    else:
        print(f"Collection {collection_name} already exists.")

def index_corpus(client: QdrantClient, collection_name: str, chunks: List[Dict[str, Any]]):
    setup_collection(client, collection_name)
    points = []
    print(f"Generating Gemini embeddings and indexing {len(chunks)} chunks into '{collection_name}'...")

    for idx, chunk in enumerate(chunks):
        chunk_id_str = chunk.get("chunk_id", f"{collection_name}_{idx}")
        # Build representation for embedding
        title = chunk.get("title", "")
        text = chunk.get("text", "")
        if not text and "ingredients" in chunk:
            # Pharmacopoeial formulation
            ingr_str = ", ".join([f"{ing.get('botanical', '')}" for ing in chunk.get("ingredients", [])])
            text = f"{title}. Dosage Form: {chunk.get('dosage_form','')}. Reference: {chunk.get('classical_reference','')}. Ingredients: {ingr_str}. Indications: {chunk.get('therapeutic_indications','')}. Preparation: {chunk.get('preparation_method','')}. Patent relevance: {chunk.get('patent_relevance','')}"

        content_to_embed = f"{title}\n{text}"
        vector = embed_text(content_to_embed)

        # Generate integer or UUID point ID
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id_str))

        point = qmodels.PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "chunk_id": chunk_id_str,
                "title": title,
                "section_or_article": chunk.get("section_or_article", ""),
                "statute": chunk.get("statute", ""),
                "jurisdiction": chunk.get("jurisdiction", ""),
                "doc_type": chunk.get("doc_type", ""),
                "effective_date": chunk.get("effective_date", ""),
                "url": chunk.get("url", ""),
                "text": text,
                "tags": chunk.get("tags", []),
                "formulation_name": chunk.get("formulation_name", ""),
                "sanskrit_name": chunk.get("sanskrit_name", ""),
                "dosage_form": chunk.get("dosage_form", ""),
                "classical_reference": chunk.get("classical_reference", ""),
                "therapeutic_indications": chunk.get("therapeutic_indications", ""),
                "patent_relevance": chunk.get("patent_relevance", "")
            }
        )
        points.append(point)
        print(f"[{idx+1}/{len(chunks)}] Embedded & prepared point: {chunk_id_str} ({title[:35]}...)")

    # Upsert all points to Qdrant
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print(f"Successfully upserted {len(points)} points into '{collection_name}'!\n")

def main():
    client = get_qdrant_client()

    india_chunks = load_chunks_from_dir(INDIA_DIR)
    intl_chunks = load_chunks_from_dir(INTL_DIR)

    print(f"Loaded {len(india_chunks)} Indian chunks and {len(intl_chunks)} International chunks.")

    index_corpus(client, "india_corpus", india_chunks)
    index_corpus(client, "international_corpus", intl_chunks)

    # Verification
    collections = client.get_collections().collections
    print("Verification of collections in Qdrant:")
    for col in collections:
        info = client.get_collection(col.name)
        print(f" - Collection: {col.name}, Points: {info.points_count}")

if __name__ == "__main__":
    main()
