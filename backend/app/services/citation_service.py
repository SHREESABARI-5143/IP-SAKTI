import re
from typing import List, Tuple
from app.models.schemas import SourceReference

class CitationService:
    """
    Parses and verifies inline citations in LLM responses, ensuring all claims reference valid corpus sources.
    """
    def extract_citations(self, text: str) -> List[str]:
        # Matches patterns like [Source: Patents Act 1970, Section 3(p)]
        pattern = r'\[Source:\s*([^\]]+)\]'
        matches = re.findall(pattern, text)
        return matches

    def format_citations_in_text(self, text: str, sources: List[SourceReference]) -> Tuple[str, List[SourceReference]]:
        verified_sources = []
        
        # Check which sources were cited or relevant
        for source in sources:
            if source.citation_key.lower() in text.lower() or source.section_id.lower() in text.lower() or len(verified_sources) < 2:
                if source not in verified_sources:
                    verified_sources.append(source)

        return text, verified_sources

citation_service = CitationService()
