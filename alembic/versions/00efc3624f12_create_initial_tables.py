"""
Create initial tables

Revision ID: 00efc3624f12
Revises: 
Create Date: 2024-10-04 13:47:54.153879

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00efc3624f12'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "email",
            sa.String(500),
            unique=True,
            nullable=False
        ),
        sa.Column("password", sa.String(200), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
