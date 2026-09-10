from typing import List, Dict, Any, Optional
from backend.app.rag.providers.router import llm_router

class LLMProvider:
    """
    Authoritative Legal RAG Synthesis Interface for IP-SAKTI Sahayak.
    Delegates to LLMRouter for multi-provider orchestration (Ollama, vLLM, Deterministic).
    """

    async def generate_grounded_answer(
        self,
        query: str,
        retrieved_sources: List[Dict[str, Any]],
        jurisdiction: str = "India",
        detected_domain: str = "General",
        language: str = "en",
        product_context: Optional[Dict[str, Any]] = None,
        execution_path: str = "STANDARD_PATH"
    ) -> Dict[str, Any]:
        return await llm_router.generate_grounded_answer(
            query=query,
            retrieved_sources=retrieved_sources,
            jurisdiction=jurisdiction,
            detected_domain=detected_domain,
            language=language,
            product_context=product_context,
            execution_path=execution_path
        )

llm_provider = LLMProvider()
