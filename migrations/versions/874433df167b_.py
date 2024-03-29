"""empty message

Revision ID: 874433df167b
Revises: 
Create Date: 2021-01-28 10:35:44.041009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '874433df167b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('papers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paper_id', sa.String(length=50), nullable=True),
    sa.Column('author', sa.String(length=50), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('publish_time', sa.String(length=50), nullable=True),
    sa.Column('doi', sa.String(length=50), nullable=True),
    sa.Column('pdf_ufl', sa.String(length=100), nullable=True),
    sa.Column('affiliation', sa.String(length=100), nullable=True),
    sa.Column('summary', sa.String(length=500), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('papers')
    # ### end Alembic commands ###
