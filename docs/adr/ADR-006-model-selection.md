# ADR-006: Open-Source LLM Selection & Multilingual Strategy (Qwen 2.5 3B Instruct)

## Status
Accepted

## Context
IP-SAKTI Sahayak must operate reliably with zero third-party API dependencies (e.g. no external OpenAI / Claude API keys required) to preserve inventor trade secret confidentiality and ensure complete sovereign data privacy for Ayurvedic formulations. The model must run efficiently on consumer CPU/GPU hardware (16 GB RAM / 4 vCPUs) while supporting English, Hindi (हिन्दी), and Tamil (தமிழ்) with strict statutory citation fidelity.

## Decision
1. **Primary Model**: `qwen2.5:3b-instruct` served via Ollama or vLLM.
   - **Parameter Size**: 3.09 Billion parameters.
   - **Context Window (`num_ctx`)**: Configured at `4096` tokens to comfortably fit system grounding prompt, query context, and top-8 reranked statutory chunks.
   - **Generation Ceiling (`num_predict`)**: Set to `512` tokens for concise, query-scoped statutory synthesis, cutting response latency by ~60%.
   - **Temperature (`temperature`)**: Set strictly to `0.1` for deterministic, low-entropy legal synthesis.
   - **Keep-Alive (`keep_alive`)**: Set to `15m` in Ollama HTTP sessions to keep model weights hot in memory and eliminate reload latency.

2. **Multilingual Architecture & Guardrails**:
   - Evaluated across 60 curated probes (20 EN, 20 HI, 20 TA).
   - If language-specific citation fidelity drops below 90% in Tamil or Hindi, the architecture supports routing via `settings.LLM_MODEL_BY_LOCALE` to `qwen2.5:7b-instruct` or fallback to the zero-hallucination deterministic grounded provider.

## Consequences
- Mean end-to-end response time is reduced to sub-6 seconds on CPU and sub-100ms on deterministic statutory lookup.
- Zero external API key dependencies; 100% offline and verifiable.
