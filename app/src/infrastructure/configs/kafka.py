import os

from pydantic import Field
from pydantic_settings import BaseSettings

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../_envs/.env-kafka")


class KafkaConfig(BaseSettings):
    class Config:
        env_file = [path]

    KAFKA_BOOTSTRAP_SERVERS: str = Field(...)
    KAFKA_TOPIC: str = Field(...)
    KAFKA_GROUP_ID_RU: str = Field(...)
    KAFKA_GROUP_ID_DE: str = Field(...)


kafka_config = KafkaConfig()
