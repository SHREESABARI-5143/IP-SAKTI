#!/usr/bin/env python3
"""
scripts/audit_corpus.py — Corpus Quality Gate for Milestone M11

Requirements:
- 100% of records have a non-null, syntactically valid source_uri and sha256.
- Zero duplicate sha256.
- Zero records with empty or under-50-character body text.
- Jurisdiction distribution reported; Indian sovereign layer must be majority.
- Language distribution reported.
- Random sample of 25 records dumped to docs/corpus-sample.md with URI, title, and first 200 characters.
"""

import os
import sys
import json
import random
from urllib.parse import urlparse
from collections import Counter

from backend.app.core.database import SyncSessionLocal
from backend.app.models.source import Document, DocumentChunk
from backend.app.models.ingestion import CorpusVersion

def audit_corpus(sample_output_path: str = "docs/corpus-sample.md"):
    session = SyncSessionLocal()
    
    documents = session.query(Document).all()
    total_docs = len(documents)
    print(f"\n{'='*50}\nSTARTING CORPUS AUDIT ({total_docs} records)\n{'='*50}")

    if total_docs < 2000:
        print(f"FAILED: Corpus size {total_docs} is less than required minimum of 2000 records.")
        sys.exit(1)

    errors = []
    seen_shas = set()
    jurisdictions = Counter()
    languages = Counter()
    instrument_types = Counter()

    for doc in documents:
        # Check source_uri
        if not doc.source_uri:
            errors.append(f"Record {doc.id} ({doc.title}) has NULL source_uri.")
        else:
            parsed = urlparse(doc.source_uri)
            if not parsed.scheme or not parsed.netloc:
                errors.append(f"Record {doc.id} has invalid source_uri: {doc.source_uri}")

        # Check sha256
        if not doc.sha256 or len(doc.sha256) != 64:
            errors.append(f"Record {doc.id} has invalid sha256: {doc.sha256}")
        elif doc.sha256 in seen_shas:
            errors.append(f"Duplicate sha256 detected: {doc.sha256} on Record {doc.id}")
        seen_shas.add(doc.sha256)

        # Check text length via linked chunk
        chunk = session.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).first()
        content = chunk.content if chunk else ""
        if len(content.strip()) < 50:
            errors.append(f"Record {doc.id} ({doc.title}) has text length < 50 characters ({len(content)} chars).")

        jurisdictions[doc.jurisdiction] += 1
        languages[doc.language] += 1
        instrument_types[doc.instrument_type] += 1

    # Invariant: Indian sovereign layer must be majority
    india_count = jurisdictions.get("India", 0)
    india_pct = (india_count / max(1, total_docs)) * 100
    if india_pct < 50.0:
        errors.append(f"Indian sovereign records ({india_count}, {india_pct:.1f}%) do not constitute the majority.")

    # Random sample of 25 records
    sample_records = random.sample(documents, min(25, total_docs))
    sample_md = "# Corpus Sample Audit (25 Random Records)\n\n"
    sample_md += "| # | Title | Sovereign Source URI | Instrument Type | Jurisdiction | Preview (First 200 chars) |\n"
    sample_md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"

    for idx, doc in enumerate(sample_records, 1):
        chunk = session.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).first()
        preview = (chunk.content[:200] if chunk else "").replace("\n", " ").replace("|", "\\|")
        sample_md += f"| {idx} | **{doc.title}** | `{doc.source_uri}` | {doc.instrument_type} | {doc.jurisdiction} | {preview}... |\n"

    os.makedirs(os.path.dirname(sample_output_path), exist_ok=True)
    with open(sample_output_path, "w", encoding="utf-8") as f:
        f.write(sample_md)

    print("\n--- JURISDICTION BREAKDOWN ---")
    for jur, cnt in jurisdictions.items():
        print(f"  {jur}: {cnt} records ({cnt/total_docs*100:.1f}%)")

    print("\n--- LANGUAGE BREAKDOWN ---")
    for lang, cnt in languages.items():
        print(f"  {lang}: {cnt} records ({cnt/total_docs*100:.1f}%)")

    print("\n--- INSTRUMENT TYPES ---")
    for itype, cnt in instrument_types.items():
        print(f"  {itype}: {cnt} records")

    session.close()

    if errors:
        print(f"\nFAILED: Found {len(errors)} corpus quality errors:")
        for err in errors[:20]:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"\nPASSED: 100% Corpus Quality Gate passed successfully across all {total_docs} records.")
        print(f"25-record spot check dumped to {sample_output_path}")
        sys.exit(0)

if __name__ == "__main__":
    audit_corpus()
