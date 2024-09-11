from typing import Optional

from pydantic import BaseModel

from src.domain.entities import CategoryRead, ManufacturerRead
from src.domain.entities.language import Translation


class Product(BaseModel):
    name: str
    description: str
    price: float
    amount: int
    manufacturer_id: int
    category_id: int


class ProductWithTranslations(Product):
    name: list[Translation] = list()
    description: list[Translation] = list()


class ProductRead(Product):
    id: int


class ProductReadWithTranslations(ProductRead):
    name: list[Translation] = list()
    description: list[Translation] = list()


class ProductReadWithCategory(ProductRead):
    category: CategoryRead


class ProductReadWithManufacturer(ProductRead):
    manufacturer: ManufacturerRead


class ProductReadWithCategoryAndManufacturer(ProductRead):
    category: CategoryRead
    manufacturer: ManufacturerRead


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    amount: Optional[int] = None
    manufacturer_id: Optional[int] = None
    category_id: Optional[int] = None


class ProductUpdateWithTranslations(ProductUpdate):
    name: list[Translation] = list()
    description: list[Translation] = list()
