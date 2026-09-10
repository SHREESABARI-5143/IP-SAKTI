#!/usr/bin/env bash
set -e

echo "=== IP-SAKTI Sahayak Smoke Test Suite ==="

echo "1. Checking Python environment and dependencies..."
python -c "import fastapi, uvicorn, sqlalchemy, rank_bm25; print('Python dependencies verified.')"

echo "2. Running seeder and live ingestion..."
python backend/app/ingestion/seeder.py

echo "3. Executing automated test suite..."
python -m pytest backend/tests/test_live_ingestion_and_citations.py backend/tests/smoke_test.py backend/tests/test_all_17_journeys.py -v

echo "4. Running Golden Dataset Benchmark..."
python scripts/run_benchmarks.py

echo "=== Smoke Test Complete: All Systems Operational ==="
