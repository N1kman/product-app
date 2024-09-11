import asyncio
import json

from aiokafka import AIOKafkaConsumer

from src.domain.entities import Product, Customer, Order
from src.domain.interfaces import Language
from src.infrastructure.configs import kafka_config
from src.infrastructure.repositories.db.base import DBRepository
from src.infrastructure.translator import MBartTranslator

models_with_name = {
    Product.__name__: Product,
    Customer.__name__: Customer,
    Order.__name__: Order,
}

methods_with_name = {
    DBRepository.add_product.__name__: DBRepository.add_product,
    DBRepository.add_customer.__name__: DBRepository.add_customer,
    DBRepository.add_order.__name__: DBRepository.add_order,
}


class KafkaConsumer:
    lock = asyncio.Lock()
    @staticmethod
    async def consume_messages(group_id, db_repo: DBRepository, language_source: Language, language_target: Language):
        consumer = AIOKafkaConsumer(kafka_config.KAFKA_TOPIC,
                                    bootstrap_servers=kafka_config.KAFKA_BOOTSTRAP_SERVERS,
                                    group_id=group_id,
                                    session_timeout_ms=30000,
                                    heartbeat_interval_ms=10000
                                    )
        translator = MBartTranslator()
        try:
            await consumer.start()
            while True:
                msg = await consumer.getone()
                if msg is not None:
                    result = json.loads(msg.value.decode('utf-8'))
                    model = models_with_name.get(result["model"])
                    method = methods_with_name.get(result["method"])
                    obj = model(**result["data"])
                    async with KafkaConsumer.lock:
                        translated = await translator.async_translate_obj(obj, language_source, language_target)
                    async with db_repo as session:
                        await method(session, translated)
        finally:
            await consumer.stop()
