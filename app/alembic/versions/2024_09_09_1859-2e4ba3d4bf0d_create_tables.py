"""create tables

Revision ID: 2e4ba3d4bf0d
Revises: 
Create Date: 2024-09-09 18:59:33.612862

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e4ba3d4bf0d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "customer",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "language",
        sa.Column("abbr", sa.String(), nullable=False),
        sa.Column("fullname", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("abbr"),
    )
    op.create_table(
        "manufacturer",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name_id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "payment_option",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("option", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "ordered_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer.id"],
        ),
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
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name_id", sa.Integer(), nullable=False),
        sa.Column("description_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("manufacturer_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.id"],
        ),
        sa.ForeignKeyConstraint(
            ["manufacturer_id"],
            ["manufacturer.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "translation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("translated", sa.String(), nullable=False),
        sa.Column("table_id", sa.Integer(), nullable=False),
        sa.Column("field_id", sa.Integer(), nullable=False),
        sa.Column("lang_abbr", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lang_abbr"],
            ["language.abbr"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "order_detail",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["order.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("order_detail")
    op.drop_table("translation")
    op.drop_table("product")
    op.drop_table("payment")
    op.drop_table("order")
    op.drop_table("payment_option")
    op.drop_table("manufacturer")
    op.drop_table("language")
    op.drop_table("customer")
    op.drop_table("category")
