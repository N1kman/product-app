"""create customer and payment_option tables

Revision ID: 83763360d2d9
Revises: 75d89e13355a
Create Date: 2024-09-02 17:15:57.893030

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "83763360d2d9"
down_revision: Union[str, None] = "75d89e13355a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customer",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("passport_number", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "payment_option",
        sa.Column("option", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "payment",
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("payment_option_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer.id"],
        ),
        sa.ForeignKeyConstraint(
            ["payment_option_id"],
            ["payment_option.id"],
        ),
        sa.PrimaryKeyConstraint("customer_id", "payment_option_id"),
    )


def downgrade() -> None:
    op.drop_table("payment")
    op.drop_table("payment_option")
    op.drop_table("customer")
