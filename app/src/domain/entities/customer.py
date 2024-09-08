from pydantic import BaseModel, EmailStr


class Payment(BaseModel):
    customer_id: int
    payment_option_id: int


class PaymentOption(BaseModel):
    option: str


class PaymentOptionRead(PaymentOption):
    id: int


class Customer(BaseModel):
    name: str
    surname: str
    email: EmailStr
    address: str


class CustomerRead(Customer):
    id: int
