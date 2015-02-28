"""create donation table

Revision ID: 1c7b5a8b7d58
Revises: 4e866256ec91
Create Date: 2015-02-28 12:11:13.010458

"""

# revision identifiers, used by Alembic.
revision = '1c7b5a8b7d58'
down_revision = '4e866256ec91'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('donation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('confirmation', sa.Unicode(length=100), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('donation')
