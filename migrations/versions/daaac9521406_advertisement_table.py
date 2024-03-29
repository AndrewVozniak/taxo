"""Advertisement table

Revision ID: daaac9521406
Revises: ee9cbc96c242
Create Date: 2024-01-23 18:34:53.475727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daaac9521406'
down_revision: Union[str, None] = 'ee9cbc96c242'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisements', sa.Column('last_published_at', sa.DateTime(), nullable=True))
    op.drop_column('advertisements', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisements', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('advertisements', 'last_published_at')
    # ### end Alembic commands ###
