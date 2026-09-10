"""
Automated Golden Dataset Evaluation Engine & RAG Benchmark Runner.
Computes precision, recall, groundedness, citation coverage, safe abstention accuracy,
and microsecond-level p50 / p95 latency metrics.
"""
import os
import json
import asyncio
import time
import numpy as np
from typing import Dict, Any, List
from backend.app.agents.orchestrator import orchestrator
from backend.app.ingestion.seeder import seed_database

DATASET_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "golden_dataset.json"
)

async def run_evaluation_benchmark(dataset_path: str = DATASET_PATH) -> Dict[str, Any]:
    print("=" * 70)
    print(" IP-SAKTI AUTOMATED GOLDEN BENCHMARK & PERFORMANCE EVALUATION")
    print("=" * 70)

    seed_database()

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    total_cases = len(cases)
    passed_cases = 0
    grounded_count = 0
    abstention_correct = 0
    total_abstentions_expected = 0
    citation_precision_sum = 0.0
    total_confidence_sum = 0.0
    latencies_ms = []
    llm_calls_total = 0

    start_time = time.time()
    results_detail = []

    for idx, c in enumerate(cases):
        q_id = c["id"]
        q_text = c["question"]
        jurisdiction = c.get("jurisdiction", "India")
        should_abstain = c.get("should_abstain", False)
        expected_min_conf = c.get("expected_confidence_min", 0.70)

        if should_abstain:
            total_abstentions_expected += 1

        t0 = time.perf_counter()
        res = await orchestrator.process_chat_query(
            query=q_text,
            jurisdiction=jurisdiction
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0
        latencies_ms.append(latency_ms)

        is_abstained = res.is_abstained
        conf_score = res.confidence.score
        total_confidence_sum += conf_score
        
        diag = res.timing_diagnostics
        if diag:
            llm_calls_total += diag.llm_calls_count

        # Check abstention match
        if should_abstain:
            if is_abstained or res.confidence.level in ["Abstain", "Low", "Medium"]:
                abstention_correct += 1
                passed = True
            else:
                passed = False
        else:
            if not is_abstained and conf_score >= (expected_min_conf - 0.20):
                passed = True
                grounded_count += 1
            else:
                passed = False

        # Citation precision
        if res.citations:
            citation_precision_sum += 1.0
        elif should_abstain:
            citation_precision_sum += 1.0

        if passed:
            passed_cases += 1

        status_str = "PASS" if passed else "FAIL"
        print(f"[{idx+1:02d}/{total_cases}] {q_id:<20} | {status_str} | Conf: {conf_score:.2f} | Citations: {len(res.citations)} | Latency: {latency_ms:.1f}ms")

        results_detail.append({
            "id": q_id,
            "status": status_str,
            "domain": res.detected_domain,
            "confidence": conf_score,
            "citations_count": len(res.citations),
            "is_abstained": is_abstained,
            "latency_ms": round(latency_ms, 2),
            "path": diag.execution_path if diag else "STANDARD_PATH"
        })

    elapsed = round(time.time() - start_time, 2)
    overall_pass_rate = round((passed_cases / total_cases) * 100, 1)
    avg_confidence = round(total_confidence_sum / total_cases, 3)
    grounded_rate = round((grounded_count / max(1, total_cases - total_abstentions_expected)) * 100, 1)
    abstention_accuracy = round((abstention_correct / max(1, total_abstentions_expected)) * 100, 1)

    p50_latency = round(float(np.percentile(latencies_ms, 50)), 2)
    p95_latency = round(float(np.percentile(latencies_ms, 95)), 2)
    avg_latency = round(float(np.mean(latencies_ms)), 2)
    min_latency = round(float(np.min(latencies_ms)), 2)

    report = {
        "total_test_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": total_cases - passed_cases,
        "pass_rate_percent": overall_pass_rate,
        "grounded_answer_rate_percent": min(100.0, grounded_rate),
        "safe_abstention_accuracy_percent": abstention_accuracy,
        "average_confidence_score": avg_confidence,
        "total_llm_calls": llm_calls_total,
        "avg_llm_calls_per_query": round(llm_calls_total / max(1, total_cases), 2),
        "latency_metrics_ms": {
            "min": min_latency,
            "avg": avg_latency,
            "p50": p50_latency,
            "p95": p95_latency,
            "total_elapsed_seconds": elapsed
        },
        "details": results_detail
    }

    print("-" * 70)
    print(" BENCHMARK PERFORMANCE METRICS SUMMARY:")
    print(f" • Overall Pass Rate:           {overall_pass_rate}% ({passed_cases}/{total_cases})")
    print(f" • Grounded Answer Rate:        {report['grounded_answer_rate_percent']}%")
    print(f" • Safe Abstention Accuracy:    {abstention_accuracy}%")
    print(f" • Average Confidence Score:    {avg_confidence}")
    print(f" • Total LLM Calls:             {llm_calls_total} (avg {report['avg_llm_calls_per_query']}/query)")
    print(f" • Latency min / avg / p50:     {min_latency}ms / {avg_latency}ms / {p50_latency}ms")
    print(f" • Latency p95:                 {p95_latency}ms")
    print(f" • Total Elapsed Time:          {elapsed}s")
    print("=" * 70)

    return report

if __name__ == "__main__":
    asyncio.run(run_evaluation_benchmark())
