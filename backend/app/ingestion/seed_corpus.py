"""
backend/app/ingestion/seed_corpus.py — Thin loader for authoritative legal corpus (Milestone M11)
Loads canonical data files from data/corpus/*.jsonl, data/knowledge_graph/, and data/play/ without inline literals.
"""

import os
from sqlalchemy.orm import Session
from scripts.ingest_corpus import run_ingestion

def ingest_large_scale_corpus(session: Session = None, corpus_version_tag: str = "v1.0"):
    """
    Thin loader delegating to the production ingestion pipeline.
    """
    print("Executing thin corpus loader from data/corpus/*.jsonl...")
    run_ingestion(source_filter="all", corpus_version_tag=corpus_version_tag, resume=True)

if __name__ == "__main__":
    ingest_large_scale_corpus()
