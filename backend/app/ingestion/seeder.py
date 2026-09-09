import uuid
import hashlib
from datetime import datetime, timezone
from backend.app.core.database import sync_engine, Base, SyncSessionLocal
from backend.app.models.source import SourceRegistry, SourceVersion, DocumentChunk
from backend.app.models.user import User
from backend.app.core.security import get_password_hash
from backend.app.ingestion.seed_corpus import AUTHORITATIVE_SOURCES

def seed_database():
    """
    Seeds initial database idempotently with all authoritative statutes, rules, treaties,
    and demo accounts.
    """
    Base.metadata.create_all(bind=sync_engine)

    session = SyncSessionLocal()
    try:
        # 1. Seed Demo Admin
        existing_admin = session.query(User).filter(User.email == "admin@ipsakti.gov.in").first()
        if not existing_admin:
            admin_user = User(
                id="admin-ipsakti-id",
                email="admin@ipsakti.gov.in",
                hashed_password=get_password_hash("ipsakti_admin_2026"),
                full_name="National IP Officer",
                role="admin"
            )
            session.add(admin_user)
            session.flush()

        # Seed Demo Innovator User
        existing_user = session.query(User).filter(User.email == "innovator@ayush-startup.in").first()
        if not existing_user:
            demo_user = User(
                id="demo-user-ipsakti",
                email="innovator@ayush-startup.in",
                hashed_password=get_password_hash("innovator2026"),
                full_name="Ayurvedic Formulation Innovator",
                role="user"
            )
            session.add(demo_user)
            session.flush()

        # 2. Seed Authoritative Source Registry and Chunks
        for src_data in AUTHORITATIVE_SOURCES:
            src_id_str = src_data["source_id"]
            existing_src = session.query(SourceRegistry).filter(SourceRegistry.source_id == src_id_str).first()
            if not existing_src:
                db_src = SourceRegistry(
                    id=str(uuid.uuid4()),
                    source_id=src_id_str,
                    name=src_data["name"],
                    authority=src_data["authority"],
                    authority_rank=src_data.get("authority_rank", 1),
                    jurisdiction=src_data["jurisdiction"],
                    domain=src_data["domain"],
                    source_type=src_data["source_type"],
                    source_url=src_data.get("source_url"),
                    update_frequency="monthly",
                    is_active=True,
                    is_demo=False
                )
                session.add(db_src)
                session.flush()

                # Source Version
                version_obj = SourceVersion(
                    id=str(uuid.uuid4()),
                    source_id=db_src.id,
                    version_tag=src_data.get("version_tag", "current"),
                    effective_from=src_data.get("effective_from"),
                    checksum=hashlib.sha256(src_data["name"].encode()).hexdigest(),
                    status="active",
                    changelog="Official verified statutory baseline text"
                )
                session.add(version_obj)

                # Chunks
                for c_idx, chunk_item in enumerate(src_data["chunks"]):
                    db_chunk = DocumentChunk(
                        id=str(uuid.uuid4()),
                        source_id=db_src.id,
                        chunk_index=c_idx,
                        section_title=chunk_item["section_title"],
                        provision_ref=chunk_item["provision_ref"],
                        content=chunk_item["content"],
                        token_count=len(chunk_item["content"].split()),
                        namespace="PUBLIC_KNOWLEDGE",
                        jurisdiction=src_data["jurisdiction"],
                        domain=src_data["domain"],
                        authority=chunk_item.get("authority", src_data["authority"]),
                        authority_score=chunk_item.get("authority_score", 1.0)
                    )
                    session.add(db_chunk)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
