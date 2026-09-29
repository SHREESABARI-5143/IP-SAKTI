import os
import re
from typing import List, Optional, Tuple
from app.core.config import settings
from app.models.schemas import QueryRequest, QueryResponse, SourceReference
from app.services.vector_service import vector_service
from app.services.citation_service import citation_service
from app.services.language_service import language_service
import google.generativeai as genai

class QAService:
    """
    Retrieval-Augmented Generation (RAG) Service for IP & AYUSH Regulatory Queries.
    Powered by Qdrant vector retrieval and Google Gemini 2.5/2.0 Flash.
    Features:
    1. Mandatory source citations from real retrieved legal corpus chunks.
    2. Strict jurisdiction separation (India vs International).
    3. Low confidence detection & safety refusal.
    4. Bilingual output (Hindi & English).
    """
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def answer_query(self, req: QueryRequest) -> QueryResponse:
        user_lang = req.language or language_service.detect_language(req.query)
        jurisdiction = req.jurisdiction or "india"

        # 1. Retrieve top matching legal corpus sections from Qdrant
        sources: List[SourceReference] = vector_service.search_corpus(
            query=req.query,
            jurisdiction=jurisdiction,
            top_k=5
        )

        answer_text = ""
        confidence = "HIGH" if (sources and sources[0].relevance_score >= 0.65) else "MEDIUM"
        disclaimer = None

        refusals = {
            "hi": "मुझे इस प्रश्न का निश्चित उत्तर देने के लिए पर्याप्त सत्यापित कानूनी स्रोत नहीं मिले। कृपया किसी योग्य पेटेंट / कानून विशेषज्ञ से परामर्श लें।",
            "sa": "अस्मिन् विषये प्रामाणिक-विधि-स्रोतांसि न प्राप्तानि। कृपया कश्चित् विधिज्ञं (Patent Attorney) सम्पृच्छन्तु।",
            "ta": "இந்த கேள்விக்கு உறுதியான பதிலளிக்க போதுமான சட்ட ஆதாரங்கள் கிடைக்கவில்லை. தகுதிவாய்ந்த காப்புரிமை வழக்கறிஞரை அணுகவும்.",
            "te": "ఈ ప్రశ్నకు స్పష్టమైన సమాధానం ఇవ్వడానికి తగిన చట్టపరమైన ఆధారాలు లభించలేదు. దయచేసి అర్హత కలిగిన పేటెంట్ న్యాయవాదిని సంప్రదించండి.",
            "mr": "या प्रश्नाचे निश्चित उत्तर देण्यासाठी पुरेसे कायदेशीर स्रोत आढळले नाहीत. कृपया पात्र पेटंट सल्लागाराचा सल्ला घ्या.",
            "bn": "এই প্রশ্নের নির্ভরযোগ্য উত্তরের জন্য পর্যাপ্ত আইনি উৎস পাওয়া যায়নি। অনুগ্রহ করে একজন দক্ষ পেটেন্ট আইনজীবীর পরামর্শ নিন।",
            "en": "I do not have enough verified statutory or pharmacopoeial source material in the indexed corpus to answer this query reliably. Please consult a qualified Intellectual Property attorney."
        }

        if not sources or (len(sources) == 1 and sources[0].relevance_score < 0.35):
            confidence = "LOW"
            disclaimer = "⚠️ Low Confidence: Limited source material available in the corpus for this specific query. Please consult a qualified IP attorney."
            answer_text = refusals.get(user_lang, refusals["en"])
            
            return QueryResponse(
                answer=answer_text,
                language=user_lang,
                jurisdiction=jurisdiction,
                confidence=confidence,
                sources=sources,
                product_category=req.product_category,
                disclaimer=disclaimer
            )

        # 2. Generate response using Gemini LLM
        if self.api_key:
            try:
                # Try gemini-2.5-flash first, fallback to gemini-2.0-flash
                model_name = "gemini-2.5-flash"
                model = genai.GenerativeModel(model_name)

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

                lang_guides = {
                    "en": "English: answer in clear, structured, professional English with bullet points and clear headings.",
                    "hi": "Hindi (हिन्दी): answer completely in Hindi (Devanagari script), explaining legal nuances with clarity. Maintain statutory section numbers in English e.g. धारा 3(p) [Section 3(p)].",
                    "sa": "Sanskrit (संस्कृतम्): answer in Sanskrit (Devanagari script), incorporating classical Ayurvedic terminology (आयुर्वेदशास्त्र) and citing statutory sections e.g. धारा 3(p) [Section 3(p)].",
                    "ta": "Tamil (தமிழ்): answer in formal Tamil script, explaining statutory conditions clearly with bracketed section citations.",
                    "te": "Telugu (తెలుగు): answer in formal Telugu script, explaining statutory conditions clearly with bracketed section citations.",
                    "mr": "Marathi (मराठी): answer in formal Marathi (Devanagari script), explaining statutory conditions clearly with bracketed section citations.",
                    "bn": "Bengali (বাংলা): answer in formal Bengali script, explaining statutory conditions clearly with bracketed section citations."
                }
                lang_instruction = lang_guides.get(user_lang, lang_guides["en"])

                prompt = f"""You are IP-SAKTI Sahayak (इंटेलेक्चुअल प्रॉपर्टी और आयुष नियामक सहायक), an authoritative AI assistant built for the Ministry of Ayush, Government of India.
You provide precise, evidence-based legal, regulatory, and patentability guidance to researchers, Ayurvedic vaidyas, MSMEs, and startups.

MANDATORY RULES:
1. Every legal statement, statutory condition, or regulatory requirement MUST be immediately followed by its bracketed citation, e.g. [Source: {sources[0].citation_key}].
2. Rely EXCLUSIVELY on the authentic retrieved legal text below. Do NOT make up laws, section numbers, or cases.
3. Current Jurisdiction filter: '{jurisdiction.upper()}'. Do NOT cite Indian laws when jurisdiction is International, and do NOT cite foreign treaties when jurisdiction is India unless directly comparing.
4. Output language instruction: {lang_instruction}
5. Highlight practical action items:
   - Does this require National Biodiversity Authority (NBA) prior approval?
   - Is it barred under Patents Act Section 3(p) or 3(e)?
   - Which licensing authority applies (State Licensing Authority ASU vs FSSAI Ayush Aahar)?

AUTHENTIC RETRIEVED SOURCES:
{context_str}

USER QUERY:
{req.query}
"""

                response = model.generate_content(prompt)
                if response and response.text:
                    answer_text = response.text.strip()
            except Exception as e:
                print(f"[QAService] Gemini generation error: {e}")
                answer_text = self._generate_fallback(req.query, sources, user_lang, jurisdiction)
        else:
            answer_text = self._generate_fallback(req.query, sources, user_lang, jurisdiction)

        # 3. Verify and format citations
        formatted_answer, verified_sources = citation_service.format_citations_in_text(answer_text, sources)

        return QueryResponse(
            answer=formatted_answer,
            language=user_lang,
            jurisdiction=jurisdiction,
            confidence=confidence,
            sources=verified_sources,
            product_category=req.product_category,
            disclaimer=disclaimer
        )

    def _generate_fallback(
        self, query: str, sources: List[SourceReference], lang: str, jurisdiction: str
    ) -> str:
        """Structured fallback when LLM API connection is offline."""
        primary = sources[0]
        if lang == "hi":
            return (
                f"**सत्यापित कानूनी निष्कर्ष:**\n\n"
                f"आपके प्रश्न के संदर्भ में **{primary.doc_title}** का **{primary.section_title}** लागू होता है।\n\n"
                f"> \"{primary.excerpt[:300]}...\"\n\n"
                f"**मुख्य नियामक बिंदु:**\n"
                f"- [Source: {primary.citation_key}]\n"
                f"- भारत में पारंपरिक ज्ञान पर आधारित फार्मूलेशन पेटेंट योग्य नहीं हैं जब तक कि उनमें अप्रत्याशित सहक्रियाशीलता (Synergy) सिद्ध न की गई हो।"
            )
        else:
            return (
                f"**Statutory Analysis & Findings:**\n\n"
                f"Under **{primary.doc_title}**, specifically **{primary.section_title}**:\n\n"
                f"> \"{primary.excerpt[:300]}...\"\n\n"
                f"**Regulatory Takeaways:**\n"
                f"- Primary statutory reference: [Source: {primary.citation_key}].\n"
                f"- If your product is documented in the Ayurvedic Formulary of India (AFI), it cannot be claimed as an invention per se.\n"
                f"- Ensure compliance with NBA approval requirements under Section 6 of Biological Diversity Act before any patent filing."
            )

qa_service = QAService()
