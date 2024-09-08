from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import Base


class ProductORM(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    description_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    price: Mapped[float] = mapped_column(
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(
        nullable=False,
    )
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturer.id"),
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
    )

    manufacturer: Mapped["ManufacturerORM"] = relationship(
        "ManufacturerORM",
    )
    category: Mapped["CategoryORM"] = relationship(
        "CategoryORM",
    )


class ManufacturerORM(Base):
    __tablename__ = "manufacturer"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    country_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    address_id: Mapped[int] = mapped_column(
        nullable=False,
    )


class CategoryORM(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name_id: Mapped[int] = mapped_column(
        nullable=False,
    )
