from pydantic import BaseModel


class Manufacturer(BaseModel):
    name: str
    country: str
    address: str


class ManufacturerRead(BaseModel):
    id: int
    