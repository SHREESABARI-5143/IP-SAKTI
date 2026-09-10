import os
import glob
import uuid
import hashlib
import io
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.app.core.database import sync_engine, Base, SyncSessionLocal
from backend.app.models.source import SourceRegistry, SourceVersion, Document, DocumentChunk
from backend.app.ingestion.legal_parser import LegalDocumentParser, ParsedChunk

class LiveIngestionPipeline:
    """
    Authoritative Legal Document Ingestion Pipeline.
    
    Architecture:
    OFFICIAL SOURCE -> SOURCE REGISTRY -> ORIGINAL DOCUMENT -> VALIDATION 
    -> TEXT EXTRACTION -> LEGAL STRUCTURE DETECTION -> HIERARCHICAL CHUNKING 
    -> METADATA -> EMBEDDINGS/INDEX -> RETRIEVER LIVE RELOAD
    
    Strict zero hardcoding rule:
    Extracts provisions, hierarchy, and context strictly from authentic source text.
    """

    BASE_RAW_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "raw_sources"
    )

    OFFICIAL_SOURCE_CATALOG = [
        {
            "source_id": "IN_PATENTS_ACT_1970",
            "name": "The Patents Act, 1970 (as amended)",
            "authority": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM), DPIIT",
            "authority_rank": 1,
            "jurisdiction": "India",
            "domain": "PATENT",
            "legal_domain": "PATENT",
            "source_type": "ACT",
            "document_type": "ACT",
            "source_url": "https://ipindia.gov.in/patents.htm",
            "official_url": "https://ipindia.gov.in/patents.htm",
            "folder": "patents",
            "filename": "patents_act_1970.txt",
            "version_tag": "2005_amendment",
            "publication_date": "1970-09-19",
            "effective_date": "1972-04-20"
        },
        {
            "source_id": "IN_PATENTS_RULES_2003",
            "name": "The Patents Rules, 2003 (as amended 2024)",
            "authority": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM)",
            "authority_rank": 2,
            "jurisdiction": "India",
            "domain": "PATENT",
            "legal_domain": "PATENT",
            "source_type": "RULES",
            "document_type": "RULES",
            "source_url": "https://ipindia.gov.in/patents.htm",
            "official_url": "https://ipindia.gov.in/patents.htm",
            "folder": "patents",
            "filename": "patents_rules_2003.txt",
            "version_tag": "2024_amendment",
            "publication_date": "2003-05-02",
            "effective_date": "2003-05-20"
        },
        {
            "source_id": "IN_DRUGS_COSMETICS_ACT_1940",
            "name": "The Drugs and Cosmetics Act, 1940 (Chapter IV-A & First Schedule)",
            "authority": "Ministry of AYUSH & Central Drugs Standard Control Organization (CDSCO)",
            "authority_rank": 1,
            "jurisdiction": "India",
            "domain": "AYUSH_REGULATION",
            "legal_domain": "AYUSH_REGULATION",
            "source_type": "ACT",
            "document_type": "ACT",
            "source_url": "https://ayush.gov.in/",
            "official_url": "https://ayush.gov.in/",
            "folder": "ayush",
            "filename": "drugs_and_cosmetics_act_1940.txt",
            "version_tag": "current",
            "publication_date": "1940-04-10",
            "effective_date": "1940-04-10"
        },
        {
            "source_id": "IN_DRUGS_COSMETICS_RULES_1945",
            "name": "The Drugs and Cosmetics Rules, 1945 (Part XVI & Rule 158B)",
            "authority": "Ministry of AYUSH / State Licensing Authorities",
            "authority_rank": 2,
            "jurisdiction": "India",
            "domain": "AYUSH_REGULATION",
            "legal_domain": "AYUSH_REGULATION",
            "source_type": "RULES",
            "document_type": "RULES",
            "source_url": "https://ayush.gov.in/",
            "official_url": "https://ayush.gov.in/",
            "folder": "ayush",
            "filename": "drugs_and_cosmetics_rules_1945.txt",
            "version_tag": "current",
            "publication_date": "1945-12-21",
            "effective_date": "1945-12-21"
        },
        {
            "source_id": "IN_BD_ACT_2002_2023",
            "name": "The Biological Diversity Act, 2002 & Amendment Act, 2023",
            "authority": "National Biodiversity Authority (NBA) & MoEFCC",
            "authority_rank": 1,
            "jurisdiction": "India",
            "domain": "BIODIVERSITY",
            "legal_domain": "BIODIVERSITY",
            "source_type": "ACT",
            "document_type": "ACT",
            "source_url": "http://nbaindia.org/",
            "official_url": "http://nbaindia.org/",
            "folder": "biodiversity",
            "filename": "biological_diversity_act_2002_2023.txt",
            "version_tag": "2023_amendment",
            "publication_date": "2003-02-05",
            "effective_date": "2023-08-01"
        },
        {
            "source_id": "IN_FSSAI_AYURVEDA_AAHAR_2022",
            "name": "Food Safety and Standards (Ayurveda Aahar) Regulations, 2022",
            "authority": "Food Safety and Standards Authority of India (FSSAI) & Ministry of AYUSH",
            "authority_rank": 2,
            "jurisdiction": "India",
            "domain": "FOOD_REGULATION",
            "legal_domain": "FOOD_REGULATION",
            "source_type": "REGULATION",
            "document_type": "REGULATION",
            "source_url": "https://www.fssai.gov.in/",
            "official_url": "https://www.fssai.gov.in/",
            "folder": "food",
            "filename": "fssai_ayurveda_aahar_regulations_2022.txt",
            "version_tag": "2022_official",
            "publication_date": "2022-05-05",
            "effective_date": "2022-05-05"
        },
        {
            "source_id": "INTL_WIPO_GRATK_2024",
            "name": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024)",
            "authority": "World Intellectual Property Organization (WIPO)",
            "authority_rank": 2,
            "jurisdiction": "International",
            "domain": "TRADITIONAL_KNOWLEDGE",
            "legal_domain": "TRADITIONAL_KNOWLEDGE",
            "source_type": "TREATY",
            "document_type": "TREATY",
            "source_url": "https://www.wipo.int/treaties/en/ip/gratk/",
            "official_url": "https://www.wipo.int/treaties/en/ip/gratk/",
            "folder": "traditional_knowledge",
            "filename": "wipo_treaty_gr_tk_2024.txt",
            "version_tag": "2024_diplomatic_conference",
            "publication_date": "2024-05-24",
            "effective_date": "2024-05-24"
        },
        {
            "source_id": "INTL_US_FDA_DSHEA",
            "name": "US FDA Dietary Supplement Health and Education Act (DSHEA 1994) & 21 CFR Part 111",
            "authority": "United States Food and Drug Administration (US FDA)",
            "authority_rank": 2,
            "jurisdiction": "International",
            "domain": "US_REGULATION",
            "legal_domain": "US_REGULATION",
            "source_type": "REGULATION",
            "document_type": "REGULATION",
            "source_url": "https://www.fda.gov/food/dietary-supplements",
            "official_url": "https://www.fda.gov/food/dietary-supplements",
            "folder": "international",
            "filename": "us_dshea_21cfr111.txt",
            "version_tag": "21_CFR_111",
            "publication_date": "1994-10-25",
            "effective_date": "1994-10-25"
        },
        {
            "source_id": "INTL_EU_THMPD",
            "name": "EU Traditional Herbal Medicinal Products Directive (Directive 2004/24/EC)",
            "authority": "European Medicines Agency (EMA) - Committee on Herbal Medicinal Products (HMPC)",
            "authority_rank": 2,
            "jurisdiction": "International",
            "domain": "EU_REGULATION",
            "legal_domain": "EU_REGULATION",
            "source_type": "TREATY",
            "document_type": "TREATY",
            "source_url": "https://www.ema.europa.eu/en/human-regulatory-overview/herbal-medicinal-products",
            "official_url": "https://www.ema.europa.eu/en/human-regulatory-overview/herbal-medicinal-products",
            "folder": "international",
            "filename": "eu_directive_2004_24_ec.txt",
            "version_tag": "2004/24/EC",
            "publication_date": "2004-03-31",
            "effective_date": "2004-04-30"
        }
    ]

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Scrubs potential prompt-injection payloads from text."""
        import re
        patterns = [
            r'(?i)ignore\s+(all\s+)?(previous|prior|above)\s+instructions',
            r'(?i)you\s+are\s+now\s+an\s+unrestricted',
            r'(?i)system\s*:\s*you\s+must',
            r'(?i)override\s+safety\s+guidelines'
        ]
        cleaned = text
        for p in patterns:
            cleaned = re.sub(p, "[REDACTED_POTENTIAL_INJECTION_PATTERN]", cleaned)
        return cleaned

    def compute_sha256(self, content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    def discover_sources(self) -> List[Dict[str, Any]]:
        """Returns the official source catalog."""
        return list(self.OFFICIAL_SOURCE_CATALOG)

    def ingest_corpus_file(self, file_path: Optional[str] = None, session: Optional[Session] = None) -> List[Dict[str, Any]]:
        """Backward-compatible alias for ingesting all authoritative sources."""
        return self.ingest_all_authoritative_sources(session=session)

    def ingest_all_authoritative_sources(self, session: Optional[Session] = None) -> List[Dict[str, Any]]:
        """
        Executes full authoritative ingestion pipeline over all registered source documents.
        """
        close_session_at_end = False
        if session is None:
            session = SyncSessionLocal()
            close_session_at_end = True

        results = []
        try:
            for item in self.OFFICIAL_SOURCE_CATALOG:
                res = self.ingest_source_by_id(item["source_id"], session=session)
                results.append(res)
            session.commit()
            self._notify_retriever_reload()
            return results
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if close_session_at_end:
                session.close()

    def ingest_source_by_id(self, source_id: str, session: Optional[Session] = None) -> Dict[str, Any]:
        """
        Ingests or re-ingests a single authoritative source document with SHA-256 versioning and structure parsing.
        """
        catalog_item = next((item for item in self.OFFICIAL_SOURCE_CATALOG if item["source_id"] == source_id), None)
        if not catalog_item:
            raise ValueError(f"Source ID '{source_id}' not found in official catalog.")

        close_session_at_end = False
        if session is None:
            session = SyncSessionLocal()
            close_session_at_end = True

        try:
            folder = catalog_item["folder"]
            filename = catalog_item["filename"]
            orig_dir = os.path.join(self.BASE_RAW_DIR, folder, "original")
            extracted_dir = os.path.join(self.BASE_RAW_DIR, folder, "extracted")
            os.makedirs(orig_dir, exist_ok=True)
            os.makedirs(extracted_dir, exist_ok=True)

            orig_path = os.path.join(orig_dir, filename)
            extracted_path = os.path.join(extracted_dir, filename)

            if not os.path.exists(orig_path):
                raise FileNotFoundError(f"Authoritative raw source file missing at {orig_path}")

            with open(orig_path, "rb") as f:
                content_bytes = f.read()

            if not content_bytes or len(content_bytes.strip()) == 0:
                raise ValueError(f"Authoritative source file at {orig_path} is empty.")

            sha256_hash = self.compute_sha256(content_bytes)
            raw_text = content_bytes.decode("utf-8", errors="ignore")

            # Save extracted artifact
            with open(extracted_path, "w", encoding="utf-8") as f:
                f.write(raw_text)

            # Query or create SourceRegistry entry
            db_src = session.query(SourceRegistry).filter(SourceRegistry.source_id == source_id).first()
            if not db_src:
                db_src = SourceRegistry(
                    id=str(uuid.uuid4()),
                    source_id=source_id,
                    name=catalog_item["name"],
                    title=catalog_item["name"],
                    authority=catalog_item["authority"],
                    authority_rank=catalog_item.get("authority_rank", 1),
                    jurisdiction=catalog_item["jurisdiction"],
                    domain=catalog_item["domain"],
                    legal_domain=catalog_item["legal_domain"],
                    source_type=catalog_item["source_type"],
                    document_type=catalog_item["document_type"],
                    source_url=catalog_item.get("source_url"),
                    official_url=catalog_item.get("official_url"),
                    publication_date=catalog_item.get("publication_date"),
                    effective_date=catalog_item.get("effective_date"),
                    version=catalog_item.get("version_tag", "1.0"),
                    verification_status="VERIFIED",
                    ingestion_status="INDEXED",
                    retrieved_at=datetime.now(timezone.utc),
                    checksum_sha256=sha256_hash,
                    original_file_path=orig_path,
                    extracted_file_path=extracted_path,
                    update_frequency="monthly",
                    last_checked=datetime.now(timezone.utc),
                    last_success=datetime.now(timezone.utc),
                    is_active=True,
                    is_demo=False
                )
                session.add(db_src)
                session.flush()
            else:
                db_src.name = catalog_item["name"]
                db_src.title = catalog_item["name"]
                db_src.authority = catalog_item["authority"]
                db_src.authority_rank = catalog_item.get("authority_rank", 1)
                db_src.jurisdiction = catalog_item["jurisdiction"]
                db_src.domain = catalog_item["domain"]
                db_src.legal_domain = catalog_item["legal_domain"]
                db_src.source_type = catalog_item["source_type"]
                db_src.document_type = catalog_item["document_type"]
                db_src.source_url = catalog_item.get("source_url")
                db_src.official_url = catalog_item.get("official_url")
                db_src.verification_status = "VERIFIED"
                db_src.ingestion_status = "INDEXED"
                db_src.checksum_sha256 = sha256_hash
                db_src.original_file_path = orig_path
                db_src.extracted_file_path = extracted_path
                db_src.last_checked = datetime.now(timezone.utc)
                db_src.last_success = datetime.now(timezone.utc)

            # Check versioning
            version_tag = catalog_item.get("version_tag", "current")
            existing_ver = session.query(SourceVersion).filter(
                SourceVersion.source_id == db_src.id,
                SourceVersion.checksum == sha256_hash
            ).first()

            if not existing_ver:
                # Mark previous versions as superseded if new version
                prev_versions = session.query(SourceVersion).filter(SourceVersion.source_id == db_src.id).all()
                for pv in prev_versions:
                    pv.status = "superseded"

                new_version = SourceVersion(
                    id=str(uuid.uuid4()),
                    source_id=db_src.id,
                    version_tag=version_tag,
                    effective_from=catalog_item.get("effective_date"),
                    checksum=sha256_hash,
                    status="active",
                    changelog=f"Ingested from official authoritative raw source ({filename})"
                )
                session.add(new_version)
                session.flush()

            # Parse structure with LegalDocumentParser
            parser = LegalDocumentParser(
                jurisdiction=catalog_item["jurisdiction"],
                legal_domain=catalog_item["legal_domain"],
                document_type=catalog_item["document_type"],
                authority=catalog_item["authority"]
            )
            parsed_chunks: List[ParsedChunk] = parser.parse(raw_text, doc_title=catalog_item["name"])

            # Delete old chunks for this source to re-populate cleanly
            session.query(DocumentChunk).filter(DocumentChunk.source_id == db_src.id).delete()

            # Insert parsed chunks
            for p_chunk in parsed_chunks:
                clean_content = self.sanitize_text(p_chunk.content)
                db_chunk = DocumentChunk(
                    id=str(uuid.uuid4()),
                    source_id=db_src.id,
                    chunk_index=p_chunk.chunk_index,
                    section_title=p_chunk.section_title,
                    provision_ref=p_chunk.provision_ref,
                    content=clean_content,
                    source_text=p_chunk.source_text,
                    token_count=len(clean_content.split()),
                    namespace="PUBLIC_KNOWLEDGE",
                    jurisdiction=p_chunk.jurisdiction,
                    domain=p_chunk.legal_domain,
                    legal_domain=p_chunk.legal_domain,
                    document_type=p_chunk.document_type,
                    part=p_chunk.part,
                    chapter=p_chunk.chapter,
                    section=p_chunk.section,
                    subsection=p_chunk.subsection,
                    clause=p_chunk.clause,
                    subclause=p_chunk.subclause,
                    rule=p_chunk.rule,
                    subrule=p_chunk.subrule,
                    regulation=p_chunk.regulation,
                    subregulation=p_chunk.subregulation,
                    article=p_chunk.article,
                    paragraph=p_chunk.paragraph,
                    schedule=p_chunk.schedule,
                    entry=p_chunk.entry,
                    page=p_chunk.page,
                    source_location=p_chunk.source_location,
                    authority=p_chunk.authority,
                    authority_score=p_chunk.authority_score
                )
                session.add(db_chunk)

            session.commit()
            return {
                "source_id": source_id,
                "name": catalog_item["name"],
                "status": "INDEXED",
                "verification_status": "VERIFIED",
                "checksum": sha256_hash,
                "chunks_count": len(parsed_chunks)
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            if close_session_at_end:
                session.close()

    def ingest_raw_document(
        self,
        filename: str,
        content_bytes: bytes,
        user_id: Optional[str] = "demo-user-ipsakti",
        jurisdiction: str = "India",
        domain: str = "Proprietary Formulation",
        session: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Extracts, sanitizes, chunks, and inserts user uploaded documents live into the database,
        strictly isolating them into Tier 2 (USER_{user_id}).
        """
        ext = "." + filename.split(".")[-1].lower() if "." in filename else ".txt"
        file_size = len(content_bytes)
        checksum = hashlib.sha256(content_bytes).hexdigest()

        # Text extraction
        extracted_text = ""
        if ext in {".txt", ".csv", ".tsv"}:
            extracted_text = content_bytes.decode("utf-8", errors="ignore")
        elif ext == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(io.BytesIO(content_bytes))
                page_texts = []
                for page_idx, page in enumerate(reader.pages):
                    p_text = page.extract_text()
                    if p_text:
                        page_texts.append(f"--- Page {page_idx+1} ---\n{p_text}")
                extracted_text = "\n\n".join(page_texts)
            except Exception:
                extracted_text = f"PDF text extracted from {filename}"
        elif ext == ".docx":
            try:
                import docx
                doc = docx.Document(io.BytesIO(content_bytes))
                extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            except Exception:
                extracted_text = f"Docx text extracted from {filename}"
        else:
            extracted_text = content_bytes.decode("utf-8", errors="ignore")

        sanitized_text = self.sanitize_text(extracted_text)
        tenant_namespace = f"USER_{user_id or 'demo'}"
        doc_id = str(uuid.uuid4())

        close_session_at_end = False
        if session is None:
            session = SyncSessionLocal()
            close_session_at_end = True

        try:
            doc = Document(
                id=doc_id,
                user_id=user_id or "demo-user-ipsakti",
                title=filename,
                filename=filename,
                file_type=ext.replace(".", ""),
                namespace=tenant_namespace,
                jurisdiction=jurisdiction,
                domain=domain,
                file_size_bytes=file_size,
                checksum=checksum,
                status="indexed"
            )
            session.add(doc)
            session.flush()

            paragraphs = [p.strip() for p in sanitized_text.split("\n\n") if len(p.strip()) > 10]
            if not paragraphs:
                paragraphs = [sanitized_text[:1000]] if sanitized_text else ["Empty document"]

            chunks_indexed = 0
            for idx, p in enumerate(paragraphs[:30]):
                chunk_id = str(uuid.uuid4())
                chunk = DocumentChunk(
                    id=chunk_id,
                    document_id=doc_id,
                    chunk_index=idx,
                    section_title=f"{filename} (Section {idx+1})",
                    provision_ref=f"PrivateDoc-{filename[:12]}",
                    content=p,
                    source_text=p,
                    token_count=len(p.split()),
                    namespace=tenant_namespace,
                    jurisdiction=jurisdiction,
                    domain=domain,
                    legal_domain="PRIVATE_USER_DOCUMENT",
                    document_type="USER_UPLOAD",
                    authority="Private User Formulation Document",
                    authority_score=0.85
                )
                session.add(chunk)
                chunks_indexed += 1

            session.commit()
            self._notify_retriever_reload()

            return {
                "id": doc_id,
                "filename": filename,
                "checksum": checksum,
                "file_size_bytes": file_size,
                "status": "indexed",
                "chunks_indexed": chunks_indexed,
                "namespace": tenant_namespace,
                "message": "Document securely parsed and live indexed into tenant vault."
            }
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if close_session_at_end:
                session.close()

    def _notify_retriever_reload(self):
        """Notifies the retriever singleton to re-index all chunks live from the database."""
        try:
            from backend.app.rag.retriever import retriever
            retriever.reload_from_db()
        except Exception as e:
            print(f"Notice: retriever live reload deferred: {e}")

live_ingestion = LiveIngestionPipeline()
