from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMProvider(ABC):
    """
    Abstract Base Class for pluggable LLM Providers in IP-SAKTI Sahayak.
    Ensures provider abstraction across Ollama, vLLM, and Deterministic Synthesizers.
    """

    @abstractmethod
    async def generate_answer(
        self,
        query: str,
        retrieved_sources: List[Dict[str, Any]],
        jurisdiction: str = "India",
        detected_domain: str = "General",
        language: str = "en",
        product_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates a grounded legal answer response dictionary:
        {
            "short_answer": str,
            "full_answer": str,
            "is_abstained": bool,
            "abstention_reason": Optional[str]
        }
        """
        pass
