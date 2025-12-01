"""add_file

Revision ID: 7d7d109797e0
Revises: d6d777ac326f
Create Date: 2025-11-28 16:39:26.434091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '7d7d109797e0'
down_revision: str | None = 'd6d777ac326f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('s3_key', sa.String(length=256), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('files')
