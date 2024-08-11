import enum

from pydantic import BaseModel, EmailStr


class ProductCategory(str, enum.Enum):
    categoryA = "category A"
    categoryB = "category B"
    categoryC = "category C"


class ProductManufacturer(BaseModel):
    id: int
    country: str
    tel: str
    email: EmailStr


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: ProductCategory
    manufacturer: ProductManufacturer
