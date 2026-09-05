"""Add uppercase enum values

Revision ID: be81b01996c1
Revises: dacd6e52eaa7
Create Date: 2026-09-05 13:45:32.742518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be81b01996c1'
down_revision: Union[str, Sequence[str], None] = 'dacd6e52eaa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'SALE'")
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'STOCK_PURCHASE'")
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'WASTAGE'")

def downgrade() -> None:
    """Downgrade schema."""
    pass
