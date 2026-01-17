"""create transactions tables

Revision ID: 0001
Revises: 
Create Date: 2026-01-17
"""

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "raw_transactions",
        sa.Column("transaction_id", sa.String(length=64), primary_key=True),
        sa.Column("account_id", sa.String(length=64), nullable=False),
        sa.Column("transaction_timestamp", sa.DateTime(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("merchant", sa.String(length=256), nullable=False),
        sa.Column("merchant_category", sa.String(length=128), nullable=True),
        sa.Column("country", sa.String(length=2), nullable=False),
        sa.Column("payment_method", sa.String(length=64), nullable=True),
        sa.Column("channel", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=True),
        sa.Column("ingested_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "curated_transactions",
        sa.Column("transaction_id", sa.String(length=64), primary_key=True),
        sa.Column("account_id", sa.String(length=64), nullable=False),
        sa.Column("transaction_timestamp", sa.DateTime(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("merchant", sa.String(length=256), nullable=False),
        sa.Column("country", sa.String(length=2), nullable=False),
        sa.Column("risk_flag", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("risk_reason", sa.Text(), nullable=True),
        sa.Column("curated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("curated_transactions")
    op.drop_table("raw_transactions")
