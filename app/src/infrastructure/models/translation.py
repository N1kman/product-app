from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models import Base


class TranslationORM(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    translated: Mapped[str] = mapped_column(
        nullable=False,
    )
    table_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    field_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    lang_id: Mapped[int] = mapped_column(
        ForeignKey("language.id")
    )


class LanguageORM(Base):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    abbr: Mapped[str] = mapped_column(
        nullable=False,
    )
    fullname: Mapped[str] = mapped_column(
        nullable=False,
    )
