"""add  tag  column

Revision ID: f646eab1ac68
Revises: e24161bfff7b
Create Date: 2022-06-01 17:53:48.798905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f646eab1ac68'
down_revision = 'e24161bfff7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('tag', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'tag')
    # ### end Alembic commands ###
