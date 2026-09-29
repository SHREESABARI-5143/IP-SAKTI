from typing import Dict, Any, Union
from app.models.schemas import (
    ClassificationQuestion,
    ClassificationQuestionOption,
    ClassificationResult
)

class ClassificationService:
    """
    Implements the 6-category AYUSH product classification wizard decision tree.
    """
    QUESTIONS: Dict[str, ClassificationQuestion] = {
        "q1": ClassificationQuestion(
            question_id="q1",
            title_en="Is your formulation and method of preparation found in an authoritative text listed in the First Schedule of the Drugs & Cosmetics Act, 1940?",
            title_hi="क्या आपका फॉर्मूलेशन और निर्माण विधि औषधीय एवं प्रसाधन सामग्री अधिनियम, 1940 की प्रथम अनुसूची में सूचीबद्ध प्रामाणिक ग्रंथ में पाई जाती है?",
            description_en="Authoritative texts include Charaka Samhita, Sushruta Samhita, Sharngadhara Samhita, Bhavaprakasha, Bhaishajya Ratnavali, AFI, etc.",
            description_hi="प्रामाणिक ग्रंथों में चरक संहिता, सुश्रुत संहिता, शार्ङ्गधर संहिता, भावप्रकाश, भैषज्य रत्नावली, एएफआई आदि शामिल हैं।",
            options=[
                ClassificationQuestionOption(
                    id="q1_yes",
                    label_en="Yes — It is directly from an authoritative text",
                    label_hi="हाँ — यह सीधे किसी प्रामाणिक ग्रंथ से है",
                    next_question_id="q2"
                ),
                ClassificationQuestionOption(
                    id="q1_no",
                    label_en="No — It is a proprietary or novel composition",
                    label_hi="नहीं — यह एक स्वदेशी/स्वामित्व या नवीन संयोजन है",
                    next_question_id="q3"
                ),
                ClassificationQuestionOption(
                    id="q1_not_sure",
                    label_en="Not Sure — Need to check First Schedule list",
                    label_hi="निश्चित नहीं — प्रथम अनुसूची सूची जांचने की आवश्यकता है",
                    next_question_id="q2"
                )
            ]
        ),
        "q2": ClassificationQuestion(
            question_id="q2",
            title_en="Is the product manufactured EXACTLY according to the traditional formula and process with no modification?",
            title_hi="क्या उत्पाद बिना किसी संशोधन के बिल्कुल पारंपरिक सूत्र और प्रक्रिया के अनुसार निर्मित किया गया है?",
            description_en="Any change in ingredients, extraction methods, or dosage form makes it non-classical.",
            description_hi="सामग्री, निष्कर्षण विधियों या खुराक के रूप में कोई भी बदलाव इसे गैर-शास्त्रीय बनाता है।",
            options=[
                ClassificationQuestionOption(
                    id="q2_exact",
                    label_en="Exact Match — Unmodified Classical Formulation",
                    label_hi="सटीक मिलान — अपरिवर्तित शास्त्रीय फॉर्मूलेशन",
                    target_category="classical_generic"
                ),
                ClassificationQuestionOption(
                    id="q2_modified",
                    label_en="Modified — Traditional base with novel additions/process",
                    label_hi="संशोधित — नए परिवर्धन/प्रक्रिया के साथ पारंपरिक आधार",
                    next_question_id="q3"
                )
            ]
        ),
        "q3": ClassificationQuestion(
            question_id="q3",
            title_en="Is the product a purified, standardized plant fraction containing active marker compounds?",
            title_hi="क्या उत्पाद सक्रिय मार्कर यौगिकों वाला एक शुद्ध, मानकीकृत पादप अंश (Plant Fraction) है?",
            description_en="Phytopharmaceuticals require standardized chemical markers (min. 4 active compounds) and allopathic-like clinical evaluation.",
            description_hi="फाइटोफार्मास्युटिकल दवाओं के लिए मानकीकृत रासायनिक मार्कर और नैदानिक मूल्यांकन की आवश्यकता होती है।",
            options=[
                ClassificationQuestionOption(
                    id="q3_yes",
                    label_en="Yes — Purified plant fraction with standardized markers",
                    label_hi="हाँ — मानकीकृत मार्करों के साथ शुद्ध पादप अंश",
                    target_category="phytopharmaceutical"
                ),
                ClassificationQuestionOption(
                    id="q3_no",
                    label_en="No — Whole herb extract, powder, or polyherbal combination",
                    label_hi="नहीं — संपूर्ण जड़ी-बूटी का अर्क, चूर्ण या बहु-जड़ी-बूटी संयोजन",
                    next_question_id="q4"
                )
            ]
        ),
        "q4": ClassificationQuestion(
            question_id="q4",
            title_en="What is the primary intended purpose and delivery claim of your product?",
            title_hi="आपके उत्पाद का प्राथमिक उद्देश्य और दावा क्या है?",
            description_en="Therapeutic disease treatment vs health supplement vs cosmetic application.",
            description_hi="रोग निवारण बनाम स्वास्थ्य पूरक (हेल्थ सप्लीमेंट) बनाम सौंदर्य प्रसाधन।",
            options=[
                ClassificationQuestionOption(
                    id="q4_drug",
                    label_en="Treatment or Prevention of Disease / Therapeutic Claim",
                    label_hi="रोग का इलाज या रोकथाम / चिकित्सीय दावा",
                    next_question_id="q5"
                ),
                ClassificationQuestionOption(
                    id="q4_food",
                    label_en="Nutritional / Dietary Health Supplement (No Disease Claims)",
                    label_hi="पोषण / आहार स्वास्थ्य पूरक (कोई बीमारी का दावा नहीं)",
                    target_category="ayush_aahar"
                ),
                ClassificationQuestionOption(
                    id="q4_cosmetic",
                    label_en="Beauty, Skin, Hair, or Hygiene enhancement",
                    label_hi="सौंदर्य, त्वचा, बाल या स्वच्छता संवर्धन",
                    target_category="cosmetic"
                )
            ]
        ),
        "q5": ClassificationQuestion(
            question_id="q5",
            title_en="Has human clinical trial safety and efficacy data been generated for this novel formulation?",
            title_hi="क्या इस नवीन फॉर्मूलेशन के लिए मानव नैदानिक परीक्षण (Clinical Trial) सुरक्षा और प्रभावकारिता डेटा उत्पन्न किया गया है?",
            description_en="New ASU drugs require full clinical trial data under Rule 158-B before drug licensing.",
            description_hi="नियम 158-बी के तहत नई एएसयू दवाओं को पूर्ण नैदानिक परीक्षण डेटा की आवश्यकता होती है।",
            options=[
                ClassificationQuestionOption(
                    id="q5_yes",
                    label_en="Yes — Clinical trial evidence & safety data available",
                    label_hi="हाँ — नैदानिक परीक्षण प्रमाण और सुरक्षा डेटा उपलब्ध है",
                    target_category="new_drug"
                ),
                ClassificationQuestionOption(
                    id="q5_no",
                    label_en="No — Proprietary brand medicine based on traditional ingredients",
                    label_hi="नहीं — पारंपरिक अवयवों पर आधारित स्वामित्व ब्रांड दवा",
                    target_category="patent_proprietary"
                )
            ]
        )
    }

    CATEGORIES_INFO: Dict[str, Dict[str, Any]] = {
        "classical_generic": {
            "category_name_en": "Classical / Generic Ayurvedic Medicine",
            "category_name_hi": "शास्त्रीय / जेनेरिक आयुर्वेदिक औषधि",
            "confidence": "HIGH",
            "reasoning": "The product is manufactured strictly according to a formulation and method described in a First-Schedule authoritative text of the Drugs & Cosmetics Act, 1940.",
            "cited_rules": [
                "Drugs & Cosmetics Act, 1940, Section 3(a)",
                "Drugs & Cosmetics Act, 1940, First Schedule",
                "Patents Act, 1970, Section 3(p) (Bars patenting per se)"
            ],
            "regulatory_implications": [
                "Requires Form 25-D AYUSH Manufacturing Licence from State Licensing Authority.",
                "No clinical trial required if exact text reference is provided.",
                "Must adhere strictly to Ayurvedic Pharmacopoeia of India (API) standards."
            ],
            "applicable_ip_instruments": [
                "Trademark (Brand name protection)",
                "Geographical Indication (if region-specific)",
                "Trade Secret (Proprietary processing parameters)",
                "Patents: NOT AVAILABLE for classical formulation per se (Section 3(p))"
            ],
            "next_steps": [
                "Verify formulation entry in Ayurvedic Formulary of India (AFI).",
                "Apply for Form 25-D licence with State AYUSH Directorate.",
                "Register Trademark for your brand name to protect market identity."
            ]
        },
        "patent_proprietary": {
            "category_name_en": "Patent & Proprietary (P&P) Medicine",
            "category_name_hi": "पेटेंट एवं प्रोप्राइटरी (P&P) औषधि",
            "confidence": "HIGH",
            "reasoning": "The product uses ingredients mentioned in First-Schedule texts but in a proprietary combination or under a proprietary brand name not found in classical texts.",
            "cited_rules": [
                "Drugs & Cosmetics Act, 1940, Section 3(h)",
                "Drugs & Cosmetics Rules, 1945, Rule 158-B",
                "Biological Diversity Act, 2002, Section 7 (SBB intimation)"
            ],
            "regulatory_implications": [
                "Requires Form 25-D manufacturing licence for P&P medicine.",
                "Requires proof of safety & rationale (published pilot studies or literature evidence).",
                "Intimation to State Biodiversity Board (SBB) for bio-resource sourcing."
            ],
            "applicable_ip_instruments": [
                "Patent (For novel synergy or inventive extraction process — Section 3(d)/(p) clearance needed)",
                "Trademark (Brand name & logo protection)",
                "Industrial Design (Unique bottle/packaging design)",
                "Trade Secret (Formulation ratio & processing parameters)"
            ],
            "next_steps": [
                "Perform TKDL prior-art search to verify novelty over classical texts.",
                "Prepare proof of safety/efficacy documents under Rule 158-B.",
                "File Trademark application with IP India."
            ]
        },
        "new_drug": {
            "category_name_en": "New / Non-Classical Ayurvedic Drug",
            "category_name_hi": "नवीन / गैर-शास्त्रीय आयुर्वेदिक दवा",
            "confidence": "HIGH",
            "reasoning": "The product contains novel active ingredients or novel therapeutic indications requiring rigorous clinical trial evidence of safety and efficacy.",
            "cited_rules": [
                "Drugs & Cosmetics Rules, 1945, Rule 158-B (New ASU Drugs)",
                "Patents Act, 1970, Section 2(1)(j)",
                "Biological Diversity Act, 2002, Section 6 (NBA approval for IPR)"
            ],
            "regulatory_implications": [
                "Requires CDSCO / AYUSH clearance for clinical trials.",
                "Mandatory Phase I-III clinical trial safety & efficacy data.",
                "Prior approval of National Biodiversity Authority (NBA) before filing patent."
            ],
            "applicable_ip_instruments": [
                "Product Patent & Process Patent (Strong patent eligibility if novelty proven)",
                "Trademark",
                "Data Exclusivity / Confidential Information"
            ],
            "next_steps": [
                "File provisional patent application prior to public disclosure.",
                "Apply for NBA Section 6 approval for IPR filing.",
                "Initiate ethics committee approved clinical trial protocols."
            ]
        },
        "phytopharmaceutical": {
            "category_name_en": "Phytopharmaceutical Drug",
            "category_name_hi": "फाइटोफार्मास्युटिकल औषधि",
            "confidence": "HIGH",
            "reasoning": "The product is a purified, standardized plant fraction with identified active marker compounds regulated under allopathic-like drug discovery pathways.",
            "cited_rules": [
                "Drugs & Cosmetics Rules, 1945, Appendix I (Phytopharmaceuticals)",
                "Patents Act, 1970, Section 3(d) (Enhancement of efficacy)",
                "Biological Diversity Act, 2002, Section 6"
            ],
            "regulatory_implications": [
                "Regulated directly under CDSCO allopathic drug pathway.",
                "Requires minimum 4 active chemical markers standardized via HPLC/LC-MS.",
                "Full toxicological, pharmacological, and clinical trial dossier required."
            ],
            "applicable_ip_instruments": [
                "Composition of Matter Patent (Purified fraction)",
                "Process Patent (Standardized extraction technology)",
                "Trademark"
            ],
            "next_steps": [
                "Establish chemical fingerprinting and marker quantification.",
                "File international PCT patent application.",
                "Submit IND application to CDSCO."
            ]
        },
        "ayush_aahar": {
            "category_name_en": "AYUSH Aahar / Nutraceutical (FSSAI)",
            "category_name_hi": "आयुष आहार / न्यूट्रास्यूटिकल (FSSAI)",
            "confidence": "HIGH",
            "reasoning": "The product is intended for health maintenance or dietary supplementation without therapeutic disease treatment claims.",
            "cited_rules": [
                "FSSAI AYUSH Aahar Regulations, 2022, Regulation 3",
                "Food Safety and Standards Act, 2006",
                "Trade Marks Act, 1999"
            ],
            "regulatory_implications": [
                "Regulated under FSSAI, NOT under Drugs & Cosmetics Act.",
                "Must display AYUSH Aahar logo on packaging.",
                "Prohibited from making medical/disease cure claims."
            ],
            "applicable_ip_instruments": [
                "Trademark & Brand Protection",
                "Industrial Design (Packaging & Container)",
                "Copyright (Label design & marketing content)",
                "Process Patent (Novel food processing technology)"
            ],
            "next_steps": [
                "Obtain FSSAI Central/State Food Manufacturing Licence.",
                "Ensure label compliance with AYUSH Aahar logo regulations.",
                "File Trademark for brand name."
            ]
        },
        "cosmetic": {
            "category_name_en": "Ayurvedic Cosmetic Product",
            "category_name_hi": "आयुर्वेदिक कॉस्मेटिक / प्रसाधन उत्पाद",
            "confidence": "HIGH",
            "reasoning": "The product is intended for topical application for beautification, cleansing, or skin/hair hygiene.",
            "cited_rules": [
                "Cosmetics Rules, 2020",
                "Drugs & Cosmetics Act, 1940",
                "Trade Marks Act, 1999"
            ],
            "regulatory_implications": [
                "Requires Cosmetic Manufacturing Licence under Cosmetics Rules 2020.",
                "Must adhere to BIS safety standards for skin/hair care.",
                "No therapeutic disease claims allowed."
            ],
            "applicable_ip_instruments": [
                "Trademark",
                "Industrial Design (Bottles, jars, dispensers)",
                "Trade Secret (Formulation scent/texture ratios)"
            ],
            "next_steps": [
                "Apply for Cosmetic Manufacturing Licence.",
                "Conduct heavy metal & micro-biological safety testing.",
                "Register Trademark and Design patents for custom packaging."
            ]
        }
    }

    def start_classification(self) -> ClassificationQuestion:
        return self.QUESTIONS["q1"]

    def submit_answer(self, question_id: str, option_id: str) -> Union[ClassificationQuestion, ClassificationResult]:
        question = self.QUESTIONS.get(question_id)
        if not question:
            return self.QUESTIONS["q1"]

        selected_option = next((opt for opt in question.options if opt.id == option_id), None)
        if not selected_option:
            return question

        # If option points directly to a category result
        if selected_option.target_category:
            cat_key = selected_option.target_category
            info = self.CATEGORIES_INFO.get(cat_key, self.CATEGORIES_INFO["patent_proprietary"])
            return ClassificationResult(
                category=cat_key,
                category_name_en=info["category_name_en"],
                category_name_hi=info["category_name_hi"],
                confidence=info["confidence"],
                reasoning=info["reasoning"],
                cited_rules=info["cited_rules"],
                regulatory_implications=info["regulatory_implications"],
                applicable_ip_instruments=info["applicable_ip_instruments"],
                next_steps=info["next_steps"]
            )

        # Otherwise navigate to next question
        next_q_id = selected_option.next_question_id or "q1"
        return self.QUESTIONS.get(next_q_id, self.QUESTIONS["q1"])

classification_service = ClassificationService()
