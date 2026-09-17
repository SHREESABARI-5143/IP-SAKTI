#!/usr/bin/env python3
"""
scripts/ingest_corpus.py — Production Corpus Ingestion Pipeline (Milestone M11)

Requirements:
- Idempotent and resumable
- Deduplicates on sha256
- Populates documents (Records) and document_chunks with strict document_id foreign keys
- Records IngestionRun telemetry and updates CorpusVersion
"""

import os
import sys
import json
import uuid
import time
import argparse
import hashlib
from datetime import datetime, timezone

from backend.app.core.database import sync_engine, Base, SyncSessionLocal
from backend.app.models.source import SourceRegistry, Document, DocumentChunk
from backend.app.models.ingestion import IngestionRun, CorpusVersion
from backend.app.models.knowledge_graph import KnowledgeEntity, KnowledgeRelationship
from backend.app.models.play import PlayScenario
from backend.app.models.reference import Jurisdiction, LegalInstrument

def run_ingestion(source_filter: str = "all", corpus_version_tag: str = "v1.0", resume: bool = True):
    start_time = time.time()
    Base.metadata.create_all(bind=sync_engine)
    session = SyncSessionLocal()

    run_id = str(uuid.uuid4())
    ingestion_run = IngestionRun(
        id=run_id,
        started_at=datetime.now(timezone.utc),
        corpus_version=corpus_version_tag,
        embedding_model="BAAI/bge-m3",
        notes=f"Ingestion run for sources: {source_filter}, resume: {resume}"
    )
    session.add(ingestion_run)
    session.commit()

    records_attempted = 0
    records_ingested = 0
    records_skipped_dup = 0
    records_failed = 0
    chunks_created = 0

    corpus_dir = "data/corpus"
    if not os.path.exists(corpus_dir):
        print(f"Error: {corpus_dir} not found. Exiting.")
        return

    force = "--force" in sys.argv or "-f" in sys.argv
    if force:
        print("Force ingestion requested: resetting document chunks and documents...")
        session.query(DocumentChunk).delete()
        session.query(Document).delete()
        session.commit()

    # Existing SHA-256 set for deduplication
    existing_shas = set(r[0] for r in session.query(Document.sha256).filter(Document.sha256.isnot(None)).all())

    # 1. Ingest Reference Data
    if os.path.exists("data/reference/jurisdictions.jsonl"):
        with open("data/reference/jurisdictions.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                if not session.query(Jurisdiction).filter(Jurisdiction.code == item["code"]).first():
                    session.add(Jurisdiction(id=str(uuid.uuid4()), **item))
        session.commit()

    if os.path.exists("data/reference/legal_instruments.jsonl"):
        with open("data/reference/legal_instruments.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                if not session.query(LegalInstrument).filter(LegalInstrument.code == item["code"]).first():
                    session.add(LegalInstrument(id=str(uuid.uuid4()), **item))
        session.commit()

    # 2. Ingest Knowledge Graph
    if os.path.exists("data/knowledge_graph/nodes.jsonl"):
        with open("data/knowledge_graph/nodes.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                if not session.query(KnowledgeEntity).filter(KnowledgeEntity.entity_id == item["entity_id"]).first():
                    session.add(KnowledgeEntity(id=str(uuid.uuid4()), **item))
        session.commit()

    if os.path.exists("data/knowledge_graph/edges.jsonl"):
        with open("data/knowledge_graph/edges.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                # Resolve IDs
                src_ent = session.query(KnowledgeEntity).filter(KnowledgeEntity.entity_id == item["source_entity_id"]).first()
                tgt_ent = session.query(KnowledgeEntity).filter(KnowledgeEntity.entity_id == item["target_entity_id"]).first()
                if src_ent and tgt_ent:
                    existing_rel = session.query(KnowledgeRelationship).filter(
                        KnowledgeRelationship.source_entity_id == src_ent.id,
                        KnowledgeRelationship.target_entity_id == tgt_ent.id,
                        KnowledgeRelationship.relationship_type == item["relationship_type"]
                    ).first()
                    if not existing_rel:
                        session.add(KnowledgeRelationship(
                            id=str(uuid.uuid4()),
                            source_entity_id=src_ent.id,
                            target_entity_id=tgt_ent.id,
                            relationship_type=item["relationship_type"],
                            weight=item.get("weight", 1.0)
                        ))
        session.commit()

    # 3. Ingest Play Scenarios
    if os.path.exists("data/play/scenarios.jsonl"):
        with open("data/play/scenarios.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line.strip())
                if not session.query(PlayScenario).filter(PlayScenario.scenario_id == item["scenario_id"]).first():
                    session.add(PlayScenario(id=str(uuid.uuid4()), **item))
        session.commit()

    # 4. Ingest Corpus Records
    for fname in sorted(os.listdir(corpus_dir)):
        if not fname.endswith(".jsonl"):
            continue
        file_path = os.path.join(corpus_dir, fname)
        print(f"Ingesting corpus file: {file_path}...")

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                records_attempted += 1
                try:
                    data = json.loads(line.strip())
                    sha = data.get("sha256")
                    
                    if sha in existing_shas:
                        records_skipped_dup += 1
                        continue

                    # Create SourceRegistry entry if not exists
                    source_id = data.get("source_id", "GENERAL")
                    src_reg = session.query(SourceRegistry).filter(SourceRegistry.source_id == source_id).first()
                    if not src_reg:
                        src_reg = SourceRegistry(
                            id=str(uuid.uuid4()),
                            source_id=source_id,
                            name=data.get("title", source_id),
                            authority=data.get("authority", "Government of India"),
                            jurisdiction=data.get("jurisdiction", "India"),
                            domain=data.get("legal_domain", "Patent"),
                            legal_domain=data.get("legal_domain", "PATENT"),
                            source_type=data.get("instrument_type", "Act"),
                            verification_status="VERIFIED",
                            ingestion_status="INDEXED"
                        )
                        session.add(src_reg)
                        session.flush()

                    # Create canonical Document Record
                    doc_id = str(uuid.uuid4())
                    doc = Document(
                        id=doc_id,
                        title=data.get("title", "Statutory Provision"),
                        filename=fname,
                        file_type="statute",
                        namespace="PUBLIC_KNOWLEDGE",
                        jurisdiction=data.get("jurisdiction", "India"),
                        language=data.get("language", "en"),
                        instrument_type=data.get("instrument_type", "STATUTE"),
                        domain=data.get("legal_domain", "Patent"),
                        source_uri=data.get("source_uri"),
                        publisher=data.get("publisher"),
                        published_date=data.get("published_date"),
                        retrieved_at=datetime.now(timezone.utc),
                        sha256=sha,
                        ingest_status="indexed",
                        chunk_count=1,
                        corpus_version=corpus_version_tag,
                        status="indexed"
                    )
                    session.add(doc)
                    session.flush()

                    # Create DocumentChunk strictly bound to Document Record
                    chunk_id = str(uuid.uuid4())
                    chunk = DocumentChunk(
                        id=chunk_id,
                        source_id=src_reg.id,
                        document_id=doc.id,
                        chunk_index=0,
                        record_index=records_attempted,
                        section_title=data.get("section_title") or data.get("title"),
                        provision_ref=data.get("provision_ref"),
                        content=data.get("content"),
                        source_text=data.get("content"),
                        token_count=len(data.get("content", "").split()),
                        namespace="PUBLIC_KNOWLEDGE",
                        jurisdiction=data.get("jurisdiction", "India"),
                        domain=data.get("legal_domain", "Patent"),
                        legal_domain=data.get("legal_domain", "PATENT"),
                        document_type=data.get("instrument_type", "ACT"),
                        authority=data.get("authority", "Government of India"),
                        authority_score=data.get("authority_score", 1.0)
                    )
                    session.add(chunk)
                    chunks_created += 1
                    records_ingested += 1
                    existing_shas.add(sha)

                    if records_ingested % 250 == 0:
                        session.commit()
                        print(f"  Ingested {records_ingested} records...")

                except Exception as ex:
                    records_failed += 1
                    print(f"  Error ingesting record line: {ex}")

        session.commit()

    # Update IngestionRun
    ingestion_run.finished_at = datetime.now(timezone.utc)
    ingestion_run.records_attempted = records_attempted
    ingestion_run.records_ingested = records_ingested
    ingestion_run.records_skipped_duplicate = records_skipped_dup
    ingestion_run.records_failed = records_failed
    ingestion_run.chunks_created = chunks_created
    session.commit()

    # Update or create CorpusVersion
    corp_ver = session.query(CorpusVersion).filter(CorpusVersion.version == corpus_version_tag).first()
    total_active_records = session.query(Document).filter(Document.corpus_version == corpus_version_tag).count()
    total_active_chunks = session.query(DocumentChunk).count()

    if not corp_ver:
        corp_ver = CorpusVersion(
            version=corpus_version_tag,
            record_count=total_active_records,
            chunk_count=total_active_chunks,
            is_active=True,
            description="Milestone M11 Production Corpus with 2000+ authoritative legal records"
        )
        session.add(corp_ver)
    else:
        corp_ver.record_count = total_active_records
        corp_ver.chunk_count = total_active_chunks
        corp_ver.is_active = True
    session.commit()

    duration = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"INGESTION COMPLETE in {duration:.2f}s")
    print(f"  Total Attempted: {records_attempted}")
    print(f"  Total Ingested:  {records_ingested}")
    print(f"  Total Skipped:   {records_skipped_dup} (duplicates)")
    print(f"  Total Failed:    {records_failed}")
    print(f"  Active Records:  {total_active_records}")
    print(f"  Active Chunks:   {total_active_chunks}")
    print(f"{'='*50}\n")
    session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest legal corpus into IP-SAKTI")
    parser.add_argument("--source", default="all", help="Source family to ingest")
    parser.add_argument("--corpus-version", default="v1.0", help="Corpus version tag")
    parser.add_argument("--resume", action="store_true", default=True, help="Resume and skip duplicates")
    parser.add_argument("--force", action="store_true", default=False, help="Force re-ingestion and reset records")
    args = parser.parse_args()
    run_ingestion(source_filter=args.source, corpus_version_tag=args.corpus_version, resume=not args.force)
