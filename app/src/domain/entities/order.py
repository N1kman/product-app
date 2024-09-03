from datetime import datetime

from pydantic import BaseModel

from src.domain.entities import CustomerRead, ProductRead


class Order(BaseModel):
    customer_id: int
    product_id: int


class OrderRead(BaseModel):
    ordered_at: datetime
    customer: CustomerRead


class ProductReadWithCustomers(ProductRead):
    orders: list[OrderRead]
