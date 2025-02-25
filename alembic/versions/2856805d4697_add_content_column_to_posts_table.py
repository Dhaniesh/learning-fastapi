"""add content column to posts table

Revision ID: 2856805d4697
Revises: 0769ae0c5920
Create Date: 2025-02-24 19:31:02.329364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2856805d4697'
down_revision: Union[str, None] = '0769ae0c5920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
