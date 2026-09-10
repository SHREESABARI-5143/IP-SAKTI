# ADR-002: Open-Source LLM Provider Architecture with Safe Deterministic Fallback

## Status
Accepted

## Context
Proprietary cloud LLM APIs (e.g., Google Gemini, OpenAI) introduce vendor lock-in, data sovereignty concerns for proprietary Ayurvedic formulations, and API rate limits. SIH 2026 mandates open-source LLM hosting (Ollama / vLLM) with deterministic legal fallback capabilities.

## Decision
We implement a pluggable `LLMProvider` interface prioritizing **local open-source models via Ollama (Qwen2.5 / Mistral / Llama 3)** backed by a **Dynamic Deterministic Legal Grounding Engine**.

## Consequences
- **Positive**: 100% data sovereignty on private formulation uploads, offline capability, zero cloud API fees.
- **Positive**: High-fidelity claim extraction and structured statutory analysis even under zero GPU availability.
- **Negative**: Requires local compute resources when running 7B+ quantization models.
