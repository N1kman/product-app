"""fill payment_option table

Revision ID: 177099881d2d
Revises: c16588e2ee7f
Create Date: 2024-09-09 11:34:22.993527

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "177099881d2d"
down_revision: Union[str, None] = "c16588e2ee7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("""
                INSERT INTO payment_option (option) VALUES
                ('cryptocurrency'),
                ('bank transfer'),
                ('installment');
            """)
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("""
                DELETE FROM payment_option
                WHERE option IN ('cryptocurrency', 'bank transfer', 'installment')
            """)
    )
