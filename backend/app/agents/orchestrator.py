import time
import re
from typing import Dict, Any, Optional, List
from backend.app.core.security import sanitize_and_check_injection
from backend.app.multilingual.normalizer import normalizer
from backend.app.knowledge_graph.engine import knowledge_graph
from backend.app.rag.retriever import retriever
from backend.app.rag.llm_provider import llm_provider
from backend.app.rag.citation_verifier import citation_verifier
from backend.app.rag.confidence import confidence_calculator
from backend.app.schemas.chat import ChatResponse, ConfidenceBreakdown, CitationOut

class AgentOrchestrator:
    """
    Coordinates end-to-end multi-agent legal RAG pipeline:
    1. Input sanitization & prompt-injection defense
    2. Intent classification (Greeting, Meta, Out-of-Scope, or Legal Query)
    3. Language detection (EN/HI/TA) & concept normalization
    4. Domain & Jurisdiction routing
    5. Knowledge graph multi-hop context expansion
    6. Hybrid retrieval (BM25 + Semantic + Metadata filter + Authority weight)
    7. Grounded answer generation
    8. Post-generation citation verification & mapping
    9. Algorithmic confidence computation & abstention checks
    """

    def is_greeting_or_meta(self, text: str) -> bool:
        """Detects if query is a greeting, introduction, or general help query."""
        clean = text.strip().lower()
        # Direct Unicode script greetings
        if clean in ["नमस्ते", "प्रणाम", "नमस्कार", "வணக்கம்", "நன்றி", "धन्यवाद"]:
            return True
            
        clean_ascii = re.sub(r'[^\w\s]', '', clean)
        greeting_patterns = [
            r'^(hi|hello|hey|hola|namaste|pranam|vanakkam|namaskaram|namaskar)(\s.*)?$',
            r'^(how are you|how r u|how are u|how do you do)(\s.*)?$',
            r'^(good morning|good afternoon|good evening|good day)(\s.*)?$',
            r'^(who are you|what is your name|what can you do|what are you)(\s.*)?$',
            r'^(help|start|menu|options|guide|introduction)(\s.*)?$',
            r'^(thanks|thank you|dhanyawad|nandri)(\s.*)?$'
        ]
        return any(re.match(p, clean_ascii) for p in greeting_patterns) or len(clean_ascii.split()) <= 2 and clean_ascii in [
            "hi", "hello", "hey", "namaste", "vanakkam", "help", "who are you"
        ]

    async def process_chat_query(
        self,
        query: str,
        jurisdiction: str = "India",
        selected_country: Optional[str] = None,
        language_preference: str = "en",
        product_context: Optional[Dict[str, Any]] = None,
        conversation_id: str = "conv_default",
        message_id: str = "msg_default"
    ) -> ChatResponse:
        start_time = time.time()

        # 1. Safety & Injection Check
        cleaned_query, is_suspicious = sanitize_and_check_injection(query)
        if is_suspicious:
            return ChatResponse(
                conversation_id=conversation_id,
                message_id=message_id,
                short_answer="Query flagged for safety policy violation.",
                full_answer="### Policy Notice\nYour query contains prohibited system override or instruction injection patterns. Please submit a valid legal or regulatory question regarding Ayurvedic IP or compliance.",
                jurisdiction=jurisdiction,
                detected_domain="Security/Safety",
                confidence=ConfidenceBreakdown(
                    level="Abstain",
                    score=0.1,
                    source_authority_score=0.0,
                    retrieval_relevance_score=0.0,
                    jurisdiction_match_score=0.0,
                    source_freshness_score=0.0,
                    citation_grounding_score=0.0,
                    explanation="Abstained due to safety filter trigger."
                ),
                citations=[],
                is_abstained=True,
                abstention_reason="Prompt injection pattern detected."
            )

        # 2. Language Detection
        detected_lang = normalizer.detect_language(cleaned_query)
        active_lang = language_preference if language_preference in ["hi", "ta"] else detected_lang

        # 3. Handle Greetings & Meta Questions
        if self.is_greeting_or_meta(cleaned_query):
            if active_lang == "hi":
                short_greet = "नमस्ते! मैं IP-SAKTI सहायक हूँ — आपका आयुर्वेदिक बौद्धिक संपदा और नियामक सलाहकार।"
                full_greet = """### स्वागत है! मैं IP-SAKTI सहायक हूँ 🙏

मैं एक **स्रोतों पर आधारित कृत्रिम बुद्धिमत्ता (AI) सहायक** हूँ, जो आयुर्वेद नवप्रवर्तकों, शोधकर्ताओं और स्टार्टअप्स को बौद्धिक संपदा (IP) और विनियामक अनुपालन में मार्गदर्शन प्रदान करता हूँ।

#### मैं आपकी किन विषयों में सहायता कर सकता हूँ:
1. **पेटेंट पात्रता और धारा 3(p) / 3(d):** क्या आपकी आयुर्वेदिक फॉर्मूलेशन पेटेंट योग्य है या पारंपरिक ज्ञान (TKDL) के तहत अपवर्जित है।
2. **जैविक विविधता अधिनियम (BDA 2023) और ABS:** राज्य जैव विविधता बोर्ड (SBB) और राष्ट्रीय जैव विविधता प्राधिकरण (NBA) की पूर्व अनुमति की आवश्यकता।
3. **उत्पाद वर्गीकरण:** शास्त्रीय औषधि (Rule 158B), पेटेंट एवं प्रोप्रायटरी औषधि, या FSSAI आयुर्वेद आहार (2022)।
4. **अंतर्राष्ट्रीय निर्यात अनुपालन:** US FDA DSHEA (21 CFR 111), EU THMPD और WIPO GRATK संधि (2024)।

---
💡 **शुरुआत करने के लिए नीचे दिए गए किसी विषय पर प्रश्न पूछें या अपना फॉर्मूलेशन साझा करें!**"""
            elif active_lang == "ta":
                short_greet = "வணக்கம்! நான் IP-SAKTI சகாயக் — உங்கள் ஆயுர்வேத அறிவுசார் சொத்து மற்றும் ஒழுங்குமுறை AI ஆலோசகர்."
                full_greet = """### வரவேற்கிறோம்! நான் IP-SAKTI சகாயக் 🙏

ஆயுர்வேத கண்டுபிடிப்பாளர்கள், ஆராய்ச்சியாளர்கள் மற்றும் ஸ்டார்ட்அப்களுக்கு அறிவுசார் சொத்துரிமை (IP) மற்றும் சட்ட வழிகாட்டுதல்களை வழங்க நான் உதவுகிறேன்.

#### எனது முக்கிய சேவைகள்:
1. **காப்புரிமை மற்றும் பிரிவு 3(p) / 3(d) பகுப்பாய்வு**
2. **உயிரியல் பன்முகத்தன்மை சட்டம் 2023 மற்றும் ABS ஒப்புதல் வழிகாட்டுதல்**
3. **ஆயுர்வேத தயாரிப்பு வகைப்பாடு (ASU மருந்துகள் vs ஆயுர்வேத ஆகார் 2022)**
4. **சர்வதேச ஏற்றுமதி தேவைகள் (US FDA DSHEA & EU THMPD)**

---
💡 **தொடங்க உங்கள் வினவலை உள்ளிடவும்!**"""
            else:
                short_greet = "Hello! I am IP-SAKTI Sahayak — your verified Ayurvedic IP & Regulatory AI Assistant."
                full_greet = """### Welcome to IP-SAKTI Sahayak 👋

I am a **citation-grounded legal and regulatory AI assistant with evidence validation and safe abstention** engineered specifically for Ayurveda researchers, AYUSH startups, MSMEs, practitioners, and bio-innovators.

#### How I Can Assist You:
1. **Patent Eligibility & Prior Art (Section 3(p) / 3(d)):** Evaluate whether your formulation overcomes Traditional Knowledge exclusions through non-obvious synergistic efficacy data.
2. **Access & Benefit Sharing (BDA 2023 & NBA):** Identify whether your raw herbs or commercialization require State Biodiversity Board (SBB) intimation or NBA Form III approval.
3. **Regulatory Classification:** Accurately classify your product across Classical ASU Medicine (Drugs Act Rule 158B), Patent & Proprietary, or FSSAI Ayurveda Aahar (2022).
4. **International Export Compliance:** Review US FDA Dietary Supplement (DSHEA / 21 CFR 111), EU Herbal Directives (2004/24/EC), and WIPO GRATK Treaty (2024) mandates.

---
💡 **To get started, try asking a question like:**
- *"Can I patent a formulation containing Turmeric and Ashwagandha?"*
- *"Do Indian AYUSH manufacturers need NBA approval under BDA 2023?"*
- *"How do FSSAI Ayurveda Aahar regulations differ from ASU Drug licenses?"*"""

            return ChatResponse(
                conversation_id=conversation_id,
                message_id=message_id,
                short_answer=short_greet,
                full_answer=full_greet,
                jurisdiction=jurisdiction,
                detected_domain="Assistant Introduction",
                confidence=ConfidenceBreakdown(
                    level="High",
                    score=1.0,
                    source_authority_score=1.0,
                    retrieval_relevance_score=1.0,
                    jurisdiction_match_score=1.0,
                    source_freshness_score=1.0,
                    citation_grounding_score=1.0,
                    explanation="Direct assistant greeting and orientation."
                ),
                citations=[],
                recommended_next_steps=[
                    "Enter your formulation details or regulatory question.",
                    "Toggle between Indian Statutes and International Export scopes in the top header.",
                    "Use the Formulation Classifier or ABS Helper in the navigation bar for structured assessment."
                ],
                followup_suggestions=[
                    "Can I patent a formulation containing Turmeric and Ashwagandha?",
                    "Do Indian AYUSH manufacturers need NBA approval under BDA 2023?",
                    "How do FSSAI Ayurveda Aahar regulations differ from ASU Drug licenses?",
                    "What are US FDA DSHEA export labeling requirements for Ayurvedic supplements?"
                ],
                is_abstained=False,
                abstention_reason=None
            )

        # 4. Terminology Normalization for Legal Queries
        rewritten_query, normalized_concepts = normalizer.normalize_query_to_english_concepts(cleaned_query, active_lang)

        # 5. Domain Routing
        query_lower = rewritten_query.lower()
        if any(w in query_lower for w in ["patent", "invent", "novel", "3(p)", "3(d)", "monopoly"]):
            detected_domain = "Patent"
        elif any(w in query_lower for w in ["abs", "biodiversity", "nba", "sbb", "bmc", "benefit sharing"]):
            detected_domain = "ABS"
        elif any(w in query_lower for w in ["rule 158b", "license", "classical", "proprietary", "aahar", "fssai", "cosmetic", "claim"]):
            detected_domain = "Regulatory"
        elif any(w in query_lower for w in ["export", "us fda", "dshea", "eu", "prop 65", "thmpd"]):
            detected_domain = "Export"
        elif any(w in query_lower for w in ["trademark", "brand", "logo", "gi", "geographical indication"]):
            detected_domain = "Trademark / GI"
        else:
            detected_domain = "General IP & Regulatory"

        # 6. Knowledge Graph Context Expansion
        graph_context = knowledge_graph.get_multi_hop_subgraph([cleaned_query, detected_domain])

        # 7. Hybrid Retrieval
        retrieved_chunks = retriever.search(
            query=rewritten_query,
            jurisdiction=jurisdiction,
            domain_filter=detected_domain,
            selected_country=selected_country,
            top_k=4
        )

        # Check retrieval relevance threshold (< 0.28 means query has virtually no match in legal corpus)
        top_score = retrieved_chunks[0].get("retrieval_score", 0.0) if retrieved_chunks else 0.0
        if not retrieved_chunks or top_score < 0.28:
            return ChatResponse(
                conversation_id=conversation_id,
                message_id=message_id,
                short_answer="I could not verify this inquiry against the verified statutory legal registry.",
                full_answer="### Safe Abstention Notice\n\nI cannot provide legal or regulatory guidance on this matter because the inquiry does not correspond to indexed Ayurvedic intellectual property statutes (Patents Act 1970, BD Act 2023, Drugs & Cosmetics Act, FSSAI Ayurveda Aahar, or WIPO treaties) in the verified knowledge registry.\n\n**Recommended Action:**\n- Please submit a valid inquiry regarding Ayurvedic patent eligibility, traditional knowledge prior art, ABS compliance, regulatory licensing, or export compliance.",
                jurisdiction=jurisdiction,
                detected_domain="Out of Domain",
                confidence=ConfidenceBreakdown(
                    level="Abstain",
                    score=0.10,
                    source_authority_score=0.0,
                    retrieval_relevance_score=0.0,
                    jurisdiction_match_score=0.0,
                    source_freshness_score=0.0,
                    citation_grounding_score=0.0,
                    explanation="Abstained: Query is out-of-scope or lacks verified statutory evidence."
                ),
                citations=[],
                is_abstained=True,
                abstention_reason="Insufficient relevance in authoritative statutory knowledge base."
            )

        # 8. Grounded Answer Synthesis
        raw_answer = await llm_provider.generate_grounded_answer(
            query=cleaned_query,
            retrieved_sources=retrieved_chunks,
            jurisdiction=jurisdiction,
            detected_domain=detected_domain,
            language=active_lang,
            product_context=product_context
        )

        if raw_answer.get("is_abstained", False):
            return ChatResponse(
                conversation_id=conversation_id,
                message_id=message_id,
                short_answer=raw_answer["short_answer"],
                full_answer=raw_answer["full_answer"],
                jurisdiction=jurisdiction,
                detected_domain=detected_domain,
                confidence=ConfidenceBreakdown(
                    level="Abstain",
                    score=0.15,
                    source_authority_score=0.0,
                    retrieval_relevance_score=0.0,
                    jurisdiction_match_score=0.0,
                    source_freshness_score=0.0,
                    citation_grounding_score=0.0,
                    explanation="Abstained: Insufficient verified statutory evidence."
                ),
                citations=[],
                is_abstained=True,
                abstention_reason=raw_answer.get("abstention_reason")
            )

        # 9. Post-generation Citation Verification & Claim Grounding
        sanitized_text, verified_citations, unsupported_count, grounding_rate = citation_verifier.verify_and_format_citations(
            raw_text=raw_answer["full_answer"],
            retrieved_sources=retrieved_chunks
        )

        # 10. Algorithmic Confidence Computation
        confidence_meta = confidence_calculator.calculate(
            retrieved_sources=retrieved_chunks,
            jurisdiction=jurisdiction,
            unsupported_claim_count=unsupported_count
        )

        # Follow-up Suggestions
        followups = [
            "Does my product qualify for the Section 40 Normally Traded Commodities list?",
            "What is the difference between Classical Ayurvedic Medicine and Rule 158B P&P medicine?",
            "How do I file Form III with the National Biodiversity Authority before patent grant?",
            "What are the US FDA DSHEA labeling guidelines for herbal dietary supplements?"
        ]

        # Recommended Next Steps
        next_steps = [
            "Verify all botanical ingredients against the First Schedule Ayurvedic Samhitas and NTC list.",
            "If seeking a patent, prepare comparative synergistic efficacy trial data to overcome Section 3(p) and 3(d).",
            "Submit prior intimation Form A to your State Biodiversity Board (SBB).",
            "Register distinct coined brand names under Trademark Class 5 or Class 30."
        ]

        return ChatResponse(
            conversation_id=conversation_id,
            message_id=message_id,
            short_answer=raw_answer["short_answer"],
            full_answer=sanitized_text,
            jurisdiction=jurisdiction,
            detected_domain=detected_domain,
            confidence=confidence_meta,
            citations=verified_citations,
            recommended_next_steps=next_steps,
            followup_suggestions=followups,
            is_abstained=False,
            abstention_reason=None
        )

orchestrator = AgentOrchestrator()
