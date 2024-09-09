from pydantic import BaseModel

from src.domain.entities import Translation


class Manufacturer(BaseModel):
    name: str
    country: str
    address: str


class ManufacturerRead(BaseModel):
    id: int


class ManufacturerReadWithTranslations(ManufacturerRead):
    name: list[Translation]
    country: list[Translation]
    address: list[Translation]
