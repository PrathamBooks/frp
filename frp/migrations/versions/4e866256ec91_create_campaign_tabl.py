"""create campaign table

Revision ID: 4e866256ec91
Revises: 52d4ac88a01f
Create Date: 2015-02-15 11:49:29.005475

"""

# revision identifiers, used by Alembic.
revision = '4e866256ec91'
down_revision = '52d4ac88a01f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('campaign',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('nbooks', sa.Integer(), nullable=True),
        sa.Column('nlic', sa.Integer(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('description', sa.Unicode(length=500), nullable=False),
        sa.Column('who', sa.Unicode(length=500), nullable=False),
        sa.Column('impact', sa.Unicode(length=500), nullable=False),
        sa.Column('utilization', sa.Unicode(length=500), nullable=False),
        sa.Column('languages', sa.Unicode(length=200), nullable=False),
        sa.Column('state', sa.Unicode(length=500), nullable=False),
        sa.Column('city', sa.Unicode(length=500), nullable=False),
        sa.Column('image', sa.Unicode(length=100), nullable=False),
        sa.Column('status', sa.Unicode(length=100), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('campaign')
