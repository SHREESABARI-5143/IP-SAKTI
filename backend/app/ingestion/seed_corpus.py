"""
Dynamic Statutory Corpus Loader for IP-SAKTI Sahayak
Loads verified statutory provisions dynamically from external structured dataset files.
"""
import os
import json

DATASET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "corpora", "statutory_corpus.json"
)

def get_authoritative_sources():
    """Dynamically loads authoritative statutory sources from external JSON corpus dataset."""
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Dynamic property / fallback
AUTHORITATIVE_SOURCES = get_authoritative_sources()
