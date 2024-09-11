import datetime

from pydantic import BaseModel


class OrderDetail(BaseModel):
    amount: int
    product_id: int


class Order(BaseModel):
    address: str
    status: bool
    order_details: list[OrderDetail]
    customer_id: int


class OrderRead(Order):
    id: int
    ordered_at: datetime.datetime
