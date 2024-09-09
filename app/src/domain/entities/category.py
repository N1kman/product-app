from typing import Optional

from pydantic import BaseModel

from src.domain.entities import Translation


class Category(BaseModel):
    name: str


class CategoryWithTranslations(Category):
    name: list[Translation] = list()


class CategoryRead(Category):
    id: int


class CategoryReadWithTranslations(CategoryRead):
    name: list[Translation] = list()


class CategoryUpdate(BaseModel):
    name: Optional[str] = None


class CategoryUpdateWithTranslations(CategoryUpdate):
    name: list[Translation] = list()
