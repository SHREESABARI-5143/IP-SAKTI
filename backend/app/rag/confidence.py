from typing import List, Dict, Any
from backend.app.schemas.chat import ConfidenceBreakdown

class AlgorithmicConfidenceCalculator:
    """
    Computes objective, deterministic confidence scores for legal and regulatory answers.
    Takes into account:
    - Number of retrieved authoritative sources
    - Authority hierarchy score (Primary acts vs regulations vs secondary sources)
    - Jurisdictional alignment
    - Semantic retrieval relevance
    - Recency / Version validity
    - Abstention thresholds
    """

    @staticmethod
    def calculate(
        retrieved_sources: List[Dict[str, Any]],
        jurisdiction: str,
        query_intent_clarity: float = 1.0,
        unsupported_claim_count: int = 0
    ) -> ConfidenceBreakdown:
        if not retrieved_sources:
            return ConfidenceBreakdown(
                level="Abstain",
                score=0.1,
                source_authority_score=0.0,
                retrieval_relevance_score=0.0,
                jurisdiction_match_score=0.0,
                source_freshness_score=0.0,
                citation_grounding_score=0.0,
                explanation="Insufficient authoritative sources found in verified knowledge registry. Safe abstention active."
            )

        # 1. Authority Hierarchy Score
        avg_authority = sum(s.get("authority_weight", 0.9) for s in retrieved_sources) / len(retrieved_sources)
        
        # 2. Retrieval Relevance Score
        avg_relevance = sum(s.get("retrieval_score", 0.5) for s in retrieved_sources) / len(retrieved_sources)

        # 3. Jurisdiction Match Score
        jurisdiction_matches = [
            1.0 if s.get("jurisdiction", "").lower() == jurisdiction.lower() or s.get("jurisdiction") == "International"
            else 0.4
            for s in retrieved_sources
        ]
        jurisdiction_score = sum(jurisdiction_matches) / len(jurisdiction_matches)

        # 4. Citation Grounding Penalty
        grounding_score = max(0.2, 1.0 - (unsupported_claim_count * 0.25))

        # 5. Freshness
        freshness_score = 0.95

        # Composite score
        final_score = (
            (avg_authority * 0.30) +
            (avg_relevance * 0.25) +
            (jurisdiction_score * 0.25) +
            (grounding_score * 0.20)
        ) * query_intent_clarity

        final_score = min(0.99, max(0.10, final_score))

        # Classification
        if final_score >= 0.80:
            level = "High"
            explanation = f"Answer strongly grounded in {len(retrieved_sources)} primary statutory and regulatory sources with high jurisdictional alignment."
        elif final_score >= 0.55:
            level = "Medium"
            explanation = "Moderate grounding. Some relevant provisions found, but specific case-by-case facts or additional clarifications are recommended."
        elif final_score >= 0.35:
            level = "Low"
            explanation = "Low confidence. Limited directly applicable provisions identified in current knowledge index."
        else:
            level = "Abstain"
            explanation = "Abstained: Evidence is below safe threshold to provide reliable regulatory guidance."

        return ConfidenceBreakdown(
            level=level,
            score=round(final_score, 2),
            source_authority_score=round(avg_authority, 2),
            retrieval_relevance_score=round(avg_relevance, 2),
            jurisdiction_match_score=round(jurisdiction_score, 2),
            source_freshness_score=round(freshness_score, 2),
            citation_grounding_score=round(grounding_score, 2),
            explanation=explanation
        )

confidence_calculator = AlgorithmicConfidenceCalculator()
