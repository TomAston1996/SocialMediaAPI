"""empty message

Revision ID: 354fd0735b8c
Revises: feecfceb17ac
Create Date: 2023-03-06 21:51:25.600751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '354fd0735b8c'
down_revision = 'feecfceb17ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', 
                          source_table='posts', 
                          referent_table='users', 
                          local_cols=['owner_id'], 
                          remote_cols=['id'], 
                          ondelete='CASCADE'
                          )


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
