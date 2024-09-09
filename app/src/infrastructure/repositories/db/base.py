from abc import ABC

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from src.infrastructure.configs import db_config


class DBRepository(ABC):

    @classmethod
    def get_url(cls) -> str:
        return db_config.get_url()

    async def __aenter__(self):
        engine: AsyncEngine = create_async_engine(
            url=self.get_url(),
            echo=True,
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
