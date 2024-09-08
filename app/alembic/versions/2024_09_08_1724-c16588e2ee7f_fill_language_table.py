"""fill language table

Revision ID: c16588e2ee7f
Revises: 7c8846b104ea
Create Date: 2024-09-08 17:24:49.486910

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c16588e2ee7f"
down_revision: Union[str, None] = "7c8846b104ea"
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
            WHERE abbr IN ('en', 'ru', 'fr')
        """)
    )
