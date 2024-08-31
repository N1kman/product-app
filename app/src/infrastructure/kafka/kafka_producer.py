import json

from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from pydantic import BaseModel

from src.domain.interfaces import BrokerProducer
from src.infrastructure.configs import kafka_config


bootstrap_servers = kafka_config.KAFKA_BOOTSTRAP_SERVERS


class KafkaProducer(BrokerProducer):

    async def __aenter__(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
        await self.producer.start()
        return self

    async def __aexit__(self, type_error, value_error, tb):
        if self.producer:
            await self.producer.stop()

    @staticmethod
    async def create_topic(topic: str, num_partitions=1, replication_factor=1):
        admin_client = AIOKafkaAdminClient(bootstrap_servers=bootstrap_servers)
        await admin_client.start()
        try:
            await admin_client.create_topics(
                [NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)]
            )
        finally:
            await admin_client.close()

    async def send_message(self, topic: str, obj: BaseModel, model, method):
        if self.producer:
            await self.producer.send_and_wait(topic, json.dumps(
                {
                   "model": model,
                   "method": method,
                   "data": obj.model_dump()
                }
            ).encode("utf-8"))

