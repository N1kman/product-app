from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities import ProductCategory
from src.infrastructure.models.base import Base


class ProductManufacturerORM(Base):
    __tablename__ = "manufacturer"

    country: Mapped[str] = mapped_column(nullable=False)
    tel: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)


class ProductORM(Base):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[ProductCategory] = mapped_column(nullable=False)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"))

    manufacturer: Mapped["ProductManufacturerORM"] = relationship("ProductManufacturerORM")
