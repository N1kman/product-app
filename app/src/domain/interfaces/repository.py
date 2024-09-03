from abc import ABC, abstractmethod

from src.domain.entities import Product, PaymentRead, Customer, CustomerRead, Order, ProductReadWithCustomers
from src.domain.entities.product import ProductRead


class IDBRepository(ABC):
    @abstractmethod
    async def get_products(self) -> list[ProductRead]:
        pass

    @abstractmethod
    async def get_product_by_id(self, id: int) -> ProductRead:
        pass

    @abstractmethod
    async def add_product(self, product: Product) -> int:
        pass

    @abstractmethod
    async def get_payment_options(self) -> list[PaymentRead]:
        pass

    @abstractmethod
    async def add_customer(self, customer: Customer) -> int:
        pass

    @abstractmethod
    async def get_customer_by_id(self, id: int) -> CustomerRead:
        pass

    @abstractmethod
    async def get_customers(self) -> list[CustomerRead]:
        pass

    @abstractmethod
    async def get_product_with_customers_by_id(self, id: int) -> ProductReadWithCustomers:
        pass

    @abstractmethod
    async def get_products_with_customers(self) -> list[ProductReadWithCustomers]:
        pass

    @abstractmethod
    async def add_order(self, order: Order) -> int:
        pass
