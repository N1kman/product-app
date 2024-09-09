"""fill language table

Revision ID: 7d0e8eab72f9
Revises: 2e4ba3d4bf0d
Create Date: 2024-09-09 19:00:27.221673

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d0e8eab72f9"
down_revision: Union[str, None] = "2e4ba3d4bf0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            INSERT INTO language (abbr, fullname) VALUES
            ('en', 'English'),
            ('ru', 'Russian'),
            ('de', 'Deutsch');
        """)
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            DELETE FROM languages
            WHERE abbr IN ('en', 'ru', 'fr');
        """)
    )
