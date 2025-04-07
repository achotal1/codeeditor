"""initial migration

Revision ID: b3f9d7156a8a
Revises: 
Create Date: 2024-03-19 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3f9d7156a8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create problems table
    op.create_table('problems',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('difficulty', sa.String(), nullable=False),
        sa.Column('acceptance_rate', sa.Float(), nullable=False),
        sa.Column('topics', sa.JSON(), nullable=True),
        sa.Column('examples', sa.JSON(), nullable=True),
        sa.Column('constraints', sa.String(), nullable=True),
        sa.Column('templates', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create test_cases table
    op.create_table('test_cases',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('problem_id', sa.String(), nullable=False),
        sa.Column('input', sa.String(), nullable=False),
        sa.Column('expected_output', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create submissions table
    op.create_table('submissions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('problem_id', sa.String(), nullable=False),
        sa.Column('language', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('execution_time', sa.Float(), nullable=True),
        sa.Column('memory_used', sa.Integer(), nullable=True),
        sa.Column('stdout', sa.String(), nullable=True),
        sa.Column('stderr', sa.String(), nullable=True),
        sa.Column('passed_count', sa.Integer(), nullable=True),
        sa.Column('total_count', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('submissions')
    op.drop_table('test_cases')
    op.drop_table('problems')
