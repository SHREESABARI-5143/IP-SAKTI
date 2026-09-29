import os
import time
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from app.core.config import settings
from app.models.schemas import SourceReference

import google.generativeai as genai
from qdrant_client import QdrantClient

# Configure Gemini
api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)

EMBEDDING_MODEL = "models/gemini-embedding-001"

class VectorService:
    """
    Production-grade Vector Service powered by Qdrant and Google Gemini Embeddings.
    Queries authentic collections: 'india_corpus' and 'international_corpus'.
    """
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client: Optional[QdrantClient] = None
        self._init_client()

    def _init_client(self):
        try:
            client = QdrantClient(url=self.qdrant_url, timeout=4.0)
            client.get_collections()
            self.client = client
            print(f"[VectorService] Connected to Qdrant at {self.qdrant_url}")
        except Exception as e:
            # Fallback to local persistent storage
            storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "qdrant_storage")
            print(f"[VectorService] Warning: Could not connect to {self.qdrant_url} ({e}). Falling back to embedded store: {storage_path}")
            try:
                self.client = QdrantClient(path=storage_path)
            except Exception as e2:
                print(f"[VectorService] Error initializing fallback Qdrant client: {e2}")
                self.client = None

    def embed_query(self, query: str) -> List[float]:
        """Embeds query using Gemini embedding-001."""
        for attempt in range(3):
            try:
                res = genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=query,
                    task_type="retrieval_query"
                )
                return res["embedding"]
            except Exception as e:
                time.sleep(1)
                if attempt == 2:
                    raise RuntimeError(f"Failed to generate query embedding: {e}")
        return []

    def search_corpus(
        self, query: str, jurisdiction: str = "india", top_k: int = 5
    ) -> List[SourceReference]:
        if not self.client:
            self._init_client()
            if not self.client:
                return []

        try:
            query_vector = self.embed_query(query)
        except Exception as e:
            print(f"[VectorService] Query embedding error: {e}")
            return []

        collections_to_search = []
        if jurisdiction in ("india", "both"):
            collections_to_search.append("india_corpus")
        if jurisdiction in ("international", "both"):
            collections_to_search.append("international_corpus")

        scored_points = []
        for col in collections_to_search:
            try:
                results = self.client.query_points(
                    collection_name=col,
                    query=query_vector,
                    limit=top_k
                )
                scored_points.extend(results.points)
            except Exception as err:
                print(f"[VectorService] Error searching collection '{col}': {err}")

        # Sort points by cosine similarity descending
        scored_points.sort(key=lambda p: p.score, reverse=True)

        references: List[SourceReference] = []
        for point in scored_points[:top_k]:
            payload = point.payload or {}
            chunk_id = payload.get("chunk_id", "unknown")
            title = payload.get("title", "Legal Document")
            statute = payload.get("statute", "Statutory Provision")
            sec_id = payload.get("section_or_article", "")
            juri = payload.get("jurisdiction", jurisdiction)
            text = payload.get("text", "")
            
            # Format clean citation key
            citation_key = f"{statute}, {sec_id}" if sec_id else statute

            references.append(SourceReference(
                doc_id=chunk_id,
                doc_title=statute,
                section_id=sec_id,
                section_title=title,
                jurisdiction=juri,
                citation_key=citation_key,
                excerpt=text,
                relevance_score=round(float(point.score), 4)
            ))

        return references

    def search_prior_art(self, ingredients: List[str], query_text: str = "") -> List[Dict[str, Any]]:
        """
        Searches authentic AFI formulations in Qdrant india_corpus matching ingredients or keywords.
        """
        combined_query = f"{query_text} {' '.join(ingredients)}".strip()
        if not combined_query:
            combined_query = "Ayurvedic formulation classical recipe ingredients"

        try:
            q_vec = self.embed_query(combined_query)
            results = self.client.query_points(
                collection_name="india_corpus",
                query=q_vec,
                limit=15
            )
        except Exception as e:
            print(f"[VectorService] Prior art vector search error: {e}")
            return []

        matches = []
        clean_user_ings = [ing.lower().strip() for ing in ingredients if ing.strip()]

        for point in results.points:
            p = point.payload or {}
            doc_type = p.get("doc_type", "")
            if doc_type != "pharmacopoeia":
                continue

            # Check overlap
            ing_list = p.get("ingredients", [])
            formulation_ings = []
            if isinstance(ing_list, list):
                for item in ing_list:
                    if isinstance(item, dict):
                        formulation_ings.append(item.get("botanical", "").lower())
                    elif isinstance(item, str):
                        formulation_ings.append(item.lower())

            matched_ings = []
            for u_ing in clean_user_ings:
                for f_ing in formulation_ings:
                    if u_ing in f_ing or f_ing in u_ing:
                        matched_ings.append(f_ing)
                        break

            # Calculate match score combining vector similarity and ingredient overlap
            vector_sim = float(point.score)
            ing_overlap_score = len(matched_ings) / max(len(clean_user_ings), 1) if clean_user_ings else 0.5
            final_score = round((vector_sim * 0.6) + (ing_overlap_score * 0.4), 3)

            matches.append({
                "id": p.get("chunk_id"),
                "name": p.get("formulation_name") or p.get("title"),
                "sanskrit_name": p.get("sanskrit_name", ""),
                "source_text": p.get("classical_reference", ""),
                "afi_reference": p.get("statute", "AFI Part I"),
                "category": "Classical Formulary / TKDL Prior Art",
                "ingredients": p.get("ingredients", []),
                "dosage_form": p.get("dosage_form", ""),
                "indication": p.get("therapeutic_indications", ""),
                "patentability_status": p.get("patent_relevance", "Barred under Section 3(p) Patents Act 1970"),
                "match_score": min(final_score, 0.99),
                "matched_ingredients": matched_ings
            })

        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches[:6]

vector_service = VectorService()
