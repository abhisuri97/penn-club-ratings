"""empty message

Revision ID: 60f555040864
Revises: 31faadef264a
Create Date: 2018-01-30 19:25:27.651941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60f555040864'
down_revision = '31faadef264a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('img_link', sa.Text(), nullable=True))
    op.drop_column('clubs', 'image_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('image_link', sa.TEXT(), nullable=True))
    op.drop_column('clubs', 'img_link')
    # ### end Alembic commands ###