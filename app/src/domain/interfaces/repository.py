from abc import ABC, abstractmethod

from src.domain.entities import Product
from src.domain.entities.product import ProductRead


class IDBRepository(ABC):

    @abstractmethod
    async def get_product_by_id(self, id: int) -> ProductRead:
        pass

    @abstractmethod
    async def add_product(self, product: Product) -> int:
        pass
