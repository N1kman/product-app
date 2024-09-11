import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models import Base


class OrderORM(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    ordered_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    address: Mapped[str] = mapped_column(
        nullable=False
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id")
    )

    customer: Mapped["CustomerORM"] = relationship(
        "CustomerORM",
        back_populates="orders",
    )
    order_details: Mapped[list["OrderDetailORM"]] = relationship(
        "OrderDetailORM",
        cascade="all, delete-orphan",
    )


class OrderDetailORM(Base):
    __tablename__ = "order_detail"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    amount: Mapped[int] = mapped_column(
        nullable=False,
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id"),
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"),
    )

    product: Mapped["ProductORM"] = relationship(
        "ProductORM",
    )
