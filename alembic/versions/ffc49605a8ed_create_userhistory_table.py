"""create userhistory table

Revision ID: ffc49605a8ed
Revises: 
Create Date: 2022-08-11 22:30:31.704777

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ffc49605a8ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_history',
        sa.Column('record_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('success', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('record_id')
    )


def downgrade() -> None:
    op.drop_table("user_history")
