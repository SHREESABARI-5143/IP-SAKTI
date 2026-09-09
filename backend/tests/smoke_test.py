import asyncio
import pytest
from backend.app.ingestion.seeder import seed_database
from backend.app.rag.retriever import retriever
from backend.app.agents.classification_agent import classification_agent
from backend.app.schemas.classification import ClassificationInput
from backend.app.agents.abs_agent import abs_agent
from backend.app.schemas.abs import ABSAssessmentInput
from backend.app.agents.ip_agent import ip_strategy_agent
from backend.app.schemas.ip_strategy import IPStrategyInput
from backend.app.agents.orchestrator import orchestrator

def test_full_pipeline():
    # 1. Test Seeder
    seed_database()

    # 2. Test Retrieval
    query = "patent turmeric and ashwagandha traditional knowledge Section 3(p)"
    results = retriever.search(query=query, jurisdiction="India", domain_filter="Patent")
    assert len(results) > 0
    print(f"PASS: Hybrid Retrieval found {len(results)} chunks. Top provision: {results[0]['provision_ref']}")

    # 3. Test Formulation Classification
    cr = classification_agent.classify(
        ClassificationInput(
            product_name="Triphala Churna",
            ingredients=["Haritaki", "Bibhitaki", "Amalaki"],
            has_classical_text_reference=True,
            classical_text_name="Charaka Samhita",
            intended_use_or_claims="Digestive therapeutic tonic",
            dosage_form="Churna"
        )
    )
    assert cr.likely_category == "Classical Ayurvedic Medicine"
    print(f"PASS: Classification -> {cr.likely_category}")

    # 4. Test ABS Assessment
    abs_res = abs_agent.assess(
        ABSAssessmentInput(
            product_name="Ashwagandha Gold Extract",
            biological_resources=["Ashwagandha (Withania somnifera)"],
            sourcing_location="India",
            user_entity_type="Indian Entity",
            is_seeking_ipr=True
        )
    )
    assert abs_res.nba_approval_required is True
    print(f"PASS: ABS Assessment -> NBA Required: {abs_res.nba_approval_required}, Risk: {abs_res.risk_level}")

    # 5. Test IP Strategy Matrix
    ip_res = ip_strategy_agent.evaluate(
        IPStrategyInput(
            product_name="AyurShield Tablet",
            product_description="Proprietary extract formula",
            ingredients=["Curcuma longa", "Withania somnifera"],
            is_classical_formulation=False,
            novel_extraction_or_synergy=True
        )
    )
    assert len(ip_res.routes) >= 5
    print(f"PASS: IP Strategy Matrix generated {len(ip_res.routes)} IP routes")

@pytest.mark.asyncio
async def test_orchestrator_chat():
    res = await orchestrator.process_chat_query(
        query="Can I patent my new Ayurvedic formulation with turmeric?",
        jurisdiction="India"
    )
    assert res.confidence.score >= 0.70
    assert len(res.citations) > 0
    print(f"PASS: Orchestrator -> Domain: {res.detected_domain}, Confidence: {res.confidence.level} ({res.confidence.score}), Citations: {len(res.citations)}")

if __name__ == "__main__":
    test_full_pipeline()
    asyncio.run(test_orchestrator_chat())
    print("ALL BACKEND TESTS PASSED SUCCESSFULLY!")
