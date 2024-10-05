"""
Create cats and ratings tables

Revision ID: fbdc37291df5
Revises: 00efc3624f12
Create Date: 2024-10-04 14:23:48.264636

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbdc37291df5'
down_revision: str | None = '00efc3624f12'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(200), unique=True, nullable=False),
    )
    op.create_table(
        "cats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
        	sa.Integer,
        	sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "category_id",
        	sa.Integer,
        	sa.ForeignKey("categories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("color", sa.String(200), nullable=False),
        sa.Column("age", sa.Integer, nullable=False),
        sa.Column("desc", sa.Text),
    )
    op.create_table(
        "ratings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
        	sa.Integer,
        	sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "cat_id",
        	sa.Integer,
        	sa.ForeignKey("cats.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("stars", sa.Integer)
    )


def downgrade() -> None:
    op.drop_table("ratings")
    op.drop_table("cats")
    op.drop_table("categories")
