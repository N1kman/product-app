from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models import Base


class TranslationORM(Base):
    __tablename__ = "translation"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    translated: Mapped[str] = mapped_column(
        nullable=False,
    )
    table_id: Mapped[str] = mapped_column(
        nullable=False,
    )
    field_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    lang_abbr: Mapped[int] = mapped_column(
        ForeignKey("language.abbr")
    )


class LanguageORM(Base):
    __tablename__ = "language"

    abbr: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    fullname: Mapped[str] = mapped_column(
        nullable=False,
    )
