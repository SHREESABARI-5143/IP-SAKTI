#!/usr/bin/env python
import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.evaluation.run_eval import run_evaluation_benchmark

if __name__ == "__main__":
    report = asyncio.run(run_evaluation_benchmark())
    if report["pass_rate_percent"] >= 80.0:
        print("\nCI/CD Quality Gate: PASSED")
        sys.exit(0)
    else:
        print("\nCI/CD Quality Gate: FAILED (Pass rate below 80%)")
        sys.exit(1)
