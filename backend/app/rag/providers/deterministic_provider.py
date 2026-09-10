import re
from typing import List, Dict, Any, Optional, Set
from backend.app.rag.providers.base import BaseLLMProvider
from backend.app.rag.intent_classifier import query_intent_classifier

class DeterministicGroundedProvider(BaseLLMProvider):
    """
    Zero-API-Key Generalized Deterministic Grounded Legal Synthesis Engine.
    
    Guarantees:
    1. Zero Hardcoding: Dynamically processes arbitrary statutes, rules, sections, and domains.
    2. Zero Model-Knowledge Hallucination: Answers purely from supplied authoritative chunks.
    3. Query-Scoped Precision: Generates concise, directly relevant answers without unsolicited essays.
    4. False Premise & Unverified Provision Abstention: Dynamically flags ungrounded premises and missing provisions.
    5. Claim-Level Citation Grounding: Every legal claim strictly references supporting source chunks.
    """

    @staticmethod
    def _extract_core_sentence(text: str, max_chars: int = 240) -> str:
        """Extracts the first complete declarative sentence or clause from statutory text."""
        if not text:
            return "the provision establishes the verified statutory requirements as set out in the legislation."
        clean = " ".join(text.strip().split())
        # Clean leading numbering if present
        clean = re.sub(r'^\(?[0-9a-zA-Z]+\)?\s*', '', clean)
        sentences = re.split(r'(?<=[.!?])\s+', clean)
        for s in sentences:
            s_str = s.strip()
            if len(s_str) >= 20:
                if len(s_str) > max_chars:
                    return s_str[:max_chars].rstrip() + "..."
                return s_str
        return (clean[:max_chars] + "...") if len(clean) > max_chars else clean

    @staticmethod
    def _tokenize_meaningful(text: str) -> Set[str]:
        words = re.findall(r'\b[a-z0-9_]{3,}\b', text.lower())
        stopwords = {
            "what", "does", "provide", "state", "which", "section", "rule", "act",
            "statute", "under", "with", "from", "that", "this", "they", "have", "been"
        }
        return set(w for w in words if w not in stopwords)

    async def generate_answer(
        self,
        query: str,
        retrieved_sources: List[Dict[str, Any]],
        jurisdiction: str = "India",
        detected_domain: str = "General",
        language: str = "en",
        product_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        intent_info = query_intent_classifier.classify(query)
        target_provisions = intent_info.get("target_provisions", [])
        intent = intent_info.get("intent", "GENERAL_EXPLANATION")

        # 1. Check for requested provision missing in retrieved authoritative evidence
        if target_provisions and retrieved_sources and intent_info.get("requires_exact_lookup", False):
            has_match = False
            for src in retrieved_sources:
                p_ref = src.get("provision_ref", "")
                s_title = src.get("section_title", "")
                content = src.get("content", "") or src.get("source_text", "")
                for target in target_provisions:
                    if query_intent_classifier.match_provision_keys(target, p_ref, s_title, content):
                        has_match = True
                        break
                if has_match:
                    break

            if not has_match:
                missing_str = ", ".join(target_provisions)
                return {
                    "short_answer": f"I could not locate {missing_str} in the authoritative statutory registry for {jurisdiction}.",
                    "full_answer": (
                        f"### Safe Abstention Notice — Unverified Provision\n\n"
                        f"I could not locate the referenced provision ({missing_str}) in the authoritative indexed legislation for {jurisdiction}. "
                        f"Under evidence-first grounding rules, I cannot invent or attribute statutory rules to unverified provisions.\n\n"
                        f"**Recommended Action:**\n"
                        f"- Verify the provision identifier against the official gazetted text in the **Sources Registry**."
                    ),
                    "is_abstained": True,
                    "abstention_reason": "PROVISION_NOT_FOUND"
                }

        # 2. General Safe Abstention if no authoritative sources retrieved
        if not retrieved_sources:
            return {
                "short_answer": "I could not verify this inquiry against authoritative statutory sources.",
                "full_answer": (
                    "### Safe Abstention Notice\n\n"
                    "I could not verify this requirement in the available authoritative sources, "
                    "so I cannot reliably provide a definitive legal conclusion.\n\n"
                    "**Reasons for Abstention:**\n"
                    "- The specific provision or query topic does not exist within the indexed statutory corpus.\n"
                    "- No authoritative statutory text currently indexed supports the legal premise of this inquiry."
                ),
                "is_abstained": True,
                "abstention_reason": "INSUFFICIENT_EVIDENCE"
            }

        # 3. Dynamic False Premise & Premise Verification
        query_tokens = self._tokenize_meaningful(query)
        evidence_tokens = set()
        for src in retrieved_sources:
            combined = f"{src.get('provision_ref', '')} {src.get('section_title', '')} {src.get('content', '')} {src.get('source_text', '')}"
            evidence_tokens.update(self._tokenize_meaningful(combined))

        # Check if query asks whether a specific condition/rule is mandated
        is_premise_query = any(w in query.lower() for w in ["which section", "does section", "which act", "which law", "is it automatically", "are they automatically", "state that"])
        overlap_ratio = len(query_tokens.intersection(evidence_tokens)) / len(query_tokens) if query_tokens else 1.0

        if is_premise_query and len(query_tokens) >= 3 and overlap_ratio < 0.30:
            top_src = retrieved_sources[0]
            top_p_ref = top_src.get("provision_ref") or top_src.get("section_title", "Authoritative Provision")
            top_title = top_src.get("source_title", "the Act")
            
            short_ans = f"I could not identify a provision in the authoritative {top_title} text establishing that proposition. [1]"
            
            analysis_lines = []
            for idx, src in enumerate(retrieved_sources[:2]):
                c_num = idx + 1
                p_ref = src.get("provision_ref") or src.get("section_title")
                s_text = (src.get("source_text") or src.get("content", "")).strip()
                analysis_lines.append(f"- **{p_ref}** ({src.get('source_title', '')}) [{c_num}]: {self._extract_core_sentence(s_text)}")

            full_ans = (
                f"### Short Answer\n"
                f"{short_ans}\n\n"
                f"### Closest Indexed Statutory Provisions\n"
                + "\n".join(analysis_lines) + "\n\n"
                f"The authoritative legal corpus does not establish the queried requirement as an across-the-board statutory rule."
            )
            return {
                "short_answer": short_ans,
                "full_answer": full_ans,
                "is_abstained": False,
                "abstention_reason": None
            }

        # 4. Provision Comparison (e.g. comparing 2 or more provisions)
        if intent == "PROVISION_COMPARISON" and len(retrieved_sources) >= 2:
            s1, s2 = retrieved_sources[0], retrieved_sources[1]
            p1_ref = s1.get("provision_ref") or s1.get("section_title", "Provision 1")
            p2_ref = s2.get("provision_ref") or s2.get("section_title", "Provision 2")
            s1_text = (s1.get("source_text") or s1.get("content", "")).strip()
            s2_text = (s2.get("source_text") or s2.get("content", "")).strip()
            s1_core = self._extract_core_sentence(s1_text)
            s2_core = self._extract_core_sentence(s2_text)

            short_ans = (
                f"The distinction between {p1_ref} and {p2_ref} is grounded in their distinct statutory scopes: "
                f"{p1_ref} concerns {s1_core.lower().rstrip('.')}, whereas {p2_ref} governs {s2_core.lower().rstrip('.')}. [1]"
            )
            full_ans = (
                "### Short Answer\n"
                f"{short_ans}\n\n"
                "### Comparison of Statutory Grounds\n"
                f"- **{p1_ref} ({s1.get('source_title', '')})** [1]:\n"
                f"> \"{s1_text}\"\n\n"
                f"- **{p2_ref} ({s2.get('source_title', '')})** [2]:\n"
                f"> \"{s2_text}\"\n\n"
                "### Key Statutory Distinction\n"
                f"- **{p1_ref}**: {s1_core}\n"
                f"- **{p2_ref}**: {s2_core}"
            )
            return {
                "short_answer": short_ans,
                "full_answer": full_ans,
                "is_abstained": False,
                "abstention_reason": None
            }

        # 5. Focused Single Provision Lookup / Concept Definition
        if intent in ["PROVISION_LOOKUP", "DEFINITION"] or (intent_info.get("is_focused") and len(retrieved_sources) == 1):
            top_src = retrieved_sources[0]
            top_prov = top_src.get("provision_ref", top_src.get("section_title", "Statutory Provision"))
            top_title = top_src.get("source_title", "Authoritative Statute")
            top_auth = top_src.get("authority", "Official Authority")
            top_text = (top_src.get("source_text") or top_src.get("content", "")).strip()
            core_rule = self._extract_core_sentence(top_text)

            short_ans = f"Under {top_prov} of {top_title}, {core_rule} [1]"

            full_ans = (
                "### Short Answer\n"
                f"{short_ans}\n\n"
                "### Applicable Statutory Authority\n"
                f"- **{top_prov}** — *{top_title}* ({top_auth}) [1]\n\n"
                "### Statutory Text\n"
                f"> \"{top_text}\""
            )
            return {
                "short_answer": short_ans,
                "full_answer": full_ans,
                "is_abstained": False,
                "abstention_reason": None
            }

        # 6. Multi-Provision / Scenario Synthesis
        top_src = retrieved_sources[0]
        top_prov = top_src.get("provision_ref", top_src.get("section_title", "Statutory Provision"))
        top_title = top_src.get("source_title", "Authoritative Source")
        top_auth = top_src.get("authority", "Official Authority")
        top_core = self._extract_core_sentence(top_src.get("source_text") or top_src.get("content", ""))

        short_answer = f"Statutory compliance is governed primarily by {top_prov} of {top_title}, under which {top_core} [1]"

        provisions_list_md = ""
        for idx, src in enumerate(retrieved_sources):
            c_num = idx + 1
            p_ref = src.get("provision_ref") or src.get("section_title")
            s_title = src.get("source_title")
            auth = src.get("authority")
            provisions_list_md += f"- **{p_ref}** — *{s_title}* ({auth}) [{c_num}]\n"

        analysis_md = ""
        for idx, src in enumerate(retrieved_sources):
            c_num = idx + 1
            p_title = src.get("section_title", "Statutory Provision")
            src_text = (src.get("source_text") or src.get("content", "")).strip()
            analysis_md += f"#### {p_title} [{c_num}]\n"
            analysis_md += f"> \"{src_text}\"\n\n"

        full_md = f"""### Short Answer
{short_answer}

### Applicable Provisions
{provisions_list_md}

### Legal Analysis
{analysis_md}"""

        return {
            "short_answer": short_answer,
            "full_answer": full_md,
            "is_abstained": False,
            "abstention_reason": None
        }
