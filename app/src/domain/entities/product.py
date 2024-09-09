from pydantic import BaseModel

from src.domain.entities import CategoryRead, ManufacturerRead, Translation


class Product(BaseModel):
    name: str
    description: str
    price: float
    amount: int
    manufacturer_id: int
    category_id: int


class ProductRead(Product):
    id: int


class ProductReadWithTranslations(ProductRead):
    name: list[Translation]
    description: list[Translation]


class ProductReadWithCategory(ProductRead):
    category: CategoryRead


class ProductReadWithManufacturer(ProductRead):
    manufacturer: ManufacturerRead


class ProductReadWithCategoryAndManufacturer(ProductRead):
    category: CategoryRead
    manufacturer: ManufacturerRead
