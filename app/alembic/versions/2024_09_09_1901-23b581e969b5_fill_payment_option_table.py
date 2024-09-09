"""fill payment_option table

Revision ID: 23b581e969b5
Revises: 7d0e8eab72f9
Create Date: 2024-09-09 19:01:10.296549

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "23b581e969b5"
down_revision: Union[str, None] = "7d0e8eab72f9"
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
            WHERE option IN ('cryptocurrency', 'bank transfer', 'installment');
        """)
    )
