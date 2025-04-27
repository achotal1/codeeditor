"""add stdout and stderr columns to submissions

Revision ID: add_stdout_stderr
Revises: reset
Create Date: 2024-04-07 03:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_stdout_stderr'
down_revision = 'reset'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add stdout and stderr columns to submissions table
    op.add_column('submissions', sa.Column('stdout', sa.String(), nullable=True))
    op.add_column('submissions', sa.Column('stderr', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove stdout and stderr columns from submissions table
    op.drop_column('submissions', 'stdout')
    op.drop_column('submissions', 'stderr') 