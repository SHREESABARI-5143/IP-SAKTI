"""
QA Service — Graph-Hybrid RAG Pipeline for IP-SAKTI Sahayak.

Implements a 3-agent orchestration architecture:
  Agent 1: Query Planner — Decomposes user query into search intents, detects
           jurisdiction, language, and product category signals.
  Agent 2: Validity Checker — Traverses knowledge graph edges (AMENDED_BY,
           REPEALED_BY, CROSS_REFERENCES) to validate temporal currency of
           retrieved provisions and enrich context.
  Agent 3: Synthesis & Citation — Generates a grounded, citation-tagged
           response using the LLM with strict hallucination barriers.

LLM Providers:
  - Primary: Local Ollama (Qwen 2.5:3b-Instruct) — 100% offline & private.
  - Fallback: Google Gemini API (if configured).
"""

import os
import json
import urllib.request
import urllib.error
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.models.schemas import QueryRequest, QueryResponse, SourceReference
from app.services.vector_service import vector_service
from app.services.graph_service import graph_service
from app.services.citation_service import citation_service
from app.services.language_service import language_service

try:
    import google.generativeai as genai
except ImportError:
    genai = None


# ─────────────────────────────────────────────────────────
# Refusal messages by language — used when corpus coverage
# is insufficient to answer reliably.
# ─────────────────────────────────────────────────────────
REFUSAL_MESSAGES: Dict[str, str] = {
    "hi": (
        "मुझे इस प्रश्न का निश्चित उत्तर देने के लिए पर्याप्त सत्यापित "
        "कानूनी स्रोत नहीं मिले। कृपया किसी योग्य पेटेंट / कानून विशेषज्ञ "
        "से परामर्श लें।"
    ),
    "sa": (
        "अस्मिन् विषये प्रामाणिक-विधि-स्रोतांसि न प्राप्तानि। "
        "कृपया कश्चित् विधिज्ञं (Patent Attorney) सम्पृच्छन्तु।"
    ),
    "ta": (
        "இந்த கேள்விக்கு உறுதியான பதிலளிக்க போதுமான சட்ட ஆதாரங்கள் "
        "கிடைக்கவில்லை. தகுதிவாய்ந்த காப்புரிமை வழக்கறிஞரை அணுகவும்."
    ),
    "te": (
        "ఈ ప్రశ్నకు స్పష్టమైన సమాధానం ఇవ్వడానికి తగిన చట్టపరమైన "
        "ఆధారాలు లభించలేదు. దయచేసి అర్హత కలిగిన పేటెంట్ న్యాయవాదిని "
        "సంప్రదించండి."
    ),
    "mr": (
        "या प्रश्नाचे निश्चित उत्तर देण्यासाठी पुरेसे कायदेशीर स्रोत "
        "आढळले नाहीत. कृपया पात्र पेटंट सल्लागाराचा सल्ला घ्या."
    ),
    "bn": (
        "এই প্রশ্নের নির্ভরযোগ্য উত্তরের জন্য পর্যাপ্ত আইনি উৎস "
        "পাওয়া যায়নি। অনুগ্রহ করে একজন দক্ষ পেটেন্ট আইনজীবীর পরামর্শ নিন।"
    ),
    "gu": (
        "આ પ્રશ્નનો ચોક્કસ જવાબ આપવા માટે પૂરતા પ્રમાણિત કાનૂની "
        "સ્ત્રોત મળ્યા નથી. કૃપા કરીને યોગ્ય પેટન્ટ વકીલની સલાહ લો."
    ),
    "en": (
        "I do not have enough verified statutory or pharmacopoeial source "
        "material in the indexed corpus to answer this query reliably. "
        "Please consult a qualified Intellectual Property attorney."
    ),
}


