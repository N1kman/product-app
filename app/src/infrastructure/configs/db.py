from urllib.parse import quote_plus

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    hostname: str = Field(...)
    port: int = Field(...)
    user: str = Field(...)
    password: SecretStr = Field(...)
    name: str = Field(...)
    driver: str = Field("postgresql+asyncpg")

    class Config:
        env_prefix = "db_"

    def get_url(self):
        encoded_password = quote_plus(self.password.get_secret_value())
        return f"{self.driver}://{self.user}:{encoded_password}@{self.hostname}:{self.port}/{self.name}"
