from typing import List, Dict, Any, Optional
import json

class KnowledgeGraphEngine:
    """
    In-memory and relational multi-hop Knowledge Graph for IP & AYUSH Regulations.
    Enables traversal from herbs to biological resources, statutory exclusions,
    regulatory pathways, and international treaty requirements.
    """

    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.relationships: List[Dict[str, Any]] = []
        self._initialize_graph()

    def _initialize_graph(self):
        # 1. Statutory & Regulatory Entities
        entities_data = [
            # Acts & Treaties
            {"id": "ACT_PATENTS_1970", "name": "Indian Patents Act, 1970", "type": "Law", "jurisdiction": "India"},
            {"id": "ACT_BD_2002_2023", "name": "Biological Diversity Act, 2002 & 2023", "type": "Law", "jurisdiction": "India"},
            {"id": "ACT_DRUGS_COSMETICS_1940", "name": "Drugs and Cosmetics Act, 1940 (Chapter IV-A)", "type": "Law", "jurisdiction": "India"},
            {"id": "REG_AYURVEDA_AAHAR_2022", "name": "FSSAI Ayurveda Aahar Regulations, 2022", "type": "Regulation", "jurisdiction": "India"},
            {"id": "TREATY_WIPO_GRATK", "name": "WIPO GRATK Treaty (2024)", "type": "Treaty", "jurisdiction": "International"},
            {"id": "TREATY_NAGOYA", "name": "Nagoya Protocol on ABS", "type": "Treaty", "jurisdiction": "International"},
            {"id": "REG_US_DSHEA", "name": "US FDA DSHEA (21 CFR 111)", "type": "Regulation", "jurisdiction": "USA"},
            {"id": "DIR_EU_THMPD", "name": "EU Traditional Herbal Directive (2004/24/EC)", "type": "Regulation", "jurisdiction": "EU"},

            # Sections & Rules
            {"id": "SEC_PATENT_3P", "name": "Section 3(p) [Traditional Knowledge Exclusion]", "type": "Section", "jurisdiction": "India"},
            {"id": "SEC_PATENT_3D", "name": "Section 3(d) [Efficacy Enhancement Requirement]", "type": "Section", "jurisdiction": "India"},
            {"id": "SEC_PATENT_10_4", "name": "Section 10(4)(d)(ii) [Source Disclosure]", "type": "Section", "jurisdiction": "India"},
            {"id": "SEC_BD_6", "name": "Section 6 [NBA Approval for IPR]", "type": "Section", "jurisdiction": "India"},
            {"id": "SEC_BD_7", "name": "Section 7 [SBB Prior Intimation]", "type": "Section", "jurisdiction": "India"},
            {"id": "RULE_158B", "name": "Rule 158B [Proof of Effectiveness for ASU Drugs]", "type": "Rule", "jurisdiction": "India"},

            # Authorities
            {"id": "AUTH_CGPDTM", "name": "Patent Office (CGPDTM / DPIIT)", "type": "Authority", "jurisdiction": "India"},
            {"id": "AUTH_NBA", "name": "National Biodiversity Authority (NBA)", "type": "Authority", "jurisdiction": "India"},
            {"id": "AUTH_AYUSH", "name": "Ministry of AYUSH / State Licensing Authorities", "type": "Authority", "jurisdiction": "India"},
            {"id": "AUTH_FSSAI", "name": "Food Safety and Standards Authority of India", "type": "Authority", "jurisdiction": "India"},
            {"id": "AUTH_USFDA", "name": "United States Food and Drug Administration", "type": "Authority", "jurisdiction": "USA"},

            # Key Ayurvedic Herbs / Biological Resources
            {"id": "HERB_ASHWAGANDHA", "name": "Ashwagandha (Withania somnifera)", "type": "BiologicalResource", "jurisdiction": "India"},
            {"id": "HERB_TURMERIC", "name": "Haridra / Turmeric (Curcuma longa)", "type": "BiologicalResource", "jurisdiction": "India"},
            {"id": "HERB_NEEM", "name": "Nimba / Neem (Azadirachta indica)", "type": "BiologicalResource", "jurisdiction": "India"},
            {"id": "HERB_BRAHMI", "name": "Brahmi (Bacopa monnieri)", "type": "BiologicalResource", "jurisdiction": "India"},
            {"id": "HERB_GUDUCHI", "name": "Guduchi / Giloy (Tinospora cordifolia)", "type": "BiologicalResource", "jurisdiction": "India"},
            {"id": "HERB_TULSI", "name": "Tulsi (Ocimum sanctum)", "type": "BiologicalResource", "jurisdiction": "India"}
        ]

        for ent in entities_data:
            self.entities[ent["id"]] = ent

        # 2. Relational Edges
        relations_data = [
            # Law -> Section
            {"source": "ACT_PATENTS_1970", "target": "SEC_PATENT_3P", "rel": "LAW_HAS_SECTION", "weight": 1.0},
            {"source": "ACT_PATENTS_1970", "target": "SEC_PATENT_3D", "rel": "LAW_HAS_SECTION", "weight": 1.0},
            {"source": "ACT_PATENTS_1970", "target": "SEC_PATENT_10_4", "rel": "LAW_HAS_SECTION", "weight": 1.0},
            {"source": "ACT_BD_2002_2023", "target": "SEC_BD_6", "rel": "LAW_HAS_SECTION", "weight": 1.0},
            {"source": "ACT_BD_2002_2023", "target": "SEC_BD_7", "rel": "LAW_HAS_SECTION", "weight": 1.0},
            {"source": "ACT_DRUGS_COSMETICS_1940", "target": "RULE_158B", "rel": "LAW_HAS_RULE", "weight": 1.0},

            # Authority -> Law
            {"source": "AUTH_CGPDTM", "target": "ACT_PATENTS_1970", "rel": "ADMINISTERS", "weight": 1.0},
            {"source": "AUTH_NBA", "target": "ACT_BD_2002_2023", "rel": "ADMINISTERS", "weight": 1.0},
            {"source": "AUTH_AYUSH", "target": "ACT_DRUGS_COSMETICS_1940", "rel": "ADMINISTERS", "weight": 1.0},
            {"source": "AUTH_FSSAI", "target": "REG_AYURVEDA_AAHAR_2022", "rel": "ADMINISTERS", "weight": 1.0},

            # Herb -> Biological Resource & Regulatory Links
            {"source": "HERB_ASHWAGANDHA", "target": "ACT_BD_2002_2023", "rel": "SUBJECT_TO_ABS", "weight": 0.95},
            {"source": "HERB_ASHWAGANDHA", "target": "SEC_PATENT_3P", "rel": "REQUIRES_TK_SCRUTINY", "weight": 0.95},
            {"source": "HERB_TURMERIC", "target": "ACT_BD_2002_2023", "rel": "SUBJECT_TO_ABS", "weight": 0.95},
            {"source": "HERB_TURMERIC", "target": "SEC_PATENT_3P", "rel": "REQUIRES_TK_SCRUTINY", "weight": 0.95},
            {"source": "HERB_NEEM", "target": "SEC_PATENT_3P", "rel": "REQUIRES_TK_SCRUTINY", "weight": 0.95},

            # Multi-hop Cross-statutory Linkages
            {"source": "SEC_PATENT_10_4", "target": "SEC_BD_6", "rel": "MANDATES_COMPLIANCE_WITH", "weight": 1.0},
            {"source": "SEC_BD_6", "target": "AUTH_NBA", "rel": "REQUIRES_APPROVAL_FROM", "weight": 1.0},
            {"source": "ACT_PATENTS_1970", "target": "TREATY_WIPO_GRATK", "rel": "ALIGNED_WITH_TREATY", "weight": 0.9}
        ]

        self.relationships.extend(relations_data)

    def find_entity_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        name_lower = name.lower()
        for ent in self.entities.values():
            if name_lower in ent["name"].lower() or name_lower in ent["id"].lower():
                return ent
        return None

    def get_multi_hop_subgraph(self, query_terms: List[str], max_hops: int = 2) -> Dict[str, Any]:
        """
        Extracts relevant subgraph connected to terms mentioned in the user query.
        """
        matched_node_ids = set()
        for term in query_terms:
            for ent_id, ent in self.entities.items():
                if term.lower() in ent["name"].lower():
                    matched_node_ids.add(ent_id)

        # Multi-hop expansion
        active_nodes = set(matched_node_ids)
        expanded_edges = []

        for _ in range(max_hops):
            new_nodes = set()
            for rel in self.relationships:
                if rel["source"] in active_nodes:
                    new_nodes.add(rel["target"])
                    expanded_edges.append(rel)
                elif rel["target"] in active_nodes:
                    new_nodes.add(rel["source"])
                    expanded_edges.append(rel)
            active_nodes.update(new_nodes)

        nodes = [self.entities[nid] for nid in active_nodes if nid in self.entities]
        return {
            "nodes": nodes,
            "edges": expanded_edges
        }

knowledge_graph = KnowledgeGraphEngine()
