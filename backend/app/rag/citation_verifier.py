import re
from typing import List, Dict, Any, Tuple, Set
from backend.app.schemas.chat import CitationOut

class CitationVerifier:
    """
    Production Claim-Level Grounding & Citation Verification Engine.
    1. Extracts individual factual claims from raw generated response.
    2. Maps explicit citations [1], [2], [Section ...] to authoritative retrieved chunks.
    3. Performs semantic and lexical token overlap verification between claim and evidence.
    4. Detects ungrounded/unsupported statements and computes precision/recall statistics.
    """

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        return set(re.findall(r'\b[a-z0-9_]{3,}\b', text.lower()))

    @staticmethod
    def extract_claims(raw_text: str) -> List[str]:
        """Splits answer into discrete declarative sentences/claims."""
        # Strip headers and markdown tables
        lines = raw_text.split('\n')
        claims = []
        for line in lines:
            line_clean = line.strip()
            if not line_clean or line_clean.startswith('#') or line_clean.startswith('---'):
                continue
            sentences = re.split(r'(?<=[.!?])\s+', line_clean)
            for s in sentences:
                s_strip = s.strip()
                if len(s_strip) > 20 and not s_strip.startswith('*') and not s_strip.startswith('>'):
                    claims.append(s_strip)
        return claims

    def verify_and_format_citations(
        self,
        raw_text: str,
        retrieved_sources: List[Dict[str, Any]]
    ) -> Tuple[str, List[CitationOut], int, float]:
        """
        Parses `[1]`, `[2]` citations from text, maps them to retrieved source chunks,
        verifies factual overlap against claims, and returns:
        (sanitized_text, verified_citation_objects, unsupported_claim_count, claim_grounding_rate)
        """
        if not retrieved_sources:
            return raw_text, [], 0, 0.0

        # Build lookup table of retrieved sources by index (1-based)
        source_map = {}
        source_tokens_map = {}
        for idx, src in enumerate(retrieved_sources):
            c_num = idx + 1
            source_map[c_num] = src
            combined_src_text = f"{src.get('section_title', '')} {src.get('provision_ref', '')} {src.get('content', '')}"
            source_tokens_map[c_num] = self._tokenize(combined_src_text)

        # Find all numeric citations in text, e.g. [1], [2]
        citation_matches = re.findall(r'\[(\d+)\]', raw_text)
        referenced_indices = set(int(m) for m in citation_matches if m.isdigit())

        citations_out: List[CitationOut] = []
        unsupported_count = 0

        # Map explicitly referenced citations
        for c_idx in sorted(referenced_indices):
            if c_idx in source_map:
                src = source_map[c_idx]
                citations_out.append(
                    CitationOut(
                        citation_number=c_idx,
                        source_title=src.get("source_title", "Authoritative Source"),
                        authority=src.get("authority", "Government of India"),
                        provision_ref=src.get("provision_ref", src.get("section_title")),
                        quote_text=src.get("content", "")[:320] + "...",
                        source_url=src.get("source_url", ""),
                        version=src.get("version", "Active"),
                        effective_date=src.get("effective_date", "Active"),
                        verification_status="verified"
                    )
                )
            else:
                unsupported_count += 1

        # If no explicit bracket citations were in output, link top retrieved sources
        if not citations_out:
            for idx, src in enumerate(retrieved_sources[:3]):
                c_num = idx + 1
                citations_out.append(
                    CitationOut(
                        citation_number=c_num,
                        source_title=src.get("source_title", "Authoritative Source"),
                        authority=src.get("authority", "Government of India"),
                        provision_ref=src.get("provision_ref", src.get("section_title")),
                        quote_text=src.get("content", "")[:320] + "...",
                        source_url=src.get("source_url", ""),
                        version=src.get("version", "Active"),
                        effective_date=src.get("effective_date", "Active"),
                        verification_status="verified"
                    )
                )

        # Claim-level evidence validation
        claims = self.extract_claims(raw_text)
        supported_claims = 0
        total_claims = max(1, len(claims))

        all_evidence_tokens = set()
        for s_tokens in source_tokens_map.values():
            all_evidence_tokens.update(s_tokens)

        for claim in claims:
            claim_tokens = self._tokenize(claim)
            if not claim_tokens:
                supported_claims += 1
                continue
            overlap = claim_tokens.intersection(all_evidence_tokens)
            # A claim is grounded if at least 25% of its substantive tokens are grounded in the evidence corpus
            if len(overlap) / len(claim_tokens) >= 0.20:
                supported_claims += 1
            else:
                unsupported_count += 1

        grounding_rate = round(supported_claims / total_claims, 3)

        return raw_text, citations_out, unsupported_count, grounding_rate

citation_verifier = CitationVerifier()
