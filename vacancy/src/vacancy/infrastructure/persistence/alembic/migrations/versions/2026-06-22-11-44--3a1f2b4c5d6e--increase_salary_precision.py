"""increase salary precision

Revision ID: 3a1f2b4c5d6e
Revises: dbdea265bda2
Create Date: 2026-06-22 11:44:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a1f2b4c5d6e'
down_revision: Union[str, Sequence[str], None] = 'dbdea265bda2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('vacancy', 'salary_min_amount',
               existing_type=sa.Numeric(10, 2),
               type_=sa.Numeric(14, 2),
               existing_nullable=True)
    op.alter_column('vacancy', 'salary_max_amount',
               existing_type=sa.Numeric(10, 2),
               type_=sa.Numeric(14, 2),
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('vacancy', 'salary_min_amount',
               existing_type=sa.Numeric(14, 2),
               type_=sa.Numeric(10, 2),
               existing_nullable=True)
    op.alter_column('vacancy', 'salary_max_amount',
               existing_type=sa.Numeric(14, 2),
               type_=sa.Numeric(10, 2),
               existing_nullable=True)
