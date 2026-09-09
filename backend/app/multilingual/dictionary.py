"""
Controlled Legal & AYUSH Multilingual Terminology Dictionary
Maps legal, regulatory, and botanical concepts across English, Hindi, and Tamil.
"""

LEGAL_AYUSH_DICTIONARY = {
    "patent": {
        "hi": "पेटेंट (एकाधिकार)",
        "ta": "காப்புரிமை (Patent)",
        "concept_en": "Patent",
        "synonyms_hi": ["पेटेंट", "एकाधिकार", "आविष्कार संरक्षण"],
        "synonyms_ta": ["காப்புரிமை", "புத்தாக்க உரிமை"]
    },
    "traditional_knowledge": {
        "hi": "पारंपरिक ज्ञान (Traditional Knowledge / TKDL)",
        "ta": "பாரம்பரிய அறிவு (Traditional Knowledge)",
        "concept_en": "Traditional Knowledge",
        "synonyms_hi": ["पारंपरिक ज्ञान", "पारंपरिक चिकित्सा पद्धति", "टीकेडीएल"],
        "synonyms_ta": ["பாரம்பரிய அறிவு", "பாரம்பரிய மருத்துவம்"]
    },
    "biological_resources": {
        "hi": "जैविक संसाधन (Biological Resources)",
        "ta": "உயிரியல் வளங்கள் (Biological Resources)",
        "concept_en": "Biological Resources",
        "synonyms_hi": ["जैविक संसाधन", "जड़ी-बूटी", "औषधीय पौधे"],
        "synonyms_ta": ["உயிரியல் வளங்கள்", "மூலிகைகள்"]
    },
    "access_and_benefit_sharing": {
        "hi": "पहुंच और लाभ साझाकरण (ABS / एनबीए)",
        "ta": "அணுகல் மற்றும் பயன் பகிர்வு (ABS)",
        "concept_en": "Access and Benefit Sharing (ABS)",
        "synonyms_hi": ["पहुंच और लाभ साझाकरण", "एबीएस", "राष्ट्रीय जैव विविधता प्राधिकरण"],
        "synonyms_ta": ["அணுகல் மற்றும் பயன் பகிர்வு", "ஏபிஎஸ்"]
    },
    "geographical_indication": {
        "hi": "भौगोलिक उपदर्शन (GI टैग)",
        "ta": "புவிசார் குறியீடு (GI Tag)",
        "concept_en": "Geographical Indication (GI)",
        "synonyms_hi": ["भौगोलिक उपदर्शन", "जीआई टैग"],
        "synonyms_ta": ["புவிசார் குறியீடு", "ஜிஐ"]
    },
    "trademark": {
        "hi": "व्यापार चिह्न (ट्रेडमार्क)",
        "ta": "வர்த்தக முத்திரை (Trademark)",
        "concept_en": "Trademark",
        "synonyms_hi": ["ट्रेडमार्क", "व्यापार चिह्न", "ब्रांड नाम"],
        "synonyms_ta": ["வர்த்தக முத்திரை", "பிராண்ட் பெயர்"]
    },
    "classical_ayurvedic_medicine": {
        "hi": "शास्त्रीय आयुर्वेदिक औषधि (Classical Medicine / प्रथम अनुसूची)",
        "ta": "சாஸ்திர ஆயுர்வேத மருந்து (Classical Ayurvedic Medicine)",
        "concept_en": "Classical Ayurvedic Medicine",
        "synonyms_hi": ["शास्त्रीय औषधि", "संहिता फॉर्मूलेशन", "चरक संहिता", "सुश्रुत संहिता", "एएफआई"],
        "synonyms_ta": ["சாஸ்திர மருந்து", "பாரம்பரிய சூத்திரம்"]
    },
    "proprietary_ayurvedic_medicine": {
        "hi": "पेटेंट या प्रोप्राइटरी आयुर्वेदिक औषधि (Rule 158B)",
        "ta": "தனியுரிம ஆயுர்வேத மருந்து (Proprietary Ayurvedic Medicine)",
        "concept_en": "Patent or Proprietary Ayurvedic Medicine",
        "synonyms_hi": ["प्रोप्राइटरी औषधि", "पेटेंट औषधि", "नियम 158बी"],
        "synonyms_ta": ["தனியுரிம மருந்து", "விதி 158B"]
    },
    "ayurveda_aahar": {
        "hi": "आयुर्वेद आहार (FSSAI 2022 विनियम)",
        "ta": "ஆயுர்வேத ஆஹார் (Ayurveda Aahar - FSSAI)",
        "concept_en": "Ayurveda Aahar",
        "synonyms_hi": ["आयुर्वेद आहार", "खाद्य सुरक्षा", "एफएसएसएआई"],
        "synonyms_ta": ["ஆயுர்வேத ஆஹார்", "உணவுப் பொருட்கள்"]
    },
    "phytopharmaceutical": {
        "hi": "फाइटोफार्मास्युटिकल औषधि (मानकीकृत वानस्पतिक अर्क)",
        "ta": "பைட்டோபார்மாசூட்டிகல் (Phytopharmaceutical)",
        "concept_en": "Phytopharmaceutical Drug",
        "synonyms_hi": ["फाइटोफार्मास्यूटिकल", "मानकीकृत सत्व"],
        "synonyms_ta": ["பைட்டோபார்மாசூட்டிகல்", "தாவர சாறு"]
    },
    "prior_art": {
        "hi": "पूर्व कला / विद्यमान ज्ञान (Prior Art)",
        "ta": "முந்தைய கலை (Prior Art)",
        "concept_en": "Prior Art",
        "synonyms_hi": ["पूर्व कला", "पूर्व ज्ञान", "विद्यमान साहित्य"],
        "synonyms_ta": ["முந்தைய கலை", "முன் அறிவு"]
    },
    "export_compliance": {
        "hi": "निर्यात अनुपालन (US FDA / EU THMPD)",
        "ta": "ஏற்றுமதி இணக்கம் (Export Compliance)",
        "concept_en": "Export Market Compliance",
        "synonyms_hi": ["निर्यात नियम", "अंतरराष्ट्रीय मानक", "यूएस एफडीए"],
        "synonyms_ta": ["ஏற்றுமதி விதிமுறைகள்", "சர்வதேச தரநிலைகள்"]
    }
}
