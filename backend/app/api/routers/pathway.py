from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/api/pathway", tags=["IP Pathway & Fees"])

PATHWAYS_DATA: Dict[str, Dict[str, Any]] = {
    "patent": {
        "title": "Patent Protection Pathway (India & PCT)",
        "instruments": ["Provisional Patent", "Complete Patent", "PCT International Phase"],
        "government_fees": {
            "individual_startup_msme": "₹1,600 (E-filing Form 1)",
            "large_entity": "₹8,000 (E-filing Form 1)",
            "nba_approval_fee": "₹10,000 (Form I to National Biodiversity Authority)"
        },
        "estimated_timeline": "18 - 36 months (Expedited examination available for startups)",
        "steps": [
            {"step": 1, "title": "TKDL & Prior Art Search", "desc": "Verify formulation against codified texts and published patents."},
            {"step": 2, "title": "NBA Section 6 Intimation", "desc": "File Form I with National Biodiversity Authority if using Indian bio-resources."},
            {"step": 3, "title": "Provisional Specification Filing", "desc": "File Form 1 & Form 2 with IPO to secure priority date."},
            {"step": 4, "title": "Complete Specification (12 Months)", "desc": "Submit complete claims, extraction protocol, and proof of efficacy."},
            {"step": 5, "title": "FER Response & Grant", "desc": "Respond to First Examination Report addressing Section 3(p)/3(d) queries."}
        ]
    },
    "trademark": {
        "title": "Trademark Registration Pathway",
        "instruments": ["Brand Name", "Logo", "Tagline"],
        "government_fees": {
            "individual_startup_msme": "₹4,500 per class (E-filing)",
            "large_entity": "₹9,000 per class"
        },
        "estimated_timeline": "6 - 12 months",
        "steps": [
            {"step": 1, "title": "TM Public Search", "desc": "Check IP India register for conflicting brand names in Class 5 (Pharmaceuticals/AYUSH) or Class 3 (Cosmetics) or Class 30/32 (AYUSH Aahar)."},
            {"step": 2, "title": "Application Filing (Form TM-A)", "desc": "File online with user affidavit if brand is already in use."},
            {"step": 3, "title": "Examination & Publication", "desc": "Respond to examination report; journal publication for 4 months opposition window."},
            {"step": 4, "title": "Registration Certificate", "desc": "Receive digital trademark registration certificate valid for 10 years."}
        ]
    },
    "gi": {
        "title": "Geographical Indication (GI) Pathway",
        "instruments": ["Regional Product GI Registration"],
        "government_fees": {
            "association_producers": "₹5,000 (Form GI-1)"
        },
        "estimated_timeline": "12 - 24 months",
        "steps": [
            {"step": 1, "title": "Producer Association Formation", "desc": "Form a collective body of regional Ayush vaidyas/producers."},
            {"step": 2, "title": "Historical & Geographical Proof Curation", "desc": "Document traditional link between region, soil/climate, and product quality."},
            {"step": 3, "title": "Filing GI Application", "desc": "Submit to GI Registry in Chennai with map and specification."},
            {"step": 4, "title": "Consultative Group Inspection", "desc": "Expert committee review and journal advertisement."}
        ]
    }
}

@router.get("/recommend/{category}")
def get_pathway_recommendation(category: str):
    """Get detailed step-by-step IP filing pathway and fees for a specific product category."""
    if category in ["classical_generic"]:
        return {
            "recommended_instruments": ["trademark", "gi"],
            "primary_pathway": PATHWAYS_DATA["trademark"],
            "secondary_pathway": PATHWAYS_DATA["gi"],
            "patent_note": "Direct patents are barred under Section 3(p). Focus on brand trademark and GI protection."
        }
    elif category in ["patent_proprietary", "new_drug", "phytopharmaceutical"]:
        return {
            "recommended_instruments": ["patent", "trademark"],
            "primary_pathway": PATHWAYS_DATA["patent"],
            "secondary_pathway": PATHWAYS_DATA["trademark"],
            "patent_note": "Eligible for extraction process patent or novel synergistic composition patent with NBA approval."
        }
    else: # ayush_aahar, cosmetic
        return {
            "recommended_instruments": ["trademark"],
            "primary_pathway": PATHWAYS_DATA["trademark"],
            "patent_note": "Focus on Trademark, Packaging Design, and FSSAI/Cosmetic licensing compliance."
        }
