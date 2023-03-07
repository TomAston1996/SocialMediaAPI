"""add columns to posts table

Revision ID: d7fbb4cf97d3
Revises: 354fd0735b8c
Create Date: 2023-03-06 21:57:46.970215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7fbb4cf97d3'
down_revision = '354fd0735b8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
