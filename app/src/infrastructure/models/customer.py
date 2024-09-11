from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.infrastructure.models import Base


class CustomerORM(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
    )
    surname: Mapped[str] = mapped_column(
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        nullable=False,
    )

    orders: Mapped[list["OrderORM"]] = relationship(
        "OrderORM",
        back_populates="customer",
    )
    payment_options: Mapped[list["PaymentORM"]] = relationship(
        "PaymentORM",
        cascade="all, delete-orphan",
    )


class PaymentOptionORM(Base):
    __tablename__ = "payment_option"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    option: Mapped[str] = mapped_column(
        nullable=False,
    )


class PaymentORM(Base):
    __tablename__ = "payment"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id"),
        primary_key=True,
    )
    payment_option_id: Mapped[int] = mapped_column(
        ForeignKey("payment_option.id"),
        primary_key=True,
    )

    payment_option: Mapped["PaymentOptionORM"] = relationship(
        "PaymentOptionORM",
    )
