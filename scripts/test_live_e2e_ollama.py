import asyncio
import json
import logging
from backend.app.core.config import settings
from backend.app.core.database import SyncSessionLocal, Base, sync_engine
from backend.app.ingestion.live_ingest import live_ingestion
from backend.app.rag.retriever import retriever
from backend.app.agents.orchestrator import orchestrator
from backend.app.rag.providers.router import llm_router

logging.basicConfig(level=logging.INFO)

QUERIES_TO_TEST = [
    "What does Section 3(p) of the Patents Act exclude?",
    "What is Section 25(1)(k) concerned with?",
    "What is the difference between Section 25(1)(j) and 25(1)(k)?",
    "Are Ayurvedic formulations automatically excluded from patent protection?",
    "Does Section 25(1)(k) require synergistic efficacy?",
    "What does Section 10(4)(d)(ii) concern?",
    "What happens if the source of biological material is not properly disclosed?",
    "What does Section 999(z) of the Patents Act provide?"
]

async def main():
    print("=" * 70)
    print("IP-SAKTI SAHAYAK — LIVE END-TO-END OLLAMA & RAG VERIFICATION")
    print("=" * 70)
    
    provider_info = llm_router.get_active_provider_info()
    print(f"Active Provider Configuration: {json.dumps(provider_info, indent=2)}")
    
    # Ensure DB is seeded and retriever loaded
    Base.metadata.create_all(bind=sync_engine)
    session = SyncSessionLocal()
    live_ingestion.ingest_all_authoritative_sources(session=session)
    session.close()
    retriever.reload_from_db()
    
    for i, q in enumerate(QUERIES_TO_TEST, 1):
        print("\n" + "-" * 70)
        print(f"[{i}/{len(QUERIES_TO_TEST)}] QUERY: {q}")
        print("-" * 70)
        
        response = await orchestrator.process_chat_query(query=q, jurisdiction="India")
        
        print(f"DOMAIN          : {response.detected_domain}")
        print(f"CONFIDENCE      : {response.confidence.score} ({response.confidence.level})")
        print(f"IS ABSTAINED    : {response.is_abstained}")
        if response.is_abstained:
            print(f"ABSTENTION REASON: {response.abstention_reason}")
        print(f"SHORT ANSWER    : {response.short_answer}")
        print(f"VERIFIED CITATIONS ({len(response.citations)}):")
        for c in response.citations:
            print(f"  - [{c.citation_number}] {c.source_title} | {c.provision_ref} | Status: {c.verification_status}")
        print(f"FULL ANSWER (First 300 chars):")
        print(response.full_answer[:300] + ("..." if len(response.full_answer) > 300 else ""))

if __name__ == "__main__":
    asyncio.run(main())
