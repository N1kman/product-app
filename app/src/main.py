import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.domain.interfaces import Language
from src.infrastructure.api.utils import allow_methods, allow_headers
from src.infrastructure.api.v1.product import router as product_router
from src.infrastructure.api.v1.customer import router as customer_router
from src.infrastructure.api.v1.order import router as order_router
from src.infrastructure.configs import api_config, kafka_config
from src.infrastructure.kafka import KafkaProducer, KafkaConsumer
from src.infrastructure.repositories import RuDBRepository, DeDBRepository, EnDBRepository, \
    payment_options_en, payment_options_ru, payment_options_de


@asynccontextmanager
async def lifespan(app: FastAPI):
    await KafkaProducer.create_topic(kafka_config.KAFKA_TOPIC)
    tasks = list()
    tasks.append(
        asyncio.create_task(
            KafkaConsumer.consume_messages(
                kafka_config.KAFKA_GROUP_ID_RU,
                RuDBRepository(),
                Language.en,
                Language.ru
            )
        )
    )
    tasks.append(
        asyncio.create_task(
            KafkaConsumer.consume_messages(
                kafka_config.KAFKA_GROUP_ID_DE,
                DeDBRepository(),
                Language.en,
                Language.de
            )
        )
    )
    async with EnDBRepository() as session_en:
        async with RuDBRepository() as session_ru:
            async with DeDBRepository() as session_de:
                await session_en.init_db(payment_options_en)
                await session_ru.init_db(payment_options_ru)
                await session_de.init_db(payment_options_de)
    yield
    for task in tasks:
        if not task.done():
            task.cancel()


main_app = FastAPI(
    lifespan=lifespan
)

main_app.include_router(product_router)
main_app.include_router(customer_router)
main_app.include_router(order_router)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.allowed_origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

# start local
if __name__ == "__main__":
    if api_config.https:
        uvicorn.run(
            "src.main:main_app",
            port=api_config.port,
            host=api_config.host,
            reload=True,
            ssl_keyfile='../../certs/keyfile.key',
            ssl_certfile='../../certs/certfile.crt'
        )
    else:
        uvicorn.run("src.main:main_app", port=api_config.port, host=api_config.host, reload=True)
