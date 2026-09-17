import os
import json
import hashlib
from datetime import datetime, timezone

# 1. Knowledge Graph Nodes & Edges
nodes = [
    {"entity_id": "ENT_LAW_PATENTS_1970", "name": "The Patents Act, 1970", "entity_type": "Law", "jurisdiction": "India", "description": "Principal Indian patent statute governing patentability of inventions."},
    {"entity_id": "ENT_SEC_3P", "name": "Section 3(p) Patents Act", "entity_type": "Section", "jurisdiction": "India", "description": "Statutory exclusion of traditional knowledge and non-synergistic admixtures."},
    {"entity_id": "ENT_SEC_3D", "name": "Section 3(d) Patents Act", "entity_type": "Section", "jurisdiction": "India", "description": "Requirement of enhanced therapeutic efficacy for new forms of known substances."},
    {"entity_id": "ENT_SEC_3E", "name": "Section 3(e) Patents Act", "entity_type": "Section", "jurisdiction": "India", "description": "Exclusion of mere admixtures lacking synergistic technical interactions."},
    {"entity_id": "ENT_SEC_10_4", "name": "Section 10(4)(d)(ii) Patents Act", "entity_type": "Section", "jurisdiction": "India", "description": "Mandatory disclosure of biological material source and geographical origin."},
    {"entity_id": "ENT_SEC_25_1_K", "name": "Section 25(1)(k) Opposition", "entity_type": "Section", "jurisdiction": "India", "description": "Pre-grant patent opposition grounds based on traditional knowledge anticipation."},
    {"entity_id": "ENT_LAW_BD_2002", "name": "Biological Diversity Act, 2002", "entity_type": "Law", "jurisdiction": "India", "description": "National legislation implementing access and benefit sharing (ABS) for Indian bio-resources."},
    {"entity_id": "ENT_LAW_BD_2023", "name": "Biological Diversity (Amendment) Act, 2023", "entity_type": "Law", "jurisdiction": "India", "description": "Decriminalized framework and codification of AYUSH practitioner exemptions."},
    {"entity_id": "ENT_SEC_3_BDA", "name": "Section 3 BDA Approvals", "entity_type": "Section", "jurisdiction": "India", "description": "Mandatory prior approval for foreign entities accessing Indian biological resources."},
    {"entity_id": "ENT_SEC_6_BDA", "name": "Section 6 BDA IPR Approval", "entity_type": "Section", "jurisdiction": "India", "description": "Mandatory NBA approval before applying for or commercializing patent rights based on Indian bio-resources."},
    {"entity_id": "ENT_SEC_40_BDA", "name": "Section 40 BDA NTC Exemptions", "entity_type": "Section", "jurisdiction": "India", "description": "Exemption from ABS provisions for Normally Traded Commodities listed in official gazette notifications."},
    {"entity_id": "ENT_AUTH_NBA", "name": "National Biodiversity Authority", "entity_type": "Authority", "jurisdiction": "India", "description": "Statutory body governing access, approvals, and benefit sharing under the BD Act."},
    {"entity_id": "ENT_AUTH_CGPDTM", "name": "Controller General of Patents, Designs and Trade Marks", "entity_type": "Authority", "jurisdiction": "India", "description": "National IP office administering patent, design, and trademark registrations."},
    {"entity_id": "ENT_LAW_DC_1940", "name": "Drugs and Cosmetics Act, 1940", "entity_type": "Law", "jurisdiction": "India", "description": "Statute regulating manufacture, licensing, and standards of ASU drugs."},
    {"entity_id": "ENT_RULE_158B", "name": "Rule 158B D&C Rules", "entity_type": "Rule", "jurisdiction": "India", "description": "Proof of safety and effectiveness requirements for Patent/Proprietary Ayurvedic medicines."},
    {"entity_id": "ENT_SCHED_T", "name": "Schedule T GMP Standards", "entity_type": "Regulation", "jurisdiction": "India", "description": "Good Manufacturing Practices mandatory for Ayurvedic medicine manufacturing facilities."},
    {"entity_id": "ENT_REG_AYURVEDA_AAHAR_2022", "name": "FSSAI Ayurveda Aahar Regulations, 2022", "entity_type": "Regulation", "jurisdiction": "India", "description": "Regulatory framework for dietary and nutritional food supplements under Ayurvedic principles."},
    {"entity_id": "ENT_TREATY_WIPO_GRATK_2024", "name": "WIPO GRATK Treaty, 2024", "entity_type": "Treaty", "jurisdiction": "International", "description": "International mandatory disclosure requirements for genetic resources and traditional knowledge in patent applications."},
    {"entity_id": "ENT_HERB_ASHWAGANDHA", "name": "Withania somnifera (Ashwagandha)", "entity_type": "BiologicalResource", "jurisdiction": "India", "description": "Standardized Rasayana herb widely documented in Ayurvedic Pharmacopoeia of India."},
    {"entity_id": "ENT_HERB_TURMERIC", "name": "Curcuma longa (Haridra / Turmeric)", "entity_type": "BiologicalResource", "jurisdiction": "India", "description": "Traditional anti-inflammatory and antiseptic botanical rhizome."},
    {"entity_id": "ENT_HERB_TULSI", "name": "Ocimum sanctum (Tulsi / Holy Basil)", "entity_type": "BiologicalResource", "jurisdiction": "India", "description": "Adaptogenic aromatic herb utilized in classical Rasayana formulations."}
]

