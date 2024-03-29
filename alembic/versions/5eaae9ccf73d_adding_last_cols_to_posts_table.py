"""adding last cols to posts table

Revision ID: 5eaae9ccf73d
Revises: 5cc81d561bf6
Create Date: 2024-02-22 13:20:23.672889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5eaae9ccf73d'
down_revision: Union[str, None] = '5cc81d561bf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
