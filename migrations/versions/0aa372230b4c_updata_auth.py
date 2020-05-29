"""updata auth

Revision ID: 0aa372230b4c
Revises: 19ea5f8757d4
Create Date: 2020-05-23 16:44:54.049464

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0aa372230b4c'
down_revision = '19ea5f8757d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('authenticate', sa.Boolean(), nullable=False))
    op.drop_column('user', 'authenticat')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('authenticat', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('user', 'authenticate')
    # ### end Alembic commands ###