"""add_deleted_at_and_user_id_to_files

Revision ID: e348fabad635
Revises: 7d7d109797e0
Create Date: 2025-12-01 11:33:35.186181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e348fabad635'
down_revision: Union[str, None] = '7d7d109797e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add deleted_at to users table
    op.add_column('users', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    
    # Add deleted_at to sessions table
    op.add_column('sessions', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    
    # Add user_id and deleted_at to files table
    op.add_column('files', sa.Column('user_id', sa.Uuid(), nullable=True))
    op.add_column('files', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # Remove columns from files table
    op.drop_column('files', 'deleted_at')
    op.drop_column('files', 'user_id')
    
    # Remove deleted_at from sessions table
    op.drop_column('sessions', 'deleted_at')
    
    # Remove deleted_at from users table
    op.drop_column('users', 'deleted_at')
