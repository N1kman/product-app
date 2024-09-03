from typing import Union

from src.domain.entities import CustomerRead
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBRepository


class GetCustomers(IUseCase):
    class Request(RequestModel):
        pass

    class Response(ResponseModel):
        customers: list[CustomerRead]

    def __init__(
            self, repository: DBRepository
    ):
        self.repository = repository

    async def execute(self, request: Request) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            async with self.repository as repository:
                customers = await repository.get_products()
            return ResponseSuccess.build(
                payload=customers,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
