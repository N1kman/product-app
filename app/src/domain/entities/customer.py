from pydantic import BaseModel, EmailStr


class Payment(BaseModel):
    option: str


class PaymentRead(Payment):
    id: int


class Customer(BaseModel):
    name: str
    surname: str
    email: EmailStr
    age: int
    passport_number: str
    payment_options: list[int]


class CustomerRead(Customer):
    id: int
    payment_options: list[PaymentRead]
