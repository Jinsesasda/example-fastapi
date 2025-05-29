"""add content table to posts

Revision ID: 446f6a79259e
Revises: 30f613b27492
Create Date: 2025-05-27 22:04:58.187629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '446f6a79259e'
down_revision: Union[str, None] = '30f613b27492'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass