"""empty message

Revision ID: 3f0c2ca00ca3
Revises: 767042088799
Create Date: 2021-05-30 17:18:03.248288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f0c2ca00ca3'
down_revision = '767042088799'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('individual', 'href')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('individual', sa.Column('href', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
