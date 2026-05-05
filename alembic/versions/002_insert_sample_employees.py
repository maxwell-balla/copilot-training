"""insert sample employees

Revision ID: 002
Revises: 001
Create Date: 2026-05-05

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    t_employee = sa.table(
        "t_employee",
        sa.column("first_name", sa.String),
        sa.column("last_name", sa.String),
        sa.column("email", sa.String),
        sa.column("phone_number", sa.String),
        sa.column("department", sa.String),
        sa.column("created_at", sa.DateTime),
    )
    now = datetime.utcnow()
    op.bulk_insert(
        t_employee,
        [
            {
                "first_name": "Alice", "last_name": "Johnson",
                "email": "alice.johnson@growtogether.io",
                "phone_number": "+1-555-0101", "department": "FINANCE",
                "created_at": now,
            },
            {
                "first_name": "Bob", "last_name": "Smith",
                "email": "bob.smith@growtogether.io",
                "phone_number": "+1-555-0102", "department": "OPERATIONS",
                "created_at": now,
            },
            {
                "first_name": "Carol", "last_name": "Williams",
                "email": "carol.williams@growtogether.io",
                "phone_number": "+1-555-0103", "department": "HR",
                "created_at": now,
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM t_employee WHERE email IN ("
        "'alice.johnson@growtogether.io',"
        "'bob.smith@growtogether.io',"
        "'carol.williams@growtogether.io')"
    )
