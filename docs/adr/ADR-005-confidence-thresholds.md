# ADR-005: Harmonization of Confidence, Escalation, and Abstention Thresholds

## Status
Accepted

## Context
Prior iterations of the codebase had divergent thresholds across different modules and documentation slides for when the multi-agent legal pipeline should escalate to a certified human IP facilitator vs when it should safely abstain. In some places, 0.55 was treated as abstention while in others 0.65 was the threshold.

For high-stakes Ayurvedic regulatory and patent compliance under Section 3(p) and NBA Section 6, the system requires clear, mathematical criteria to prevent hallucination while providing actionable guidance when sufficient statutory evidence exists.

## Decision
We harmonize all confidence calculations onto a single source of truth defined in `backend/app/core/config.py` as typed Pydantic Settings with environment variable overrides:

1. **High Confidence (`>= 0.80`)**:
   - The query is completely answered by retrieved primary legislation with high jurisdictional match and >= 80% claim-level token overlap grounding.
   - Result: Display answer with full citation breakdown.

2. **Medium Confidence / Escalation Eligible (`>= settings.CONFIDENCE_ESCALATE_THRESHOLD`, default: `0.55`)**:
   - Relevant statutory provisions exist (e.g. patent eligibility principles or NTC trade exemptions), but specific proprietary formulation factors (such as synergy proving data or specific process variations) require attorney review.
   - Result: Display answer with highlighted escalation button ("Consult Certified Facilitator").

3. **Low Confidence / Safe Abstention (`< settings.CONFIDENCE_ABSTAIN_THRESHOLD`, default: `0.65` when no specific match is found, or `< 0.35` aggregate score)**:
   - When no verified primary source is retrieved or when a queried statutory section does not exist in the gazetted legal registry.
   - Result: Safe abstention notice explaining exact missing provisions and preventing fabricated legal claims.

## Consequences
- Single unified source of truth across all providers (`deterministic`, `ollama`, `vllm`).
- All slide decks and user documentation are aligned with `CONFIDENCE_ABSTAIN_THRESHOLD = 0.65` and `CONFIDENCE_ESCALATE_THRESHOLD = 0.55`.
