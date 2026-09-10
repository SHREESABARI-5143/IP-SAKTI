import pytest
import httpx
from unittest.mock import AsyncMock, patch
from backend.app.core.config import settings
from backend.app.rag.providers.ollama_provider import OllamaProvider
from backend.app.rag.providers.deterministic_provider import DeterministicGroundedProvider
from backend.app.rag.providers.router import LLMRouter
from backend.app.rag.citation_verifier import citation_verifier
from backend.app.rag.retriever import retriever

SAMPLE_SOURCES = [
    {
        "source_id": "src-patents-1970",
        "source_title": "The Patents Act, 1970",
        "authority": "Intellectual Property India (CGPDTM)",
        "provision_ref": "Section 3(p)",
        "section_title": "Section 3(p) — Traditional Knowledge Exclusion",
        "legal_domain": "Patent",
        "jurisdiction": "India",
        "source_text": (
            "Section 3. What are not inventions.—The following are not inventions within the meaning of this Act,—\n"
            "(p) an invention which in effect, is traditional knowledge or which is an aggregation or duplication "
            "of known properties of traditionally known component or components."
        )
    }
]

@pytest.mark.asyncio
async def test_ollama_provider_configuration():
    """Verify Ollama provider initializes with configured model and URL."""
    provider = OllamaProvider()
    assert "11434" in provider.base_url
    assert provider.model in ["llama3.1:latest", "llama3.1"]
    assert provider.timeout >= 15.0

@pytest.mark.asyncio
async def test_ollama_fake_provision_abstention():
    """Verify Ollama provider detects non-existent / fake sections and safely abstains."""
    provider = OllamaProvider()
    res = await provider.generate_answer(
        query="What does Section 999(z) of the Patents Act provide?",
        retrieved_sources=SAMPLE_SOURCES,
        jurisdiction="India"
    )
    assert res["is_abstained"] is True
    assert res["abstention_reason"] == "PROVISION_NOT_FOUND"

@pytest.mark.asyncio
async def test_router_deterministic_mode():
    """Verify router delegates directly to deterministic provider when LLM_PROVIDER=deterministic."""
    router = LLMRouter()
    with patch.object(settings, "LLM_PROVIDER", "deterministic"):
        res = await router.generate_grounded_answer(
            query="What does Section 3(p) of the Patents Act exclude?",
            retrieved_sources=SAMPLE_SOURCES,
            jurisdiction="India"
        )
        assert res["is_abstained"] is False
        assert "Section 3(p)" in res["full_answer"]
        assert res.get("provider_used") == "deterministic"

@pytest.mark.asyncio
async def test_router_ollama_connection_failure_fallback():
    """Verify router catches connection failure to Ollama and falls back to deterministic provider."""
    router = LLMRouter()
    # Point Ollama to an unreachable port
    router.ollama_provider.base_url = "http://localhost:59999"
    
    with patch.object(settings, "LLM_PROVIDER", "ollama"):
        res = await router.generate_grounded_answer(
            query="What does Section 3(p) of the Patents Act exclude?",
            retrieved_sources=SAMPLE_SOURCES,
            jurisdiction="India"
        )
        assert res["is_abstained"] is False
        assert "Section 3(p)" in res["full_answer"]
        assert "deterministic (fallback" in res.get("provider_used", "")

@pytest.mark.asyncio
async def test_router_ollama_timeout_fallback():
    """Verify router catches timeout and falls back to deterministic provider."""
    router = LLMRouter()
    
    async def mock_timeout(*args, **kwargs):
        raise httpx.TimeoutException("Mocked timeout")

    with patch.object(router.ollama_provider, "generate_answer", side_effect=mock_timeout):
        with patch.object(settings, "LLM_PROVIDER", "ollama"):
            res = await router.generate_grounded_answer(
                query="What does Section 3(p) of the Patents Act exclude?",
                retrieved_sources=SAMPLE_SOURCES,
                jurisdiction="India"
            )
            assert res["is_abstained"] is False
            assert "Section 3(p)" in res["full_answer"]
            assert "fallback" in res.get("provider_used", "")

@pytest.mark.asyncio
async def test_router_ollama_empty_response_fallback():
    """Verify router handles empty response from Ollama and falls back to deterministic provider."""
    router = LLMRouter()

    async def mock_empty(*args, **kwargs):
        raise RuntimeError("Ollama returned empty response")

    with patch.object(router.ollama_provider, "generate_answer", side_effect=mock_empty):
        with patch.object(settings, "LLM_PROVIDER", "ollama"):
            res = await router.generate_grounded_answer(
                query="What does Section 3(p) of the Patents Act exclude?",
                retrieved_sources=SAMPLE_SOURCES,
                jurisdiction="India"
            )
            assert res["is_abstained"] is False
            assert "fallback" in res.get("provider_used", "")

@pytest.mark.asyncio
async def test_citation_verification_on_generated_output():
    """Verify citation verification runs and validates citations on synthesized text."""
    synthesized_text = (
        "### Short Answer\n"
        "Section 3(p) excludes traditional knowledge from patentability. [1]\n\n"
        "### Applicable Provisions\n"
        "- Section 3(p) — The Patents Act, 1970 [1]\n"
    )
    sanitized, citations, unsupported, grounding_rate = citation_verifier.verify_and_format_citations(
        raw_text=synthesized_text,
        retrieved_sources=SAMPLE_SOURCES
    )
    assert len(citations) >= 1
    assert citations[0].provision_ref == "Section 3(p)"
    assert citations[0].verification_status == "verified"
    assert unsupported == 0
    assert grounding_rate > 0.8

@pytest.mark.asyncio
async def test_live_ollama_generation_and_grounding():
    """Verify live Ollama invocation against local llama3.1 if Ollama is running."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            ping = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if ping.status_code != 200:
                pytest.skip("Local Ollama service is not responding")
    except Exception:
        pytest.skip("Local Ollama service is not reachable")

    provider = OllamaProvider(model="llama3.1:latest")
    res = await provider.generate_answer(
        query="What does Section 3(p) of the Patents Act exclude?",
        retrieved_sources=SAMPLE_SOURCES,
        jurisdiction="India"
    )
    assert res["is_abstained"] is False
    assert len(res["full_answer"]) > 20
    assert "Section 3(p)" in res["full_answer"] or "traditional knowledge" in res["full_answer"].lower()

    sanitized, citations, unsupported, grounding_rate = citation_verifier.verify_and_format_citations(
        raw_text=res["full_answer"],
        retrieved_sources=SAMPLE_SOURCES
    )
    assert len(citations) >= 1
    assert any(c.verification_status == "verified" for c in citations)


