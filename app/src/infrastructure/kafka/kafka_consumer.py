import asyncio
from typing import Annotated

from aiokafka import AIOKafkaConsumer
from fastapi import Depends

from src.domain.entities import Product
from src.domain.interfaces import Language
from src.infrastructure.configs import kafka_config
from src.infrastructure.repositories import RuDBRepository, DeDBRepository
from src.infrastructure.repositories.db import DBRepository
from src.infrastructure.translator import MBartTranslator


class KafkaConsumer:
    lock = asyncio.Lock()
    @staticmethod
    async def consume_messages(group_id, db_repo: DBRepository, language_source: Language, language_target: Language):
        consumer = AIOKafkaConsumer(kafka_config.KAFKA_TOPIC,
                                    bootstrap_servers=kafka_config.KAFKA_BOOTSTRAP_SERVERS,
                                    group_id=group_id)
        translator = MBartTranslator()
        try:
            await consumer.start()
            while True:
                msg = await consumer.getone()
                if msg is not None:
                    product: Product = Product.parse_raw(msg.value.decode('utf-8'))
                    print(product.model_dump())
                    async with KafkaConsumer.lock:
                        tr_product = await translator.async_translate_obj(product, language_source, language_target)
                    print(tr_product.model_dump())
                    async with db_repo as session:
                        await session.add_product(tr_product)
        finally:
            await consumer.stop()
