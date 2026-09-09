from typing import List
from backend.app.schemas.classification import ClassificationInput, ClassificationResult

class FormulationClassificationAgent:
    """
    Expert system for classifying Ayurvedic and herbal products across Indian
    and International regulatory categories under the Drugs & Cosmetics Act 1940 (Rule 158B),
    FSSAI Ayurveda Aahar Regulations 2022, and Phytopharmaceutical Drug guidelines.
    """

    @staticmethod
    def classify(data: ClassificationInput) -> ClassificationResult:
        product_name = data.product_name
        claims_lower = (data.intended_use_or_claims or "").lower()
        hint_lower = (data.product_type_hint or "").lower()
        has_text_ref = data.has_classical_text_reference
        is_modified = data.is_modified_or_extract
        novel_process = data.novel_processing_method

        is_therapeutic = any(term in claims_lower for term in ["cure", "treat", "manage disease", "therapeutic", "relieve", "remedy", "disorder", "fever", "arthritis", "diabetes", "asthma"])
        is_dietary = any(term in claims_lower for term in ["food", "dietary", "nutrition", "wellness", "rasayana", "daily health", "immunity boost", "digestive tonic"])
        is_cosmetic = any(term in claims_lower for term in ["skin glow", "hair growth", "complexion", "wrinkle", "external application", "soap", "shampoo", "oil for hair"])

        # Decision Tree Logic
        if is_cosmetic and not is_therapeutic:
            likely_cat = "Cosmetic (Ayurvedic/Herbal)"
            conf = "High"
            conf_score = 0.92
            governance = "Drugs and Cosmetics Act, 1940 (Chapter IV-A & Schedule S/Cosmetic Rules)"
            why = f"The product '{product_name}' is intended for external beauty/cleansing application without systemic therapeutic claims."
            licensing = ["Form 32 (State Licensing Authority)", "Schedule T GMP compliance", "Heavy metal and microbiological safety test reports"]
            routes = ["Trademark (Class 3 - Cosmetics)", "Design Patent for packaging bottle/container", "Trade Secret for manufacturing formulation"]
            tk_concerns = "Low if formulation does not claim proprietary exclusivity over public traditional recipes."
            abs_concerns = "SBB intimation required under Section 7 if sourcing Indian biological resources."
            labels = ["'For External Use Only'", "Manufacturing Batch & Expiry", "Full ingredient declaration with INCI/Sanskrit names"]

        elif is_dietary and not is_therapeutic:
            likely_cat = "Ayurveda-Aahar (Ayurvedic Food / Dietary Supplement)"
            conf = "High"
            conf_score = 0.94
            governance = "Food Safety and Standards (Ayurveda Aahar) Regulations, 2022 (FSSAI) & MoA"
            why = f"The product '{product_name}' is prepared using principles from authoritative Ayurvedic texts for dietary nourishment and health promotion, without disease treatment claims."
            licensing = ["FSSAI Central / State License under Ayurveda Aahar category", "Schedule A herb compliance certificate", "Purity and heavy metal analysis"]
            routes = ["Trademark (Class 30 - Foods / Class 32 - Beverages)", "Trade Secret for extraction recipe", "GI tagging if regional variety is utilized"]
            tk_concerns = "Cannot patent classical food recipes; brand and trade dress protection are primary."
            abs_concerns = "Exempt if botanical ingredients are on the Section 40 Normally Traded Commodities (NTC) list; otherwise SBB intimation applies."
            labels = ["Official 'Ayurveda Aahar' Logo", "Mandatory warning: 'ONLY FOR DIETARY PURPOSES AND NOT FOR MEDICINAL USE'", "Recommended target dosha balance"]

        elif is_modified and novel_process and ("extract" in product_name.lower() or "fraction" in product_name.lower() or "standardized" in hint_lower):
            likely_cat = "Phytopharmaceutical Drug (Standardized Botanical Fraction)"
            conf = "High"
            conf_score = 0.88
            governance = "Drugs and Cosmetics Rules, 1945 (Schedule Y / New Drugs & Clinical Trials Rules, 2019)"
            why = f"The product '{product_name}' utilizes purified, standardized botanical fractions and novel extraction processes for therapeutic indications."
            licensing = ["CDSCO Form 44 / New Drug Approval", "Phase I-III Clinical Trials", "Pre-clinical safety and toxicology documentation", "cGMP manufacturing license"]
            routes = ["Process Patent (Extraction/Purification method)", "Composition Patent (demonstrating non-obvious synergistic efficacy under Sec 3(d))", "Trademark (Class 5)"]
            tk_concerns = "Must prove technical efficacy improvement beyond classical knowledge to overcome Section 3(p) and 3(d) of Indian Patents Act."
            abs_concerns = "Mandatory NBA prior approval under Section 6 before filing patent and Section 3 for commercial access."
            labels = ["Schedule H / Prescription warnings", "Standardized active marker percentage", "Precise dosage instructions"]

        elif has_text_ref and not is_modified:
            likely_cat = "Classical Ayurvedic Medicine"
            conf = "High"
            conf_score = 0.96
            governance = "Drugs and Cosmetics Act, 1940 (Section 3(a) & Rule 158B(1))"
            why = f"The product '{product_name}' strictly adheres to formulae specified in First Schedule authoritative Ayurvedic texts (e.g., {data.classical_text_name or 'Charaka Samhita / AFI'}) without modifications."
            licensing = ["Manufacturing License on Form 25-D from State Licensing Authority (SLA)", "Proof of textual citation from First Schedule book", "GMP Certificate (Schedule T)"]
            routes = ["Trademark for proprietary brand name (Class 5 - Pharmaceuticals)", "Not eligible for product patent under Section 3(p) as it is public traditional knowledge", "GI Tag if region-specific heritage applies"]
            tk_concerns = "Public domain traditional knowledge. Any attempt to patent will be rejected by the Patent Office and challenged via TKDL."
            abs_concerns = "Under 2023 Amendment, registered AYUSH practitioners and local cultivators have specific statutory exemptions; commercial body corporates require SBB intimation."
            labels = ["Ayurvedic Proprietary / Classical Medicine statement", "First Schedule textual reference", "Batch, Manufacturing date, and Expiry"]

        else:
            likely_cat = "Patent or Proprietary Ayurvedic Medicine (P&P)"
            conf = "High"
            conf_score = 0.90
            governance = "Drugs and Cosmetics Rules, 1945 (Rule 158B(2) - P&P Medicine)"
            why = f"The product '{product_name}' combines authoritative Ayurvedic ingredients in novel proportions, modified delivery mechanisms, or proprietary formulations."
            licensing = ["Manufacturing License (Form 25-D) with Rule 158B proof of safety/effectiveness", "Pilot clinical trial data or published literary evidence", "Schedule T GMP compliance"]
            routes = ["Trademark (Class 5 - Pharmaceuticals)", "Process/Formulation Patent if unexpected synergy and enhanced efficacy are established (overcoming Sec 3(p)/3(d))", "Trade Secret"]
            tk_concerns = "Scrutiny under Section 3(p) of Patents Act. Aggregation of known herbs is not patentable without synergistic data."
            abs_concerns = "Mandatory SBB intimation under Section 7; NBA Form III approval if applying for IPR."
            labels = ["'Ayurvedic Proprietary Medicine'", "Full qualitative and quantitative list of ingredients with classical Latin/Sanskrit names", "Storage and dosage instructions"]

        return ClassificationResult(
            likely_category=likely_cat,
            confidence=conf,
            confidence_score=conf_score,
            regulatory_classification=f"Category: {likely_cat}",
            statutory_governance=governance,
            why_explanation=why,
            licensing_requirements=licensing,
            potential_ip_routes=routes,
            traditional_knowledge_concerns=tk_concerns,
            abs_considerations=abs_concerns,
            mandatory_labeling_rules=labels,
            export_implications="Exporting to USA requires US FDA DSHEA dietary supplement compliance (21 CFR 111); EU requires Directive 2004/24/EC compliance."
        )

classification_agent = FormulationClassificationAgent()
