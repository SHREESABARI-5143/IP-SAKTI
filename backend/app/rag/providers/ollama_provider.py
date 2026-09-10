import re
import logging
import httpx
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.rag.providers.base import BaseLLMProvider
from backend.app.rag.providers.deterministic_provider import DeterministicGroundedProvider

logger = logging.getLogger(__name__)

class OllamaProvider(BaseLLMProvider):
    """
    Local Ollama Provider for offline open-source model inference (e.g. Llama 3.1 8B, Qwen 2.5 7B).
    Features:
    - Persistent HTTP connection pooling (limits & keep-alive)
    - Fast 1.5s connection probe for instantaneous deterministic fallback
    - Strict Evidence-First System Directives with provision boundary preservation
    - Zero cloud dependency & zero API key requirement
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None
    ):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or getattr(settings, "OLLAMA_MODEL", None) or settings.DEFAULT_MODEL
        self.timeout = float(timeout or getattr(settings, "OLLAMA_TIMEOUT_SECONDS", 30.0))
        # Connection pool with keep-alive
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            limits = httpx.Limits(max_keepalive_connections=10, max_connections=20, keepalive_expiry=300.0)
            timeout_cfg = httpx.Timeout(self.timeout, connect=1.5)
            self._client = httpx.AsyncClient(limits=limits, timeout=timeout_cfg)
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def generate_answer(
        self,
        query: str,
        retrieved_sources: List[Dict[str, Any]],
        jurisdiction: str = "India",
        detected_domain: str = "General",
        language: str = "en",
        product_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # 1. Safe Abstention if no sources retrieved
        if not retrieved_sources:
            return {
                "short_answer": "I could not verify this requirement in authoritative sources.",
                "full_answer": "### Safe Abstention Notice\n\nNo matching authoritative statutes in knowledge registry.",
                "is_abstained": True,
                "abstention_reason": "INSUFFICIENT_EVIDENCE",
                "provider": "ollama",
                "model": self.model
            }

        # 2. Generic provision check: if query requests a specific provision that is absent from evidence, safely abstain
        from backend.app.rag.intent_classifier import query_intent_classifier
        intent_info = query_intent_classifier.classify(query)
        target_provisions = intent_info.get("target_provisions", [])
        if target_provisions and intent_info.get("requires_exact_lookup", False):
            has_match = any(
                query_intent_classifier.match_provision_keys(t, s.get("provision_ref", ""), s.get("section_title", ""), s.get("content", "") or s.get("source_text", ""))
                for s in retrieved_sources
                for t in target_provisions
            )
            if not has_match:
                missing_str = ", ".join(target_provisions)
                return {
                    "short_answer": f"I could not locate {missing_str} in the authoritative statutory registry for {jurisdiction}.",
                    "full_answer": (
                        f"### Safe Abstention Notice — Unverified / Non-Existent Statutory Provision\n\n"
                        f"I could not locate the referenced provision ({missing_str}) in the authoritative legislation, so I cannot attribute a legal rule to it.\n\n"
                        f"**Verification Steps:**\n"
                        f"1. Confirm the provision number against official gazetted statutory texts.\n"
                        f"2. Browse the **Sources Registry** to inspect verified sections of the active Acts."
                    ),
                    "is_abstained": True,
                    "abstention_reason": "PROVISION_NOT_FOUND",
                    "provider": "ollama (safeguard)",
                    "model": self.model
                }

        sources_context = "\n\n".join([
            f"[{idx+1}] {s.get('source_title', 'Statutory Source')} ({s.get('authority', 'Official Authority')})\n"
            f"Provision: {s.get('section_title', '')} ({s.get('provision_ref', '')})\n"
            f"Legal Domain: {s.get('legal_domain', s.get('domain', 'General'))}\n"
            f"Text: {s.get('source_text') or s.get('content', '')}"
            for idx, s in enumerate(retrieved_sources)
        ])

        system_prompt = (
            "You are IP-SAKTI Sahayak, an authoritative, strictly source-grounded Legal RAG system.\n\n"
            "MANDATORY EVIDENCE-FIRST & SCOPE DIRECTIVES:\n"
            "1. Answer ONLY from the supplied authoritative sources. Never use pretrained model memory to fill gaps.\n"
            "2. Answer ONLY the specific question asked. Do NOT broaden the question into unsolicited advice, checklists, or classification.\n"
            "3. If the user asks whether a specific legal requirement (e.g. synergistic efficacy) is required and the evidence does not establish it, state clearly that it is not established in the authoritative Act.\n"
            "4. Preserve exact provision boundaries. Do not merge or conflate distinct provisions.\n"
            "5. Include inline citations [1], [2] matching the sources used.\n"
            "6. Output format:\n"
            "   ### Short Answer\n"
            "   <Concise direct answer with citation>\n\n"
            "   ### Applicable Provisions\n"
            "   <Directly relevant provisions only>\n\n"
            "   ### Legal Analysis\n"
            "   <Grounded statutory explanation>\n"
        )

        user_prompt = (
            f"JURISDICTION: {jurisdiction}\n"
            f"DOMAIN: {detected_domain}\n"
            f"USER QUERY: {query}\n\n"
            f"AUTHORITATIVE SOURCES:\n{sources_context}\n\n"
            f"GROUNDED ANSWER:"
        )

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{user_prompt}",
            "stream": False,
            "keep_alive": "5m",
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 1024
            }
        }

        client = self._get_client()
        try:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data.get("response", "").strip()
                if not text:
                    raise RuntimeError(f"Ollama returned empty response for model '{self.model}'")
                
                lines = [l.strip() for l in text.split("\n") if l.strip() and not l.strip().startswith("#")]
                short_ans = lines[0] if lines else "Legal analysis derived from verified sources."
                
                if "[1]" not in short_ans and retrieved_sources:
                    short_ans = f"{short_ans} [1]"

                return {
                    "short_answer": short_ans,
                    "full_answer": text,
                    "is_abstained": False,
                    "abstention_reason": None,
                    "provider": "ollama",
                    "model": self.model
                }
            else:
                raise RuntimeError(f"Ollama server at {self.base_url} returned HTTP {resp.status_code}: {resp.text}")
        except httpx.ConnectError as exc:
            logger.warning(f"Ollama connection error at {self.base_url}: {exc}")
            raise RuntimeError(f"Ollama connection failed: Unable to reach {self.base_url}") from exc
        except httpx.TimeoutException as exc:
            logger.warning(f"Ollama request timed out after {self.timeout}s: {exc}")
            raise RuntimeError(f"Ollama request timed out after {self.timeout}s") from exc
        except Exception as exc:
            logger.warning(f"Ollama invocation error: {exc}")
            raise
