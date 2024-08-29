from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaConfig(BaseSettings):
    class Config:
        env_file = ["../_envs/.env-kafka", "../../_envs/.env-kafka"]

    KAFKA_BOOTSTRAP_SERVERS: str = Field(...)
    KAFKA_TOPIC: str = Field(...)
    KAFKA_GROUP_ID_RU: str = Field(...)
    KAFKA_GROUP_ID_DE: str = Field(...)


kafka_config = KafkaConfig()
