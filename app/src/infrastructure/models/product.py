import datetime
from enum import Enum

from sqlalchemy import ForeignKey, text
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
    orders: Mapped[list["OrderORM"]] = relationship("OrderORM")


class OrderORM(Base):
    __tablename__ = "order"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id"),
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"),
        primary_key=True
    )

    ordered_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    customer: Mapped["CustomerORM"] = relationship("CustomerORM")
