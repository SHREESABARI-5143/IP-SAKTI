import re
from typing import Dict, Tuple, Optional

class LanguageService:
    """
    Handles Hindi/English detection and domain glossary term translation.
    """
    GLOSSARY: Dict[str, Dict[str, str]] = {
        "patent": {"hi": "पेटेंट (एकस्वत्व)", "en": "Patent"},
        "trademark": {"hi": "ट्रेडमार्क (व्यापार चिह्न)", "en": "Trademark"},
        "geographical indication": {"hi": "भौगोलिक संकेत (GI)", "en": "Geographical Indication"},
        "traditional knowledge": {"hi": "पारंपरिक ज्ञान (TK)", "en": "Traditional Knowledge"},
        "prior art": {"hi": "पूर्व कला / पूर्ववर्ती ज्ञान", "en": "Prior Art"},
        "access and benefit sharing": {"hi": "पहुँच एवं लाभ साझाकरण (ABS)", "en": "Access and Benefit Sharing"},
        "classical drug": {"hi": "शास्त्रोक्त / शास्त्रीय औषधि", "en": "Classical / Generic Drug"},
        "proprietary medicine": {"hi": "स्वामित्व औषधि (P&P)", "en": "Patent & Proprietary Medicine"},
        "phytopharmaceutical": {"hi": "फाइटोफार्मास्युटिकल औषधि", "en": "Phytopharmaceutical"},
        "ayush aahar": {"hi": "आयुष आहार (पोषक उत्पाद)", "en": "AYUSH Aahar / Nutraceutical"},
        "biodiversity": {"hi": "जैव विविधता", "en": "Biodiversity"},
    }

    def detect_language(self, text: str) -> str:
        # Check for Devanagari Unicode range (\u0900-\u097F)
        devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
        if devanagari_chars > 3:
            return "hi"
        return "en"

    def get_glossary_term(self, term: str, target_lang: str = "hi") -> Optional[str]:
        term_lower = term.lower().strip()
        if term_lower in self.GLOSSARY:
            return self.GLOSSARY[term_lower].get(target_lang)
        return None

language_service = LanguageService()
