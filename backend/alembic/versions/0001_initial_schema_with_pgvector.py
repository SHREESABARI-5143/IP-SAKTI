"""initial_schema_with_pgvector

Revision ID: 0001_initial
Revises: 
Create Date: 2026-09-14 21:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Enable pgvector if PostgreSQL
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2. organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('registration_number', sa.String(100), nullable=True),
        sa.Column('jurisdiction', sa.String(50), default='India'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 3. users
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), default='researcher'),
        sa.Column('preferred_language', sa.String(10), default='en'),
        sa.Column('preferred_jurisdiction', sa.String(50), default='India'),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id'), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 4. source_registry
    op.create_table(
        'source_registry',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('source_id', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('authority', sa.String(255), nullable=False),
        sa.Column('authority_rank', sa.Integer(), default=1),
        sa.Column('jurisdiction', sa.String(50), nullable=False),
        sa.Column('domain', sa.String(100), nullable=False),
        sa.Column('legal_domain', sa.String(100), nullable=True),
        sa.Column('source_type', sa.String(100), nullable=False),
        sa.Column('document_type', sa.String(100), nullable=True),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('official_url', sa.String(500), nullable=True),
        sa.Column('publication_date', sa.String(50), nullable=True),
        sa.Column('effective_date', sa.String(50), nullable=True),
        sa.Column('version', sa.String(50), default='1.0'),
        sa.Column('verification_status', sa.String(50), default='NOT_VERIFIED'),
        sa.Column('ingestion_status', sa.String(50), default='DISCOVERED'),
        sa.Column('retrieved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('checksum_sha256', sa.String(64), nullable=True),
        sa.Column('original_file_path', sa.String(500), nullable=True),
        sa.Column('extracted_file_path', sa.String(500), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('update_frequency', sa.String(50), default='monthly'),
        sa.Column('last_checked', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_success', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_demo', sa.Boolean(), default=False)
    )

    # 5. source_versions
    op.create_table(
        'source_versions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('source_id', sa.String(36), sa.ForeignKey('source_registry.id'), nullable=False),
        sa.Column('version_tag', sa.String(50), nullable=False),
        sa.Column('effective_from', sa.String(50), nullable=True),
        sa.Column('effective_until', sa.String(50), nullable=True),
        sa.Column('checksum', sa.String(64), nullable=False),
        sa.Column('status', sa.String(50), default='active'),
        sa.Column('changelog', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 6. documents
    op.create_table(
        'documents',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('file_type', sa.String(50), nullable=False),
        sa.Column('namespace', sa.String(50), default='PUBLIC_KNOWLEDGE'),
        sa.Column('jurisdiction', sa.String(50), default='India'),
        sa.Column('domain', sa.String(100), default='General'),
        sa.Column('file_size_bytes', sa.Integer(), default=0),
        sa.Column('status', sa.String(50), default='indexed'),
        sa.Column('checksum', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 7. document_chunks (Authoritative Legal & Botanical Knowledge Records)
    op.create_table(
        'document_chunks',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('source_id', sa.String(36), sa.ForeignKey('source_registry.id'), nullable=True),
        sa.Column('document_id', sa.String(36), sa.ForeignKey('documents.id'), nullable=True),
        sa.Column('version_id', sa.String(36), nullable=True),
        sa.Column('chunk_index', sa.Integer(), default=0),
        sa.Column('record_index', sa.Integer(), default=0),
        sa.Column('section_title', sa.String(255), nullable=True),
        sa.Column('provision_ref', sa.String(100), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('source_text', sa.Text(), nullable=True),
        sa.Column('token_count', sa.Integer(), default=0),
        sa.Column('embedding_json', sa.Text(), nullable=True),
        sa.Column('namespace', sa.String(50), default='PUBLIC_KNOWLEDGE'),
        sa.Column('jurisdiction', sa.String(50), default='India'),
        sa.Column('domain', sa.String(100), default='General'),
        sa.Column('legal_domain', sa.String(100), default='PATENT'),
        sa.Column('document_type', sa.String(100), default='ACT'),
        sa.Column('part', sa.String(100), nullable=True),
        sa.Column('chapter', sa.String(100), nullable=True),
        sa.Column('section', sa.String(100), nullable=True),
        sa.Column('subsection', sa.String(100), nullable=True),
        sa.Column('clause', sa.String(100), nullable=True),
        sa.Column('subclause', sa.String(100), nullable=True),
        sa.Column('rule', sa.String(100), nullable=True),
        sa.Column('subrule', sa.String(100), nullable=True),
        sa.Column('regulation', sa.String(100), nullable=True),
        sa.Column('subregulation', sa.String(100), nullable=True),
        sa.Column('article', sa.String(100), nullable=True),
        sa.Column('paragraph', sa.String(100), nullable=True),
        sa.Column('schedule', sa.String(100), nullable=True),
        sa.Column('entry', sa.String(100), nullable=True),
        sa.Column('page', sa.Integer(), nullable=True),
        sa.Column('source_location', sa.String(255), nullable=True),
        sa.Column('parent_chunk_id', sa.String(36), nullable=True),
        sa.Column('authority', sa.String(255), default='Government of India'),
        sa.Column('authority_score', sa.Float(), default=1.0),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 8. conversations
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('title', sa.String(255), default='New Legal Consultation'),
        sa.Column('jurisdiction', sa.String(50), default='India'),
        sa.Column('primary_domain', sa.String(100), default='General'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 9. messages
    op.create_table(
        'messages',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('conversation_id', sa.String(36), sa.ForeignKey('conversations.id'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('short_answer', sa.Text(), nullable=True),
        sa.Column('jurisdiction', sa.String(50), default='India'),
        sa.Column('detected_domain', sa.String(100), default='General'),
        sa.Column('confidence_level', sa.String(20), default='High'),
        sa.Column('confidence_score', sa.Float(), default=1.0),
        sa.Column('is_abstained', sa.Boolean(), default=False),
        sa.Column('abstention_reason', sa.String(255), nullable=True),
        sa.Column('execution_path', sa.String(50), default='STANDARD_PATH'),
        sa.Column('total_latency_ms', sa.Float(), default=0.0),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 10. citations
    op.create_table(
        'citations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('message_id', sa.String(36), sa.ForeignKey('messages.id'), nullable=False),
        sa.Column('chunk_id', sa.String(36), sa.ForeignKey('document_chunks.id'), nullable=True),
        sa.Column('citation_number', sa.Integer(), nullable=False),
        sa.Column('claim_text', sa.Text(), nullable=True),
        sa.Column('source_title', sa.String(255), nullable=False),
        sa.Column('authority', sa.String(255), nullable=False),
        sa.Column('provision_ref', sa.String(100), nullable=False),
        sa.Column('jurisdiction', sa.String(50), nullable=False),
        sa.Column('grounding_score', sa.Float(), default=1.0),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 11. products & ingredients
    op.create_table(
        'products',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('product_type', sa.String(100), nullable=False),
        sa.Column('dosage_form', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('intended_claims', sa.Text(), nullable=True),
        sa.Column('classical_reference_text', sa.String(255), nullable=True),
        sa.Column('is_proprietary', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    op.create_table(
        'ingredients',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('product_id', sa.String(36), sa.ForeignKey('products.id'), nullable=False),
        sa.Column('sanskrit_name', sa.String(255), nullable=True),
        sa.Column('botanical_name', sa.String(255), nullable=False),
        sa.Column('part_used', sa.String(100), nullable=True),
        sa.Column('percentage_or_quantity', sa.String(50), nullable=True),
        sa.Column('is_normally_traded_commodity', sa.Boolean(), default=False),
        sa.Column('source_geography', sa.String(100), default='India')
    )

    # 12. escalations & audit logs
    op.create_table(
        'escalations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('conversation_id', sa.String(36), nullable=True),
        sa.Column('subject', sa.String(255), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('jurisdiction', sa.String(50), default='India'),
        sa.Column('status', sa.String(50), default='Submitted'),
        sa.Column('contact_email', sa.String(255), nullable=False),
        sa.Column('contact_phone', sa.String(50), nullable=True),
        sa.Column('assigned_facilitator_name', sa.String(255), nullable=True),
        sa.Column('facilitator_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(100), nullable=False),
        sa.Column('resource_id', sa.String(100), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True)
    )

def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('escalations')
    op.drop_table('ingredients')
    op.drop_table('products')
    op.drop_table('citations')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('document_chunks')
    op.drop_table('documents')
    op.drop_table('source_versions')
    op.drop_table('source_registry')
    op.drop_table('users')
    op.drop_table('organizations')
