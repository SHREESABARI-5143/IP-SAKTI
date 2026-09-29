"""
Graph Service — In-memory Knowledge Graph for IP-SAKTI Sahayak.

Builds a directed graph of statutory provisions from the local corpus,
with typed edges representing legal relationships:
  - AMENDS: A later provision that modifies an earlier one.
  - REPEALED_BY: A provision made defunct by a later enactment.
  - CROSS_REFERENCES: Sections that cite or depend on each other.
  - SUPPLEMENTS: International treaties underpinning domestic law.
  - IMPLEMENTS: Domestic rules that implement a parent Act.

Used by the QA Validity Checker to resolve temporal supersession
and assemble deterministic, citation-grounded context.
"""

import os
import json
from typing import List, Dict, Any, Optional, Set, Tuple


class GraphNode:
    """Represents a single statutory provision in the knowledge graph."""

    __slots__ = (
        "chunk_id", "title", "section_or_article", "statute",
        "jurisdiction", "doc_type", "effective_date", "url",
        "text", "tags", "edges", "metadata"
    )

    def __init__(self, chunk_data: Dict[str, Any]):
        self.chunk_id: str = chunk_data.get("chunk_id", "")
        self.title: str = chunk_data.get("title", "")
        self.section_or_article: str = chunk_data.get("section_or_article", "")
        self.statute: str = chunk_data.get("statute", "")
        self.jurisdiction: str = chunk_data.get("jurisdiction", "")
        self.doc_type: str = chunk_data.get("doc_type", "")
        self.effective_date: str = chunk_data.get("effective_date", "")
        self.url: str = chunk_data.get("url", "")
        self.text: str = chunk_data.get("text", "")
        self.tags: List[str] = chunk_data.get("tags", [])
        self.edges: List[Dict[str, str]] = []
        # Preserve any extra fields (e.g. ingredients, formulation_name)
        self.metadata: Dict[str, Any] = {
            k: v for k, v in chunk_data.items()
            if k not in {
                "chunk_id", "title", "section_or_article", "statute",
                "jurisdiction", "doc_type", "effective_date", "url",
                "text", "tags"
            }
        }

    def add_edge(self, edge_type: str, target_id: str, label: str = ""):
        """Add a directed edge from this node to another node."""
        self.edges.append({
            "type": edge_type,
            "target": target_id,
            "label": label
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "title": self.title,
            "section_or_article": self.section_or_article,
            "statute": self.statute,
            "jurisdiction": self.jurisdiction,
            "doc_type": self.doc_type,
            "effective_date": self.effective_date,
            "text": self.text,
            "tags": self.tags,
            "edges": self.edges
        }


# ─────────────────────────────────────────────────────────
# Static edge definitions derived from statutory relationships.
# Each tuple: (source_chunk_id, edge_type, target_chunk_id, label)
# These encode the legal cross-references inherent in the corpus.
# ─────────────────────────────────────────────────────────
STATUTORY_EDGES: List[Tuple[str, str, str, str]] = [
    # Patents Act internal cross-references
    ("in-patent-sec3-p", "CROSS_REFERENCES", "in-patent-sec25",
     "Section 3(p) inventions are grounds for pre-grant opposition under Section 25(1)(f)"),
    ("in-patent-sec3-p", "CROSS_REFERENCES", "in-patent-sec64-1-p",
     "Section 3(p) violations are grounds for revocation under Section 64(1)(p)"),
    ("in-patent-sec3-d", "CROSS_REFERENCES", "in-patent-sec3-e",
     "Known substance (3d) and mere admixture (3e) are co-assessed for Ayurvedic formulations"),
    ("in-patent-sec3-e", "CROSS_REFERENCES", "in-patent-sec3-p",
     "Mere admixture (3e) and traditional knowledge (3p) are co-bars for classical herb combinations"),
    ("in-patent-sec10-4", "CROSS_REFERENCES", "in-patent-sec25",
     "Non-disclosure of bio-material source (10(4)) is ground for opposition under 25(1)(j)"),
    ("in-patent-sec10-4", "CROSS_REFERENCES", "in-patent-sec64-1-p",
     "Non-disclosure of bio-material source is ground for revocation under 64(1)(p)"),
    ("in-patent-sec2-1-j", "CROSS_REFERENCES", "in-patent-sec3-a",
     "Definition of invention (2(1)(j)) is qualified by non-patentable exclusions under Section 3"),

    # Patents Act <-> Biological Diversity Act cross-references
    ("in-patent-sec10-4", "CROSS_REFERENCES", "in-bda-sec6",
     "Patent applications on Indian bio-resources require NBA approval under BDA Section 6"),
    ("in-bda-sec6", "CROSS_REFERENCES", "in-patent-sec10-4",
     "NBA IPR approval requirement links to patent disclosure obligations under Patents Act 10(4)"),
    ("in-bda-sec3", "CROSS_REFERENCES", "in-bda-sec55",
     "Contravention of Section 3 (foreign access) triggers penalties under Section 55"),
    ("in-bda-sec6", "CROSS_REFERENCES", "in-bda-sec55",
     "Contravention of Section 6 (IPR without NBA) triggers penalties under Section 55"),
    ("in-bda-sec6", "CROSS_REFERENCES", "in-bda-sec21",
     "NBA approval under Section 6 is linked to benefit sharing under Section 21"),

    # Drugs & Cosmetics Act internal cross-references
    ("in-dca-sec3-a", "CROSS_REFERENCES", "in-dca-first-schedule",
     "Classical ASU drug definition (3(a)) depends on authoritative texts listed in First Schedule"),
    ("in-dca-sec3-h", "CROSS_REFERENCES", "in-dca-first-schedule",
     "P&P medicine definition (3(h)) references ingredients from First Schedule texts"),
    ("in-dca-sec3-h", "CROSS_REFERENCES", "in-dca-rule-158-b",
     "P&P medicines require licensing under Rule 158-B categories"),
    ("in-dca-sec3-a", "CROSS_REFERENCES", "in-dca-rule-158-b",
     "Classical drugs are Category 1 under Rule 158-B licensing"),

    # Drugs & Cosmetics Act <-> Patents Act cross-references
    ("in-dca-sec3-a", "CROSS_REFERENCES", "in-patent-sec3-p",
     "Classical ASU drugs documented in First Schedule texts are barred from patenting under 3(p)"),
    ("in-dca-rule-158-b", "CROSS_REFERENCES", "in-patent-sec3-d",
     "Rule 158-B Category 2(C) extracts must overcome Section 3(d) efficacy enhancement bar"),

    # International treaty implementations
    ("in-bda-sec3", "IMPLEMENTS", "intl-nagoya-art6",
     "BDA Section 3 implements Nagoya Protocol Article 6 PIC requirements domestically"),
    ("in-bda-sec6", "IMPLEMENTS", "intl-nagoya-art5",
     "BDA Section 6 implements Nagoya Protocol Article 5 benefit sharing for IPR"),
    ("in-bda-sec21", "IMPLEMENTS", "intl-nagoya-art5",
     "BDA Section 21 implements Nagoya Article 5 equitable benefit sharing"),
    ("in-patent-sec3-p", "IMPLEMENTS", "intl-nagoya-art7",
     "Section 3(p) TK protection aligns with Nagoya Article 7 on TK access safeguards"),

    # International treaty cross-references
    ("intl-nagoya-art5", "CROSS_REFERENCES", "intl-nagoya-art6",
     "Benefit sharing (Art 5) requires prior informed consent (Art 6)"),
    ("intl-nagoya-art6", "CROSS_REFERENCES", "intl-nagoya-art7",
     "PIC for genetic resources (Art 6) extends to traditional knowledge (Art 7)"),
    ("intl-nagoya-art7", "CROSS_REFERENCES", "intl-nagoya-art15-16",
     "TK access safeguards (Art 7) enforced by compliance mechanisms (Arts 15-16)"),

    # Amendment tracking
    ("in-patent-sec3-p", "AMENDS", "in-patent-sec2-1-j",
     "Patents (Amendment) Act 2002 added Section 3(p) qualifying the definition of invention"),
    ("in-patent-sec3-d", "AMENDS", "in-patent-sec2-1-j",
     "Patents (Amendment) Act 2005 refined Section 3(d) enhanced efficacy requirement"),
    ("in-bda-sec2-c", "AMENDS", "in-bda-sec7",
     "BDA Amendment 2023 exempted registered AYUSH practitioners from SBB intimation"),
    ("in-bda-sec55", "AMENDS", "in-bda-sec55",
     "BDA Amendment 2023 changed criminal penalties to civil penalties with fines up to Rs 50 lakhs"),
]


class GraphService:
    """
    In-memory Knowledge Graph built from statutory corpus JSON files.
    Provides traversal, cross-reference resolution, and temporal
    supersession checking for the QA pipeline.
    """

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.backend_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.corpus_dir = os.path.join(self.backend_dir, "corpus", "processed")
        self._build_graph()

    def _build_graph(self):
        """Load all corpus chunks as nodes and wire up edges."""
        # 1. Load all chunks as nodes
        for juri in ["india", "international"]:
            juri_dir = os.path.join(self.corpus_dir, juri)
            if not os.path.exists(juri_dir):
                continue
            for fname in os.listdir(juri_dir):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(juri_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        items = data if isinstance(data, list) else [data]
                        for item in items:
                            chunk_id = item.get("chunk_id", "")
                            if chunk_id:
                                self.nodes[chunk_id] = GraphNode(item)
                except Exception as e:
                    print(f"[GraphService] Error reading {fpath}: {e}")

        # 2. Wire up statutory edges
        for src_id, edge_type, tgt_id, label in STATUTORY_EDGES:
            if src_id in self.nodes and tgt_id in self.nodes:
                self.nodes[src_id].add_edge(edge_type, tgt_id, label)

        node_count = len(self.nodes)
        edge_count = sum(len(n.edges) for n in self.nodes.values())
        print(f"[GraphService] Built knowledge graph: {node_count} nodes, {edge_count} edges.")

    def get_node(self, chunk_id: str) -> Optional[GraphNode]:
        """Get a node by its chunk_id."""
        return self.nodes.get(chunk_id)

    def get_edges(self, chunk_id: str, edge_type: Optional[str] = None) -> List[Dict[str, str]]:
        """Get all edges from a node, optionally filtered by type."""
        node = self.nodes.get(chunk_id)
        if not node:
            return []
        if edge_type:
            return [e for e in node.edges if e["type"] == edge_type]
        return node.edges

    def traverse_cross_references(
        self, chunk_ids: List[str], max_depth: int = 2
    ) -> List[GraphNode]:
        """
        BFS traversal from seed chunk IDs following CROSS_REFERENCES edges.
        Returns additional nodes discovered up to max_depth hops.
        """
        visited: Set[str] = set(chunk_ids)
        discovered: List[GraphNode] = []
        frontier = list(chunk_ids)

        for depth in range(max_depth):
            next_frontier = []
            for cid in frontier:
                node = self.nodes.get(cid)
                if not node:
                    continue
                for edge in node.edges:
                    target_id = edge["target"]
                    if target_id not in visited and edge["type"] in (
                        "CROSS_REFERENCES", "IMPLEMENTS"
                    ):
                        visited.add(target_id)
                        target_node = self.nodes.get(target_id)
                        if target_node:
                            discovered.append(target_node)
                            next_frontier.append(target_id)
            frontier = next_frontier
            if not frontier:
                break

        return discovered

    def check_temporal_validity(self, chunk_ids: List[str]) -> List[Dict[str, Any]]:
        """
        For each provided chunk, check if it has been amended or repealed.
        Returns a list of validity annotations.
        """
        annotations = []
        for cid in chunk_ids:
            node = self.nodes.get(cid)
            if not node:
                continue

            # Check inbound AMENDS edges (other nodes that amend this one)
            amending_nodes = []
            repealing_nodes = []
            for other_id, other_node in self.nodes.items():
                for edge in other_node.edges:
                    if edge["target"] == cid:
                        if edge["type"] == "AMENDS":
                            amending_nodes.append({
                                "amending_chunk": other_id,
                                "amending_title": other_node.title,
                                "label": edge["label"]
                            })
                        elif edge["type"] == "REPEALED_BY":
                            repealing_nodes.append({
                                "repealing_chunk": other_id,
                                "repealing_title": other_node.title,
                                "label": edge["label"]
                            })

            # Check outbound AMENDS edges (this node amends another)
            outbound_amends = self.get_edges(cid, "AMENDS")

            status = "CURRENT"
            if repealing_nodes:
                status = "REPEALED"
            elif amending_nodes:
                status = "AMENDED"

            annotation = {
                "chunk_id": cid,
                "title": node.title,
                "effective_date": node.effective_date,
                "status": status,
                "amended_by": amending_nodes,
                "repealed_by": repealing_nodes,
                "amends_others": [
                    {"target": e["target"], "label": e["label"]}
                    for e in outbound_amends
                ]
            }
            annotations.append(annotation)

        return annotations

    def get_related_provisions(
        self, chunk_ids: List[str], jurisdiction: str = "india"
    ) -> Dict[str, Any]:
        """
        Given seed chunks from vector search, enriches context with:
        1. Cross-referenced provisions (1-2 hops)
        2. Temporal validity annotations
        3. International treaty linkages

        Returns a structured context payload for the QA Synthesis agent.
        """
        # 1. Traverse cross-references
        related_nodes = self.traverse_cross_references(chunk_ids, max_depth=2)

        # Filter by jurisdiction if needed
        if jurisdiction != "both":
            # Keep all — international linkages are always relevant for context
            pass

        # 2. Get temporal validity for all relevant chunks
        all_ids = list(chunk_ids) + [n.chunk_id for n in related_nodes]
        validity = self.check_temporal_validity(all_ids)

        # 3. Separate into categories
        cross_ref_context = []
        for node in related_nodes:
            cross_ref_context.append({
                "chunk_id": node.chunk_id,
                "title": node.title,
                "section_or_article": node.section_or_article,
                "statute": node.statute,
                "jurisdiction": node.jurisdiction,
                "text_excerpt": node.text[:500],
                "edge_labels": [
                    e["label"] for e in node.edges
                    if e["target"] in chunk_ids
                ]
            })

        return {
            "cross_references": cross_ref_context,
            "temporal_validity": validity,
            "graph_node_count": len(all_ids),
            "related_node_count": len(related_nodes)
        }

    def get_amendment_chain(self, chunk_id: str) -> List[Dict[str, Any]]:
        """
        Traces the amendment chain for a provision.
        Returns the full chain from original to latest amendment.
        """
        chain = []
        visited = set()
        current = chunk_id

        while current and current not in visited:
            visited.add(current)
            node = self.nodes.get(current)
            if not node:
                break

            chain.append({
                "chunk_id": node.chunk_id,
                "title": node.title,
                "effective_date": node.effective_date,
                "statute": node.statute
            })

            # Find what this node amends
            amends_edges = self.get_edges(current, "AMENDS")
            if amends_edges:
                current = amends_edges[0]["target"]
            else:
                break

        return chain


# Singleton instance
graph_service = GraphService()
