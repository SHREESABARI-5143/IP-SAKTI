import uuid
import hashlib
from datetime import datetime, timezone
from backend.app.core.database import sync_engine, Base, SyncSessionLocal
from backend.app.models.user import User
from backend.app.core.security import get_password_hash
from backend.app.ingestion.live_ingest import live_ingestion

def seed_database():
    """
    Seeds initial database idempotently with demo accounts and runs live ingestion
    of verified statutory corpora from data files.
    """
    Base.metadata.create_all(bind=sync_engine)

    session = SyncSessionLocal()
    try:
        # 1. Seed Demo Admin User
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

        # 2. Seed Demo Innovator User
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

        session.commit()

        # 3. Live Ingest Statutory Corpora from structured dataset
        live_ingestion.ingest_corpus_file(session=session)

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
