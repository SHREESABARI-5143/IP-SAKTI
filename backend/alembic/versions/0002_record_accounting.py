"""record_accounting

Revision ID: 0002_record_accounting
Revises: 0001_initial
Create Date: 2026-09-15 07:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0002_record_accounting'
down_revision: Union[str, None] = '0001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Add record accounting columns to documents table
    with op.batch_alter_table('documents') as batch_op:
        batch_op.add_column(sa.Column('source_uri', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('publisher', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('published_date', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('retrieved_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('sha256', sa.String(64), nullable=True))
        batch_op.add_column(sa.Column('language', sa.String(10), server_default='en', nullable=False))
        batch_op.add_column(sa.Column('instrument_type', sa.String(50), server_default='STATUTE', nullable=False))
        batch_op.add_column(sa.Column('ingest_status', sa.String(50), server_default='indexed', nullable=False))
        batch_op.add_column(sa.Column('chunk_count', sa.Integer(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('corpus_version', sa.String(50), server_default='v1.0', nullable=False))
        batch_op.create_unique_constraint('uq_documents_sha256', ['sha256'])

    # 2. Table: ingestion_runs
    op.create_table(
        'ingestion_runs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('corpus_version', sa.String(50), nullable=False),
        sa.Column('records_attempted', sa.Integer(), default=0),
        sa.Column('records_ingested', sa.Integer(), default=0),
        sa.Column('records_skipped_duplicate', sa.Integer(), default=0),
        sa.Column('records_failed', sa.Integer(), default=0),
        sa.Column('chunks_created', sa.Integer(), default=0),
        sa.Column('embedding_model', sa.String(100), default='BAAI/bge-m3'),
        sa.Column('notes', sa.Text(), nullable=True)
    )

    # 3. Table: corpus_versions
    op.create_table(
        'corpus_versions',
        sa.Column('version', sa.String(50), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('record_count', sa.Integer(), default=0),
        sa.Column('chunk_count', sa.Integer(), default=0),
        sa.Column('is_active', sa.Boolean(), default=False),
        sa.Column('description', sa.Text(), nullable=True)
    )

    # 4. Table: play_scenarios
    op.create_table(
        'play_scenarios',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('scenario_id', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('locale', sa.String(10), default='en'),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('choices_json', sa.Text(), nullable=False),
        sa.Column('outcomes_json', sa.Text(), nullable=False),
        sa.Column('citation_ids_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 5. Table: jurisdictions
    op.create_table(
        'jurisdictions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(50), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('region', sa.String(100), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 6. Table: legal_instruments
    op.create_table(
        'legal_instruments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('jurisdiction_code', sa.String(50), nullable=False),
        sa.Column('instrument_type', sa.String(100), nullable=False),
        sa.Column('official_publisher', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

def downgrade() -> None:
    op.drop_table('legal_instruments')
    op.drop_table('jurisdictions')
    op.drop_table('play_scenarios')
    op.drop_table('corpus_versions')
    op.drop_table('ingestion_runs')
    with op.batch_alter_table('documents') as batch_op:
        batch_op.drop_constraint('uq_documents_sha256', type_='unique')
        batch_op.drop_column('corpus_version')
        batch_op.drop_column('chunk_count')
        batch_op.drop_column('ingest_status')
        batch_op.drop_column('instrument_type')
        batch_op.drop_column('language')
        batch_op.drop_column('sha256')
        batch_op.drop_column('retrieved_at')
        batch_op.drop_column('published_date')
        batch_op.drop_column('publisher')
        batch_op.drop_column('source_uri')
