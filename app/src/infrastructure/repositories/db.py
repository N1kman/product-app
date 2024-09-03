from typing import AsyncGenerator

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import selectinload

from src.domain.entities import Product, Customer, PaymentRead, CustomerRead, ProductReadWithCustomers, Order
from src.domain.entities.product import ProductRead
from src.domain.interfaces import IDBRepository
from src.infrastructure.configs import ru_db_config, en_db_config, de_db_config
from src.infrastructure.models import ProductORM, ProductManufacturerORM, PaymentOptionORM, CustomerORM, payment_table
from src.infrastructure.models.product import OrderORM
from src.infrastructure.repositories.exceptions import NoSuchItem


class DBRepository(IDBRepository):

    @classmethod
    def get_url(cls) -> str:
        pass

    async def init_db(self, options: list[PaymentRead]) -> None:
        if not await self.is_options_exist():
            for option in options:
                await self.add_payment_option(option)

    async def is_options_exist(self) -> bool:
        query = select(
            PaymentOptionORM
        )
        res = await self.session.execute(query)
        res = res.scalars().all()
        return res or False

    async def __aenter__(self):
        engine: AsyncEngine = create_async_engine(
            url=self.get_url(),
            echo=False,
            echo_pool=False,
            pool_size=5,
            max_overflow=10
        )
        session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self.session = session_factory()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if exc_value:
            await self.session.rollback()
            await self.session.close()
            return
        await self.session.commit()
        await self.session.close()

    async def get_product_by_id(self, id: int) -> ProductRead:
        query = (
            select(ProductORM)
            .where(ProductORM.id == id)
            .options(selectinload(ProductORM.manufacturer))
        )
        query_response = await self.session.execute(query)
        result = query_response.scalars().first()
        if result is None:
            raise NoSuchItem(f"there is no such item for ID {id}")
        return ProductRead.model_validate(result, from_attributes=True)

    async def get_products(self) -> list[ProductRead]:
        query = (
            select(ProductORM)
            .options(selectinload(ProductORM.manufacturer))
        )
        query_response = await self.session.execute(query)
        result = query_response.scalars().all()
        if result is None:
            raise NoSuchItem(f"there is no such items")
        return [ProductRead.model_validate(item, from_attributes=True) for item in result]

    async def add_product(self, product: Product):
        new_manufacturer = None
        if product.manufacturer_id is not None:
            query = (
                select(ProductManufacturerORM)
                .where(ProductManufacturerORM.id == product.manufacturer_id)
            )
            result = await self.session.execute(query)
            new_manufacturer = result.scalars().first()
        if new_manufacturer is None:
            new_manufacturer = ProductManufacturerORM(
                country=product.manufacturer.country,
                tel=product.manufacturer.tel,
                email=product.manufacturer.email
            )
            self.session.add(new_manufacturer)
        new_product = ProductORM(
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            manufacturer=new_manufacturer
        )
        self.session.add(new_product)
        await self.session.flush()
        if new_product.id is None:
            raise NoSuchItem(f"error with insert")
        return new_product.id

    async def add_payment_option(self, payment_option: PaymentRead):
        payment_option_orm = PaymentOptionORM(
            id=payment_option.id,
            option=payment_option.option
        )
        self.session.add(payment_option_orm)

    async def get_payment_options(self) -> list[PaymentRead]:
        query = (
            select(PaymentOptionORM)
        )
        query_response = await self.session.execute(query)
        result = query_response.scalars().all()
        if result is None:
            raise NoSuchItem(f"there is no such items")
        return [PaymentRead.model_validate(item, from_attributes=True) for item in result]

    async def add_customer(self, customer: Customer) -> int:
        customer_orm = CustomerORM(
            name=customer.name,
            surname=customer.surname,
            email=customer.email,
            age=customer.age,
            passport_number=customer.email
        )
        self.session.add(customer_orm)
        await self.session.flush()
        if customer_orm.id is None:
            raise NoSuchItem(f"error with insert")
        for option_id in customer.payment_options:
            insert_stmt = payment_table.insert().values(customer_id=customer_orm.id, payment_option_id=option_id)
            await self.session.execute(insert_stmt)
        return customer_orm.id

    async def get_customer_by_id(self, id: int) -> CustomerRead:
        query = (
            select(CustomerORM)
            .where(CustomerORM.id == id)
            .options(selectinload(CustomerORM.payment_options))
        )
        query_response = await self.session.execute(query)
        result = query_response.scalars().first()
        if result is None:
            raise NoSuchItem(f"there is no such item for ID {id}")
        return CustomerRead.model_validate(result, from_attributes=True)

    async def get_customers(self) -> list[CustomerRead]:
        query = (
            select(CustomerORM)
            .options(selectinload(CustomerORM.payment_options))
        )
        query_response = await self.session.execute(query)
        result = query_response.scalars().all()
        if result is None:
            raise NoSuchItem(f"there is no such items")
        return [CustomerRead.model_validate(item, from_attributes=True) for item in result]

    async def get_product_with_customers_by_id(self, id: int) -> ProductReadWithCustomers:
        query = (
            select(ProductORM)
            .where(ProductORM.id == id)
            .options(
                selectinload(ProductORM.manufacturer),
                selectinload(ProductORM.orders)
                .selectinload(OrderORM.customer)
                .selectinload(CustomerORM.payment_options)
            )
        )
        query_response = await self.session.execute(query)
        result = query_response.scalars().first()
        if result is None:
            raise NoSuchItem(f"there is no such item for ID {id}")
        return ProductReadWithCustomers.model_validate(result, from_attributes=True)

    async def get_products_with_customers(self) -> list[ProductReadWithCustomers]:
        query = (
            select(ProductORM)
            .options(
                selectinload(ProductORM.manufacturer),
                selectinload(ProductORM.orders)
                .selectinload(OrderORM.customer)
                .selectinload(CustomerORM.payment_options)
            )
        )
        query_response = await self.session.execute(query)
        result = query_response.scalars().all()
        print(result)
        if result is None:
            raise NoSuchItem(f"there is no such items")
        return [ProductReadWithCustomers.model_validate(item, from_attributes=True) for item in result]

    async def add_order(self, order: Order) -> int:
        order_orm = OrderORM(
                customer_id=order.customer_id,
                product_id=order.product_id
            )
        self.session.add(
            order_orm
        )
        await self.session.flush()
        if order_orm.id is None:
            raise NoSuchItem(f"error with insert")
        return order_orm.id


class RuDBRepository(DBRepository):
    @classmethod
    def get_url(cls) -> str:
        return ru_db_config.get_url()


class EnDBRepository(DBRepository):
    @classmethod
    def get_url(cls) -> str:
        return en_db_config.get_url()


class DeDBRepository(DBRepository):
    @classmethod
    def get_url(cls) -> str:
        return de_db_config.get_url()