# ─────────────────────────────────────────────────────────
# Language instruction guide for multilingual generation.
# ─────────────────────────────────────────────────────────
LANG_GUIDES: Dict[str, str] = {
    "en": (
        "English: answer in clear, structured, professional English "
        "with bullet points and clear headings."
    ),
    "hi": (
        "Hindi (हिन्दी): answer completely in Hindi (Devanagari script), "
        "explaining legal nuances with clarity. Maintain statutory section "
        "numbers e.g. धारा 3(p) [Section 3(p)]."
    ),
    "sa": (
        "Sanskrit (संस्कृतम्): answer in Sanskrit (Devanagari script), "
        "incorporating classical Ayurvedic terminology and citing statutory "
        "sections e.g. धारा 3(p) [Section 3(p)]."
    ),
    "ta": (
        "Tamil (தமிழ்): answer in formal Tamil script, explaining "
        "statutory conditions clearly with bracketed section citations."
    ),
    "te": (
        "Telugu (తెలుగు): answer in formal Telugu script, explaining "
        "statutory conditions clearly with bracketed section citations."
    ),
    "mr": (
        "Marathi (मराठी): answer in formal Marathi (Devanagari script), "
        "explaining statutory conditions clearly with bracketed section "
        "citations."
    ),
    "bn": (
        "Bengali (বাংলা): answer in formal Bengali script, explaining "
        "statutory conditions clearly with bracketed section citations."
    ),
    "gu": (
        "Gujarati (ગુજરાતી): answer in formal Gujarati script, explaining "
        "statutory conditions clearly with bracketed section citations."
    ),
}


