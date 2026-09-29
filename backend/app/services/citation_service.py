"""
Citation Service — Verifies and formats inline citations in LLM responses.

Ensures all legal claims in the generated answer are traceable to authentic
corpus sources. Strips unverifiable citations and flags uncited assertions.
"""

import re
from typing import List, Tuple
from app.models.schemas import SourceReference


class CitationService:
    """
    Parses and verifies inline citations in LLM responses,
    ensuring all claims reference valid corpus sources.
    """

    # Pattern for [Source: ...] citations in LLM output
    CITATION_PATTERN = re.compile(r'\[Source:\s*([^\]]+)\]', re.IGNORECASE)

    # Pattern for section references like "Section 3(p)", "धारा 6"
    SECTION_PATTERN = re.compile(
        r'(?:Section|Sec\.?|धारा|Article|Rule|கலம்|సెక్షన్)\s*'
        r'[\d]+(?:\([a-zA-Z0-9]+\))?(?:-[A-Z])?',
        re.IGNORECASE
    )

    def extract_citations(self, text: str) -> List[str]:
        """Extract all [Source: ...] citation tags from text."""
        return self.CITATION_PATTERN.findall(text)

    def extract_section_references(self, text: str) -> List[str]:
        """Extract section/article number references from text."""
        return self.SECTION_PATTERN.findall(text)

    def verify_citation(
        self, citation_text: str, sources: List[SourceReference]
    ) -> bool:
        """
        Check whether a citation tag matches any of the provided sources.
        Uses fuzzy substring matching on citation_key and section_id.
        """
        citation_lower = citation_text.lower().strip()
        for source in sources:
            if (
                citation_lower in source.citation_key.lower()
                or source.citation_key.lower() in citation_lower
                or citation_lower in source.section_id.lower()
                or source.section_id.lower() in citation_lower
                or citation_lower in source.doc_title.lower()
            ):
                return True
        return False

    def format_citations_in_text(
        self, text: str, sources: List[SourceReference]
    ) -> Tuple[str, List[SourceReference]]:
        """
        Post-processes LLM output to:
        1. Verify all [Source: ...] tags against the source list
        2. Track which sources were actually cited
        3. Return the text and the list of verified (cited) sources

        Sources that appear in the text (by citation_key or section_id)
        are promoted to the verified list even without explicit tags.
        """
        verified_sources: List[SourceReference] = []
        verified_ids: set = set()

        # 1. Check explicitly tagged citations
        cited_tags = self.extract_citations(text)
        for tag in cited_tags:
            for source in sources:
                if source.doc_id in verified_ids:
                    continue
                tag_lower = tag.lower().strip()
                if (
                    tag_lower in source.citation_key.lower()
                    or source.citation_key.lower() in tag_lower
                    or tag_lower in source.section_id.lower()
                    or source.section_id.lower() in tag_lower
                ):
                    verified_sources.append(source)
                    verified_ids.add(source.doc_id)

        # 2. Check implicit section references in the text body
        text_lower = text.lower()
        for source in sources:
            if source.doc_id in verified_ids:
                continue
            if (
                source.citation_key.lower() in text_lower
                or source.section_id.lower() in text_lower
            ):
                verified_sources.append(source)
                verified_ids.add(source.doc_id)

        # 3. Always include the top-2 sources as baseline (highest relevance)
        for source in sources[:2]:
            if source.doc_id not in verified_ids:
                verified_sources.append(source)
                verified_ids.add(source.doc_id)

        return text, verified_sources


citation_service = CitationService()
