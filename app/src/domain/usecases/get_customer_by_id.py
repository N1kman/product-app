from typing import Union

from src.domain.entities import CustomerRead
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBRepository


class GetCustomerById(IUseCase):
    class Request(RequestModel):
        id: int

    class Response(ResponseModel):
        product: CustomerRead

    def __init__(
            self, repository: DBRepository
    ):
        self.repository = repository

    async def execute(self, request: Request) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            async with self.repository as repository:
                customer = await repository.get_customer_by_id(request.id)
            return ResponseSuccess.build(
                payload=customer,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
