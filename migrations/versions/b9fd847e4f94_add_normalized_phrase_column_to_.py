"""Add normalized_phrase column to Submission

Revision ID: b9fd847e4f94
Revises: 
Create Date: 2024-06-18 18:39:26.988048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9fd847e4f94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submission')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submission',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('phrase', sa.VARCHAR(length=256), nullable=False),
    sa.Column('player_id', sa.VARCHAR(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
