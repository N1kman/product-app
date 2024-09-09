from typing import Optional

from pydantic import BaseModel

from src.domain.entities import Translation


class Manufacturer(BaseModel):
    name: str
    country: str
    address: str


class ManufacturerWithTranslations(Manufacturer):
    name: list[Translation] = list()
    country: list[Translation] = list()
    address: list[Translation] = list()


class ManufacturerRead(BaseModel):
    id: int


class ManufacturerReadWithTranslations(ManufacturerRead):
    name: list[Translation] = list()
    country: list[Translation] = list()
    address: list[Translation] = list()


class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None


class ManufacturerUpdateWithTranslations(ManufacturerUpdate):
    name: list[Translation] = list()
    country: list[Translation] = list()
    address: list[Translation] = list()