class QAService:
    """
    Graph-Hybrid RAG Pipeline implementing 3-agent orchestration.
    """

    def __init__(self):
        self.provider = getattr(settings, "LLM_PROVIDER", "ollama").lower()
        self.ollama_url = getattr(
            settings, "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.ollama_model = getattr(
            settings, "OLLAMA_MODEL", "qwen2.5:3b-instruct"
        )
        self.gemini_api_key = (
            getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
        )
        if self.gemini_api_key and genai:
            try:
                genai.configure(api_key=self.gemini_api_key)
            except Exception as e:
                print(f"[QAService] Gemini configure warning: {e}")

    # ═══════════════════════════════════════════════════════
    # PUBLIC API
    # ═══════════════════════════════════════════════════════

    def answer_query(self, req: QueryRequest) -> QueryResponse:
        """
        Main entry point. Orchestrates the 3-agent pipeline:
        1. Query Planner → parse intent, detect language/jurisdiction
        2. Hybrid Search → vector retrieval + graph enrichment
        3. Validity Checker → temporal supersession + cross-refs
        4. Synthesis → LLM generation with hallucination barriers
        """
        # ── Agent 1: Query Planner ──────────────────────────
        plan = self._agent_query_planner(req)
        user_lang = plan["language"]
        jurisdiction = plan["jurisdiction"]

        # ── Hybrid Search: Vector + BM25 ────────────────────
        sources: List[SourceReference] = vector_service.search_corpus(
            query=req.query,
            jurisdiction=jurisdiction,
            top_k=5,
        )

        # ── Early refusal if corpus coverage insufficient ───
        if not sources or (
            len(sources) == 1 and sources[0].relevance_score < 0.35
        ):
            return self._build_refusal_response(
                user_lang, jurisdiction, sources, req.product_category
            )

        confidence = (
            "HIGH" if sources[0].relevance_score >= 0.65 else "MEDIUM"
        )

        # ── Agent 2: Validity Checker ───────────────────────
        validity_context = self._agent_validity_checker(sources)

        # ── Agent 3: Synthesis & Citation ───────────────────
        answer_text = self._agent_synthesis(
            req.query, sources, validity_context,
            user_lang, jurisdiction
        )

        # ── Citation verification ───────────────────────────
        formatted_answer, verified_sources = (
            citation_service.format_citations_in_text(answer_text, sources)
        )

        disclaimer = None
        if confidence == "MEDIUM":
            disclaimer = (
                "⚠️ Moderate Confidence: The answer is grounded in corpus "
                "provisions but may not cover all applicable statutes. "
                "Please verify with a qualified IP attorney."
            )

        return QueryResponse(
            answer=formatted_answer,
            language=user_lang,
            jurisdiction=jurisdiction,
            confidence=confidence,
            sources=verified_sources,
            product_category=req.product_category,
            disclaimer=disclaimer,
        )

    # ═══════════════════════════════════════════════════════
    # AGENT 1: QUERY PLANNER
    # ═══════════════════════════════════════════════════════

    def _agent_query_planner(self, req: QueryRequest) -> Dict[str, Any]:
        """
        Decomposes the user query into search parameters:
        - Detected language
        - Jurisdiction filter
        - Key statutory terms / section references
        """
        user_lang = req.language or language_service.detect_language(req.query)
        jurisdiction = req.jurisdiction or "india"

        return {
            "language": user_lang,
            "jurisdiction": jurisdiction,
            "original_query": req.query,
            "product_category": req.product_category,
        }

    # ═══════════════════════════════════════════════════════
    # AGENT 2: VALIDITY CHECKER
    # ═══════════════════════════════════════════════════════

    def _agent_validity_checker(
        self, sources: List[SourceReference]
    ) -> Dict[str, Any]:
        """
        Traverses the knowledge graph to:
        1. Check temporal validity of each retrieved source
           (AMENDED_BY, REPEALED_BY edges)
        2. Discover cross-referenced provisions (1-2 hops)
        3. Build enriched context payload for synthesis

        Returns a dict with validity annotations and cross-reference context.
        """
        seed_chunk_ids = [s.doc_id for s in sources]

        # 1. Get graph enrichment (cross-refs + validity)
        graph_context = graph_service.get_related_provisions(
            chunk_ids=seed_chunk_ids,
            jurisdiction=sources[0].jurisdiction if sources else "india",
        )

        # 2. Build validity summary for the prompt
        validity_notes = []
        for v in graph_context.get("temporal_validity", []):
            status = v.get("status", "CURRENT")
            title = v.get("title", "")
            if status == "AMENDED":
                amendments = v.get("amended_by", [])
                for amend in amendments:
                    validity_notes.append(
                        f"⚠️ NOTE: {title} has been AMENDED by "
                        f"{amend['amending_title']}: {amend['label']}"
                    )
            elif status == "REPEALED":
                for repeal in v.get("repealed_by", []):
                    validity_notes.append(
                        f"🚫 WARNING: {title} has been REPEALED by "
                        f"{repeal['repealing_title']}: {repeal['label']}"
                    )

        # 3. Build cross-reference context blocks
        cross_ref_blocks = []
        for ref in graph_context.get("cross_references", []):
            cross_ref_blocks.append(
                f"CROSS-REFERENCE: {ref['title']} "
                f"({ref['section_or_article']}, {ref['statute']})\n"
                f"Jurisdiction: {ref['jurisdiction']}\n"
                f"Excerpt: {ref['text_excerpt'][:300]}"
            )

        return {
            "validity_notes": validity_notes,
            "cross_reference_blocks": cross_ref_blocks,
            "graph_stats": {
                "total_nodes_consulted": graph_context.get(
                    "graph_node_count", 0
                ),
                "related_provisions_found": graph_context.get(
                    "related_node_count", 0
                ),
            },
        }

    # ═══════════════════════════════════════════════════════
    # AGENT 3: SYNTHESIS & CITATION
    # ═══════════════════════════════════════════════════════

    def _agent_synthesis(
        self,
        query: str,
        sources: List[SourceReference],
        validity_context: Dict[str, Any],
        user_lang: str,
        jurisdiction: str,
    ) -> str:
        """
        Constructs the final prompt and calls the LLM with:
        - Primary retrieved sources
        - Validity annotations from graph traversal
        - Cross-referenced provisions
        - Strict hallucination barrier instructions
        """
        # 1. Build primary source context
        context_blocks = []
        for idx, s in enumerate(sources, 1):
            context_blocks.append(
                f"SOURCE [{idx}]:\n"
                f"- Statute / Document: {s.doc_title}\n"
                f"- Section / Article: {s.section_id} ({s.section_title})\n"
                f"- Jurisdiction: {s.jurisdiction}\n"
                f"- Citation Tag: [{s.citation_key}]\n"
                f"- Statutory Text Excerpt:\n{s.excerpt}"
            )
        context_str = "\n\n".join(context_blocks)

        # 2. Build validity annotation block
        validity_str = ""
        validity_notes = validity_context.get("validity_notes", [])
        if validity_notes:
            validity_str = (
                "\n\n=== TEMPORAL VALIDITY ANNOTATIONS (from Knowledge Graph) ===\n"
                + "\n".join(validity_notes)
            )

        # 3. Build cross-reference block
        cross_ref_str = ""
        cross_refs = validity_context.get("cross_reference_blocks", [])
        if cross_refs:
            cross_ref_str = (
                "\n\n=== CROSS-REFERENCED PROVISIONS (Graph Traversal) ===\n"
                + "\n\n".join(cross_refs[:5])  # Limit to 5 to stay within context
            )

        # 4. Build graph stats
        graph_stats = validity_context.get("graph_stats", {})
        graph_info = (
            f"\n[Graph Engine: {graph_stats.get('total_nodes_consulted', 0)} "
            f"nodes consulted, "
            f"{graph_stats.get('related_provisions_found', 0)} "
            f"related provisions discovered]"
        )

        # 5. Get language instruction
        lang_instruction = LANG_GUIDES.get(user_lang, LANG_GUIDES["en"])

        # 6. Assemble final prompt
        citation_key_example = sources[0].citation_key if sources else "N/A"
        prompt = (
            f"You are IP-SAKTI Sahayak (इंटेलेक्चुअल प्रॉपर्टी और आयुष "
            f"नियामक सहायक), the authoritative AI legal assistant for the "
            f"Ministry of Ayush, Government of India.\n"
            f"You assist Ayurvedic researchers, vaidyas, MSMEs, startups, "
            f"and regulators.\n\n"
            f"=== STRICT HALLUCINATION BARRIER (ZERO FABRICATIONS) ===\n"
            f"1. You are strictly prohibited from inventing, extrapolating, "
            f"or synthesizing legal sections, article numbers, or statutory "
            f"rules not found in the authentic sources below.\n"
            f"2. Every legal assertion MUST be immediately followed by its "
            f"bracketed citation, e.g. [Source: {citation_key_example}].\n"
            f"3. Current Jurisdiction filter: '{jurisdiction.upper()}'. "
            f"Only cite provisions matching this jurisdiction.\n"
            f"4. If a question cannot be answered from the provided sources, "
            f"state clearly that the indexed corpus does not contain "
            f"sufficient verified provisions on that point.\n"
            f"5. If a provision has been AMENDED or REPEALED (see Temporal "
            f"Validity section), you MUST note the amendment/repeal status "
            f"and cite the amending provision.\n"
            f"6. Output Language Requirement: {lang_instruction}\n\n"
            f"=== AUTHENTIC RETRIEVED STATUTORY SOURCES ===\n"
            f"{context_str}"
            f"{validity_str}"
            f"{cross_ref_str}"
            f"{graph_info}\n\n"
            f"=== USER QUERY ===\n"
            f"{query}\n\n"
            f"=== PRECISE CITATION-GROUNDED ANALYSIS ===\n"
        )

        # 7. Call LLM
        generated_answer = self._call_llm(prompt)

        if generated_answer:
            return generated_answer

        # 8. Deterministic fallback (no LLM available)
        return self._generate_deterministic_summary(
            query, sources, validity_context, user_lang, jurisdiction
        )

    # ═══════════════════════════════════════════════════════
    # LLM PROVIDER LAYER
    # ═══════════════════════════════════════════════════════

    def _call_llm(self, prompt: str) -> Optional[str]:
        """Routes to configured LLM provider with automatic fallback."""
        if self.provider == "ollama":
            result = self._call_ollama(prompt)
            if not result and self.gemini_api_key:
                print(
                    "[QAService] Local Ollama unavailable, "
                    "falling back to Gemini..."
                )
                result = self._call_gemini(prompt)
            return result
        elif self.provider == "gemini":
            result = self._call_gemini(prompt)
            if not result:
                print(
                    "[QAService] Gemini unavailable, "
                    "falling back to local Ollama..."
                )
                result = self._call_ollama(prompt)
            return result
        return None

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Calls local Ollama instance with Qwen 2.5:3b-instruct."""
        try:
            url = f"{self.ollama_url.rstrip('/')}/api/generate"
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.85,
                    "num_ctx": 4096,
                },
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                response_text = result.get("response", "").strip()
                if response_text:
                    return response_text
        except Exception as e:
            print(f"[QAService] Ollama call error ({self.ollama_model}): {e}")
        return None

    def _call_gemini(self, prompt: str) -> Optional[str]:
        """Calls Google Gemini if configured."""
        if not self.gemini_api_key or not genai:
            return None
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            resp = model.generate_content(prompt)
            if resp and resp.text:
                return resp.text.strip()
        except Exception as e:
            print(f"[QAService] Gemini generation error: {e}")
        return None

    # ═══════════════════════════════════════════════════════
    # DETERMINISTIC FALLBACK (NO LLM)
    # ═══════════════════════════════════════════════════════

    def _generate_deterministic_summary(
        self,
        query: str,
        sources: List[SourceReference],
        validity_context: Dict[str, Any],
        lang: str,
        jurisdiction: str,
    ) -> str:
        """
        Grounded factual summary constructed directly from authentic
        corpus chunks and graph validity data. Used when no LLM is
        available.
        """
        primary = sources[0]

        # Build validity notes
        validity_section = ""
        validity_notes = validity_context.get("validity_notes", [])
        if validity_notes:
            validity_section = "\n\n**Temporal Status:**\n" + "\n".join(
                f"- {note}" for note in validity_notes
            )

        # Build cross-reference notes
        cross_ref_section = ""
        cross_refs = validity_context.get("cross_reference_blocks", [])
        if cross_refs:
            cross_ref_section = (
                "\n\n**Related Provisions:**\n"
                + "\n".join(f"- {ref[:200]}" for ref in cross_refs[:3])
            )

        if lang == "hi":
            return (
                f"### प्रामाणिक विधिक निष्कर्ष\n\n"
                f"आपके प्रश्न के संदर्भ में **{primary.doc_title}** के "
                f"प्रावधान (विशेष रूप से **{primary.section_title}**) "
                f"लागू होते हैं:\n\n"
                f"> \"{primary.excerpt[:350]}...\"\n\n"
                f"**मुख्य विधिक बिंदु:**\n"
                f"- [Source: {primary.citation_key}]\n"
                f"- यह प्रावधान '{jurisdiction.upper()}' क्षेत्राधिकार के "
                f"अंतर्गत लागू है।"
                f"{validity_section}{cross_ref_section}"
            )
        elif lang == "gu":
            return (
                f"### પ્રમાણિત કાનૂની તારણ\n\n"
                f"તમારા પ્રશ્નના સંદર્ભમાં **{primary.doc_title}** ની કલમ "
                f"**{primary.section_title}** લાગુ પડે છે:\n\n"
                f"> \"{primary.excerpt[:350]}...\"\n\n"
                f"**મુખ્ય નિયમનકારી મુદ્દા:**\n"
                f"- [Source: {primary.citation_key}]"
                f"{validity_section}{cross_ref_section}"
            )
        else:
            return (
                f"### Statutory Analysis & Findings\n\n"
                f"Under **{primary.doc_title}**, specifically "
                f"**{primary.section_title}**:\n\n"
                f"> \"{primary.excerpt[:350]}...\"\n\n"
                f"**Key Regulatory Takeaways:**\n"
                f"- Primary Statutory Citation: "
                f"[Source: {primary.citation_key}].\n"
                f"- Jurisdiction: {jurisdiction.upper()}."
                f"{validity_section}{cross_ref_section}"
            )

    # ═══════════════════════════════════════════════════════
    # REFUSAL RESPONSE
    # ═══════════════════════════════════════════════════════

    def _build_refusal_response(
        self,
        user_lang: str,
        jurisdiction: str,
        sources: List[SourceReference],
        product_category: Optional[str],
    ) -> QueryResponse:
        """Builds a safe refusal response when corpus coverage is insufficient."""
        return QueryResponse(
            answer=REFUSAL_MESSAGES.get(user_lang, REFUSAL_MESSAGES["en"]),
            language=user_lang,
            jurisdiction=jurisdiction,
            confidence="LOW",
            sources=sources,
            product_category=product_category,
            disclaimer=(
                "⚠️ Low Confidence: Limited source material available in the "
                "corpus for this specific query. Please consult a qualified "
                "IP attorney."
            ),
        )


qa_service = QAService()
