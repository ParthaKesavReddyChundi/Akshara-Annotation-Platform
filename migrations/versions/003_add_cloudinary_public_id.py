"""Add cloudinary_public_id

Revision ID: 003
Revises: 002
Create Date: 2026-08-10 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('audio_files', sa.Column('cloudinary_public_id', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('audio_files', 'cloudinary_public_id')
