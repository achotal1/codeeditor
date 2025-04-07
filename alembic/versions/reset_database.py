"""reset database

Revision ID: reset
Revises: 
Create Date: 2024-04-07 03:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'reset'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create problems table
    op.create_table(
        'problems',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('difficulty', sa.String(), nullable=False),
        sa.Column('acceptance_rate', sa.Float(), nullable=False),
        sa.Column('topics', sa.JSON(), nullable=True),
        sa.Column('examples', sa.JSON(), nullable=True),
        sa.Column('constraints', sa.String(), nullable=True),
        sa.Column('templates', sa.JSON(), nullable=True),
        sa.Column('premium', sa.Boolean(), default=False),
        sa.Column('likes', sa.Integer(), default=0),
        sa.Column('dislikes', sa.Integer(), default=0),
        sa.Column('frequency', sa.Float(), default=0.0),
        sa.Column('has_examples', sa.Boolean(), default=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create test_cases table
    op.create_table(
        'test_cases',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('problem_id', sa.String(), nullable=False),
        sa.Column('input', sa.String(), nullable=False),
        sa.Column('expected_output', sa.String(), nullable=False),
        sa.Column('is_hidden', sa.Boolean(), default=False),
        sa.Column('time_limit', sa.Integer(), nullable=True),
        sa.Column('memory_limit', sa.Integer(), nullable=True),
        sa.Column('order', sa.Integer(), default=0),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create submissions table
    op.create_table(
        'submissions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('problem_id', sa.String(), nullable=False),
        sa.Column('language', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.String(), nullable=False),
        sa.Column('execution_time', sa.Float(), nullable=True),
        sa.Column('memory_used', sa.Float(), nullable=True),
        sa.Column('passed_count', sa.Integer(), nullable=True),
        sa.Column('total_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('submissions')
    op.drop_table('test_cases')
    op.drop_table('problems') 