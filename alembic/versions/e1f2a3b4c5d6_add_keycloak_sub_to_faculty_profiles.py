"""add keycloak_sub to faculty_profiles

Revision ID: e1f2a3b4c5d6
Revises: d8f4e02a95c3
Create Date: 2026-09-17 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e1f2a3b4c5d6'
down_revision: Union[str, Sequence[str], None] = 'd8f4e02a95c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_cols = {c["name"] for c in inspector.get_columns("faculty_profiles")}
    if "keycloak_sub" not in existing_cols:
        op.add_column(
            "faculty_profiles",
            sa.Column("keycloak_sub", sa.String(), nullable=True),
        )
        op.create_index(
            "idx_faculty_profiles_keycloak_sub",
            "faculty_profiles",
            ["keycloak_sub"],
            unique=True,
            postgresql_where=sa.text("keycloak_sub IS NOT NULL")
        )


def downgrade() -> None:
    op.drop_index("idx_faculty_profiles_keycloak_sub", table_name="faculty_profiles")
    op.drop_column("faculty_profiles", "keycloak_sub")
