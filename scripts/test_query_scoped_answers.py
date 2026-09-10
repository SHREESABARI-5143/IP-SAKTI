import asyncio
import json
from backend.app.core.database import SyncSessionLocal, Base, sync_engine
from backend.app.ingestion.live_ingest import live_ingestion
from backend.app.rag.retriever import retriever
from backend.app.agents.orchestrator import orchestrator

TEST_QUESTIONS = [
    ("A. Section 3(p) Lookup", "What does Section 3(p) of the Patents Act provide?"),
    ("B. Synergistic Efficacy Premise", "Which section of the Patents Act states that inventions lacking synergistic efficacy are excluded from patent protection?"),
    ("C. Provision Comparison", "What is the difference between Section 25(1)(j) and Section 25(1)(k)?"),
    ("D. Section 10(4)(d)(ii) Lookup", "What does Section 10(4)(d)(ii) concern?"),
    ("E. Automatic Exclusion Premise", "Are Ayurvedic formulations automatically excluded from patent protection?"),
    ("F. Multi-Provision Request", "Give me all Indian legal provisions relevant to patenting Ayurvedic formulations.")
]

async def run_tests():
    Base.metadata.create_all(bind=sync_engine)
    session = SyncSessionLocal()
    live_ingestion.ingest_all_authoritative_sources(session=session)
    session.close()
    retriever.reload_from_db()

    print("=" * 80)
    print("QUERY-SCOPED ANSWERING EVALUATION")
    print("=" * 80)

    for label, q in TEST_QUESTIONS:
        print(f"\n>>> [{label}]")
        print(f"QUERY: {q}")
        res = await orchestrator.process_chat_query(query=q, jurisdiction="India")
        print(f"DOMAIN      : {res.detected_domain}")
        print(f"CONFIDENCE  : {res.confidence.score} ({res.confidence.level})")
        print(f"CITATIONS ({len(res.citations)}): {[c.provision_ref for c in res.citations]}")
        print(f"NEXT STEPS  : {res.recommended_next_steps}")
        print(f"SHORT ANSWER: {res.short_answer}")
        print("FULL ANSWER :")
        print(res.full_answer)
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(run_tests())
