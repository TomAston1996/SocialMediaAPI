"""add content column to post table

Revision ID: ee89d086e959
Revises: 39f00fdaa468
Create Date: 2023-03-06 21:40:27.257969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee89d086e959'
down_revision = '39f00fdaa468'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
