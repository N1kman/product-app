from pydantic import BaseModel


class Payment(BaseModel):
    option: str


class Customer(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    passport_number: str
    payment: Payment
