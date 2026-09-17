"""
backend/app/knowledge_graph/engine.py — Dynamic Relational Knowledge Graph Engine (Milestone M11)
Queries nodes and edges from database tables (KnowledgeEntity, KnowledgeRelationship) with in-memory caching.
"""

from typing import List, Dict, Any, Optional
import json
import time
from backend.app.core.database import SyncSessionLocal
from backend.app.models.knowledge_graph import KnowledgeEntity, KnowledgeRelationship

class KnowledgeGraphEngine:
    """
    Relational multi-hop Knowledge Graph for IP & AYUSH Regulations.
    Traverses herbs, biological resources, statutory exclusions, regulatory pathways, and international treaties.
    """

    def __init__(self, cache_ttl_seconds: int = 300):
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.relationships: List[Dict[str, Any]] = []
        self._cache_ttl = cache_ttl_seconds
        self._last_loaded_time = 0.0
        self.reload()

    def reload(self):
        """Loads entities and relationships directly from the database."""
        session = SyncSessionLocal()
        try:
            db_entities = session.query(KnowledgeEntity).all()
            db_rels = session.query(KnowledgeRelationship).all()

            self.entities = {}
            for ent in db_entities:
                self.entities[ent.entity_id] = {
                    "id": ent.entity_id,
                    "db_id": ent.id,
                    "name": ent.name,
                    "type": ent.entity_type,
                    "jurisdiction": ent.jurisdiction,
                    "description": ent.description
                }

            self.relationships = []
            for rel in db_rels:
                src = session.query(KnowledgeEntity).filter(KnowledgeEntity.id == rel.source_entity_id).first()
                tgt = session.query(KnowledgeEntity).filter(KnowledgeEntity.id == rel.target_entity_id).first()
                if src and tgt:
                    self.relationships.append({
                        "source": src.entity_id,
                        "target": tgt.entity_id,
                        "rel": rel.relationship_type,
                        "weight": rel.weight
                    })

            self._last_loaded_time = time.time()
        finally:
            session.close()

    def _ensure_fresh(self):
        if time.time() - self._last_loaded_time > self._cache_ttl:
            self.reload()

    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        self._ensure_fresh()
        return self.entities.get(entity_id)

    def find_neighbors(self, entity_id: str, rel_type: Optional[str] = None) -> List[Dict[str, Any]]:
        self._ensure_fresh()
        neighbors = []
        for edge in self.relationships:
            if edge["source"] == entity_id:
                if rel_type is None or edge["rel"] == rel_type:
                    target_ent = self.entities.get(edge["target"])
                    if target_ent:
                        neighbors.append({
                            "direction": "outgoing",
                            "relationship": edge["rel"],
                            "weight": edge["weight"],
                            "entity": target_ent
                        })
            elif edge["target"] == entity_id:
                if rel_type is None or edge["rel"] == rel_type:
                    source_ent = self.entities.get(edge["source"])
                    if source_ent:
                        neighbors.append({
                            "direction": "incoming",
                            "relationship": edge["rel"],
                            "weight": edge["weight"],
                            "entity": source_ent
                        })
        return neighbors

    def multi_hop_search(self, start_entity_id: str, max_depth: int = 2) -> Dict[str, Any]:
        self._ensure_fresh()
        visited = set()
        nodes = []
        links = []

        def traverse(current_id: str, depth: int):
            if depth > max_depth or current_id in visited:
                return
            visited.add(current_id)

            curr_node = self.entities.get(current_id)
            if curr_node:
                nodes.append(curr_node)

            for edge in self.relationships:
                if edge["source"] == current_id:
                    links.append(edge)
                    traverse(edge["target"], depth + 1)
                elif edge["target"] == current_id:
                    links.append(edge)
                    traverse(edge["source"], depth + 1)

        traverse(start_entity_id, 0)
        return {"nodes": nodes, "links": links}

    def get_multi_hop_subgraph(self, keywords: List[str], max_hops: int = 2) -> List[Dict[str, Any]]:
        self._ensure_fresh()
        results = []
        matched_eids = set()
        for kw in keywords:
            if not kw:
                continue
            kw_low = str(kw).lower()
            for eid, ent in self.entities.items():
                if kw_low in ent["name"].lower() or kw_low in ent["type"].lower():
                    matched_eids.add(eid)

        for eid in matched_eids:
            neighbors = self.find_neighbors(eid)
            for n in neighbors:
                results.append({
                    "source_entity": self.entities[eid]["name"],
                    "relationship": n["relationship"],
                    "target_entity": n["entity"]["name"],
                    "target_type": n["entity"]["type"],
                    "jurisdiction": n["entity"].get("jurisdiction", "India")
                })
        return results

    def analyze_ingredient_ip_risk(self, ingredient_name: str) -> Dict[str, Any]:
        """Analyzes statutory and biological IP risk for a given Ayurvedic herb or ingredient."""
        self._ensure_fresh()
        matched_id = None
        for eid, ent in self.entities.items():
            if ingredient_name.lower() in ent["name"].lower():
                matched_id = eid
                break

        if not matched_id:
            return {
                "matched": False,
                "ingredient": ingredient_name,
                "risk_factors": ["No statutory knowledge graph entity match found in local registry."]
            }

        neighbors = self.find_neighbors(matched_id)
        risks = []
        statutory_citations = []

        for n in neighbors:
            rel = n["relationship"]
            ent = n["entity"]
            if rel == "EXCLUDED_UNDER_3P":
                risks.append(f"Statutory bar under Section 3(p) of Patents Act 1970 for {ent['name']}")
                statutory_citations.append("Section 3(p), Patents Act 1970")
            elif rel == "REQUIRES_NBA_APPROVAL":
                risks.append(f"Mandatory National Biodiversity Authority approval under Section 6 of Biological Diversity Act")
                statutory_citations.append("Section 6, Biological Diversity Act 2002/2023")
            elif rel == "EXEMPT_UNDER_NTC":
                risks.append(f"Exempted from commercial trade benefit sharing under Section 40 NTC notification")
                statutory_citations.append("Section 40 Normally Traded Commodities Notification")

        return {
            "matched": True,
            "entity": self.entities[matched_id],
            "risk_factors": risks,
            "statutory_citations": list(set(statutory_citations))
        }

kg_engine = KnowledgeGraphEngine()
knowledge_graph = kg_engine
