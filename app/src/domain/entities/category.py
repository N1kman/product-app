from pydantic import BaseModel


class Category(BaseModel):
    name: str


class CategoryRead(Category):
    id: int
