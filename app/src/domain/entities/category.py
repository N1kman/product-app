from pydantic import BaseModel

from src.domain.entities import Translation


class Category(BaseModel):
    name: str


class CategoryRead(Category):
    id: int


class CategoryReadWithTranslations(CategoryRead):
    name: list[Translation]
