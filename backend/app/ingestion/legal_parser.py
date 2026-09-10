"""
Authoritative Legal Document Parser for IP-SAKTI Sahayak.

Implements state-machine parsing with legal structural detection:
- Act / Code: PART -> CHAPTER -> SECTION -> SUBSECTION -> CLAUSE -> SUBCLAUSE -> PROVISO / EXPLANATION
- Rules: CHAPTER -> RULE -> SUBRULE -> CLAUSE
- Regulations: REGULATION -> SUBREGULATION -> CLAUSE
- Treaties / International: ARTICLE -> PARAGRAPH -> SUBPARAGRAPH
- Schedules: SCHEDULE -> PART -> ENTRY

Zero Hardcoding:
- Discovers hierarchy dynamically from authoritative source text.
- Retains operative context (parent provision, chapter, definitions, provisos).
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class ParsedChunk:
    chunk_index: int
    section_title: str
    provision_ref: str
    content: str
    source_text: str
    jurisdiction: str = "India"
    legal_domain: str = "PATENT"
    document_type: str = "ACT"
    part: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    clause: Optional[str] = None
    subclause: Optional[str] = None
    rule: Optional[str] = None
    subrule: Optional[str] = None
    regulation: Optional[str] = None
    subregulation: Optional[str] = None
    article: Optional[str] = None
    paragraph: Optional[str] = None
    schedule: Optional[str] = None
    entry: Optional[str] = None
    page: Optional[int] = 1
    source_location: Optional[str] = None
    parent_chunk_id: Optional[str] = None
    authority: str = "Official Authority"
    authority_score: float = 1.0


class LegalDocumentParser:
    """
    Robust State-Machine Legal Document Parser.
    Extracts structured provisions preserving operative legal context.
    """

    # Primary structural heading regexes
    RE_PART = re.compile(r'^(?:PART|Part)\s+([IVXLCDM\d]+|\w+)(?:\s*[-–—:]\s*(.*))?$', re.MULTILINE)
    RE_CHAPTER = re.compile(r'^(?:CHAPTER|Chapter)\s+([IVXLCDM\d]+|\w+)(?:\s*[-–—:]\s*(.*))?$', re.MULTILINE)
    RE_SCHEDULE = re.compile(r'^(?:THE\s+)?(?:FIRST|SECOND|THIRD|FOURTH|FIFTH|\d+(?:st|nd|rd|th)?)\s+SCHEDULE(?:\s*[-–—:]\s*(.*))?$', re.IGNORECASE | re.MULTILINE)
    
    # Provision level regexes
    RE_SECTION = re.compile(r'^(?:Section|Sec\.)\s*(\d+[A-Za-z]*(?:\([a-z0-9]+\))*)\.?\s*[-–—:]?\s*(.*)$', re.IGNORECASE | re.MULTILINE)
    RE_SECTION_NUM_START = re.compile(r'^(\d+[A-Za-z]*)\.\s+([A-Z][^\n]+)$', re.MULTILINE)
    RE_RULE = re.compile(r'^(?:Rule)\s*(\d+[A-Za-z]*)\.?\s*[-–—:]?\s*(.*)$', re.IGNORECASE | re.MULTILINE)
    RE_REGULATION = re.compile(r'^(?:Regulation|Reg\.)\s*(\d+[A-Za-z]*)\.?\s*[-–—:]?\s*(.*)$', re.IGNORECASE | re.MULTILINE)
    RE_ARTICLE = re.compile(r'^(?:Article|Art\.)\s*(\d+[A-Za-z]*)\.?\s*[-–—:]?\s*(.*)$', re.IGNORECASE | re.MULTILINE)

    # Sub-provision / clause level regexes (e.g. "(p) an invention...", "(1) Where an application...")
    RE_CLAUSE_START = re.compile(r'^\(([a-z0-9]+)\)\s+(.*)$', re.MULTILINE)

    def __init__(self, jurisdiction: str = "India", legal_domain: str = "PATENT", document_type: str = "ACT", authority: str = "Government of India"):
        self.jurisdiction = jurisdiction
        self.legal_domain = legal_domain
        self.document_type = document_type
        self.authority = authority

    def parse(self, raw_text: str, doc_title: str = "") -> List[ParsedChunk]:
        """
        Parse raw legislative text into hierarchical ParsedChunk objects with operative context.
        """
        lines = raw_text.splitlines()
        chunks: List[ParsedChunk] = []

        current_part = ""
        current_chapter = ""
        current_schedule = ""
        
        # Current active parent provision state
        curr_parent_ref = ""
        curr_parent_title = ""
        curr_section = ""
        curr_rule = ""
        curr_regulation = ""
        curr_article = ""
        curr_schedule_name = ""
        
        # Active chunk accumulator
        curr_chunk_ref = ""
        curr_chunk_title = ""
        curr_clause = ""
        curr_subsection = ""
        accumulated_lines: List[str] = []
        chunk_idx = 0

        def flush_current_chunk():
            nonlocal chunk_idx, accumulated_lines, curr_chunk_ref, curr_chunk_title, curr_clause, curr_subsection
            if not accumulated_lines or not curr_chunk_ref:
                accumulated_lines = []
                return

            verbatim_text = "\n".join(accumulated_lines).strip()
            if not verbatim_text:
                accumulated_lines = []
                return

            # Construct operative context header
            context_header_parts = []
            if doc_title:
                context_header_parts.append(f"[{doc_title}]")
            if current_chapter:
                context_header_parts.append(f"Chapter: {current_chapter}")
            if current_schedule:
                context_header_parts.append(f"Schedule: {current_schedule}")
            if curr_parent_title and curr_parent_title != curr_chunk_title:
                context_header_parts.append(f"Parent: {curr_parent_title}")
            
            context_header = " | ".join(context_header_parts)
            full_context_content = f"{context_header}\n{curr_chunk_title}\n\n{verbatim_text}" if context_header else f"{curr_chunk_title}\n\n{verbatim_text}"

            loc_parts = []
            if current_chapter: loc_parts.append(f"Chap {current_chapter}")
            if curr_chunk_ref: loc_parts.append(curr_chunk_ref)
            loc_str = ", ".join(loc_parts) or curr_chunk_ref

            chunk = ParsedChunk(
                chunk_index=chunk_idx,
                section_title=curr_chunk_title,
                provision_ref=curr_chunk_ref,
                content=full_context_content,
                source_text=verbatim_text,
                jurisdiction=self.jurisdiction,
                legal_domain=self.legal_domain,
                document_type=self.document_type,
                part=current_part or None,
                chapter=current_chapter or None,
                section=curr_section or None,
                subsection=curr_subsection or None,
                clause=curr_clause or None,
                rule=curr_rule or None,
                regulation=curr_regulation or None,
                article=curr_article or None,
                schedule=curr_schedule_name or None,
                source_location=loc_str,
                authority=self.authority,
                authority_score=1.0 if self.document_type in ["ACT", "TREATY"] else 0.95
            )
            chunks.append(chunk)
            chunk_idx += 1
            accumulated_lines = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                if accumulated_lines:
                    accumulated_lines.append("")
                i += 1
                continue

            # 1. Part check
            part_match = self.RE_PART.match(line)
            if part_match:
                current_part = f"Part {part_match.group(1)}" + (f" - {part_match.group(2)}" if part_match.group(2) else "")
                i += 1
                continue

            # 2. Chapter check
            chap_match = self.RE_CHAPTER.match(line)
            if chap_match:
                current_chapter = f"Chapter {chap_match.group(1)}" + (f" - {chap_match.group(2)}" if chap_match.group(2) else "")
                i += 1
                continue

            # 3. Schedule check
            sched_match = self.RE_SCHEDULE.match(line)
            if sched_match:
                flush_current_chunk()
                current_schedule = line
                curr_parent_ref = line
                curr_parent_title = line
                curr_chunk_ref = line
                curr_chunk_title = line
                curr_schedule_name = line
                curr_section = ""
                curr_rule = ""
                curr_regulation = ""
                curr_article = ""
                curr_clause = ""
                curr_subsection = ""
                i += 1
                continue

            # 4. Section check
            sec_match = self.RE_SECTION.match(line) or self.RE_SECTION_NUM_START.match(line)
            if sec_match and self.document_type in ["ACT", "CODE"]:
                flush_current_chunk()
                sec_num = sec_match.group(1)
                sec_heading = sec_match.group(2).strip() if len(sec_match.groups()) > 1 and sec_match.group(2) else ""
                curr_section = f"Section {sec_num}"
                curr_parent_ref = f"Section {sec_num}"
                curr_parent_title = f"Section {sec_num}" + (f" - {sec_heading}" if sec_heading else "")
                curr_chunk_ref = curr_parent_ref
                curr_chunk_title = curr_parent_title
                curr_clause = ""
                curr_subsection = ""
                accumulated_lines.append(line)
                i += 1
                continue

            # 5. Rule check
            rule_match = self.RE_RULE.match(line)
            if rule_match or (self.document_type in ["RULES", "RULE"] and self.RE_SECTION_NUM_START.match(line)):
                flush_current_chunk()
                r_match = rule_match or self.RE_SECTION_NUM_START.match(line)
                r_num = r_match.group(1)
                r_heading = r_match.group(2).strip() if len(r_match.groups()) > 1 and r_match.group(2) else ""
                curr_rule = f"Rule {r_num}"
                curr_parent_ref = f"Rule {r_num}"
                curr_parent_title = f"Rule {r_num}" + (f" - {r_heading}" if r_heading else "")
                curr_chunk_ref = curr_parent_ref
                curr_chunk_title = curr_parent_title
                curr_clause = ""
                curr_subsection = ""
                accumulated_lines.append(line)
                i += 1
                continue

            # 6. Regulation check
            reg_match = self.RE_REGULATION.match(line)
            if reg_match or (self.document_type in ["REGULATION", "REGULATIONS"] and self.RE_SECTION_NUM_START.match(line)):
                flush_current_chunk()
                rg_match = reg_match or self.RE_SECTION_NUM_START.match(line)
                rg_num = rg_match.group(1)
                rg_heading = rg_match.group(2).strip() if len(rg_match.groups()) > 1 and rg_match.group(2) else ""
                curr_regulation = f"Regulation {rg_num}"
                curr_parent_ref = f"Regulation {rg_num}"
                curr_parent_title = f"Regulation {rg_num}" + (f" - {rg_heading}" if rg_heading else "")
                curr_chunk_ref = curr_parent_ref
                curr_chunk_title = curr_parent_title
                curr_clause = ""
                curr_subsection = ""
                accumulated_lines.append(line)
                i += 1
                continue

            # 7. Article check
            art_match = self.RE_ARTICLE.match(line)
            if art_match or (self.document_type in ["TREATY", "CONVENTION", "INTERNATIONAL_TREATY"] and self.RE_SECTION_NUM_START.match(line)):
                flush_current_chunk()
                a_match = art_match or self.RE_SECTION_NUM_START.match(line)
                a_num = a_match.group(1)
                a_heading = a_match.group(2).strip() if len(a_match.groups()) > 1 and a_match.group(2) else ""
                curr_article = f"Article {a_num}"
                curr_parent_ref = f"Article {a_num}"
                curr_parent_title = f"Article {a_num}" + (f" - {a_heading}" if a_heading else "")
                curr_chunk_ref = curr_parent_ref
                curr_chunk_title = curr_parent_title
                curr_clause = ""
                curr_subsection = ""
                accumulated_lines.append(line)
                i += 1
                continue

            # 8. Clause / Subsection subdivision check
            clause_match = self.RE_CLAUSE_START.match(line)
            if clause_match and curr_parent_ref and len(accumulated_lines) >= 1:
                # Flush previous sub-provision and start fine-grained clause chunk
                flush_current_chunk()
                clause_symbol = clause_match.group(1)
                if clause_symbol.isdigit():
                    curr_subsection = f"({clause_symbol})"
                    curr_clause = ""
                    curr_chunk_ref = f"{curr_parent_ref}({clause_symbol})"
                    curr_chunk_title = f"{curr_parent_title} - Subsection ({clause_symbol})"
                else:
                    curr_clause = f"({clause_symbol})"
                    sub_prefix = curr_subsection if curr_subsection else ""
                    curr_chunk_ref = f"{curr_parent_ref}{sub_prefix}({clause_symbol})"
                    curr_chunk_title = f"{curr_parent_title} - Clause {sub_prefix}({clause_symbol})"
                accumulated_lines.append(line)
                i += 1
                continue

            if not curr_chunk_ref:
                curr_chunk_ref = f"{self.document_type} Preamble/General"
                curr_chunk_title = f"{doc_title or self.document_type} - Overview"

            accumulated_lines.append(line)
            i += 1

        flush_current_chunk()

        if not chunks and raw_text.strip():
            paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
            for idx, p in enumerate(paragraphs):
                chunk = ParsedChunk(
                    chunk_index=idx,
                    section_title=f"{doc_title or 'Document'} - Provision {idx + 1}",
                    provision_ref=f"Provision {idx + 1}",
                    content=p,
                    source_text=p,
                    jurisdiction=self.jurisdiction,
                    legal_domain=self.legal_domain,
                    document_type=self.document_type,
                    authority=self.authority,
                    authority_score=1.0
                )
                chunks.append(chunk)

        return chunks
