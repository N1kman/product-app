import enum

from pydantic import Field
from pydantic_settings import BaseSettings


class APIMode(str, enum.Enum):
    local = "local"
    dev = "dev"
    stage = "stage"
    prod = "prod"


class LogLevels(str, enum.Enum):
    info = "info"
    debug = "debug"


class APIConfig(BaseSettings):
    class Config:
        env_file = ["../_envs/.env-api", "../../_envs/.env-api"]

    host: str = Field(..., alias="api_host")
    port: int = Field(..., alias="api_port")
    mode: APIMode = Field(APIMode.local, alias="api_mode")
    log_level: LogLevels = Field(LogLevels.info)
    allowed_origins_str: str = Field(..., alias="allowed_origins")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins_str.split(",")]

    @property
    def is_local(self):
        return self.mode == APIMode.local

    @property
    def is_dev(self):
        return self.mode == APIMode.dev

    @property
    def is_prod(self):
        return self.mode == APIMode.prod

    @property
    def is_stage(self):
        return self.mode == APIMode.stage


api_config = APIConfig()
