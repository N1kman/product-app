import enum
from typing import Self

from pydantic import BaseModel, EmailStr, model_validator


class ProductCategory(str, enum.Enum):
    categoryA = "category A"
    categoryB = "category B"
    categoryC = "category C"


class ProductManufacturer(BaseModel):
    country: str
    tel: str
    email: EmailStr


class ProductManufacturerRead(ProductManufacturer):
    id: int


class Product(BaseModel):
    name: str
    description: str
    price: float
    category: ProductCategory
    manufacturer_id: int | None
    manufacturer: ProductManufacturer | None

    @model_validator(mode='after')
    def check_manufacturer_properties(self) -> Self:
        if self.manufacturer_id is None and self.manufacturer is None:
            raise ValueError('manufacturer_id or manufacturer must be filled in')
        return self


class ProductRead(Product):
    id: int
    manufacturer: ProductManufacturerRead
