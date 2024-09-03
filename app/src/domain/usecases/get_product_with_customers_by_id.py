from typing import Union

from src.domain.entities import ProductReadWithCustomers
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBRepository


class GetProductWithCustomersById(IUseCase):
    class Request(RequestModel):
        id: int

    class Response(ResponseModel):
        product: ProductReadWithCustomers

    def __init__(
            self, repository: DBRepository
    ):
        self.repository = repository

    async def execute(self, request: Request) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            async with self.repository as repository:
                product = await repository.get_product_with_customers_by_id(request.id)
            return ResponseSuccess.build(
                payload=product,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
