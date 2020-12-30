"""Update Column completed

Revision ID: 0a506ef1b67b
Revises: d4c3e40aaeb4
Create Date: 2020-12-28 11:10:55.526844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a506ef1b67b'
down_revision = 'd4c3e40aaeb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todo', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todo', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
