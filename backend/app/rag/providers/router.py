import os
import logging
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.rag.providers.base import BaseLLMProvider
from backend.app.rag.providers.ollama_provider import OllamaProvider
from backend.app.rag.providers.vllm_provider import VLLMProvider
from backend.app.rag.providers.deterministic_provider import DeterministicGroundedProvider

logger = logging.getLogger(__name__)

class LLMRouter:
    """
    LLM Provider Router for IP-SAKTI Sahayak.
    
    Coordinates provider selection with dynamic execution paths:
    - FAST_PATH: Instant Deterministic Grounded Synthesis (0 LLM calls, <50ms latency)
    - STANDARD_PATH: Single LLM call (Ollama / vLLM) with automatic offline fallback
    - DEEP_PATH: Comprehensive synthesis with strict claim grounding
    """

    def __init__(self):
        self.ollama_provider = OllamaProvider()
        self.vllm_provider = VLLMProvider()
        self.deterministic_provider = DeterministicGroundedProvider()
        logger.info(
            f"LLMRouter initialized with primary provider: '{settings.LLM_PROVIDER}', "
            f"Ollama model: '{getattr(settings, 'OLLAMA_MODEL', settings.DEFAULT_MODEL)}' at '{settings.OLLAMA_BASE_URL}'"
        )

    def get_active_provider_info(self) -> Dict[str, Any]:
        """Returns diagnostic metadata about the currently configured provider."""
        provider_name = settings.LLM_PROVIDER.lower()
        return {
            "provider": provider_name,
            "ollama_model": getattr(settings, "OLLAMA_MODEL", settings.DEFAULT_MODEL),
            "ollama_base_url": settings.OLLAMA_BASE_URL,
            "deterministic_available": True,
            "offline_mode": provider_name == "deterministic"
        }

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
        """
        Routes the generation request according to the execution path and configured provider.
        """
        provider_name = settings.LLM_PROVIDER.lower()

        # Check for FAST_PATH: use high-confidence deterministic synthesis directly (0 LLM calls)
        has_direct_evidence = any(s.get("evidence_type") == "DIRECT" or s.get("exact_provision_match") for s in retrieved_sources)
        if execution_path == "FAST_PATH" and (has_direct_evidence or provider_name == "deterministic"):
            logger.info("LLMRouter: FAST_PATH triggered — generating direct deterministic answer (0 LLM calls)")
            res = await self.deterministic_provider.generate_answer(
                query=query,
                retrieved_sources=retrieved_sources,
                jurisdiction=jurisdiction,
                detected_domain=detected_domain,
                language=language,
                product_context=product_context
            )
            res["provider_used"] = "deterministic (fast-path)"
            res["llm_calls_count"] = 0
            return res

        # If configured for Ollama, try Ollama first
        if provider_name == "ollama":
            try:
                logger.info(
                    f"LLMRouter: Routing generation to Ollama (model={self.ollama_provider.model}, "
                    f"base_url={self.ollama_provider.base_url})"
                )
                res = await self.ollama_provider.generate_answer(
                    query=query,
                    retrieved_sources=retrieved_sources,
                    jurisdiction=jurisdiction,
                    detected_domain=detected_domain,
                    language=language,
                    product_context=product_context
                )
                res["provider_used"] = "ollama"
                res["llm_calls_count"] = 1
                return res
            except Exception as exc:
                logger.warning(
                    f"LLMRouter: Ollama generation failed ({type(exc).__name__}: {exc}). "
                    f"Falling back safely to Deterministic Grounded Synthesizer."
                )
                fallback_res = await self.deterministic_provider.generate_answer(
                    query=query,
                    retrieved_sources=retrieved_sources,
                    jurisdiction=jurisdiction,
                    detected_domain=detected_domain,
                    language=language,
                    product_context=product_context
                )
                fallback_res["provider_used"] = "deterministic (fallback from ollama)"
                fallback_res["fallback_reason"] = str(exc)
                fallback_res["llm_calls_count"] = 0
                return fallback_res

        # If configured for vLLM, try vLLM first
        elif provider_name == "vllm":
            try:
                logger.info(f"LLMRouter: Routing generation to vLLM ({self.vllm_provider.base_url})")
                res = await self.vllm_provider.generate_answer(
                    query=query,
                    retrieved_sources=retrieved_sources,
                    jurisdiction=jurisdiction,
                    detected_domain=detected_domain,
                    language=language,
                    product_context=product_context
                )
                res["provider_used"] = "vllm"
                res["llm_calls_count"] = 1
                return res
            except Exception as exc:
                logger.warning(
                    f"LLMRouter: vLLM generation failed ({type(exc).__name__}: {exc}). "
                    f"Falling back safely to Deterministic Grounded Synthesizer."
                )
                fallback_res = await self.deterministic_provider.generate_answer(
                    query=query,
                    retrieved_sources=retrieved_sources,
                    jurisdiction=jurisdiction,
                    detected_domain=detected_domain,
                    language=language,
                    product_context=product_context
                )
                fallback_res["provider_used"] = "deterministic (fallback from vllm)"
                fallback_res["fallback_reason"] = str(exc)
                fallback_res["llm_calls_count"] = 0
                return fallback_res

        # Default & Zero-API Primary: Deterministic Grounded Synthesizer
        logger.info("LLMRouter: Routing generation to Deterministic Grounded Synthesizer (zero-API mode)")
        res = await self.deterministic_provider.generate_answer(
            query=query,
            retrieved_sources=retrieved_sources,
            jurisdiction=jurisdiction,
            detected_domain=detected_domain,
            language=language,
            product_context=product_context
        )
        res["provider_used"] = "deterministic"
        res["llm_calls_count"] = 0
        return res

llm_router = LLMRouter()
