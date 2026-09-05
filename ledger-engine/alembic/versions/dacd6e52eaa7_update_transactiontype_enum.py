"""Update transactiontype enum

Revision ID: dacd6e52eaa7
Revises: 22280d015df2
Create Date: 2026-09-05 13:36:16.558339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dacd6e52eaa7'
down_revision: Union[str, Sequence[str], None] = '22280d015df2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add IF NOT EXISTS doesn't work in postgres versions before 12 for enum, but we'll try to just catch or use a standard approach if possible.
    # Postgres 10+ supports IF NOT EXISTS for ALTER TYPE
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'Sale'")
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'Stock purchase'")
    op.execute("ALTER TYPE transactiontype ADD VALUE IF NOT EXISTS 'Wastage'")

def downgrade() -> None:
    """Downgrade schema."""
    pass
