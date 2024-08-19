import enum

from pydantic import BaseModel

from src.infrastructure.configs import APIConfig
from src.infrastructure.repositories.exceptions import (
    BadRequest,
    ConflictError,
    NoSuchItem,
)


class ResponseModel(BaseModel):
    pass


class ResponseFailure:
    class ResponseStatus(enum.Enum):
        BAD_REQUEST = 400
        CONFLICT = 409
        NOT_FOUND = 404
        INTERNAL_ERROR = 500

    def __init__(self, err_msg: str, status_code: ResponseStatus) -> None:
        self.status = status_code
        self.err_msg = err_msg

    @classmethod
    def build(cls, exc: Exception):
        if isinstance(exc, NoSuchItem):
            status_code = cls.ResponseStatus.NOT_FOUND
        elif isinstance(exc, ConflictError):
            status_code = cls.ResponseStatus.CONFLICT
        elif isinstance(exc, BadRequest):
            status_code = cls.ResponseStatus.BAD_REQUEST
        else:
            status_code = cls.ResponseStatus.INTERNAL_ERROR
            if APIConfig().log_level == APIConfig().log_level.debug:
                raise exc

        return cls(f"{exc.__class__.__name__}: {str(exc)}", status_code)


class ResponseSuccess:
    class ResponseStatus(enum.Enum):
        SUCCESS = "200"
        CREATED = "201"

    def __init__(self, payload: ResponseModel, status: ResponseStatus) -> None:
        self.payload = payload
        self.status = status

    @classmethod
    def build(cls, payload: ResponseModel, status: ResponseStatus):
        return cls(payload, status)
