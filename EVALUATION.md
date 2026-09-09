# AI EVALUATION & BENCHMARKING SUITE — IP-SAKTI SAHAYAK

The platform includes an automated regression benchmark evaluator against a curated **Golden Dataset** (`backend/app/evaluation/golden_dataset.json`).

---

## Evaluation Metrics

1. **Groundedness Score ($\ge 90\%$)**: Ratio of factual legal claims supported by verified retrieved chunks.
2. **Citation Completeness ($100\%$)**: Verifies that every statutory claim includes a valid reference to an official act, rule, or treaty.
3. **Retrieval Recall@3 ($\ge 95\%$)**: Measures whether the correct primary act appears in the top 3 retrieved chunks.
4. **MRR (Mean Reciprocal Rank)**: Quality of top-ranked provisions.
5. **Abstention Accuracy**: Ensures the model cleanly abstains when presented with out-of-scope, ungrounded, or adversarial jailbreak inputs.

---

## Running Benchmarks

### Via API Endpoint:
```bash
curl -X POST http://localhost:8000/api/v1/evaluation/run-benchmark
```

### Via Admin Console:
Navigate to `/admin` in the web application and click **"Run Golden Benchmark"**.
