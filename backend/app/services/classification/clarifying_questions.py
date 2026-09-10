"""
Multi-turn Clarifying Questions Engine for Ayurvedic Formulation Classification
Provides structured contextual clarifying questions in English, Hindi, and Tamil (Specification Section 98).
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ClarifyingOption(BaseModel):
    id: str
    label_en: str
    label_hi: str
    label_ta: str

class ClarifyingQuestion(BaseModel):
    id: str
    question_en: str
    question_hi: str
    question_ta: str
    options: List[ClarifyingOption]

CLARIFYING_QUESTIONS_REGISTRY: List[ClarifyingQuestion] = [
    ClarifyingQuestion(
        id="classical_text_authority",
        question_en="Is this formulation manufactured strictly according to the recipe in an authoritative book listed in the First Schedule of the Drugs & Cosmetics Act?",
        question_hi="क्या यह फॉर्मूलेशन औषधि एवं प्रसाधन सामग्री अधिनियम की प्रथम अनुसूची में उल्लिखित किसी प्रामाणिक ग्रंथ के अनुसार निर्मित है?",
        question_ta="இந்த மருந்து தயாரிப்பு மருந்துகள் சட்டத்தின் முதல் அட்டவணை நூல்களில் குறிப்பிடப்பட்டுள்ளவாறு சரியாக தயாரிக்கப்படுகிறதா?",
        options=[
            ClarifyingOption(
                id="exact_classical",
                label_en="Yes, exact classical recipe (e.g. Charaka / Sushruta Samhita)",
                label_hi="हाँ, सटीक शास्त्रीय ग्रंथ विधि (उदा. चरक / सुश्रुत संहिता)",
                label_ta="ஆம், பாரம்பரிய மருத்துவ நூல் முறைப்படி (எ.கா. சரக / சுஸ்ருத சம்ஹிதை)"
            ),
            ClarifyingOption(
                id="modified_ratio",
                label_en="Contains classical ingredients, but in modified ratios or modern extraction form",
                label_hi="शास्त्रीय घटक मौजूद हैं, लेकिन परिवर्तित अनुपात या आधुनिक निष्कर्षण रूप में",
                label_ta="பாரம்பரிய மூலிகைகள் உள்ளன, ஆனால் மாற்றியமைக்கப்பட்ட விகிதத்தில்"
            ),
            ClarifyingOption(
                id="novel_combination",
                label_en="Completely new proprietary combination of herbal extracts",
                label_hi="हर्बल अर्क का पूरी तरह से नया प्रोप्रायटरी संयोजन",
                label_ta="முற்றிலும் புதிய மூலிகை கலவை"
            )
        ]
    ),
    ClarifyingQuestion(
        id="intended_claims_and_use",
        question_en="What is the primary commercial label claim and administration intended for this product?",
        question_hi="इस उत्पाद के लिए मुख्य व्यावसायिक लेबल दावा और उपयोग का क्या उद्देश्य है?",
        question_ta="இந்த தயாரிப்பின் முக்கிய லேபிள் பயன்பாட்டு நோக்கம் என்ன?",
        options=[
            ClarifyingOption(
                id="therapeutic_cure",
                label_en="Therapeutic treatment, mitigation, or diagnosis of a specific medical disease/disorder",
                label_hi="किसी विशिष्ट चिकित्सीय बीमारी/रोग का उपचार या शमन (औषधि श्रेणी)",
                label_ta="குறிப்பிட்ட நோய் சிகிச்சை அல்லது நிவாரணம் (மருந்து வகை)"
            ),
            ClarifyingOption(
                id="ayurveda_aahar",
                label_en="Nutritional wellness, Rasayana, or general health maintenance without disease claims",
                label_hi="पोषण, रसायन या सामान्य स्वास्थ्य संवर्धन (रोग निवारण के दावे के बिना)",
                label_ta="ஊட்டச்சத்து, புத்துணர்ச்சி அல்லது பொது ஆரோக்கியம் (நோய் சிகிச்சை கூற்றுகள் இல்லாமல்)"
            ),
            ClarifyingOption(
                id="cosmetic_external",
                label_en="External topical application solely for cleansing, beautifying, or altering appearance",
                label_hi="त्वचा/बालों की सुंदरता एवं स्वच्छता हेतु केवल बाह्य उपयोग (प्रसाधन)",
                label_ta="வெளிப்புற அழகு மற்றும் சுத்திகரிப்பு பயன்பாடு மட்டுமே"
            )
        ]
    ),
    ClarifyingQuestion(
        id="biological_sourcing",
        question_en="How are the raw biological materials (herbs, extracts) sourced for this product?",
        question_hi="इस उत्पाद के लिए कच्चे जैविक पदार्थ (जड़ी-बूटियाँ) कहाँ से प्राप्त किए जाते हैं?",
        question_ta="இந்த தயாரிப்புக்கான மூலிகைகள் எவ்வாறு பெறப்படுகின்றன?",
        options=[
            ClarifyingOption(
                id="wild_india",
                label_en="Harvested from wild natural habitats / forests in India",
                label_hi="भारत में जंगलों या प्राकृतिक आवासों से एकत्र किया गया",
                label_ta="இந்திய காடுகள் அல்லது இயற்கை மூலங்களிலிருந்து பெறப்பட்டது"
            ),
            ClarifyingOption(
                id="cultivated_india",
                label_en="Sourced from certified cultivated agricultural farms in India (NTC commodity)",
                label_hi="भारत में प्रमाणित कृषि फार्मों से (सामान्य व्यापारिक वस्तु)",
                label_ta="இந்தியாவில் சான்றளிக்கப்பட்ட விவசாய பண்ணைகளில் இருந்து"
            ),
            ClarifyingOption(
                id="imported_abroad",
                label_en="Imported entirely from foreign suppliers outside India",
                label_hi="भारत के बाहर विदेशी आपूर्तिकर्ताओं से पूर्णतः आयातित",
                label_ta="வெளிநாடுகளில் இருந்து முழுமையாக இறக்குமதி செய்யப்பட்டது"
            )
        ]
    ),
    ClarifyingQuestion(
        id="synergy_clinical_data",
        question_en="Do you possess verifiable comparative experimental or pilot clinical data proving unexpected synergy beyond individual herb properties?",
        question_hi="क्या आपके पास व्यक्तिगत जड़ी-बूटियों के ज्ञात गुणों से परे अप्रत्याशित सहक्रिया (Synergy) सिद्ध करने वाले तुलनात्मक आंकड़े हैं?",
        question_ta="தனிப்பட்ட மூலிகைகளின் பண்புகளுக்கு அப்பால் எதிர்பாராத ஒருங்கிணைந்த செயல்திறனை நிரூபிக்கும் மருத்துவ சான்றுகள் உங்களிடம் உள்ளதா?",
        options=[
            ClarifyingOption(
                id="has_synergy_data",
                label_en="Yes, documented laboratory/clinical synergy data is available",
                label_hi="हाँ, प्रलेखित प्रयोगशाला/नैदानिक सहक्रिया आंकड़े उपलब्ध हैं",
                label_ta="ஆம், ஆவணப்படுத்தப்பட்ட ஆய்வக/மருத்துவ செயல்திறன் சான்றுகள் உள்ளன"
            ),
            ClarifyingOption(
                id="no_synergy_data",
                label_en="No, formulation is based solely on traditional textual knowledge",
                label_hi="नहीं, फॉर्मूलेशन केवल पारंपरिक ग्रंथ ज्ञान पर आधारित है",
                label_ta="இல்லை, பாரம்பரிய மருத்துவ நூல்களின் அடிப்படையில் மட்டுமே"
            )
        ]
    )
]

def get_clarifying_questions(language: str = "en", max_questions: int = 4) -> List[Dict[str, Any]]:
    """Returns contextual clarifying questions localized to EN, HI, or TA."""
    lang = language.lower()
    questions_out = []
    for q in CLARIFYING_QUESTIONS_REGISTRY[:max_questions]:
        q_text = q.question_en
        if lang == "hi":
            q_text = q.question_hi
        elif lang == "ta":
            q_text = q.question_ta

        options_out = []
        for opt in q.options:
            opt_label = opt.label_en
            if lang == "hi":
                opt_label = opt.label_hi
            elif lang == "ta":
                opt_label = opt.label_ta
            options_out.append({"id": opt.id, "label": opt_label})

        questions_out.append({
            "id": q.id,
            "question": q_text,
            "options": options_out
        })
    return questions_out