edges = [
    {"source_entity_id": "ENT_LAW_PATENTS_1970", "target_entity_id": "ENT_SEC_3P", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_PATENTS_1970", "target_entity_id": "ENT_SEC_3D", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_PATENTS_1970", "target_entity_id": "ENT_SEC_3E", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_PATENTS_1970", "target_entity_id": "ENT_SEC_10_4", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_PATENTS_1970", "target_entity_id": "ENT_SEC_25_1_K", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_BD_2002", "target_entity_id": "ENT_SEC_3_BDA", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_BD_2002", "target_entity_id": "ENT_SEC_6_BDA", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_BD_2002", "target_entity_id": "ENT_SEC_40_BDA", "relationship_type": "LAW_HAS_SECTION", "weight": 1.0},
    {"source_entity_id": "ENT_SEC_10_4", "target_entity_id": "ENT_SEC_6_BDA", "relationship_type": "REQUIRES_NBA_APPROVAL", "weight": 1.0},
    {"source_entity_id": "ENT_HERB_ASHWAGANDHA", "target_entity_id": "ENT_SEC_3P", "relationship_type": "EXCLUDED_UNDER_3P", "weight": 0.9},
    {"source_entity_id": "ENT_HERB_TURMERIC", "target_entity_id": "ENT_SEC_3P", "relationship_type": "EXCLUDED_UNDER_3P", "weight": 0.9},
    {"source_entity_id": "ENT_HERB_TURMERIC", "target_entity_id": "ENT_SEC_40_BDA", "relationship_type": "EXEMPT_UNDER_NTC", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_DC_1940", "target_entity_id": "ENT_RULE_158B", "relationship_type": "LAW_HAS_RULE", "weight": 1.0},
    {"source_entity_id": "ENT_LAW_DC_1940", "target_entity_id": "ENT_SCHED_T", "relationship_type": "LAW_HAS_REGULATION", "weight": 1.0},
    {"source_entity_id": "ENT_TREATY_WIPO_GRATK_2024", "target_entity_id": "ENT_SEC_10_4", "relationship_type": "HARMONIZED_WITH", "weight": 1.0}
]

with open("data/knowledge_graph/nodes.jsonl", "w", encoding="utf-8") as f:
    for n in nodes:
        f.write(json.dumps(n, ensure_ascii=False) + "\n")

with open("data/knowledge_graph/edges.jsonl", "w", encoding="utf-8") as f:
    for e in edges:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")

# 2. Grounded Play Scenarios with Verified Legal Citations
play_scenarios = [
    {
        "scenario_id": "SCENARIO_01_ASHWAGANDHA_EXTRACT",
        "locale": "en",
        "title": "The Ashwagandha Bio-Extraction Dilemma",
        "description": "Your biotech startup developed a proprietary hydro-ethanolic extraction process yielding 10x withanolide content from Withania somnifera. You want to commercialize and export to the US.",
        "choices_json": json.dumps([
            {"id": "A", "label": "File patent claiming raw Ashwagandha powder for stress relief"},
            {"id": "B", "label": "File patent claiming the novel extraction process + synergistic formulation with proving data, while seeking Section 6 NBA approval before grant"},
            {"id": "C", "label": "Export directly to US as a prescription drug without DSHEA compliance"}
        ]),
        "outcomes_json": json.dumps({
            "A": {"status": "REJECTED", "feedback": "Statutory refusal under Section 3(p) of the Patents Act, 1970: Raw Ashwagandha for stress relief is codified Traditional Knowledge.", "legal_risk": "HIGH"},
            "B": {"status": "SUCCESS", "feedback": "Compliant pathway: Process patent overcomes Section 3(p) when backed by unexpected efficacy data under Section 3(d), while NBA Section 6 approval satisfies biological resource disclosure.", "legal_risk": "LOW"},
            "C": {"status": "VIOLATION", "feedback": "Export detention under US FDA DSHEA (21 CFR Part 111 cGMP) and misbranding regulations.", "legal_risk": "CRITICAL"}
        }),
        "citation_ids_json": json.dumps(["SRC_IN_PATENTS_ACT_1970_36", "SRC_IN_BD_ACT_2002_2023_6", "SRC_INTL_IP_AND_EXPORT_REGULATIONS_3"])
    },
    {
        "scenario_id": "SCENARIO_02_CURCUMIN_NTC_EXPORT",
        "locale": "en",
        "title": "Normally Traded Commodity & Benefit Sharing",
        "description": "An FMCG enterprise purchases 5 tonnes of Curcuma longa (dry turmeric rhizomes) from the domestic agricultural market for Ayurvedic culinary seasoning export.",
        "choices_json": json.dumps([
            {"id": "A", "label": "Apply for full Section 3 NBA prior approval for raw commodity trading"},
            {"id": "B", "label": "Rely on Section 40 BDA Normally Traded Commodities (NTC) notification exemption for commercial trade"},
            {"id": "C", "label": "Claim exclusive global patent on turmeric's anti-inflammatory properties"}
        ]),
        "outcomes_json": json.dumps({
            "A": {"status": "UNNECESSARY", "feedback": "Normally Traded Commodities notified under Section 40 are explicitly exempt from Section 3 approval for direct trade.", "legal_risk": "LOW"},
            "B": {"status": "SUCCESS", "feedback": "Legally compliant: Turmeric rhizomes are notified under Gazette S.O. 1352(E) NTC list, exempting pure commercial trade from ABS levy.", "legal_risk": "NONE"},
            "C": {"status": "REJECTED", "feedback": "Statutory bar under Section 3(p) (CSIR Turmeric Patent Revocation precedent, US Patent 5,401,504).", "legal_risk": "CRITICAL"}
        }),
        "citation_ids_json": json.dumps(["SRC_IN_BD_ACT_2002_2023_40", "SRC_IN_BD_NTC_2023_1", "SRC_IN_PATENTS_ACT_1970_36"])
    },
    {
        "scenario_id": "SCENARIO_03_AYURVEDA_AAHAR_LABELING",
        "locale": "en",
        "title": "Ayurveda Aahar vs Proprietary Medicine Licensing",
        "description": "A startup develops an Ayurvedic Chyawanprash-inspired wellness energy bar and wishes to market it through national supermarket chains.",
        "choices_json": json.dumps([
            {"id": "A", "label": "Apply for FSSAI Ayurveda Aahar license with mandatory logo and target Rasayana claims under Regulation 4 & 6"},
            {"id": "B", "label": "Market as a pharmaceutical cure for acute respiratory infections without clinical trials"},
            {"id": "C", "label": "Sell as generic confectionary omitting all botanical ingredient proportions"}
        ]),
        "outcomes_json": json.dumps({
            "A": {"status": "SUCCESS", "feedback": "Compliant route: FSSAI (Ayurveda Aahar) Regulations 2022 allow authoritative Rasayana wellness claims with official logo.", "legal_risk": "LOW"},
            "B": {"status": "VIOLATION", "feedback": "Severe violation of Rule 158B and Drugs & Magic Remedies (Objectionable Advertisements) Act, 1954.", "legal_risk": "CRITICAL"},
            "C": {"status": "VIOLATION", "feedback": "Non-compliant with FSSAI labeling mandates and consumer disclosure standards.", "legal_risk": "HIGH"}
        }),
        "citation_ids_json": json.dumps(["SRC_IN_AYURVEDA_AAHAR_2022_4", "SRC_IN_AYURVEDA_AAHAR_2022_6", "SRC_IN_DRUGS_COSMETICS_ACT_1940_15"])
    }
]

with open("data/play/scenarios.jsonl", "w", encoding="utf-8") as f:
    for sc in play_scenarios:
        f.write(json.dumps(sc, ensure_ascii=False) + "\n")

# 3. Reference Tables (Jurisdictions & Legal Instruments)
jurisdictions = [
    {"code": "IN", "name": "India", "region": "Domestic", "is_active": True},
    {"code": "US", "name": "United States", "region": "North America", "is_active": True},
    {"code": "EU", "name": "European Union", "region": "Europe", "is_active": True},
    {"code": "WIPO", "name": "International Treaties", "region": "Global", "is_active": True},
    {"code": "UK", "name": "United Kingdom", "region": "Europe", "is_active": True},
    {"code": "JP", "name": "Japan", "region": "Asia-Pacific", "is_active": True}
]

legal_instruments = [
    {"code": "IN_PATENTS_ACT_1970", "name": "The Patents Act, 1970", "jurisdiction_code": "IN", "instrument_type": "Act", "official_publisher": "CGPDTM, DPIIT"},
    {"code": "IN_PATENTS_RULES_2003", "name": "The Patents Rules, 2003", "jurisdiction_code": "IN", "instrument_type": "Rule", "official_publisher": "CGPDTM"},
    {"code": "IN_BD_ACT_2002_2023", "name": "Biological Diversity Act, 2002/2023", "jurisdiction_code": "IN", "instrument_type": "Act", "official_publisher": "NBA & MoEFCC"},
    {"code": "IN_BD_NTC_2023", "name": "Section 40 Normally Traded Commodities Notification", "jurisdiction_code": "IN", "instrument_type": "Notification", "official_publisher": "MoEFCC Gazette"},
    {"code": "IN_AYUSH_API_MONOGRAPHS", "name": "Ayurvedic Pharmacopoeia of India", "jurisdiction_code": "IN", "instrument_type": "Pharmacopoeia", "official_publisher": "PCIM&H / Ministry of AYUSH"},
    {"code": "IN_DRUGS_COSMETICS_ACT_1940", "name": "The Drugs and Cosmetics Act, 1940", "jurisdiction_code": "IN", "instrument_type": "Act", "official_publisher": "Ministry of AYUSH & CDSCO"},
    {"code": "IN_AYURVEDA_AAHAR_2022", "name": "FSSAI (Ayurveda Aahar) Regulations, 2022", "jurisdiction_code": "IN", "instrument_type": "Regulation", "official_publisher": "FSSAI & Ministry of AYUSH"},
    {"code": "INTL_WIPO_GRATK_2024", "name": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge", "jurisdiction_code": "WIPO", "instrument_type": "Treaty", "official_publisher": "WIPO"}
]

with open("data/reference/jurisdictions.jsonl", "w", encoding="utf-8") as f:
    for j in jurisdictions:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")

with open("data/reference/legal_instruments.jsonl", "w", encoding="utf-8") as f:
    for li in legal_instruments:
        f.write(json.dumps(li, ensure_ascii=False) + "\n")

print("Exported knowledge graph, play scenarios, jurisdictions, and legal instruments to data/ directories.")
