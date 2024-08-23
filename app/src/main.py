import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.domain.entities import Product, ProductCategory
from src.infrastructure.api.v1.product import router as product_router
from src.infrastructure.configs import APIConfig, DBConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

main_app = FastAPI(
    lifespan=lifespan
)

main_app.include_router(product_router)

# if __name__ == "__main__":
#     uvicorn.run("src.main:main_app", port=APIConfig().port, host=APIConfig().host, reload=True)
