"""Advertisement table

Revision ID: ee9cbc96c242
Revises: 074a4cb13c80
Create Date: 2024-01-23 17:56:50.702913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee9cbc96c242'
down_revision: Union[str, None] = '074a4cb13c80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisements', sa.Column('text', sa.Text(), nullable=True))
    op.drop_column('advertisements', 'url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisements', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('advertisements', 'text')
    # ### end Alembic commands ###
