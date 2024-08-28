from urllib.parse import quote_plus

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):

    class Config:
        env_prefix = "db_"

    hostname: str = Field(...)
    port: int = Field(...)
    user: str = Field(...)
    password: SecretStr = Field(...)
    name: str = Field(...)
    driver: str = Field("postgresql+asyncpg")

    def get_url(self):
        encoded_password = quote_plus(self.password.get_secret_value())
        return f"{self.driver}://{self.user}:{encoded_password}@{self.hostname}:{self.port}/{self.name}"


class EnDBConfig(DBConfig):
    class Config:
        env_file = ["../_envs/.env-db_en", "../../_envs/.env-db_en"]


class RuDBConfig(DBConfig):
    class Config:
        env_file = ["../_envs/.env-db_ru", "../../_envs/.env-db_ru"]


class DeDBConfig(DBConfig):
    class Config:
        env_file = ["../_envs/.env-db_de", "../../_envs/.env-db_de"]


en_db_config = EnDBConfig()
ru_db_config = RuDBConfig()
de_db_config = DeDBConfig()