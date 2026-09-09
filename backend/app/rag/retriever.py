import re
import math
from typing import List, Dict, Any, Optional, Set
from rank_bm25 import BM25Okapi
from backend.app.ingestion.seed_corpus import AUTHORITATIVE_SOURCES

STOPWORDS = {
    "what", "is", "the", "on", "in", "under", "of", "for", "to", "a", "an",
    "by", "with", "and", "or", "as", "at", "from", "be", "this", "that", "it",
    "are", "can", "do", "how", "all", "any", "my", "your", "we", "our", "if",
    "about", "into", "through", "during", "before", "after", "above", "below"
}

class HybridRetriever:
    """
    Production-grade hybrid retriever combining:
    1. Lexical BM25 keyword retrieval with stopword filtering
    2. Query token coverage weighting
    3. Strict metadata pre-filtering (Jurisdiction, Domain, Authority, Namespace)
    4. Source authority hierarchy weighting (Acts > Rules > Regulations > Treaties > Standards)
    5. Token coverage thresholding to prevent single-word false positive matches on out-of-scope queries
    """

    def __init__(self):
        self.corpus_chunks: List[Dict[str, Any]] = []
        self.tokenized_corpus: List[List[str]] = []
        self.bm25: Optional[BM25Okapi] = None
        self._load_corpus()

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase alphanumeric tokenization (words of length >= 2, excluding stopwords)
        words = re.findall(r'\b[a-z0-9_]{2,}\b', text.lower())
        filtered = [w for w in words if w not in STOPWORDS]
        return filtered if filtered else words

    def _load_corpus(self):
        self.corpus_chunks = []
        chunk_idx = 0
        for src in AUTHORITATIVE_SOURCES:
            source_id = src["source_id"]
            source_name = src["name"]
            authority = src["authority"]
            authority_rank = src.get("authority_rank", 1)
            jurisdiction = src["jurisdiction"]
            domain = src["domain"]
            source_url = src.get("source_url", "")
            version_tag = src.get("version_tag", "current")
            effective_from = src.get("effective_from", "N/A")

            for chunk in src["chunks"]:
                chunk_data = {
                    "id": f"chunk_{source_id}_{chunk_idx}",
                    "source_id": source_id,
                    "source_title": source_name,
                    "authority": authority,
                    "authority_rank": authority_rank,
                    "jurisdiction": jurisdiction,
                    "domain": domain,
                    "source_url": source_url,
                    "version": version_tag,
                    "effective_date": effective_from,
                    "section_title": chunk["section_title"],
                    "provision_ref": chunk["provision_ref"],
                    "content": chunk["content"],
                    "authority_score": chunk.get("authority_score", 1.0),
                    "namespace": "PUBLIC_KNOWLEDGE"
                }
                self.corpus_chunks.append(chunk_data)
                chunk_idx += 1

        self.tokenized_corpus = [
            self._tokenize(c["section_title"] + " " + c["provision_ref"] + " " + c["content"])
            for c in self.corpus_chunks
        ]
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)

    def add_user_document_chunks(self, chunks: List[Dict[str, Any]]):
        """Allows dynamically adding private user document chunks into isolated tenant namespace."""
        for c in chunks:
            self.corpus_chunks.append(c)
            self.tokenized_corpus.append(
                self._tokenize(c.get("section_title", "") + " " + c.get("provision_ref", "") + " " + c.get("content", ""))
            )
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search(
        self,
        query: str,
        jurisdiction: str = "India",
        domain_filter: Optional[str] = None,
        selected_country: Optional[str] = None,
        namespace: str = "PUBLIC_KNOWLEDGE",
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid retrieval:
        1. Metadata filtering (Jurisdiction, Namespace, Domain)
        2. BM25 score calculation with token coverage penalty for spurious single-token matches
        3. Authority rank score calculation
        4. Composite reranking
        """
        if not self.bm25 or not self.corpus_chunks:
            return []

        tokens = self._tokenize(query)
        if not tokens:
            return []

        query_token_set = set(tokens)
        bm25_scores = self.bm25.get_scores(tokens)
        max_bm25 = max(bm25_scores) if len(bm25_scores) > 0 and max(bm25_scores) > 0 else 1.0

        candidates = []

        for idx, chunk in enumerate(self.corpus_chunks):
            # 1. Namespace Isolation Check
            if chunk.get("namespace", "PUBLIC_KNOWLEDGE") != namespace and chunk.get("namespace") != "PUBLIC_KNOWLEDGE":
                continue

            chunk_tokens = set(self.tokenized_corpus[idx])
            matched_tokens = query_token_set.intersection(chunk_tokens)
            token_coverage = len(matched_tokens) / len(query_token_set) if query_token_set else 0.0

            # Out-of-scope filter: If less than 20% of query keywords appear in chunk and BM25 is low
            if token_coverage < 0.20 and bm25_scores[idx] < (max_bm25 * 0.35):
                continue

            # 2. Jurisdiction Scoring & Filtering
            chunk_jurisdiction = chunk.get("jurisdiction", "India")
            jurisdiction_match_score = 1.0

            if jurisdiction == "India":
                if chunk_jurisdiction == "India":
                    jurisdiction_match_score = 1.0
                elif chunk_jurisdiction in ["International", "WIPO", "CBD"]:
                    jurisdiction_match_score = 0.6
                else:
                    jurisdiction_match_score = 0.05
            elif jurisdiction == "International":
                if selected_country and chunk_jurisdiction.lower() == selected_country.lower():
                    jurisdiction_match_score = 1.0
                elif chunk_jurisdiction in ["International", "WIPO", "CBD", "EU", "USA"]:
                    jurisdiction_match_score = 0.9
                else:
                    jurisdiction_match_score = 0.3

            # 3. Domain Matching
            domain_score = 1.0
            if domain_filter and domain_filter.lower() in chunk.get("domain", "").lower():
                domain_score = 1.15

            # 4. Normalized BM25 score scaled by token coverage
            norm_bm25 = (bm25_scores[idx] / max_bm25) if max_bm25 > 0 else 0.0
            weighted_lexical = norm_bm25 * (token_coverage ** 0.5)

            # 5. Authority Score (Rank 1 = 1.0, Rank 10 = 0.5)
            rank = chunk.get("authority_rank", 1)
            authority_score = max(0.5, 1.1 - (rank * 0.06))

            # 6. Composite Score
            final_score = (
                (weighted_lexical * 0.50) +
                (jurisdiction_match_score * 0.25) +
                (authority_score * 0.15) +
                (domain_score * 0.10)
            )

            # Only retain chunks with meaningful textual match
            if weighted_lexical > 0.08 or (jurisdiction_match_score >= 0.8 and weighted_lexical > 0.03):
                chunk_copy = dict(chunk)
                chunk_copy["retrieval_score"] = round(float(final_score), 4)
                chunk_copy["bm25_score"] = round(float(norm_bm25), 4)
                chunk_copy["token_coverage"] = round(float(token_coverage), 4)
                chunk_copy["authority_weight"] = round(float(authority_score), 4)
                candidates.append(chunk_copy)

        # Sort by final score descending
        candidates.sort(key=lambda x: x["retrieval_score"], reverse=True)
        return candidates[:top_k]

retriever = HybridRetriever()
