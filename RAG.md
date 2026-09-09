# HYBRID RAG & RETRIEVAL PIPELINE — IP-SAKTI SAHAYAK

## Retrieval Pipeline Overview

```text
User Query
   ↓
Language Detection (EN / HI / TA)
   ↓
Semantic Normalization to Canonical Concepts
   ↓
Domain & Intent Classification (Patent / ABS / Regulatory / Export / TM)
   ↓
Knowledge Graph Context Expansion
   ↓
Hybrid Multi-Stage Retrieval:
   - BM25 Lexical Keyword Matching
   - Vector Embedding Similarity
   - Strict Metadata Pre-Filtering (Jurisdiction, Domain, Namespace)
   - Source Authority Hierarchy Weighting
   ↓
Context Assembly & Prompt Grounding Contract
   ↓
LLM Synthesis (Gemini / OpenAI / Grounded Engine)
   ↓
Post-Generation Citation Verifier
   ↓
Algorithmic Confidence & Abstention Evaluation
   ↓
Grounded Response with Clickable Primary Citations
```

---

## 1. Hybrid Retrieval Scoring Formula

The retrieval score for each statutory chunk combines lexical matching, jurisdiction alignment, authority hierarchy, and domain relevance:

$$\text{Final Score} = (\text{BM25}_{\text{norm}} \times 0.45) + (\text{Jurisdiction Match} \times 0.30) + (\text{Authority Rank} \times 0.15) + (\text{Domain Match} \times 0.10)$$

Where:
- **Authority Rank**: Primary Government Acts receive a multiplier of $1.0$, Official Rules $0.95$, International Treaties $0.90$, Guidelines $0.85$.
- **Jurisdiction Match**: When `India` is selected, foreign statutes (e.g. US FDA) are strictly down-weighted. When `International` is selected with target country `USA`, US FDA DSHEA regulations are prioritized.

---

## 2. Citation Verification & Validation

After response synthesis, the `CitationVerifier` parses inline citations (e.g. `[1]`, `[2]`):
1. Verifies that cited indices exist in the retrieved chunk list.
2. Checks that the quoted provision matches the retrieved source title and authority.
3. If an ungrounded claim is detected, it penalizes the citation grounding score and flags the answer.

---

## 3. Algorithmic Confidence Computation

Confidence is calculated objectively based on 5 parameters:
- **Source Authority Score**: Hierarchy level of retrieved sources.
- **Retrieval Relevance Score**: Semantic and BM25 density.
- **Jurisdiction Match Score**: Exact jurisdictional alignment.
- **Source Freshness Score**: Validity of source version.
- **Citation Grounding Score**: Proportion of supported claims.

Thresholds:
- $\ge 80\% \rightarrow \textbf{High Confidence}$
- $55\% - 79\% \rightarrow \textbf{Medium Confidence}$
- $35\% - 54\% \rightarrow \textbf{Low Confidence}$
- $< 35\% \rightarrow \textbf{Abstain}$
