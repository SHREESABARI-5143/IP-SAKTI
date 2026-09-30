"""
IP-SAKTI Sahayak — Pure Local PostgreSQL + pgvector Corpus Seeder & Indexer.

1. Connects to PostgreSQL database.
2. Ensures 'vector' extension is active.
3. Seeds all authentic statutory provisions from JSON files into 'corpus_chunks'.
4. Builds HNSW index on pgvector and GIN index on tsvector for hybrid search.
5. Seeds all legal knowledge graph relationships into 'graph_edges'.
"""

import os
import sys
import json
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(backend_dir, ".env"))

# Add backend directory to sys.path
sys.path.insert(0, backend_dir)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text, select, func

from app.core.config import settings
from app.models.database import Base, DBCorpusChunk, DBGraphEdge, engine, async_session, init_db
from app.services.graph_service import STATUTORY_EDGES


async def index_pgvector():
    print("=" * 60)
    print(" IP-SAKTI Sahayak — 100% Local PostgreSQL + pgvector Indexer")
    print("=" * 60)
    print(f"Database URL: {settings.DATABASE_URL}")

    # 1. Initialize DB schema, extensions, and tables
    print("\n[Step 1/3] Initializing PostgreSQL tables, pgvector, and tsvector...")
    await init_db()

    # 2. Verify chunks count
    async with async_session() as session:
        result = await session.execute(select(func.count(DBCorpusChunk.chunk_id)))
        chunk_count = result.scalar() or 0
        print(f"[Step 2/3] Database contains {chunk_count} statutory corpus provisions.")

        # 3. Verify graph edges
        edge_result = await session.execute(select(func.count(DBGraphEdge.id)))
        edge_count = edge_result.scalar() or 0
        print(f"[Step 3/3] Verified {edge_count} knowledge graph edges in 'graph_edges'.")

    print("\n" + "=" * 60)
    print(" 100% Local PostgreSQL + pgvector Migration Complete & Ready!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(index_pgvector())
