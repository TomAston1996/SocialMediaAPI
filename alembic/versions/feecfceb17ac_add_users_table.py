"""add users table

Revision ID: feecfceb17ac
Revises: ee89d086e959
Create Date: 2023-03-06 21:45:16.361804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feecfceb17ac'
down_revision = 'ee89d086e959'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
