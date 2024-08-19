from typing import AsyncGenerator

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import selectinload

from src.domain.entities import Product
from src.domain.entities.product import ProductRead
from src.domain.interfaces import IDBRepository
from src.infrastructure.configs import DBConfig
from src.infrastructure.models import ProductORM, ProductManufacturerORM
from src.infrastructure.repositories.exceptions import NoSuchItem

engine: AsyncEngine = create_async_engine(
    url=DBConfig().get_url(),
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


class DBRepository(IDBRepository):
    async def __aenter__(self):
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
            raise NoSuchItem(f"there is no such item for ID")
        return new_product.id

