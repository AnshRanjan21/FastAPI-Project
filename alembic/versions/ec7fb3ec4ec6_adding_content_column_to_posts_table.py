"""adding content column to posts table

Revision ID: ec7fb3ec4ec6
Revises: caa24e732333
Create Date: 2024-02-22 00:55:56.626683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec7fb3ec4ec6'
down_revision: Union[str, None] = 'caa24e732333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content" , sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
