from sqlalchemy import ForeignKey, Column, Table, PrimaryKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.infrastructure.models import Base


payment_table = Table(
    "payment",
    Base.metadata,
    Column("customer_id", ForeignKey("customer.id")),
    Column("payment_option_id", ForeignKey("payment_option.id")),
    PrimaryKeyConstraint("customer_id", "payment_option_id")
)


class PaymentOptionORM(Base):
    __tablename__ = "payment_option"

    option: Mapped[str] = mapped_column(nullable=False)


class CustomerORM(Base):
    __tablename__ = "customer"

    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    passport_number: Mapped[str] = mapped_column(nullable=False)

    payment_options: Mapped[list["PaymentOptionORM"]] = relationship(
        'PaymentOptionORM',
        secondary=payment_table
    )


