import enum

from pydantic import BaseModel


class ProductCategory(str, enum.Enum):
    categoryA = "category A"
    categoryB = "category B"
    categoryC = "category C"


class ProductManufacturer(BaseModel):
    id: int


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: ProductCategory
    manufacturer: ProductManufacturer
    