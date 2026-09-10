import re
from typing import Tuple, List, Dict, Set
from backend.app.multilingual.dictionary import LEGAL_AYUSH_DICTIONARY

class MultilingualNormalizer:
    """
    Production-grade Multilingual & Code-Mixed (Hinglish/Tanglish) Query Normalizer.
    1. Detects native scripts (Devanagari, Tamil) or romanized transliteration (Hinglish, Tanglish).
    2. Maps regional legal terms and colloquial stems into canonical English concepts.
    3. Retains original user language for target-language response synthesis while enabling language-neutral retrieval.
    """

    # Transliteration markers
    TANGLISH_MARKERS = [
        r'\b(en|indha|andha|namakku|product-ku|formulation-ku|patent-ku|abs-ku)\b',
        r'\b(kidaikkuma|venuma|irukka|mudiyuma|pannalama|seiyalama|thevaiya)\b',
        r'\b(aaguma|solla|mudiyum|enna|epdi|theriyuma|ippo)\b'
    ]

    HINGLISH_MARKERS = [
        r'\b(kya|kaise|chahiye|hoga|hota|sakte|karna|h|hain|hai|meri|is)\b',
        r'\b(formulation|product|ka|ke|ki|mein|se|ko|liye|baare|karein)\b',
        r'\b(milega|hogi|kar|rahe|chahiye|batao|kripya)\b'
    ]

    HERB_MAP = {
        # Devanagari
        "अश्वगंधा": "Ashwagandha Withania somnifera",
        "हल्दी": "Turmeric Curcuma longa",
        "नीम": "Neem Azadirachta indica",
        "तुलसी": "Tulsi Ocimum sanctum",
        "त्रिफला": "Triphala",
        "शल्लकी": "Shallaki Boswellia serrata",
        "गुग्गुलु": "Guggulu Commiphora mukul",
        "च्यवनप्राश": "Chyawanprash classical formulation",
        "गिलोय": "Guduchi Tinospora cordifolia",
        # Tamil
        "அஸ்வகந்தா": "Ashwagandha Withania somnifera",
        "மஞ்சள்": "Turmeric Curcuma longa",
        "வேம்பு": "Neem Azadirachta indica",
        "துளசி": "Tulsi Ocimum sanctum",
        "திரிபலா": "Triphala",
        "குக்குலு": "Guggulu Commiphora mukul",
        "சயவன்பிராஷ்": "Chyawanprash classical formulation",
        "சீந்தில்": "Guduchi Tinospora cordifolia",
        # Romanized / Transliterated
        "ashwagandha": "Ashwagandha Withania somnifera",
        "aswagandha": "Ashwagandha Withania somnifera",
        "haldi": "Turmeric Curcuma longa",
        "manjal": "Turmeric Curcuma longa",
        "turmeric": "Turmeric Curcuma longa",
        "neem": "Neem Azadirachta indica",
        "veppam": "Neem Azadirachta indica",
        "tulsi": "Tulsi Ocimum sanctum",
        "triphala": "Triphala",
        "chyawanprash": "Chyawanprash classical formulation",
        "chyavanaprasha": "Chyawanprash classical formulation",
        "guduchi": "Guduchi Tinospora cordifolia",
        "shallaki": "Shallaki Boswellia serrata",
        "guggulu": "Guggulu Commiphora mukul"
    }

    COLLOQUIAL_INTENT_MAP = {
        # Tanglish patterns
        r'patent.*(kidaikkuma|mudiyuma|pannalama)': "Patent eligibility Section 3(p) Traditional Knowledge",
        r'abs.*(venuma|thevaiya|irukka)': "Access and Benefit Sharing Biological Diversity Act 2023 NBA approval",
        r'export.*(us fda|fda|rules|enna)': "Export compliance US FDA DSHEA 21 CFR 111",
        r'license.*(epdi|vaanga|mudiyum)': "Drugs and Cosmetics Act Chapter IV-A Rule 158B Manufacturing License",
        # Hinglish patterns
        r'patent.*(ho sakta hai|milega|kar sakte)': "Patent eligibility Section 3(p) Traditional Knowledge",
        r'nba.*(approval|permission).*(chahiye|hogi)': "Access and Benefit Sharing Biological Diversity Act 2023 NBA approval",
        r'license.*(kaise milega|lena hoga)': "Drugs and Cosmetics Act Chapter IV-A Rule 158B Manufacturing License",
        r'export.*(kaise karein|guidelines kya hai)': "Export compliance US FDA DSHEA 21 CFR 111"
    }

    def detect_language(self, text: str) -> str:
        """
        Detects if the text contains Devanagari (Hindi), Tamil script, Hinglish, Tanglish, or standard English.
        """
        if not text:
            return "en"

        # 1. Native Devanagari Unicode
        if re.search(r'[\u0900-\u097F]', text):
            return "hi"

        # 2. Native Tamil Unicode
        if re.search(r'[\u0B80-\u0BFF]', text):
            return "ta"

        text_lower = text.lower()

        # 3. Tanglish check
        tanglish_hits = sum(1 for p in self.TANGLISH_MARKERS if re.search(p, text_lower))
        if tanglish_hits >= 1:
            return "ta"  # Process as Tamil-intent query

        # 4. Hinglish check
        hinglish_hits = sum(1 for p in self.HINGLISH_MARKERS if re.search(p, text_lower))
        if hinglish_hits >= 2:
            return "hi"  # Process as Hindi-intent query

        return "en"

    def normalize_query_to_english_concepts(self, query: str, detected_lang: str) -> Tuple[str, List[str]]:
        """
        Extracts legal concepts and herbs, supplements query with canonical keywords for hybrid retrieval.
        """
        extracted_concepts: List[str] = []
        supplemental_keywords: List[str] = []
        query_lower = query.lower()

        # 1. Check Colloquial Code-Mixed Intent Patterns
        for pattern, canonical_phrase in self.COLLOQUIAL_INTENT_MAP.items():
            if re.search(pattern, query_lower):
                supplemental_keywords.append(canonical_phrase)
                extracted_concepts.append(canonical_phrase)

        # 2. Check Dictionary Concepts
        for concept_key, data in LEGAL_AYUSH_DICTIONARY.items():
            found = False
            # Check Hindi synonyms
            if detected_lang == "hi":
                for syn in data.get("synonyms_hi", []):
                    if syn in query:
                        found = True
                        break
            # Check Tamil synonyms
            elif detected_lang == "ta":
                for syn in data.get("synonyms_ta", []):
                    if syn in query:
                        found = True
                        break

            # Check English/Romanized concept
            if concept_key.replace("_", " ") in query_lower:
                found = True

            if found:
                extracted_concepts.append(data["concept_en"])
                supplemental_keywords.append(data["concept_en"])

        # 3. Check Herbs & Botanical Entities
        for herb_term, canonical_botanical in self.HERB_MAP.items():
            if herb_term in query_lower or herb_term in query:
                supplemental_keywords.append(canonical_botanical)
                extracted_concepts.append(canonical_botanical)

        # 4. Canonical Provision & Keyword Mapping (Multilingual)
        if any(w in query_lower or w in query for w in ["patent", "turmeric", "ashwagandha", "herbal", "formulation", "traditional", "3(p)", "3p", "पेटेंट", "காப்புரிமை", "हल्दी", "அஸ்வகந்தா", "மஞ்சள்", "अश्वगंधा", "आयुर्वेदिक"]):
            supplemental_keywords.append("traditional knowledge aggregation duplication Section 3(p) Patents Act 1970")
        if any(p in query_lower for p in ["3(p)", "3p", "section 3(p)", "dhara 3(p)", "pirivu 3(p)"]):
            supplemental_keywords.append("Section 3(p) Patents Act 1970 Traditional Knowledge non-patentable")
        if any(p in query_lower for p in ["3(d)", "3d", "section 3(d)", "efficacy", "synergy"]):
            supplemental_keywords.append("Section 3(d) Patents Act 1970 Enhanced Efficacy Synergistic Formulation")
        if any(w in query_lower or w in query for w in ["158b", "rule 158b", "p&p", "proprietary", "लाइसेंस", "உரிமம்"]):
            supplemental_keywords.append("Rule 158B Drugs and Cosmetics Rules 1945 Patent or Proprietary ASU Medicine")
        if any(w in query_lower or w in query for w in ["bda", "bda 2023", "nba", "sbb", "form 3", "form iii", "biological resource", "जैव विविधता", "உயிரியல் பன்முகத்தன்மை"]):
            supplemental_keywords.append("Biological Diversity Act 2023 Section 6 NBA Form III Prior Approval")

        # Build final search query
        rewritten = query
        if supplemental_keywords:
            unique_kws = " ".join(list(dict.fromkeys(supplemental_keywords)))
            rewritten = f"{query} {unique_kws}"

        return rewritten, list(set(extracted_concepts))

normalizer = MultilingualNormalizer()
