"""Deleted block table

Revision ID: 1188d15e430a
Revises: cd0acae24ed3
Create Date: 2024-01-20 16:59:09.866880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1188d15e430a'
down_revision: Union[str, None] = 'cd0acae24ed3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blocks')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('passenger_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['passenger_id'], ['passengers.id'], name='blocks_passenger_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='blocks_pkey')
    )
    # ### end Alembic commands ###
