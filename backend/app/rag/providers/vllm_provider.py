import httpx
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.rag.providers.base import BaseLLMProvider

class VLLMProvider(BaseLLMProvider):
    """
    Local vLLM / OpenAI-compatible endpoint provider for high-throughput local inference.
    """

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or getattr(settings, "VLLM_BASE_URL", "http://localhost:8000/v1")).rstrip("/")
        self.model = model or settings.DEFAULT_MODEL

    async def generate_answer(
        self,
        query: str,
        retrieved_sources: List[Dict[str, Any]],
        jurisdiction: str = "India",
        detected_domain: str = "General",
        language: str = "en",
        product_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not retrieved_sources:
            return {
                "short_answer": "I could not verify this requirement in authoritative sources.",
                "full_answer": "### Safe Abstention Notice\n\nNo matching authoritative statutes in knowledge registry.",
                "is_abstained": True,
                "abstention_reason": "No matching authoritative statutes in knowledge registry."
            }

        sources_context = "\n\n".join([
            f"[{idx+1}] {s['source_title']} ({s['authority']})\n"
            f"Provision: {s.get('section_title', '')} ({s.get('provision_ref', '')})\n"
            f"Text: {s.get('source_text') or s.get('content')}"
            for idx, s in enumerate(retrieved_sources)
        ])

        system_prompt = (
            "You are IP-SAKTI Sahayak, an authoritative, source-grounded Legal RAG system for Indian & International IP law.\n"
            "Use inline citations [1], [2]. Base all statements strictly on retrieved excerpts."
        )

        user_prompt = f"USER QUERY: {query}\n\nAUTHORITATIVE SOURCES:\n{sources_context}"

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"].strip()
                lines = [l.strip() for l in text.split("\n") if l.strip() and not l.strip().startswith("#")]
                short_ans = lines[0] if lines else "Legal analysis derived from verified sources."
                return {
                    "short_answer": short_ans,
                    "full_answer": text,
                    "is_abstained": False,
                    "abstention_reason": None
                }
            else:
                raise RuntimeError(f"vLLM server returned HTTP {resp.status_code}")
