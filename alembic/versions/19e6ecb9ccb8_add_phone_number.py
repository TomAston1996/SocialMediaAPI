"""add phone number

Revision ID: 19e6ecb9ccb8
Revises: 143a6e6d3d05
Create Date: 2023-03-06 22:13:17.978905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19e6ecb9ccb8'
down_revision = '143a6e6d3d05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
