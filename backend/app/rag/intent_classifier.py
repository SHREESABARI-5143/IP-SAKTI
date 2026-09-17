import re
from typing import Dict, Any, List, Optional, Set, Tuple
from backend.app.core.config import settings

class QueryIntentClassifier:
    """
    Generalized, zero-hardcoding legal query understanding and execution scope analyzer.
    
    Responsibilities:
    1. Universal Statutory Provision Extraction (Section X, Rule Y, Reg Z, Art W, Sched N)
    2. Dynamic Execution Path Routing (FAST_PATH, STANDARD_PATH, DEEP_PATH)
    3. Generic False Premise & Hypothesis Detection
    4. 4-Tier Evidence Relevance Classification (DIRECT, CONTEXTUAL, NON_SUPPORTING, IRRELEVANT)
    5. Evidence Sufficiency Evaluation
    """

    # Universal statutory provision identifier regex
    # Matches: Section 3, Section 3(p), Section 10(4)(d)(ii), Section 25(1)(k), Rule 158B, Rule 158B(1),
    # Regulation 4, Article 3, Clause 4, First Schedule, Second Schedule, etc.
    RE_PROVISION_UNIVERSAL = re.compile(
        r'(?:section|sec\.?|rule|regulation|reg\.?|article|art\.?|clause|பிரிவு|விதி|धारा|नियम|अनुच्छेद)\s*'
        r'([0-9]+(?:[\(\[][a-zA-Z0-9_\-]+[\)\]])*(?:[a-zA-Z])?)'
        r'|((?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|1st|2nd|3rd|4th|5th)\s+schedule)',
        re.IGNORECASE
    )

    RE_LOOKUP_INTENT = re.compile(
        r'^(?:what\s+(?:does|is|are|shall)|which\s+(?:section|rule|regulation|provision|article|schedule|act|clause)|where\s+in\s+the|explain\s+(?:section|rule|regulation|article)|tell\s+me\s+about\s+(?:section|rule|regulation))\b',
        re.IGNORECASE
    )

    RE_COMPARISON_INTENT = re.compile(
        r'\b(?:difference|differ|compare|distinguish|versus|vs\.?|between)\b',
        re.IGNORECASE
    )

    RE_MULTI_PROVISION_INTENT = re.compile(
        r'\b(?:all\s+(?:the\s+)?(?:legal\s+)?provisions|all\s+sections|list\s+all|comprehensive\s+(?:list|overview)|every\s+provision|summary\s+of\s+all)\b',
        re.IGNORECASE
    )

    RE_DEFINITION_INTENT = re.compile(
        r'^(?:what\s+is|define|meaning\s+of)\s+(?:a\s+|an\s+|the\s+)?(?:patent|prior\s+art|traditional\s+knowledge|tkdl|abs|novelty|inventive\s+step|ayurveda\s+aahar|biological\s+resource|prior\s+informed\s+consent)\b',
        re.IGNORECASE
    )

    RE_PATENTABILITY_INTENT = re.compile(
        r'\b(?:is\s+.+\s+patentable|can\s+i\s+patent|patent\s+eligibility|patentability|excluded\s+from\s+patent|patentable\s+or\s+not)\b',
        re.IGNORECASE
    )

    RE_PROCEDURE_INTENT = re.compile(
        r'\b(?:how\s+(?:do|to|can)\s+i\s+file|procedure|process\s+to\s+apply|steps\s+to\s+obtain|form\s+[i|ii|iii|iv|1-4]|application\s+process)\b',
        re.IGNORECASE
    )

    RE_FALSE_PREMISE_PATTERN = re.compile(
        r'\b(?:which\s+(?:section|rule|law|provision|act)\s+(?:requires|mandates|states|says\s+that)|does\s+(?:section|rule|regulation|article|schedule)\s+[^\s]+\s+(?:require|mandate|prescribe|state\s+that))\b',
        re.IGNORECASE
    )

    @staticmethod
    def match_provision_keys(target: str, chunk_ref: str, chunk_title: str, chunk_content: str = "") -> bool:
        """Robustly checks whether a target provision key matches a chunk reference, title, or content."""
        if not target:
            return False
        p_ref = re.sub(r'[\s\(\)\[\]\-_,.]+', '', (chunk_ref or "").lower())
        sec_title = re.sub(r'[\s\(\)\[\]\-_,.]+', '', (chunk_title or "").lower())
        t_norm = re.sub(r'[\s\(\)\[\]\-_,.]+', '', target.lower())

        # Category guard: statutory sections/rules and bare numeric targets must not match monograph/ntc entries unless specifically Section 40
        c_ref_low = (chunk_ref or "").lower()
        c_title_low = (chunk_title or "").lower()
        c_content_low = (chunk_content or "").lower()
        is_mono_chunk = ("monograph" in c_ref_low or c_title_low.startswith("monograph"))
        is_ntc_chunk = (c_ref_low.startswith("ntc") or "ntc entry" in c_title_low or "normally traded" in c_title_low or "section 40" in c_content_low)
        is_mono_target = ("monograph" in t_norm)
        is_ntc_target = ("ntc" in t_norm or "40" in t_norm)

        if (is_mono_chunk and not is_mono_target) or (is_ntc_chunk and not is_ntc_target):
            return False

        # 1. Exact or substring match on reference / title or explicit provision in content
        if t_norm in p_ref or t_norm in sec_title or p_ref in t_norm or (f"section {t_norm}" in c_content_low or f"section{t_norm}" in c_content_low):
            return True

        # 2. Extract base section/rule number and clause suffix e.g. "2ja" -> base 2, clause ja
        m_target = re.match(r'^(?:section|sec|rule|regulation|reg|article|art|clause)?(\d+)(.*)$', t_norm)
        m_chunk = re.match(r'^(?:section|sec|rule|regulation|reg|article|art|clause)?(\d+)(.*)$', p_ref)

        if m_target:
            sec_t = m_target.group(1)
            rest_t = m_target.group(2)  # e.g. "ja" or "l" or "1k"

            # Check if chunk reference or title contains base section number
            base_matched = False
            if m_chunk and m_chunk.group(1) == sec_t:
                base_matched = True
            elif f"section{sec_t}" in p_ref or f"rule{sec_t}" in p_ref or f"regulation{sec_t}" in p_ref or f"article{sec_t}" in p_ref:
                base_matched = True
            elif f"section{sec_t}" in sec_title or f"rule{sec_t}" in sec_title or f"regulation{sec_t}" in sec_title or f"article{sec_t}" in sec_title:
                base_matched = True

            if base_matched:
                if not rest_t:
                    return True
                # If clause specified (e.g. 'ja', 'l', 'a'), check if it exists in ref, title, or content
                clean_rest = re.sub(r'[^a-zA-Z0-9]', '', rest_t)
                if clean_rest in p_ref or clean_rest in sec_title:
                    return True
                # Check clause in content e.g. "(ja)" or "(l)" or "ja."
                if chunk_content:
                    c_low = chunk_content.lower()
                    if f"({clean_rest})" in c_low or f"clause ({clean_rest})" in c_low or f"sub-clause ({clean_rest})" in c_low or f"({clean_rest[0]})" in c_low:
                        return True

        return False

    def extract_provision_keys(self, text: str) -> List[str]:
        """
        Dynamically extracts all normalized statutory provision keys from arbitrary text.
        Returns normalized lowercase strings like ['3p', '251k', '158b', 'firstschedule'].
        """
        raw_matches = self.RE_PROVISION_UNIVERSAL.findall(text.lower())
        keys = []
        for m in raw_matches:
            item = (m[0] or m[1]) if isinstance(m, tuple) else m
            if item:
                norm = re.sub(r'[\s\(\)\[\]\-]+', '', str(item).lower())
                if norm and norm not in keys:
                    keys.append(norm)
        return keys

    def detect_false_premise_inquiry(self, query: str) -> bool:
        """Detects whether user query poses a potentially unverified statutory hypothesis/premise."""
        return bool(self.RE_FALSE_PREMISE_PATTERN.search(query))

    def classify(self, query: str) -> Dict[str, Any]:
        q_clean = query.strip()
        q_lower = q_clean.lower()

        target_provisions = self.extract_provision_keys(q_clean)
        has_explicit_provision = len(target_provisions) > 0
        is_false_premise_query = self.detect_false_premise_inquiry(q_clean)

        # 1. Multi-provision / comprehensive request -> DEEP_PATH
        if self.RE_MULTI_PROVISION_INTENT.search(q_lower):
            return {
                "intent": "MULTI_PROVISION_ANALYSIS",
                "execution_path": "DEEP_PATH",
                "is_focused": False,
                "target_provisions": target_provisions,
                "max_chunks": 4,
                "requires_exact_lookup": has_explicit_provision,
                "is_false_premise_query": is_false_premise_query,
                "allow_broad_analysis": True,
                "description": "Comprehensive multi-provision synthesis requested"
            }

        # 2. Provision Comparison -> STANDARD_PATH
        if self.RE_COMPARISON_INTENT.search(q_lower) and len(target_provisions) >= 2:
            return {
                "intent": "PROVISION_COMPARISON",
                "execution_path": "STANDARD_PATH",
                "is_focused": True,
                "target_provisions": target_provisions,
                "max_chunks": min(len(target_provisions), 3),
                "requires_exact_lookup": True,
                "is_false_premise_query": is_false_premise_query,
                "allow_broad_analysis": False,
                "description": f"Targeted comparison between provisions: {', '.join(target_provisions)}"
            }

        # 3. Direct Provision Lookup / Definition -> FAST_PATH
        if has_explicit_provision and (self.RE_LOOKUP_INTENT.search(q_lower) or len(q_clean.split()) <= 15):
            return {
                "intent": "PROVISION_LOOKUP",
                "execution_path": "FAST_PATH",
                "is_focused": True,
                "target_provisions": target_provisions,
                "max_chunks": max(1, len(target_provisions)),
                "requires_exact_lookup": True,
                "is_false_premise_query": is_false_premise_query,
                "allow_broad_analysis": False,
                "description": f"Direct statutory lookup for: {', '.join(target_provisions)}"
            }

        if self.RE_DEFINITION_INTENT.search(q_lower):
            return {
                "intent": "DEFINITION",
                "execution_path": "FAST_PATH",
                "is_focused": True,
                "target_provisions": target_provisions,
                "max_chunks": 1,
                "requires_exact_lookup": has_explicit_provision,
                "is_false_premise_query": is_false_premise_query,
                "allow_broad_analysis": False,
                "description": "Direct legal concept definition"
            }

        # 4. Specific Patentability / Exclusion -> STANDARD_PATH
        if self.RE_PATENTABILITY_INTENT.search(q_lower):
            return {
                "intent": "PATENTABILITY",
                "execution_path": "STANDARD_PATH",
                "is_focused": False,
                "target_provisions": target_provisions,
                "max_chunks": 3,
                "requires_exact_lookup": has_explicit_provision,
                "is_false_premise_query": is_false_premise_query,
                "allow_broad_analysis": False,
                "description": "Patentability evaluation"
            }

        # 5. Procedure / Filing -> STANDARD_PATH
        if self.RE_PROCEDURE_INTENT.search(q_lower):
            return {
                "intent": "PROCEDURE",
                "execution_path": "STANDARD_PATH",
                "is_focused": True,
                "target_provisions": target_provisions,
                "max_chunks": 2,
                "requires_exact_lookup": has_explicit_provision,
                "is_false_premise_query": is_false_premise_query,
                "allow_broad_analysis": False,
                "description": "Regulatory or filing procedure inquiry"
            }

        # 6. General Legal Query -> STANDARD_PATH
        return {
            "intent": "GENERAL_EXPLANATION",
            "execution_path": "STANDARD_PATH",
            "is_focused": False,
            "target_provisions": target_provisions,
            "max_chunks": 3,
            "requires_exact_lookup": has_explicit_provision,
            "is_false_premise_query": is_false_premise_query,
            "allow_broad_analysis": False,
            "description": "General statutory explanation"
        }

    def filter_evidence_by_scope(
        self,
        query: str,
        intent_info: Dict[str, Any],
        candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Classifies retrieved candidates into 4 distinct categories:
        A. DIRECT EVIDENCE: Directly supports target provision or core query propositions.
        B. CONTEXTUAL EVIDENCE: Useful background/parent provision context.
        C. RELATED BUT NON-SUPPORTING: Topically related but irrelevant to the proposition -> DROPPED.
        D. IRRELEVANT: Poor score/out-of-scope -> DROPPED.
        
        Only Category A and necessary Category B evidence reach the generator.
        """
        if not candidates:
            return []

        target_provisions = intent_info.get("target_provisions", [])
        max_chunks = intent_info.get("max_chunks", 3)

        direct_evidence: List[Dict[str, Any]] = []
        contextual_evidence: List[Dict[str, Any]] = []

        # 1. Exact Target Provision Matching
        if target_provisions:
            for chunk in candidates:
                p_ref = chunk.get("provision_ref", "")
                sec_title = chunk.get("section_title", "")
                content = chunk.get("content", "") or chunk.get("source_text", "")
                
                is_direct = False
                for t in target_provisions:
                    if self.match_provision_keys(t, p_ref, sec_title, content):
                        chunk["evidence_type"] = "DIRECT"
                        direct_evidence.append(chunk)
                        is_direct = True
                        break
                
                if not is_direct and chunk.get("retrieval_score", 0.0) >= settings.INTENT_EVIDENCE_DIRECT_THRESHOLD:
                    chunk["evidence_type"] = "CONTEXTUAL"
                    contextual_evidence.append(chunk)

            if direct_evidence:
                fused = direct_evidence[:max_chunks]
                if len(fused) < max_chunks and contextual_evidence:
                    fused.extend(contextual_evidence[:max_chunks - len(fused)])
                return fused

        # 2. General Scope Filtering based on composite retrieval score
        top_score = candidates[0].get("retrieval_score", 1.0)
        filtered = []
        for c in candidates:
            score = c.get("retrieval_score", 0.0)
            if score >= (top_score * settings.INTENT_EVIDENCE_DIRECT_THRESHOLD) or c.get("exact_provision_match", False):
                c["evidence_type"] = "DIRECT" if score >= (top_score * settings.INTENT_EVIDENCE_CONTEXTUAL_THRESHOLD) else "CONTEXTUAL"
                filtered.append(c)

        return filtered[:max_chunks] if filtered else candidates[:max_chunks]

    def check_evidence_sufficiency(
        self,
        intent_info: Dict[str, Any],
        evidence: List[Dict[str, Any]]
    ) -> Tuple[bool, Optional[str]]:
        """
        Pre-generation Evidence Availability Gate:
        Verifies whether retrieved evidence is sufficient to answer without pretrained knowledge leakage.
        """
        if not evidence:
            return False, "NO_EVIDENCE_RETRIEVED"

        target_provisions = intent_info.get("target_provisions", [])
        if target_provisions and intent_info.get("requires_exact_lookup"):
            # Ensure at least one target provision was directly matched
            has_match = False
            for chunk in evidence:
                p_ref = chunk.get("provision_ref", "")
                sec_title = chunk.get("section_title", "")
                content = chunk.get("content", "") or chunk.get("source_text", "")
                for t in target_provisions:
                    if self.match_provision_keys(t, p_ref, sec_title, content):
                        has_match = True
                        break
                if has_match:
                    break
            
            if not has_match:
                # Requested provision does not exist in authoritative corpus
                return False, "REQUESTED_PROVISION_NOT_IN_CORPUS"

        # Check retrieval score confidence
        top_score = evidence[0].get("retrieval_score", 0.0)
        top_chunk = evidence[0]
        token_coverage = top_chunk.get("token_coverage", 1.0)
        is_exact = top_chunk.get("exact_provision_match", False)

        if not is_exact and (top_score < settings.RRF_DEFAULT_MIN_SCORE or token_coverage < settings.RRF_FALLBACK_MIN_SCORE):
            return False, "INSUFFICIENT_RETRIEVAL_SCORE"

        return True, None

query_intent_classifier = QueryIntentClassifier()
